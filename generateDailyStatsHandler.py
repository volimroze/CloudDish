import boto3
import datetime

# AWS Clients
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CloudDishOrders')

sns = boto3.client('sns')
s3 = boto3.client('s3')

# Constants
SNS_TOPIC_ARNS = [
    'arn:aws:sns:us-east-1:075381376422:cloudDishDailyStatsTopic',
    # Add more SNS topic ARNs here if needed
]
S3_BUCKET_NAME = 'clouddish-daily-reports'

def lambda_handler(event, context):
    # Determine yesterday’s date
    today = datetime.date.today() - datetime.timedelta(days=1)
    formatted_date = today.strftime('%Y-%m-%d')

    # Scan the table and filter by date
    response = table.scan()
    items = response.get('Items', [])

    stats = {}
    for item in items:
        timestamp = item.get('orderTimestamp', '')
        if timestamp.startswith(formatted_date):
            name = item['dishName']
            stats[name] = stats.get(name, 0) + int(item.get('quantity', 1))

    # Generate report content
    if stats:
        report_lines = [f"{dish}: {count} orders" for dish, count in stats.items()]
        report = f"📊 Daily stats for {formatted_date}:\n" + "\n".join(report_lines)
    else:
        report = f"📊 Daily stats for {formatted_date}:\nNo CloudDish orders were placed."

    # Send report to SNS (always, even if empty)
    for topic_arn in SNS_TOPIC_ARNS:
        sns.publish(
            TopicArn=topic_arn,
            Subject=f"Daily CloudDish Stats for {formatted_date}",
            Message=report
        )

    # Upload report to S3
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
