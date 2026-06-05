import json
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_table():
    with patch("lambdas.Create.lambda_function.table") as mock:
        yield mock


def make_event(body=None):
    return {
        "body": body,
        "pathParameters": None,
        "queryStringParameters": None
    }


def make_context():
    context = MagicMock()
    context.aws_request_id = "test-request-id"
    return context


def test_create_success(mock_table):
    mock_table.put_item.return_value = {}
    event = make_event(body='{"name": "Mi nota de prueba"}')
    context = make_context()

    from lambdas.Create.lambda_function import lambda_handler
    response = lambda_handler(event, context)

    assert response["statusCode"] == 201
    body = json.loads(response["body"])
    assert "id" in body
    assert body["request_id"] == "test-request-id"
    mock_table.put_item.assert_called_once()


def test_create_no_body(mock_table):
    event = make_event(body=None)
    context = make_context()

    from lambdas.Create.lambda_function import lambda_handler
    response = lambda_handler(event, context)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert body["message"] == "Request body is required"


def test_create_invalid_json(mock_table):
    event = make_event(body="esto no es json")
    context = make_context()

    from lambdas.Create.lambda_function import lambda_handler
    response = lambda_handler(event, context)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert body["message"] == "Invalid JSON in request body"


def test_create_no_name(mock_table):
    event = make_event(body='{"title": "sin campo name"}')
    context = make_context()

    from lambdas.Create.lambda_function import lambda_handler
    response = lambda_handler(event, context)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert body["message"] == "Name is required"


def test_create_name_too_long(mock_table):
    long_name = "a" * 201
    event = make_event(body=json.dumps({"name": long_name}))
    context = make_context()

    from lambdas.Create.lambda_function import lambda_handler
    response = lambda_handler(event, context)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert "cannot exceed" in body["message"]