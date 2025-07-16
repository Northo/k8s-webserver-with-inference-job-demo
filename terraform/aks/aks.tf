resource "azurerm_kubernetes_cluster" "aks" {
  name                = "aks-cluster"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "aks"

  oidc_issuer_enabled              = true
  workload_identity_enabled        = true

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_D2_v2"

    # Without upgrade_settings, we get a drift (where on every apply, the node pool is updated).
    upgrade_settings {
      drain_timeout_in_minutes      = 0
      max_surge                     = "10%"
      node_soak_duration_in_minutes = 0
    }
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    environment = "development"
  }
}

## There are problems with getting GPUs, due to quotas.
## For now, we will not use GPU nodes.

# resource "azurerm_kubernetes_cluster_node_pool" "gpu" {
#   name                  = "gpu"
#   kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id
#   vm_size               = "standard_nc4as_t4_v3"
#   node_count            = 0
#   auto_scaling_enabled  = true
#   min_count             = 0
#   max_count             = 3
#   tags = {
#     environment = "development"
#   }

#   node_taints = [
#     "key=gpu:NoSchedule",
#   ]
# }
