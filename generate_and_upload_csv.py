import csv
import boto3
from datetime import datetime

# Load bucket name from Terraform output file
with open("bucket_name.txt", "r") as f:
    bucket_name = f.read().strip()

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='ca-central-1')
table = dynamodb.Table('Emails')

# Initialize S3 client
s3_client = boto3.client('s3')

def fetch_emails_from_dynamodb():
    response = table.scan()
    items = response['Items']
    return items

def write_csv_file(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["email", "message"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def upload_to_s3(bucket_name, filename):
    s3_client.upload_file(filename, bucket_name, filename)

if __name__ == "__main__":
    filename = f"emails_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

    # Fetch emails from DynamoDB
    data = fetch_emails_from_dynamodb()

    # Prepare data with a sample message
    for item in data:
        item['message'] = f"Hello {item['email']}, this is your personalized message!"

    # Write data to CSV file
    write_csv_file(filename, data)

    # Upload CSV file to S3
    upload_to_s3(bucket_name, filename)

    print(f"CSV file {filename} generated and uploaded to S3 bucket {bucket_name}")
