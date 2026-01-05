# keep_alive.ps1
$logFile = "logs/keep_alive.log"
$projectRoot = "C:\Users\bours\Documents\Esilv\A4\Python, Git and Linux\project_root"

# Créer le dossier logs si nécessaire
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs"
}

# Vérifier si Streamlit tourne
$streamlitProcess = Get-Process -Name "streamlit" -ErrorAction SilentlyContinue

if ($null -eq $streamlitProcess) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $logFile -Value "$timestamp : Streamlit n'est pas en cours d'exécution. Redémarrage..."
    
    # Redémarrer Streamlit
    Set-Location $projectRoot
    Start-Process -FilePath "streamlit" -ArgumentList "run", "app/main.py", "--server.port=8501" -WindowStyle Hidden
    
    Add-Content -Path $logFile -Value "$timestamp : Streamlit redémarré"
} else {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $logFile -Value "$timestamp : Streamlit est en cours d'exécution"
}