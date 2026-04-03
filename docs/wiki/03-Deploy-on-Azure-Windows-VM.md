# 03 - Deploy on Azure Windows VM

## Step 1: Initialize Terraform

```bash
cd terraform/azure
terraform init
```

## Step 2: Apply Infrastructure

```bash
terraform apply \
  -var="vm_admin_username=<admin_user>" \
  -var="vm_admin_password=<strong_password>" \
  -var="allowed_admin_cidr=<your_cidr>"
```

## Step 3: Capture Outputs

Record:
- `vm_public_ip`
- `log_analytics_workspace_id`

## Step 4: Access VM

- RDP to the VM
- Open PowerShell as Administrator

