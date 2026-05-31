import json
import os
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])


def build_response(status_code, body, request_id):
    body['request_id'] = request_id
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }


def lambda_handler(event, context):
    request_id = context.aws_request_id

    params = event.get('queryStringParameters') or {}

    try:
        limit = int(params.get('limit', 10))
        if limit < 1 or limit > 100:
            logger.warning(json.dumps({'action': 'getall', 'error': 'Limit must be between 1 and 100', 'request_id': request_id}))
            return build_response(400, {'message': 'Limit must be between 1 and 100'}, request_id)
    except (ValueError, TypeError):
        logger.warning(json.dumps({'action': 'getall', 'error': 'Limit must be an integer', 'request_id': request_id}))
        return build_response(400, {'message': 'Limit must be an integer'}, request_id)

    last_key = params.get('last_key')
    scan_kwargs = {'Limit': limit}

    if last_key:
        scan_kwargs['ExclusiveStartKey'] = {'id': last_key}

    try:
        result = table.scan(**scan_kwargs)
    except ClientError as e:
        logger.error(json.dumps({'action': 'getall', 'error': str(e), 'request_id': request_id}))
        return build_response(500, {'message': 'Internal server error'}, request_id)

    items = result['Items']
    next_key = result.get('LastEvaluatedKey', {}).get('id')

    logger.info(json.dumps({'action': 'getall', 'count': len(items), 'request_id': request_id}))
    return build_response(200, {'count': len(items), 'data': items, 'next_key': next_key}, request_id)
