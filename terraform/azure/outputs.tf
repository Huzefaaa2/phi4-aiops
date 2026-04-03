output "vm_public_ip" {
  value = azurerm_public_ip.this.ip_address
}

output "log_analytics_workspace_id" {
  value = azurerm_log_analytics_workspace.this.id
}
