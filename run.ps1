Write-Host "Financial Controlling Dashboard Setup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if execution policy might block the script
$policy = Get-ExecutionPolicy -Scope CurrentUser
if ($policy -eq "Restricted") {
    Write-Host "Warning: Your execution policy is set to Restricted." -ForegroundColor Yellow
    Write-Host "You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Installing dependencies..." -ForegroundColor Green
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
    Write-Host "Starting Financial Dashboard..." -ForegroundColor Green
    streamlit run app.py
} else {
    Write-Host "Failed to install dependencies. Please check your Python installation." -ForegroundColor Red
}

Read-Host -Prompt "Press Enter to exit"