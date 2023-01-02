resource "azurerm_redis_cache" "redis" {
  name                = var.redis_name
  location            = var.location
  resource_group_name = var.rg_main

  family              = var.redis_family
  sku_name            = var.redis_sku_name

  minimum_tls_version = var.redis_tls_version
  capacity            = var.redis_capacity

  redis_configuration {
  }
}