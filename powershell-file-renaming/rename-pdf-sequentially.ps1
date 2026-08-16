
$files = Get-ChildItem -Path "C:\Projects\pdf" -Filter *.pdf
$i = 7
 ForEach ($file in $files) {
    Write-Host "Renaming $($file.Name) -> Building 1. Section $i.pdf"
    Rename-Item -LiteralPath $file.FullName -NewName "Building 1. Section $i.pdf"
    $i++
 }
