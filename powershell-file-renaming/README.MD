# PowerShell File Management Tools

A collection of PowerShell scripts developed to automate repetitive file-management tasks in technical drafting workflows.

These scripts were created to solve practical problems encountered when working with large numbers of drawing and documentation files.

## Scripts

### 1. Project Part Renaming

**File:** `rename-by-prefix.ps1`

#### Problem

Some projects are divided into several parts or volumes. When starting a new part, I usually copy the previous part and rename the main directory.

For example:

`2. Drawings` → `3. Drawings`

However, the files and subdirectories inside the copied directory still contain the old part number.

Renaming them manually is repetitive and can lead to mistakes.

#### Solution

The script recursively processes the copied directory and replaces the old part number at the beginning of file and directory names.

For example:

```text
2. Drawing 01.dwg
2. Drawing 02.dwg
2. Details
```

becomes:

```text
3. Drawing 01.dwg
3. Drawing 02.dwg
3. Details
```

The script processes both files and directories.

### 2. Sequential PDF Renaming

**File:** `rename-pdf-sequentially.ps1`

#### Problem

A client representative required a set of drawings in a specific PDF naming format.

A typical batch contained approximately 11–15 files. Renaming the files manually took around 30 minutes and could result in numbering or naming mistakes.

#### Solution

The script takes all PDF files in a directory and renames them sequentially according to the required naming convention.

For example:

```text
drawing1.pdf
drawing2.pdf
drawing3.pdf
```

becomes:

```text
Building 1. Section 7.pdf
Building 1. Section 8.pdf
Building 1. Section 9.pdf
```

The starting section number can be adjusted depending on the project.

#### Result

The complete batch can be renamed automatically and consistently instead of being processed manually.

### 3. DWG Filename Shortening

**File:** `shorten-dwg-filenames.ps1`

#### Problem

A client representative provided approximately 20–30 architectural building plans in DWG format.

When attempting to open the drawings, AutoCAD reported an error indicating that the filename was too long.

Manually shortening the filenames would have been time-consuming, especially for a large batch of drawings.

#### Solution

The script recursively processes the files, extracts the page number from the beginning of each filename using a regular expression, and creates a short standardized filename.

For example:

```text
001 [long descriptive filename].dwg
002 [long descriptive filename].dwg
003 [long descriptive filename].dwg
```

becomes:

```text
001.dwg
002.dwg
003.dwg
```

The page number is preserved while the unnecessary part of the filename is removed.

#### Result

The large batch of drawings can be renamed automatically, making the files usable without manually processing each drawing.

### Techniques Used
PowerShell
File-system operations
Get-ChildItem
Rename-Item
Recursive file processing
File filtering
Regular expressions
Named capture groups
$Matches
Sequential numbering
Automated filename generation

### Background

These scripts were developed as small automation tools for real-world drafting and documentation workflows.

They were not created as standalone software products. Each script was written in response to a specific repetitive problem encountered during day-to-day work.

The common approach was to identify a predictable pattern in the files and automate the operation instead of repeating it manually.