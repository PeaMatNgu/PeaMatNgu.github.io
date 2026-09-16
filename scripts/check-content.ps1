param(
  [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot ".."))
)

$ErrorActionPreference = "Stop"
$issues = [System.Collections.Generic.List[object]]::new()
$markdownFiles = Get-ChildItem -LiteralPath $Root -Recurse -File -Include *.md,*.markdown | Where-Object {
  $_.FullName -notmatch '[\\/]_site[\\/]' -and $_.Name -ne 'README.md'
}
$imagePattern = '!\[[^\]]*\]\((?<url>[^\s\)]+)(?:\s+["''][^"'']*["''])?\)'

foreach ($file in $markdownFiles) {
  $lineNumber = 0
  foreach ($line in Get-Content -LiteralPath $file.FullName) {
    $lineNumber++
    foreach ($match in [regex]::Matches($line, $imagePattern)) {
      $url = $match.Groups['url'].Value.Trim('<', '>')
      $reason = $null
      if ($url -match '^file:///') { $reason = 'file:/// path' }
      elseif ($url -match '^[A-Za-z]:[\\/]') { $reason = 'Absolute local path' }
      elseif ($url -match '^https://github\.com/user-attachments/assets/') { $reason = 'GitHub user-attachment should be stored locally' }
      elseif ($url -notmatch '^(https?:)?//' -and $url -notmatch '^\{\{' -and $url -notmatch '^data:') {
        $clean = ($url -split '[?#]')[0]
        if ($clean.StartsWith('/')) { $target = Join-Path $Root $clean.TrimStart('/') }
        else { $target = Join-Path $file.DirectoryName $clean }
        if (-not (Test-Path -LiteralPath $target)) { $reason = 'Missing local image' }
      }
      if ($reason) {
        $issues.Add([pscustomobject]@{ File = $file.FullName.Substring($Root.Length).TrimStart('\\'); Line = $lineNumber; Url = $url; Issue = $reason })
      }
    }
  }
}

if ($issues.Count -eq 0) {
  Write-Host "No problematic Markdown image paths found."
  exit 0
}

$issues | Format-Table -AutoSize -Wrap
Write-Host "`nFound $($issues.Count) issue(s)."
exit 1
