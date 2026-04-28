# Create HunterOS Desktop Shortcut
$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.IO.Path]::Combine($env:USERPROFILE, "Desktop")
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\HunterOS.lnk")
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-ExecutionPolicy Bypass -File `"C:\Users\User\Documents\Job-Hunter\launch_hunter.ps1`""
$Shortcut.WorkingDirectory = "C:\Users\User\Documents\Job-Hunter"
$Shortcut.WindowStyle = 1
$Shortcut.Description = "Launch HunterOS Platform"
# Note: Using a custom icon would require a .ico file. For now we use a default or generic icon.
# If we had a .ico, we could set $Shortcut.IconLocation = "path/to/icon.ico"
$Shortcut.Save()

Write-Host "HunterOS Desktop Shortcut created successfully!" -ForegroundColor Green
