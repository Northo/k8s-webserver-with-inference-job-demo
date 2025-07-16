output "aks_oidc_issuer" {
  value = azurerm_kubernetes_cluster.aks.oidc_issuer_url
}

output "storage_account_key" {
  value     = azurerm_storage_account.main.primary_access_key
  sensitive = true
}

output "aks_storage_identity_id" {
  value = azurerm_user_assigned_identity.aks_storage_identity.id
}

output "public_ip_address" {
  value = azurerm_public_ip.aks_ingress.ip_address
}

output "fqdn" {
  value = azurerm_public_ip.aks_ingress.fqdn
}