# stop_streamlit.ps1
Get-Process -Name "streamlit" -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "Streamlit arrêté"