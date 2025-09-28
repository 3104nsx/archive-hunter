
param(
  [switch]$Rebuild = $false,
  [switch]$Doctor = $false
)

if ($Rebuild) {
  docker compose down
  docker compose build --no-cache
  docker compose up -d
  exit 0
}

if ($Doctor) {
  docker compose exec -T hunter-eu python tools/doctor.py
  exit 0
}

Write-Host "Usage: .\run.ps1 -Rebuild | -Doctor"
