# Managed identity, roles, and federation for AKS to access storage account

resource "azurerm_user_assigned_identity" "aks_storage_identity" {
  name                = "aks-storage-identity"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_role_assignment" "aks_storage_blob_data_contributor" {
  scope                = azurerm_storage_account.main.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.aks_storage_identity.principal_id
}

resource "azurerm_federated_identity_credential" "aks_storage_federation" {
  name                = "aks-storage-federation"
  resource_group_name = azurerm_resource_group.main.name
  parent_id           = azurerm_user_assigned_identity.aks_storage_identity.id

  audience = ["api://AzureADTokenExchange"]
  subject  = "system:serviceaccount:demo:storage-access-sa"
  issuer   = azurerm_kubernetes_cluster.aks.oidc_issuer_url
}