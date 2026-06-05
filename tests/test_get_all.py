import json
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_table():
    with patch("lambdas.GetAll.lambda_function.table") as mock:
        yield mock


def make_event(query_params=None):
    return {
        "body": None,
        "pathParameters": None,
        "queryStringParameters": query_params,
    }


def make_context():
    context = MagicMock()
    context.aws_request_id = "test-request-id"
    return context


def test_get_all_success(mock_table):
    mock_table.scan.return_value = {
        "Items": [{"id": "1", "name": "Note 1"}, {"id": "2", "name": "Note 2"}],
        "LastEvaluatedKey": None,
    }

    from lambdas.GetAll.lambda_function import lambda_handler

    response = lambda_handler(make_event(), make_context())
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["count"] == 2
    assert len(body["data"]) == 2


def test_get_all_with_pagination(mock_table):
    mock_table.scan.return_value = {
        "Items": [{"id": "3", "name": "Note 3"}],
        "LastEvaluatedKey": {"id": "3"},
    }

    from lambdas.GetAll.lambda_function import lambda_handler

    response = lambda_handler(make_event({"limit": "1"}), make_context())
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["next_key"] == "3"


def test_get_all_limit_too_low(mock_table):
    from lambdas.GetAll.lambda_function import lambda_handler

    response = lambda_handler(make_event({"limit": "0"}), make_context())
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert "limit" in body["message"].lower()


def test_get_all_limit_too_high(mock_table):
    from lambdas.GetAll.lambda_function import lambda_handler

    response = lambda_handler(make_event({"limit": "101"}), make_context())
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert "limit" in body["message"].lower()


def test_get_all_limit_not_integer(mock_table):
    from lambdas.GetAll.lambda_function import lambda_handler

    response = lambda_handler(make_event({"limit": "abc"}), make_context())
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert "integer" in body["message"].lower()


def test_get_all_dynamodb_error(mock_table):
    from botocore.exceptions import ClientError

    mock_table.scan.side_effect = ClientError(
        {"Error": {"Code": "InternalServerError", "Message": "DynamoDB error"}},
        "Scan",
    )

    from lambdas.GetAll.lambda_function import lambda_handler

    response = lambda_handler(make_event(), make_context())
    body = json.loads(response["body"])

    assert response["statusCode"] == 500
    assert "internal" in body["message"].lower()
