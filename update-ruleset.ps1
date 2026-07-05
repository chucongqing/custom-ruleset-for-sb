#!/usr/bin/env pwsh
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

Write-Host "Updating sing-geosite submodule to latest rule-set..."
git submodule update --init --recursive
git submodule update --remote --merge sing-geosite

Write-Host "Done."
