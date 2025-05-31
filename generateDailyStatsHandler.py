import boto3
import datetime
from dateutil import parser  # Make sure to include python-dateutil in your Lambda layer or package

# AWS Clients
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CloudDishOrders')

sns = boto3.client('sns')
s3 = boto3.client('s3')

# Constants
SNS_TOPIC_ARNS = [
    'arn:aws:sns:us-east-1:075381376422:cloudDishDailyStatsTopic',
    # Add more SNS topic ARNs if needed
]
S3_BUCKET_NAME = 'clouddish-daily-reports'

def lambda_handler(event, context):
    # Step 1: Determine yesterday’s date
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    # Step 2: Scan the table
    response = table.scan()
    items = response.get('Items', [])

    stats = {}

    for item in items:
        timestamp_str = item.get('orderTimestamp', '')
        try:
            order_date = parser.parse(timestamp_str).date()
            if order_date == yesterday:
                dish = item.get('dishName', 'Unknown')
                quantity = int(item.get('quantity', 1))
                stats[dish] = stats.get(dish, 0) + quantity
        except Exception:
            continue  # Skip if timestamp is invalid

    # Step 3: Generate report
    formatted_date = yesterday.strftime('%Y-%m-%d')
    if stats:
        report_lines = [f"{dish}: {count} orders" for dish, count in stats.items()]
        report = f"📊 Daily stats for {formatted_date}:\n" + "\n".join(report_lines)
    else:
        report = f"📊 Daily stats for {formatted_date}:\nNo CloudDish orders were placed."

    # Step 4: Send report to SNS
    for topic_arn in SNS_TOPIC_ARNS:
        sns.publish(
            TopicArn=topic_arn,
            Subject=f"Daily CloudDish Stats for {formatted_date}",
            Message=report
        )

    # Step 5: Upload report to S3
    filename = f"cloudDishReport_{formatted_date}.txt"
    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=filename,
        Body=report.encode('utf-8')
    )

    return {
        'statusCode': 200,
        'body': f"Report emailed and saved to S3 as {filename}"
    }
