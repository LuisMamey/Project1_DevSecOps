import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):

    id = event.get('pathParameters', {}).get('id')

    if not id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Path parameter id is required'})
        }

    response = table.get_item(
        Key={
            'id': id
        }
    )

    item = response.get('Item')

    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps({
                "message": "Item not found"
            })
        }

    return {
        'statusCode': 200,
        'body': json.dumps({
            "id": id,
            "name": item['name']
        })
    }