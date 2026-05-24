locals {
  lambdas = {
    Create = {
        route_key = "POST /"
    }
    GetById = {
        route_key = "GET /{id}"
    }
    GetAll = {
        route_key = "GET /"
    }
    Update = {
        route_key = "PUT /{id}"
    }
    Delete = {
        route_key = "DELETE /{id}"
    }
  }
}