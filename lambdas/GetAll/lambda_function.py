import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    
    params = event.get('queryStringParameters') or {}
    try:
        limit = int(params.get('limit', 10))
        if limit > 100:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Limit cannot be greater than 100'})
            }
    except:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Limit must be an integer'})
        }

    last_key = params.get('last_key')

    scan_kwargs = {'Limit': limit}
    
    if last_key:
        check = table.get_item(Key={'id': last_key})
        if not check.get('Item'):
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid last_key'})
            }
        scan_kwargs['ExclusiveStartKey'] = {'id': last_key}

    response = table.scan(**scan_kwargs)
    
    items = response['Items']
    next_key = response.get('LastEvaluatedKey', {}).get('id')

    return {
        'statusCode': 200,
        'body': json.dumps({
            'count': len(items),
            'data': items,
            'next_key': next_key
        })
    }