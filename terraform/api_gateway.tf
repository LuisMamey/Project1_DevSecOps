resource "aws_apigatewayv2_api" "notes_api" {
    name          = "${var.project_name}_api"
    protocol_type  = "HTTP"
}

resource "aws_apigatewayv2_stage" "notes_api_stage" {
    api_id     = aws_apigatewayv2_api.notes_api.id
    name        = "staging"
    auto_deploy = true
}

resource "aws_apigatewayv2_integration" "notes_lambda_integrations" {
    for_each = local.lambdas
    api_id = aws_apigatewayv2_api.notes_api.id
    integration_type = "AWS_PROXY"
    integration_uri = aws_lambda_function.notes_functions[each.key].invoke_arn
    payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "notes_lambda_routes" {
  for_each    = local.lambdas
  api_id    = aws_apigatewayv2_api.notes_api.id
  route_key = each.value.route_key
  target    = "integrations/${aws_apigatewayv2_integration.notes_lambda_integrations[each.key].id}"
}
