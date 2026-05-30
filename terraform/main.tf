terraform {
  backend "s3" {
    bucket         = "project1-terraform-state-delvalle"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    use_lockfile   = true
  }

  required_providers {
    aws = {
        source  = "hashicorp/aws"
        version = "~> 5.0"
    }
    archive = {
        source  = "hashicorp/archive"
        version = "~> 2.0"
    }
  }
}

provider "aws" {
  region = var.region
}