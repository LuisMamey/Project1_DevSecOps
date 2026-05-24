resource "aws_dynamodb_table" "notes" {
  name           = "${var.project_name}_${var.table_name}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }
}