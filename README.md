# AWS Email Application

## Overview

This project demonstrates an AWS-based email application that allows users to subscribe to a newsletter via a web form, store the subscription information in DynamoDB, generate a CSV file of subscribers, and send personalized emails using AWS Lambda, SES, and S3. The infrastructure is managed using Terraform.

## Features

- **React Frontend**: A user-friendly web form for subscribing to the newsletter.
- **Flask Backend**: A REST API to handle subscription requests and store data in DynamoDB.
- **AWS Lambda**: Processes uploaded CSV files and sends personalized emails.
- **AWS SES**: Sends emails to subscribers.
- **AWS S3**: Stores the CSV files.
- **DynamoDB**: Stores subscription information.
- **Terraform**: Manages the AWS infrastructure.

## Architecture

![Architecture Diagram](aws-email-app/diagram.png)

## Prerequisites

- Node.js (v16.x)
- Python (v3.x)
- AWS CLI configured with appropriate permissions
- Terraform
- Git

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/your-username/aws-email-project.git
cd aws-email-project
```

### 2. Set up the Frontend
Navigate to the email-collection directory, install dependencies, and start the development server.

```sh
cd email-collection
npm install
npm start
```
### 3. Set up the Backend
Navigate to the email-api directory, install dependencies, and start the Flask server.

```sh
cd ../email-api
pip install Flask boto3 flask-cors
python app.py
```

### 4. Deploy the AWS resources with terraform
Navigate to the root directory and initialize and apply the Terraform configuration.

```sh
cd ..
terraform init
terraform apply
```

### 5. Generate & Upload the CSV file
Run the script to generate and upload a CSV file with subscriber emails.

```sh
python generate_and_upload_csv.py
```

## Usage

1. Subscribe to the Newsletter: Open the React application (http://localhost:3000), enter your email, and click the subscribe button (The button works with multiple clicks it just doesn't show the gloved hand cursor when hovering over the second time).
2. Verify Subscription: Check the DynamoDB table Emails in the AWS Management Console to ensure your email is stored.
3. Generate CSV: Run the generate_and_upload_csv.py script to create and upload a CSV file to S3.
4. Send Emails: The Lambda function will process the uploaded CSV file and send personalized emails to the subscribers.

## Cleaning up

To avoid incurring charges, run the following command to destroy all the AWS resources created by Terraform.

```sh
terraform destroy
```

