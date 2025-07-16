resource "random_pet" "storage_account" {
  separator = ""
}

resource "azurerm_storage_account" "main" {
  name                     = "k8sdemo${random_pet.storage_account.id}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

output "storage_account_key" {
  value = azurerm_storage_account.main.primary_access_key
  sensitive = true
}
