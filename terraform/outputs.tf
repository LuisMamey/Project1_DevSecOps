output "notes_api_url" {
  value = aws_apigatewayv2_stage.notes_api_stage.invoke_url
  description = "Base URL for the Notes API"
}

output "github_actions_role_arn" {
  value       = aws_iam_role.github_actions_role.arn
  description = "Use this ARN as AWS_ROLE_ARN secret in GitHub"
}
