locals {
  region_abbr = {
    "us-east-1"      = "use1"
    "us-east-2"      = "use2"
    "us-west-1"      = "usw1"
    "us-west-2"      = "usw2"
    "eu-west-1"      = "euw1"
    "eu-west-2"      = "euw2"
    "eu-central-1"   = "euc1"
    "ap-southeast-1" = "apse1"
    "ap-southeast-2" = "apse2"
    "ap-northeast-1" = "apne1"
  }

  region_short = local.region_abbr[var.region]
  name_prefix  = "${var.company}-${var.project_name}-${var.environment}-${local.region_short}-${var.service}"

  common_tags = {
    org         = var.company
    project     = var.project_name
    environment = var.environment
    service     = var.service
    region      = var.region
    managed_by  = "terraform"
  }

  lambdas = {
    Create = {
      route_key   = "POST /"
      permissions = ["dynamodb:PutItem"]
    }
    GetById = {
      route_key   = "GET /{id}"
      permissions = ["dynamodb:GetItem"]
    }
    GetAll = {
      route_key   = "GET /"
      permissions = ["dynamodb:Scan"]
    }
    Update = {
      route_key   = "PUT /{id}"
      permissions = ["dynamodb:GetItem", "dynamodb:UpdateItem"]
    }
    Delete = {
      route_key   = "DELETE /{id}"
      permissions = ["dynamodb:GetItem", "dynamodb:DeleteItem"]
    }
  }
}
