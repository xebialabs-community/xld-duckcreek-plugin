$source1 = "$($deployed.file)\$($source)"
$dest = "C:\\Windows\Temp\$($target)\"

robocopy $source1 $dest /S
$source1 = "$($deployed.file)\$($source)"
$dest = "C:\\Windows\Temp\$($target)"

Write-Host "Source val: $source"
Write-Host "File val: $file"
Write-Host "Deployed file source: $source1"
Write-Host "Deployed file destination: $dest"
Write-Host "COPY TYPE: $copytype"

# Add check to return proper exit code, for some reason ROBOCOPY returns 1 on success o.0
function ROBO_exit_check ($val)
{
  Write-Host "val: $val"
  if ($val -eq 0)
  {
     write-host "Robocopy exit code 0: No errors occurred, and no copying was done. The source and destination directory trees are completely synchronized."
   }
   elseif ($val -eq 1)
   {
     write-host "Robocopy exit code 1: One or more files were copied successfully (that is, new files have arrived)."
     exit 0
    }
    else
    {
      Write-Host "Robocopy error code $lastexitcode"
    }
}

if ($copytype -eq "full")
{
  robocopy $source1 $dest /S
  ROBO_exit_check($lastexitcode)
}
elseif ($copytype -eq "only-files")
{
  if ($file -eq "")
  {
    robocopy $source1 $dest /S
    ROBO_exit_check($lastexitcode)
  }
  else
  {
    robocopy $source1 $dest $file /S
    ROBO_exit_check($lastexitcode)
  }
}
