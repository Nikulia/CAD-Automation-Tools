# Directory to search
$path = "C:\Projects"

# Find files with duplicate names
$duplicateNameGroups = Get-ChildItem -Path $path -Recurse -File | 
    Group-Object Name | 
    Where-Object {$_.Count -gt 1}

# From the duplicate-name groups, keep only groups
# where the files have different sizes
$duplicateNamesWithDifferentSizes = $duplicateNameGroups | 
    Where-Object {
        # Get all files belonging to the current filename group
        $_.Group | 
        
        # Get the size of each file
        ForEach-Object { $_.Length } | 
        
        # Remove duplicate sizes
        Select-Object -Unique | 
        
        # Count how many different sizes remain
        Measure-Object | 
        
        # Keep the group only if there is more than one different size
        Where-Object {$_.Count -gt 1}
    }

# Display the full paths of files with the same name but different sizes
foreach ($group in $duplicateNamesWithDifferentSizes) {
    Write-Output "Files with the name '$($group.Name)' but different sizes:"
    
    ForEach ($file in $group.Group) {
        Write-Output $file.FullName 
    }
}