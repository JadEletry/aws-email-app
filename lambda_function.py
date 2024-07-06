import json
import boto3
import csv
import os

s3 = boto3.client('s3')
ses = boto3.client('ses')
sns = boto3.client('sns')

SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    csv_file = s3.get_object(Bucket=bucket_name, Key=object_key)
    csv_content = csv_file['Body'].read().decode('utf-8').splitlines()

    reader = csv.DictReader(csv_content)
    for row in reader:
        email = row['email']
        message = row['message']

        ses.send_email(
            Source='verified-email@example.com',
            Destination={
                'ToAddresses': [email]
            },
            Message={
                'Subject': {
                    'Data': 'Personalized Subject'
                },
                'Body': {
                    'Text': {
                        'Data': message
                    }
                }
            }
        )

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=f"Emails sent successfully for file {object_key}."
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Emails sent successfully!')
    }
