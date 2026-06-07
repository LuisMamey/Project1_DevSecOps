resource "aws_sns_topic" "alerts" {
  name = "${local.name_prefix}-alerts"
  kms_master_key_id = "alias/aws/sns"
  tags = local.common_tags
}

resource "aws_sns_topic_subscription" "alert_email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  for_each = local.lambdas

  alarm_name          = "${local.name_prefix}-${lower(each.key)}-errors"
  alarm_description   = "Lambda ${each.key} error rate"
  namespace           = "AWS/Lambda"
  metric_name         = "Errors"
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 1
  comparison_operator = "GreaterThanOrEqualToThreshold"

  dimensions = {
    FunctionName = aws_lambda_function.notes_functions[each.key].function_name
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
  tags          = local.common_tags
}
