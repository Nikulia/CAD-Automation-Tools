ls "C:\Projects\3. Drawings" -Recurse | ForEach-Object {
$dest=$_.Name -replace '^2.', '3.'
Rename-Item -LiteralPath $_.FullName -NewName $dest -ErrorAction SilentlyContinue}
