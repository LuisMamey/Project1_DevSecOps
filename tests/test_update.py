import json
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_table():
    with patch("lambdas.Update.lambda_function.table") as mock:
        yield mock


def make_event(note_id=None, body=None):
    return {
        "body": body,
        "pathParameters": {"id": note_id} if note_id else {},
        "queryStringParameters": None,
    }


def make_context():
    context = MagicMock()
    context.aws_request_id = "test-request-id"
    return context


def test_update_success(mock_table):
    mock_table.get_item.return_value = {"Item": {"id": "abc-123", "name": "Old Name"}}

    from lambdas.Update.lambda_function import lambda_handler

    response = lambda_handler(
        make_event("abc-123", json.dumps({"name": "New Name"})), make_context()
    )
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert "updated" in body["message"].lower()
    mock_table.update_item.assert_called_once()


def test_update_no_body(mock_table):
    from lambdas.Update.lambda_function import lambda_handler

    response = lambda_handler(make_event("abc-123"), make_context())
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert "body" in body["message"].lower()


def test_update_invalid_json(mock_table):
    from lambdas.Update.lambda_function import lambda_handler

    response = lambda_handler(make_event("abc-123", "not-json"), make_context())
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert "json" in body["message"].lower()


def test_update_missing_id(mock_table):
    from lambdas.Update.lambda_function import lambda_handler

    response = lambda_handler(
        make_event(body=json.dumps({"name": "New Name"})), make_context()
    )
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert "id" in body["message"].lower()


def test_update_missing_name(mock_table):
    from lambdas.Update.lambda_function import lambda_handler

    response = lambda_handler(make_event("abc-123", json.dumps({})), make_context())
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert "name" in body["message"].lower()


def test_update_name_too_long(mock_table):
    from lambdas.Update.lambda_function import lambda_handler

    response = lambda_handler(
        make_event("abc-123", json.dumps({"name": "a" * 201})), make_context()
    )
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert "200" in body["message"]


def test_update_not_found(mock_table):
    mock_table.get_item.return_value = {}

    from lambdas.Update.lambda_function import lambda_handler

    response = lambda_handler(
        make_event("nonexistent", json.dumps({"name": "New Name"})), make_context()
    )
    body = json.loads(response["body"])

    assert response["statusCode"] == 404
    assert "not found" in body["message"].lower()


def test_update_dynamodb_error(mock_table):
    from botocore.exceptions import ClientError

    mock_table.get_item.side_effect = ClientError(
        {"Error": {"Code": "InternalServerError", "Message": "DynamoDB error"}},
        "GetItem",
    )

    from lambdas.Update.lambda_function import lambda_handler

    response = lambda_handler(
        make_event("abc-123", json.dumps({"name": "New Name"})), make_context()
    )
    body = json.loads(response["body"])

    assert response["statusCode"] == 500
    assert "internal" in body["message"].lower()
