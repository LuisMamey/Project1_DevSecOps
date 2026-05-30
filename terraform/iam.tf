resource "aws_iam_role" "notes_lambda_roles" {
  for_each = local.lambdas
  name = "${var.project_name}_${each.key}_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "notes_lambda_basic_execution" {
  for_each   = local.lambdas
  role       = aws_iam_role.notes_lambda_roles[each.key].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy" "notes_lambda_dynamodb_policies" {
  for_each = local.lambdas
  name = "${var.project_name}_${each.key}_policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = each.value.permissions
        Resource = aws_dynamodb_table.notes.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "notes_lambda_dynamodb_attachment" {
  for_each   = local.lambdas
  role       = aws_iam_role.notes_lambda_roles[each.key].name
  policy_arn = aws_iam_policy.notes_lambda_dynamodb_policies[each.key].arn
}
