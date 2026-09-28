import csv
import time
from enum import Enum
from typing import Self, cast

import laya
from laya import Router

class ContextTypes(Enum):
    SIMPLE = 1
    STRUCTURED = 2

class LayaRunner:
    """
    This class will be used to configure and run various
    permutations of the email classifier, helping to assess
    performance and accuracy for each one.

    It will use a fluent builder pattern style for constructing
    the specific configuration of a new test.
    """
    _router_agent: Router | None = None
    _direct_model_agent = {}

    def __init__(self, dataset_file: str = "dataset/full_dataset.csv"):
        self._dataset_file = dataset_file
        self._questions = self._questions()
        self._context = lambda row: None # Note this will be replaced by a lambda using the builder
        self._agent = None
        self._structured_context = False
        self._using_router = False
        self._report_failures = False
        self._error_count = 0
        self._total_records = 0
        self._failure_categories = {}


    def context_type(self, context_type: ContextTypes = ContextTypes.SIMPLE) -> Self:
        """
        Determines how to provide context to the model
        :return: The LayaRunner instance to continue fluent builder
        """
        if context_type == ContextTypes.SIMPLE:
            self._structured_context = False
            self._context = lambda row: row['text']
        else:
            self._structured_context = True
            self._context = lambda row: {
               "subject": row['subject'],
               "body": row['body']
            }

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


    def report_failures(self, show_failures: bool) -> Self:
        """
        Indicate whether to include a failure report
        """
        self._report_failures = show_failures

        return self


    def process(self):
        """
        Processes the dataset using the Python CSV parser
        """
        self._reset()
        self._report_test_configuration()
        print("Starting file load")
        file_load = time.perf_counter_ns()

        # Open and read the CSV file
        with open(self._dataset_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Process line-by-line (Memory efficient!)
            for row in reader:
                result = self._agent.predict(self._context(row), self._questions)
                self._total_records += 1

                row_result = result["answers"]["email_category"]
                if row_result["choice"] != row['category']:
                    expected = row['category']
                    actual = row_result["choice"]
                    key = expected + "+" + actual
                    self._failure_categories[key] = self._failure_categories.get(key, 0) + 1
                    self._error_count += 1

        print("Processing time (ms):", (time.perf_counter_ns() - file_load) / 1000000)

        self._report('CSV')

    def _report_test_configuration(self):
        """
        Prints a report of the processing
        """
        print("Test Configuration: ")
        print(" - Structured Context: ", self._structured_context)
        print(" - Using Laya Router: ", self._using_router)
        processor_type = "Router" if self._using_router else "Direct Model Access"
        print(" - Processor Type: ", processor_type)
        print()

    def _report(self, processor_type: str):
        """
        Prints a report of the processing
        """
        print("Error Count: ", self._error_count)
        print("Total Rows: ", self._total_records)

        failure_rate = (self._error_count / self._total_records) * 100.0
        print("Failure Rate: ", failure_rate, "%")
        if self._report_failures:
            for key in self._failure_categories:
                print(f"Failure count for {key}: {self._failure_categories[key]}")

        print("--------------------------------")

    def _reset(self):
        """
        Reset key internal metrics used for reporting
        :return:
        """
        self._error_count = 0
        self._total_records = 0
        self._failure_categories = {}
        
    @staticmethod
    def _questions():
        """
        Returns a collection of questions to be asked.
        """

        return {
            "email_category": {
                "type": "choice",
                "instructions": "Which category does this email belong to?",
                "criteria": {
                    "promotions": "Marketing emails, sales, offers, and advertisements",
                    "spam": "Unwanted emails, scams, and phishing attempts",
                    "social_media": "Notifications from social platforms",
                    "forum": "Forum posts, discussions, and community notifications",
                    "verify_code": "Authentication codes and verification emails",
                    "updates": "System updates, security patches, maintenance notices"
                }
            }
        }

    @classmethod
    def get_router_agent(cls) -> Router:
        """
        Retrieves a Router-based agent from the cache if available or initializes a new one.
        :return:
        """
        if cls._router_agent is None:
            print("Initializing Router models")
            model_load = time.perf_counter_ns()
            cls._router_agent = Router(preload=True, device="mps")
            print("Model load time (ms):", (time.perf_counter_ns() - model_load) / 1000000)

        return cast(Router, cls._router_agent)

    @classmethod
    def get_direct_model_agent(cls, model_name: str) -> Router:
        """
        Retrieves a Direct Model Access agent from the cache if available or initializes a new one.
        :return:
        """
        if cls._direct_model_agent.get(model_name) is None:
            print("Initializing Direct model: ", model_name)
            model_load = time.perf_counter_ns()
            cls._direct_model_agent[model_name] = laya.load(model_name)

            print("Model load time (ms):", (time.perf_counter_ns() - model_load) / 1000000)

        return cls._direct_model_agent[model_name]