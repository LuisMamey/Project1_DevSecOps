resource "aws_apigatewayv2_api" "api" {
    name          = "${var.project_name}_api"
    protocol_type  = "HTTP"
}

resource "aws_apigatewayv2_stage" "staging" {
    api_id     = aws_apigatewayv2_api.api.id
    name        = "staging"
    auto_deploy = true
}

resource "aws_apigatewayv2_integration" "lambda_integrations" {
    for_each = local.lambdas
    api_id = aws_apigatewayv2_api.api.id
    integration_type = "AWS_PROXY"
    integration_uri = aws_lambda_function.lambdas[each.key].invoke_arn
    payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "lambda_routes" {
  for_each    = local.lambdas
  api_id    = aws_apigatewayv2_api.api.id
  route_key = each.value.route_key
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integrations[each.key].id}"
}