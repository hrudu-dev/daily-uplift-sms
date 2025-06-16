import json
import random
import boto3
import os
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize SNS client
sns = boto3.client('sns')

# Get SNS topic ARN from environment variable
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

# List of uplifting messages and mental health tips
MESSAGES = [
    "You are capable of amazing things. Keep going!",
    "Take a moment to breathe deeply and appreciate this moment.",
    "Your mental health matters. Be kind to yourself today.",
    "Small steps forward are still progress. Celebrate them!",
    "It's okay to ask for help when you need it.",
    "You don't have to be perfect to be worthy of love and respect.",
    "Remember to drink water and take short breaks throughout your day.",
    "Your feelings are valid, but they don't define you.",
    "Today is a new opportunity to create positive change.",
    "Self-care isn't selfish, it's necessary.",
    "You've overcome difficult things before, and you can do it again.",
    "Progress isn't always visible, but that doesn't mean it's not happening.",
    "Your worth isn't measured by your productivity.",
    "Be proud of yourself for making it this far.",
    "It's okay to set boundaries that protect your peace.",
    "You are stronger than you think and braver than you believe.",
    "Healing isn't linear, and that's perfectly normal.",
    "Don't forget to celebrate your small victories today.",
    "You matter, even on the days when you don't feel like you do.",
    "Your best is enough, and it will always be enough."
]

def lambda_handler(event, context):
    try:
        # Select a random message
        message = random.choice(MESSAGES)
        logger.info(f"Selected message: {message}")
        
        # Publish message to SNS topic
        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject='Daily Uplift',
            MessageAttributes={
                'SMSType': {
                    'DataType': 'String',
                    'StringValue': 'Transactional'
                }
            }
        )
        
        logger.info(f"Message sent successfully: {response['MessageId']}")
        return {
            'statusCode': 200,
            'body': json.dumps('Daily message sent successfully!')
        }
        
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
