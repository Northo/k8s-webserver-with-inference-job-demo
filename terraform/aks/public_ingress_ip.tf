resource "random_pet" "aks_domain_name_suffix" {
  length = 2
}

resource "azurerm_public_ip" "aks_ingress" {
  name                = "aks-pip"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  allocation_method = "Static"
  sku               = "Standard"

  domain_name_label = "${random_pet.aks_domain_name_suffix.id}-aks"
}