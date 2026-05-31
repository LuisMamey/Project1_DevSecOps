resource "aws_cloudwatch_log_group" "notes_api_logs" {
  name              = "/aws/apigateway/${local.name_prefix}-api"
  retention_in_days = 30
  tags              = local.common_tags
}

resource "aws_apigatewayv2_api" "notes_api" {
  name          = "${local.name_prefix}-api"
  protocol_type = "HTTP"
  tags          = local.common_tags
}

resource "aws_apigatewayv2_stage" "notes_api_stage" {
  api_id      = aws_apigatewayv2_api.notes_api.id
  name        = var.environment
  auto_deploy = var.environment != "prod"

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.notes_api_logs.arn
    format = jsonencode({
      requestId        = "$context.requestId"
      ip               = "$context.identity.sourceIp"
      httpMethod       = "$context.httpMethod"
      routeKey         = "$context.routeKey"
      status           = "$context.status"
      responseLength   = "$context.responseLength"
      integrationError = "$context.integrationErrorMessage"
    })
  }

  default_route_settings {
    throttling_burst_limit = 100
    throttling_rate_limit  = 50
  }

  tags = local.common_tags
}

resource "aws_apigatewayv2_integration" "notes_lambda_integrations" {
  for_each               = local.lambdas
  api_id                 = aws_apigatewayv2_api.notes_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.notes_functions[each.key].invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "notes_lambda_routes" {
  for_each  = local.lambdas
  api_id    = aws_apigatewayv2_api.notes_api.id
  route_key = each.value.route_key
  target    = "integrations/${aws_apigatewayv2_integration.notes_lambda_integrations[each.key].id}"

  authorization_type = "JWT"
  authorizer_id      = aws_apigatewayv2_authorizer.notes_jwt_authorizer.id
}
