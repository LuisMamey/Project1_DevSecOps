import json
import os
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

MAX_NAME_LENGTH = 200


def build_response(status_code, body, request_id):
    body['request_id'] = request_id
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }


def lambda_handler(event, context):
    request_id = context.aws_request_id

    request = event.get('body')
    if not request:
        return build_response(400, {'message': 'Request body is required'}, request_id)

    try:
        body = json.loads(request)
    except json.JSONDecodeError:
        return build_response(400, {'message': 'Invalid JSON in request body'}, request_id)

    note_id = event.get('pathParameters', {}).get('id')
    if not note_id:
        return build_response(400, {'message': 'Path parameter id is required'}, request_id)

    name = body.get('name')
    if not name:
        return build_response(400, {'message': 'Field name is required'}, request_id)

    if len(name) > MAX_NAME_LENGTH:
        return build_response(400, {'message': f'Name cannot exceed {MAX_NAME_LENGTH} characters'}, request_id)

    try:
        result = table.get_item(Key={'id': note_id})
        if not result.get('Item'):
            return build_response(404, {'message': 'Item not found'}, request_id)

        table.update_item(
            Key={'id': note_id},
            UpdateExpression="SET #n = :name",
            ExpressionAttributeNames={'#n': 'name'},
            ExpressionAttributeValues={':name': name}
        )
    except ClientError as e:
        logger.error(json.dumps({'action': 'update', 'error': str(e), 'request_id': request_id}))
        return build_response(500, {'message': 'Internal server error'}, request_id)

    logger.info(json.dumps({'action': 'update', 'id': note_id, 'request_id': request_id}))
    return build_response(200, {'message': 'Item updated successfully'}, request_id)
