param(
  [string]$InstallRoot = "C:\\Phi4AIOps",
  [string]$OllamaModel = "phi4:mini"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
  Set-ExecutionPolicy Bypass -Scope Process -Force
  [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
  Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

choco install -y python git ollama

$python = "C:\\Python312\\python.exe"
if (-not (Test-Path $python)) { $python = "python" }

New-Item -Path $InstallRoot -ItemType Directory -Force | Out-Null
Set-Location $InstallRoot

if (-not (Test-Path "$InstallRoot\\venv")) {
  & $python -m venv "$InstallRoot\\venv"
}

& "$InstallRoot\\venv\\Scripts\\pip.exe" install --upgrade pip
& "$InstallRoot\\venv\\Scripts\\pip.exe" install fastapi uvicorn httpx faiss-cpu sentence-transformers python-dotenv tenacity

Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
Start-Sleep -Seconds 5
ollama pull $OllamaModel

$taskAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File C:\\Phi4AIOps\\collect-events.ps1"
$taskTrigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 15)
Register-ScheduledTask -TaskName "Phi4AIOpsCollectEvents" -Action $taskAction -Trigger $taskTrigger -RunLevel Highest -Force

Write-Host "Bootstrap complete. Next: deploy app service and Teams integration."
