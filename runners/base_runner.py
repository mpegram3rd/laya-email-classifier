from abc import ABC, abstractmethod
from typing import Self

from models import ContextTypes


class BaseRunner(ABC):

    def __init__(self, dataset_file: str = "dataset/full_dataset.csv"):
        self._dataset_file = dataset_file
        self._structured_context = False
        self._report_failures = False
        self._error_count = 0
        self._total_records = 0
        self._failure_categories = {}

    @abstractmethod
    def process(self):
        """
        Processes the dataset
        """
        pass

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

    def report_failures(self, show_failures: bool) -> Self:
        """
        Indicate whether to include a failure report
        """
        self._report_failures = show_failures

        return self


    def _report_test_configuration(self):
        """
        Prints a report of the processing
        """
        print("Test Configuration: ")
        print(" - Structured Context: ", self._structured_context)

    def _report(self):
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

