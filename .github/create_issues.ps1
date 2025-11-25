# Creates GitHub issues from markdown files in .github/ISSUES using the gh CLI
# Usage: ./create_issues.ps1

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
  Write-Error "GitHub CLI (gh) not found. Install from https://cli.github.com/ and authenticate with 'gh auth login'."
  exit 1
}

$issueFiles = Get-ChildItem -Path .github/ISSUES -Filter '*.md' | Sort-Object Name
foreach ($f in $issueFiles) {
  $content = Get-Content $f -Raw
  $titleLine = ($content -split "`n" | Select-String -Pattern '^#\s+' | Select-Object -First 1).ToString()
  if ($titleLine -match '^#\s+(.*)') { $title = $Matches[1].Trim() } else { $title = $f.BaseName }
  Write-Host "Creating issue: $title from $($f.Name)"
  gh issue create --title "$title" --body-file "$($f.FullName)" --label "hackathon" || Write-Warning "Failed to create issue for $($f.Name)"
}

Write-Host "Done. Check the repo issues tab."
