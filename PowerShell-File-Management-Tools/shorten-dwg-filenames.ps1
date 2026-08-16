ls "C:\Projects\Drawings" -Recurse | ForEach-Object {
$_.Name -match '(?<page>^0\d{2})'
$dest=$_.Name -replace '^.*', "$($Matches.page).dwg"
Rename-Item -LiteralPath $_.FullName -NewName $dest -ErrorAction SilentlyContinue
}
