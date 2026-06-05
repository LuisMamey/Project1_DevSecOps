import json
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_table():
    with patch("lambdas.Delete.lambda_function.table") as mock:
        yield mock


def make_event(note_id=None):
    return {
        "body": None,
        "pathParameters": {"id": note_id} if note_id else {},
        "queryStringParameters": None,
    }


def make_context():
    context = MagicMock()
    context.aws_request_id = "test-request-id"
    return context


def test_delete_success(mock_table):
    mock_table.get_item.return_value = {"Item": {"id": "abc-123", "name": "My Note"}}

    from lambdas.Delete.lambda_function import lambda_handler

    response = lambda_handler(make_event("abc-123"), make_context())
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert "deleted" in body["message"].lower()
    mock_table.delete_item.assert_called_once_with(Key={"id": "abc-123"})


def test_delete_missing_id(mock_table):
    from lambdas.Delete.lambda_function import lambda_handler

    response = lambda_handler(make_event(), make_context())
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert "id" in body["message"].lower()


def test_delete_not_found(mock_table):
    mock_table.get_item.return_value = {}

    from lambdas.Delete.lambda_function import lambda_handler

    response = lambda_handler(make_event("nonexistent"), make_context())
    body = json.loads(response["body"])

    assert response["statusCode"] == 404
    assert "not found" in body["message"].lower()


def test_delete_dynamodb_error(mock_table):
    from botocore.exceptions import ClientError

    mock_table.get_item.side_effect = ClientError(
        {"Error": {"Code": "InternalServerError", "Message": "DynamoDB error"}},
        "GetItem",
    )

    from lambdas.Delete.lambda_function import lambda_handler

    response = lambda_handler(make_event("abc-123"), make_context())
    body = json.loads(response["body"])

    assert response["statusCode"] == 500
    assert "internal" in body["message"].lower()
