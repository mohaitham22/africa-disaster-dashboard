# Africa Disaster Dashboard - Quick Deploy Script
# This script helps you deploy your dashboard to GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Africa Disaster Dashboard Deploy    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "✓ Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git is not installed!" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Host ""
Write-Host "This script will help you deploy to GitHub" -ForegroundColor Yellow
Write-Host ""

# Get GitHub username
$username = Read-Host "Enter your GitHub username"

if ([string]::IsNullOrWhiteSpace($username)) {
    Write-Host "✗ Username cannot be empty!" -ForegroundColor Red
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Host ""
Write-Host "Great! Your repository will be:" -ForegroundColor Green
Write-Host "https://github.com/$username/africa-disaster-dashboard" -ForegroundColor Cyan
Write-Host ""

$confirm = Read-Host "Continue? (yes/no)"

if ($confirm -ne "yes" -and $confirm -ne "y") {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "Starting deployment..." -ForegroundColor Cyan
Write-Host ""

# Initialize Git
Write-Host "[1/5] Initializing Git repository..." -ForegroundColor Yellow
git init
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Git initialized" -ForegroundColor Green
} else {
    Write-Host "✗ Git initialization failed" -ForegroundColor Red
}

# Add files
Write-Host ""
Write-Host "[2/5] Adding files to Git..." -ForegroundColor Yellow
git add .
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Files added" -ForegroundColor Green
} else {
    Write-Host "✗ Adding files failed" -ForegroundColor Red
}

# Commit
Write-Host ""
Write-Host "[3/5] Committing files..." -ForegroundColor Yellow
git commit -m "Initial commit - Africa Disaster Dashboard"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Files committed" -ForegroundColor Green
} else {
    Write-Host "✗ Commit failed" -ForegroundColor Red
}

# Add remote
Write-Host ""
Write-Host "[4/5] Adding GitHub remote..." -ForegroundColor Yellow
$repoUrl = "https://github.com/$username/africa-disaster-dashboard.git"
git remote remove origin 2>$null  # Remove if exists
git remote add origin $repoUrl
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Remote added: $repoUrl" -ForegroundColor Green
} else {
    Write-Host "✗ Adding remote failed" -ForegroundColor Red
}

# Set branch to main
Write-Host ""
Write-Host "[5/5] Setting main branch..." -ForegroundColor Yellow
git branch -M main
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Branch set to main" -ForegroundColor Green
} else {
    Write-Host "✗ Branch setting failed" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "      Local Setup Complete! ✓          " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Create repository on GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Cyan
Write-Host "   Name: africa-disaster-dashboard" -ForegroundColor Cyan
Write-Host "   Make it PUBLIC (required for free deployment)" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. After creating the repository, run:" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Then deploy on Streamlit Cloud:" -ForegroundColor White
Write-Host "   https://share.streamlit.io" -ForegroundColor Cyan
Write-Host ""
Write-Host "For detailed instructions, see DEPLOYMENT_GUIDE.md" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
