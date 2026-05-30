locals {
  lambdas = {
    Create = {
        route_key = "POST /"
        permissions = ["dynamodb:PutItem"]
    }
    GetById = {
        route_key = "GET /{id}"
        permissions = ["dynamodb:GetItem"]
    }
    GetAll = {
        route_key = "GET /"
        permissions = ["dynamodb:Scan"]
    }
    Update = {
        route_key = "PUT /{id}"
        permissions = ["dynamodb:GetItem", "dynamodb:UpdateItem"]
    }
    Delete = {
        route_key = "DELETE /{id}"
        permissions = ["dynamodb:GetItem", "dynamodb:DeleteItem"]
    }
  }
}