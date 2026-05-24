import json
import os
import boto3

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
    
    id = event.get('pathParameters', {}).get('id')

    if not id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Path parameter id is required'})
        }
    
    name = body.get('name')

    if not name:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Field name is required'})
        }

    response = table.get_item(Key={'id': id})
    item = response.get('Item')

    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Item not found'})
        }

    table.update_item(
        Key={'id': id},
        UpdateExpression="SET #n = :name",
        ExpressionAttributeNames={'#n': 'name'},
        ExpressionAttributeValues={':name': name}
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Item updated successfully'})
    }