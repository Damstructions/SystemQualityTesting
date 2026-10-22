if (Get-Command npm -ErrorAction SilentlyContinue) {
    Write-Host "npm already installed: $(npm --version)"
    exit 0
}

Write-Host "npm not found. Installing Node.js LTS via winget..."
winget install --id OpenJS.NodeJS.LTS --exact --silent `
    --accept-package-agreements --accept-source-agreements --disable-interactivity

Write-Host "Installation complete. Please open a new PowerShell window and run: npm --version"