# start_streamlit.ps1
$projectRoot = "C:\Users\bours\Documents\Esilv\A4\Python, Git and Linux\project_root"

# Créer le dossier logs
if (-not (Test-Path "$projectRoot\logs")) {
    New-Item -ItemType Directory -Path "$projectRoot\logs"
}

# Arrêter les anciennes instances
Get-Process -Name "streamlit" -ErrorAction SilentlyContinue | Stop-Process -Force

# Attendre
Start-Sleep -Seconds 2

# Démarrer Streamlit
Set-Location $projectRoot
Start-Process -FilePath "streamlit" -ArgumentList "run", "app\main.py", "--server.port=8501" -RedirectStandardOutput "logs\streamlit.log" -RedirectStandardError "logs\streamlit_error.log" -WindowStyle Hidden

Write-Host "Streamlit démarré sur le port 8501"
Write-Host "Logs: logs\streamlit.log"