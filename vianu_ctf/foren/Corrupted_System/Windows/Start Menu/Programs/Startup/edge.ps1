Add-Type -AssemblyName "System.Windows.Forms"
Add-Type -AssemblyName "System.Drawing"

# Create a form but don't show it.
$form = New-Object System.Windows.Forms.Form
$form.Text = "U hacked"
$form.Size = New-Object System.Drawing.Size(200, 100)
$form.TopMost = $true
$form.ShowInTaskbar = $false  # Hide the form from the taskbar

$form.FormBorderStyle = [System.Windows.Forms.FormBorderStyle]::FixedToolWindow
$form.StartPosition = [System.Windows.Forms.FormStartPosition]::Manual
$form.Location = New-Object System.Drawing.Point(100, 100) # Start position (you can adjust)

$form.Show()

while ($true) {
    Start-Sleep -Seconds 0.1
    
    $screenWidth = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width
    $screenHeight = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height
    $randX = Get-Random -Minimum 0 -Maximum ($screenWidth - $form.Width)
    $randY = Get-Random -Minimum 0 -Maximum ($screenHeight - $form.Height)

    $form.Location = New-Object System.Drawing.Point($randX, $randY)
}