resource "azurerm_cosmosdb_account" "account" {
	name = var.cosmosdb_account_name
	location = var.location
	resource_group_name = var.rg_main
	offer_type = var.cosmosdb_offer_type
	kind = var.cosmosdb_kind

	consistency_policy {
		consistency_level = "Session"
	}

	geo_location {
    	location = var.location
    	failover_priority = var.cosmosdb_failover_priority
	}
}

resource "azurerm_cosmosdb_mongo_database" "database" {
	name = var.cosmosdb_database_name
	resource_group_name = var.rg_main
	account_name = var.cosmosdb_account_name
	
	autoscale_settings {
		max_throughput = var.max_throughput
	}

	depends_on = [azurerm_cosmosdb_account.account,]
}

resource "azurerm_cosmosdb_mongo_collection" "collection" {
	resource_group_name = var.rg_main
	account_name = var.cosmosdb_account_name
	database_name = var.cosmosdb_database_name
	
	count = length(var.regionais)
	name = var.regionais[count.index]
	
	depends_on = [azurerm_cosmosdb_mongo_database.database,]
}