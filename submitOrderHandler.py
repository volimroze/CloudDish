import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CloudDishOrders')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    dish_name = body['dishName']
    quantity = body['quantity']

    # genera timestamp UTC in formato ISO 8601
    timestamp = datetime.utcnow().isoformat()

    table.put_item(
        Item={
            'dishName': dish_name,
            'orderTimestamp': timestamp,
            'quantity': quantity
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Order registered with success'})
    }
