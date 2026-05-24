import json
import os
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    
    request = event.get('body')

    if not request:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Request body is required'})
        }
    
    try:
        body = json.loads(request)
    except:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid JSON in request body'})
        }

    name = body.get('name')

    if not name:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Name is required'})
        }
    
    id = str(uuid.uuid4())
    note = {
        'id': id,
        'name': name
    }

    table.put_item(Item=note)
    
    return {
        'statusCode': 201,
        'body': json.dumps(
            {'id': id},
        )
    }