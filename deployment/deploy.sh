#!/bin/bash

# Exit on error
set -e

# Configuration
STACK_NAME="daily-uplift-sms"
S3_BUCKET="daily-uplift-sms-deployment-$(aws sts get-caller-identity --query 'Account' --output text)"
REGION=$(aws configure get region)
if [ -z "$REGION" ]; then
    REGION="us-east-1"  # Default region if not configured
fi

echo "Deploying Daily Uplift SMS to region: $REGION"

# Create S3 bucket if it doesn't exist
if ! aws s3api head-bucket --bucket $S3_BUCKET 2>/dev/null; then
    echo "Creating S3 bucket: $S3_BUCKET"
    aws s3 mb s3://$S3_BUCKET --region $REGION
    
    # Set bucket policy to block public access
    aws s3api put-public-access-block \
        --bucket $S3_BUCKET \
        --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
fi

# Package CloudFormation template
echo "Packaging CloudFormation template..."
aws cloudformation package \
    --template-file template.yaml \
    --s3-bucket $S3_BUCKET \
    --output-template-file packaged-template.yaml

# Deploy CloudFormation stack
echo "Deploying CloudFormation stack..."
aws cloudformation deploy \
    --template-file packaged-template.yaml \
    --stack-name $STACK_NAME \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides ScheduleExpression="cron(0 8 * * ? *)"

# Get outputs
echo "Deployment complete! Stack outputs:"
aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --query "Stacks[0].Outputs" \
    --output table

echo ""
echo "To subscribe a phone number to the SMS service, use the following command:"
echo "aws sns subscribe --topic-arn <SNS_TOPIC_ARN> --protocol sms --notification-endpoint +1XXXXXXXXXX"
echo ""
echo "Replace <SNS_TOPIC_ARN> with the UpliftSMSTopicARN from the outputs above."
echo "Replace +1XXXXXXXXXX with the phone number including country code."
