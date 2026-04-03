output "vm_name" {
  value = vsphere_virtual_machine.windows_aiops.name
}

output "vm_ip" {
  value = vsphere_virtual_machine.windows_aiops.default_ip_address
}
