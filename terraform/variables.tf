variable "company" {
  type        = string
  description = "Company or organization name"
  default     = "jocalev"

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.company))
    error_message = "Company name must be lowercase alphanumeric and hyphens only."
  }
}

variable "project_name" {
  type        = string
  description = "Project name"
  default     = "project1"

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "Project name must be lowercase alphanumeric and hyphens only."
  }
}

variable "service" {
  type        = string
  description = "Microservice or business domain name (e.g. notes, users, orders)"
  default     = "notes"

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.service))
    error_message = "Service name must be lowercase alphanumeric and hyphens only."
  }
}

variable "environment" {
  type        = string
  description = "Deployment environment"
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "region" {
  type        = string
  description = "AWS region to deploy resources"
  default     = "us-east-1"

  validation {
    condition = contains([
      "us-east-1", "us-east-2", "us-west-1", "us-west-2",
      "eu-west-1", "eu-west-2", "eu-central-1",
      "ap-southeast-1", "ap-southeast-2", "ap-northeast-1"
    ], var.region)
    error_message = "Region must be one of the supported AWS regions."
  }
}

variable "github_repo" {
  type        = string
  description = "GitHub repository in format owner/repo"
  default     = "LuisMamey/Project1_DevSecOps"

  validation {
    condition     = can(regex("^[\\w.-]+/[\\w.-]+$", var.github_repo))
    error_message = "Must be in format owner/repo."
  }
}