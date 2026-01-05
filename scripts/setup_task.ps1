# setup_task.ps1
$taskName = "StreamlitKeepAlive"
$scriptPath = "C:\Users\bours\Documents\Esilv\A4\Python, Git and Linux\project_root\scripts\keep_alive.ps1"

# Supprimer la tâche si elle existe déjà
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

# Créer la tâche planifiée
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Maintient Streamlit en vie"

Write-Host "Tâche planifiée créée avec succès !"