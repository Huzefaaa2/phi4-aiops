variable "location" { type = string default = "eastus" }
variable "resource_group_name" { type = string default = "rg-phi4-aiops" }
variable "vm_admin_username" { type = string }
variable "vm_admin_password" { type = string sensitive = true }
variable "vm_size" { type = string default = "Standard_D8s_v5" }
variable "server_name" { type = string default = "win-az-aiops-01" }
variable "allowed_admin_cidr" { type = string default = "0.0.0.0/0" }
