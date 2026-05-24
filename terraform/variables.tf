variable "table_name" {
  type        = string
  description = "DynamoDB table name"
  default     = "notes"
}

variable "project_name" {
  type        = string
  description = "Project name for lambda function naming"
  default     = "project1"
}

variable "region" {
  type        = string
  description = "AWS region to deploy resources"
  default     = "us-east-1"
}