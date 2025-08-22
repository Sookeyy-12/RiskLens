# RiskLens Streamlit App Launcher for Windows
# PowerShell script to launch the volatility analysis dashboard

Write-Host "🔥 RiskLens - Volatility Analysis Dashboard" -ForegroundColor Red
Write-Host "===============================================" -ForegroundColor Cyan

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AppPath = Join-Path $ScriptDir "app\main.py"

# Check if the main.py file exists
if (-not (Test-Path $AppPath)) {
    Write-Host "❌ Error: Could not find $AppPath" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if poetry is available
try {
    $null = Get-Command poetry -ErrorAction Stop
    $UsePoetry = $true
    Write-Host "✅ Poetry found - using virtual environment" -ForegroundColor Green
} catch {
    $UsePoetry = $false
    Write-Host "⚠️  Poetry not found - using system Python" -ForegroundColor Yellow
}

# Check if streamlit is installed
try {
    if ($UsePoetry) {
        $null = poetry run python -c "import streamlit" 2>$null
    } else {
        $null = Get-Command streamlit -ErrorAction Stop
    }
    Write-Host "✅ Streamlit found" -ForegroundColor Green
} catch {
    Write-Host "❌ Streamlit not found. Please install it with:" -ForegroundColor Red
    if ($UsePoetry) {
        Write-Host "   poetry add streamlit" -ForegroundColor Yellow
    } else {
        Write-Host "   pip install streamlit" -ForegroundColor Yellow
    }
    Read-Host "Press Enter to exit"
    exit 1
}

# Launch the application
try {
    Write-Host "🚀 Starting RiskLens Dashboard..." -ForegroundColor Green
    Write-Host "📁 App location: $AppPath" -ForegroundColor Gray
    Write-Host "🌐 Opening in your default browser..." -ForegroundColor Gray
    Write-Host "⏹️  Press Ctrl+C to stop the application" -ForegroundColor Yellow
    Write-Host "===============================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Run streamlit with dark theme
    if ($UsePoetry) {
        Write-Host "🎯 Using poetry environment" -ForegroundColor Cyan
        streamlit run $AppPath --theme.base dark --theme.primaryColor "#ff6b6b" --theme.backgroundColor "#0e1117" --theme.secondaryBackgroundColor "#262730" --theme.textColor "#fafafa"
    } else {
        streamlit run $AppPath --theme.base dark --theme.primaryColor "#ff6b6b" --theme.backgroundColor "#0e1117" --theme.secondaryBackgroundColor "#262730" --theme.textColor "#fafafa"
    }
    
} catch {
    Write-Host "❌ Error launching application: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "👋 RiskLens application stopped." -ForegroundColor Yellow
