param(
  [string]$ServerName = $env:COMPUTERNAME,
  [string]$OutputPath = "C:\\ProgramData\\Phi4AIOps\\logs",
  [int]$LookbackMinutes = 60
)

$ErrorActionPreference = "Stop"
New-Item -Path $OutputPath -ItemType Directory -Force | Out-Null

$events = Get-WinEvent -FilterHashtable @{
  LogName='Application','System','Security'
  StartTime=(Get-Date).AddMinutes(-$LookbackMinutes)
}

$file = Join-Path $OutputPath ("{0}-{1}.jsonl" -f $ServerName.ToLower(), (Get-Date -Format "yyyyMMddHHmm"))

foreach ($e in $events) {
  $obj = [ordered]@{
    server = $ServerName.ToLower()
    source = $e.ProviderName
    level = $e.LevelDisplayName
    event_id = $e.Id
    timestamp = $e.TimeCreated.ToUniversalTime().ToString("o")
    message = $e.Message
    tags = @("windows","eventlog")
  }
  ($obj | ConvertTo-Json -Compress -Depth 4) | Out-File -FilePath $file -Append -Encoding utf8
}

Write-Host "Collected $($events.Count) events into $file"
