import laya
import csv
from typing import Literal

from laya import Router
import time

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
    # Preload checkpoints into memory for instant sub-35ms routing
    print("Starting model load")
    model_load = time.perf_counter_ns()
#    agent = Router(preload=True, device="mps")
    agent = laya.load("convaiinnovations/laya")
    print("Model load time (ms):", (time.perf_counter_ns() - model_load) / 1000000)


    print("Starting file load")
    file_load = time.perf_counter_ns()
    # Open and read the CSV file
    with open('dataset/full_dataset.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Create and store a count of the occurrences of each category in a dictionary
        # category_counts = {}

        # Get the collection of questions for the agent
        question_payload = questions()

        # Counters for errors and total predictions
        error_count = 0
        total_count = 0

        # Process line-by-line (Memory efficient!)
        for row in reader:
            context = row["text"]

#            context = {
#                "subject": row['subject'],
#                "body": row['body']
#            }

            result = agent.predict(context, question_payload)
            total_count += 1

            row_result = result["answers"]["email_category"]
            if (row_result["choice"] != row['category']):
                # confidence = row_result['confidence']
                # if confidence > 0.55:
                #     print(f"Mismatch: Id: {row['id']} Predicted: {row_result['choice']}, Actual: {row['category']}: Decision Confidence: {row_result['confidence']}")
                error_count += 1

            if total_count % 1000 == 0:
                print(f"Processed {total_count} rows")

            # category_counts[row['category']] = category_counts.get(row['category'], 0) + 1

    print("Error count:", error_count)
    print("Total count:", total_count)
    print("File Processing time (ms):", (time.perf_counter_ns() - file_load) / 1000000)

    # print("Distinct categories and their counts:", category_counts)

if __name__ == "__main__":
    main()
