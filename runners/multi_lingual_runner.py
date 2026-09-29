import time
from typing import Self, cast

import laya
from datasets import load_dataset
from laya import Router

from models import ContextTypes
from runners import BaseRunner


class MultiLingualRunner(BaseRunner):
    """
    This class will be used to configure and run various
    permutations of the email classifier, helping to assess
    performance and accuracy for each one.

    It will use a fluent builder pattern style for constructing
    the specific configuration of a new test.
    """
    _router_agent: Router | None = None
    _direct_model_agent = {}

    def __init__(self, dataset_file: str = "dataset/matters-spam"):
        super().__init__(dataset_file)
        self._questions = self._questions()
        self._context = lambda row: None # Note this will be replaced by a lambda using the builder
        self._agent = None
        self._using_router = False

    def context_type(self, context_type: ContextTypes = ContextTypes.SIMPLE) -> Self:
        """
        Determines how to provide context to the model
        :return: The LayaRunner instance to continue fluent builder
        """
        if context_type == ContextTypes.SIMPLE:
            self._structured_context = False
            self._context = lambda row: row['text']
        else:
            self._structured_context = False
            self._context = lambda row: row['text']

        return self

    def use_router(self, router_agent: bool = False, model_name: str = "convaiinnovations/laya") -> Self:
        """
        Instruct the processor to use an agent based off of Laya's model router or direct model access
        :return: The LayaRunner instance to continue fluent builder
        """
        self._using_router = router_agent
        if router_agent:
            self._agent = self.get_router_agent()
        else:
            self._agent = self.get_direct_model_agent(model_name)

        return self

    def process(self):
        """
        Processes the dataset using the Python CSV parser
        """
        self._reset()
        self._report_test_configuration()
        print("Starting file load")
        file_load = time.perf_counter_ns()

        streamed_dataset = load_dataset(self._dataset_file, split="validation", streaming=True)

        for row in streamed_dataset:
            email_text = self._context(row)
            if len(email_text) > 8192:
                print("Skipping record with text length > 8192: ", len(email_text))
                continue
            result = self._agent.predict(email_text, self._questions)
            self._total_records += 1
            if self._total_records % 10000 == 0:
                print("Processed records: ", self._total_records)

            row_result = result["answers"]["email_category"]
            result_str = "ham" if row_result["noul"] < 0.5 else "spam"
            if result_str != row['label']:
                expected = row['label']
                actual = result_str
                key = expected + "+" + actual
                self._failure_categories[key] = self._failure_categories.get(key, 0) + 1
                self._error_count += 1

        print("Processing time (ms):", (time.perf_counter_ns() - file_load) / 1000000)

        self._report()

    def _report_test_configuration(self):
        """
        Prints a report of the processing
        """
        super()._report_test_configuration()
        processor_type = "Router" if self._using_router else "Direct Model Access"
        print(" - Processor Type: ", processor_type)
        print()

    @classmethod
    def get_router_agent(cls) -> Router:
        """
        Retrieves a Router-based agent from the cache if available or initializes a new one.
        :return:
        """
        print("Using Router agent")
        if cls._router_agent is None:
            model_load = time.perf_counter_ns()
            cls._router_agent = Router(preload=True)
            print("Model load time (ms):", (time.perf_counter_ns() - model_load) / 1000000)

        return cast(Router, cls._router_agent)

    @classmethod
    def get_direct_model_agent(cls, model_name: str) -> Router:
        """
        Retrieves a Direct Model Access agent from the cache if available or initializes a new one.
        :return:
        """
        print("Using Direct model: ", model_name)
        if cls._direct_model_agent.get(model_name) is None:
            model_load = time.perf_counter_ns()
            cls._direct_model_agent[model_name] = laya.load(model_name)

            print("Model load time (ms):", (time.perf_counter_ns() - model_load) / 1000000)

        return cls._direct_model_agent[model_name]

    @staticmethod
    def _questions():
        """
        Returns a collection of questions to be asked.
        """

        return {
            "email_category": {
                "type": "noul",
                "instructions": "Is this email spam?",
            }
        }
