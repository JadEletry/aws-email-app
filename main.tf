provider "aws" {
  region = "ca-central-1"
}

resource "random_id" "bucket_id" {
  byte_length = 8
}

resource "random_id" "lambda_id" {
  byte_length = 8
}

resource "aws_s3_bucket" "email_csv_bucket" {
  bucket = "email-csv-bucket-${random_id.bucket_id.hex}"
  force_destroy = true

  versioning {
    enabled = true
  }
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda-email-role-${random_id.lambda_id.hex}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "ses_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSESFullAccess"
}

resource "aws_iam_role_policy_attachment" "s3_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy" "lambda_sns_policy" {
  name = "lambda-sns-policy-${random_id.lambda_id.hex}"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sns:Publish",
        Effect = "Allow",
        Resource = "*"
      }
    ]
  })
}

resource "aws_sns_topic" "email_notifications" {
  name = "email-notifications-${random_id.lambda_id.hex}"
}

resource "aws_lambda_function" "email_lambda" {
  filename         = "lambda_function.zip"
  function_name    = "email-lambda-function-${random_id.lambda_id.hex}"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.8"
  source_code_hash = filebase64sha256("lambda_function.zip")

  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.email_notifications.arn
    }
  }
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.email_lambda.function_name
  principal     = "s3.amazonaws.com"
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.email_csv_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.email_lambda.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".csv"
  }

  depends_on = [aws_lambda_function.email_lambda]
}

resource "aws_dynamodb_table" "emails" {
  name           = "Emails"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "email"

  attribute {
    name = "email"
    type = "S"
  }

  tags = {
    Name = "Emails"
  }
}
