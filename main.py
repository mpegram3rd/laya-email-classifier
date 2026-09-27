import laya
import csv
from typing import Literal

from laya import Router
import time

import laya_runner


def questions():
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

def main():
    runner = laya_runner.LayaRunner()

    # Run the direct model access permutations with CSV
    runner.use_router(False)
    runner.context_type(laya_runner.ContextTypes.SIMPLE).process_csv()
    runner.context_type(laya_runner.ContextTypes.STRUCTURED).process_csv()

    # Run Router-based tests with CSV
    runner.use_router(True)
    runner.context_type(laya_runner.ContextTypes.SIMPLE).process_csv()
    runner.context_type(laya_runner.ContextTypes.STRUCTURED).process_csv()

    # Switch over to using the pandas loader with direct model access
    runner.use_router(False)
    runner.context_type(laya_runner.ContextTypes.SIMPLE).process_pandas()
    runner.context_type(laya_runner.ContextTypes.STRUCTURED).process_pandas()

    # Switch over to using the pandas loader with direct model access
    runner.use_router(True)
    runner.context_type(laya_runner.ContextTypes.SIMPLE).process_pandas()
    runner.context_type(laya_runner.ContextTypes.STRUCTURED).report_failures(True).process_pandas()


if __name__ == "__main__":
    main()
