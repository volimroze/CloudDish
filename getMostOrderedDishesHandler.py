import json
import boto3
from collections import defaultdict
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CloudDishOrders')

def lambda_handler(event, context):
    query_params = event.get('queryStringParameters') or {}
    start_date = query_params.get('startDate')
    end_date = query_params.get('endDate')

    if not start_date and not end_date:
        # default: oggi UTC
        start_date = end_date = datetime.utcnow().date().isoformat()

    # se una sola delle due date è specificata, le equiparo
    if start_date and not end_date:
        end_date = start_date
    if end_date and not start_date:
        start_date = end_date

    response = table.scan()
    items = response.get('Items', [])

    dish_counts = defaultdict(int)
    for item in items:
        dish = item.get('dishName')
        quantity = int(item.get('quantity', 0))
        timestamp = item.get('orderTimestamp', '')
        order_date = timestamp[:10]

        if start_date <= order_date <= end_date:
            dish_counts[dish] += quantity

    result = [
        {"dishName": dish, "totalQuantity": total}
        for dish, total in sorted(dish_counts.items(), key=lambda x: x[1], reverse=True)
    ]

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        'body': json.dumps({'topDishes': result})
    }
