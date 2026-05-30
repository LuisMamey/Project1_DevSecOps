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

    note_id = event.get('pathParameters', {}).get('id')
    if not note_id:
        return build_response(400, {'message': 'Path parameter id is required'}, request_id)

    try:
        result = table.get_item(Key={'id': note_id})
    except ClientError as e:
        logger.error(json.dumps({'action': 'getbyid', 'error': str(e), 'request_id': request_id}))
        return build_response(500, {'message': 'Internal server error'}, request_id)

    item = result.get('Item')
    if not item:
        return build_response(404, {'message': 'Item not found'}, request_id)

    logger.info(json.dumps({'action': 'getbyid', 'id': note_id, 'request_id': request_id}))
    return build_response(200, {'id': note_id, 'name': item['name']}, request_id)
