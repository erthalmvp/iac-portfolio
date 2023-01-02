resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.aks_cluster_name
  location            = var.location
  resource_group_name = var.aks_rg
  dns_prefix          = var.aks_dns_prefix
  kubernetes_version  = var.kubernetes_cluster_version

  default_node_pool {
    enable_auto_scaling  = true
    max_count            = var.node_pool_max_count
    min_count            = var.node_pool_min_count
    name                 = var.node_pool_name
    node_count           = var.node_pool_node_count
    vm_size              = var.nodesize
    orchestrator_version = var.orchestrator_version
    vnet_subnet_id       = "/subscriptions/${var.subscription}/resourceGroups/${var.rg_vnet}/providers/Microsoft.Network/virtualNetworks/${var.nome_vnet}/subnets/${var.subnet_aks_name}"
  }

  identity {
    type = var.identity_type
  }

  upgrade_settings {
    max_surge = 1
  }
}