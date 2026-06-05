output "notes_api_url" {
  value = aws_apigatewayv2_stage.notes_api_stage.invoke_url
  description = "Base URL for the Notes API"
}

output "github_actions_role_arn" {
  value       = aws_iam_role.github_actions_role.arn
  description = "Use this ARN as AWS_ROLE_ARN secret in GitHub"
}

output "cognito_user_pool_id" {
  value       = aws_cognito_user_pool.notes_user_pool.id
  description = "Cognito User Pool ID for user management"
}

output "cognito_client_id" {
  value       = aws_cognito_user_pool_client.notes_user_pool_client.id
  description = "Cognito Client ID for authentication requests"
}

output "cloudfront_url" {
  value       = "https://${aws_cloudfront_distribution.notes_api.domain_name}"
  description = "CloudFront URL for the Notes API"
}
