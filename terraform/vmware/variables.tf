variable "vsphere_server" { type = string }
variable "vsphere_user" { type = string }
variable "vsphere_password" { type = string sensitive = true }
variable "datacenter" { type = string }
variable "cluster" { type = string }
variable "datastore" { type = string }
variable "network" { type = string }
variable "template_name" { type = string }
variable "vm_name" { type = string default = "win-vmw-aiops-01" }
variable "admin_password" { type = string sensitive = true }
variable "domain" { type = string default = "corp.local" }
variable "ipv4_address" { type = string }
variable "ipv4_netmask" { type = number default = 24 }
variable "ipv4_gateway" { type = string }
variable "dns_servers" { type = list(string) default = [] }
