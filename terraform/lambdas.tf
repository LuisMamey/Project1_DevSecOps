data "archive_file" "notes_lambda_zips" {
  for_each    = local.lambdas
  type        = "zip"
  source_file  = "../lambdas/${each.key}/lambda_function.py"
  output_path = "../lambdas/${each.key}/lambda_function.zip"
}

resource "aws_lambda_function" "notes_functions" {
  for_each    = local.lambdas
  function_name = "${var.project_name}_${each.key}_lambda"
  role          = aws_iam_role.notes_lambda_roles[each.key].arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.12"
  filename      = data.archive_file.notes_lambda_zips[each.key].output_path
  source_code_hash = data.archive_file.notes_lambda_zips[each.key].output_base64sha256

  environment {
    variables = {
      TABLE_NAME = "${var.project_name}_${var.table_name}"
    }
  }
}

resource "aws_lambda_permission" "notes_apigw_invoke_permission" {
  for_each    = local.lambdas
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.notes_functions[each.key].function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.notes_api.execution_arn}/*/*"
}
