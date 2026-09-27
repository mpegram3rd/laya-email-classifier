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
    # (laya_runner.LayaRunner()
    #     .simple_context()
    #     .use_direct_model()
    #     .process_csv()
    #  )

    # (laya_runner.LayaRunner()
    #     .simple_context()
    #     .use_router()
    #     .process_csv()
    #  )
    #
    # (laya_runner.LayaRunner()
    #     .structured_context()
    #     .use_router()
    #     .process_csv()
    #  )
    #
    # (laya_runner.LayaRunner()
    #     .structured_context()
    #     .use_direct_model()
    #     .process_csv()
    #  )
    #
    # (laya_runner.LayaRunner()
    #     .simple_context()
    #     .use_direct_model()
    #     .process_pandas()
    #  )
    #
    # (laya_runner.LayaRunner()
    #     .simple_context()
    #     .use_router()
    #     .process_pandas()
    #  )
    #
    # (laya_runner.LayaRunner()
    #     .structured_context()
    #     .use_router()
    #     .process_pandas()
    #  )
    #
    (laya_runner.LayaRunner()
        .structured_context()
        .use_direct_model()
        .process_pandas()
     )

if __name__ == "__main__":
    main()
