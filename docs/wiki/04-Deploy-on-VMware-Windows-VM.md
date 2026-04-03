# 04 - Deploy on VMware Windows VM

## Step 1: Prepare Template

Ensure template has:
- VMware Tools
- Sysprep customization support
- Windows patch baseline

## Step 2: Initialize Terraform

```bash
cd terraform/vmware
terraform init
```

## Step 3: Apply Infrastructure

```bash
terraform apply \
  -var="vsphere_server=<vcenter>" \
  -var="vsphere_user=<user>" \
  -var="vsphere_password=<password>" \
  -var="datacenter=<dc>" \
  -var="cluster=<cluster>" \
  -var="datastore=<datastore>" \
  -var="network=<portgroup>" \
  -var="template_name=<template>" \
  -var="admin_password=<windows_pwd>" \
  -var="ipv4_address=<ip>" \
  -var="ipv4_gateway=<gateway>"
```

