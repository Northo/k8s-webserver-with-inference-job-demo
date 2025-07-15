terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.36.0"
    }
  }

  required_version = ">= 1.1.0"
}

variable subscription_id {
  type        = string
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

resource "azurerm_resource_group" "main" {
  name     = "k8s-demo-application"
  location = "north europe"
}
