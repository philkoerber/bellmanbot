
# Exit script on any error
$ErrorActionPreference = "Stop"

# Install Chocolatey (if not already installed)
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Output "Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force;
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'));
}

# Install Docker Desktop using Chocolatey
Write-Output "Installing Docker Desktop..."
choco install docker-desktop -y

# Start Docker Desktop
Write-Output "Starting Docker Desktop..."
Start-Process -Wait -FilePath "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# Wait until Docker is fully running
Write-Output "Waiting for Docker to start..."
while (-not (docker info -ErrorAction SilentlyContinue)) {
    Start-Sleep -Seconds 5
}

# Install Docker Compose (included in Docker Desktop)
Write-Output "Docker Compose is included with Docker Desktop, skipping separate installation."

# Navigate to the directory containing docker-compose.yml (change this to your project's directory)
cd "C:\path\to\your\project"

# Start Docker Compose
Write-Output "Starting Docker Compose..."
docker-compose up --build -d

Write-Output "Docker Compose has started successfully."