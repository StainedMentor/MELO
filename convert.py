import json
import csv

input_file = "Magazine_Subscriptions.jsonl"
output_file = "Magazine_Subscriptions_converted.csv"

with open(output_file, "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["rating", "reviewerID", "product_id", "date"])

    with open(input_file, 'r') as jsonl_file:
        for line in jsonl_file:
            try:
                record = json.loads(line.strip())

                rating = int(record.get("rating", None))
                reviewerID = record.get("user_id", "")
                product_id = record.get("asin", "")
                timestamp = int(record.get("timestamp", 0) / 1000)

                if rating is not None:
                    writer.writerow([rating, reviewerID, product_id, timestamp])
            except json.JSONDecodeError as e:
                print(f"Error decoding line: {e}")

