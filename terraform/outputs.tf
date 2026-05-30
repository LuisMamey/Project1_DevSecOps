output "notes_api_url" {
  value = aws_apigatewayv2_stage.notes_api_stage.invoke_url
}
