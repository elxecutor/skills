# Read-only hidden-home-folder inventory for Windows. Python's -B prevents bytecode writes.
[CmdletBinding()]
param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]] $Arguments
)

$python = $null
foreach ($candidate in 'python', 'python3', 'py') {
  $command = Get-Command $candidate -ErrorAction SilentlyContinue
  if ($command) { $python = $command.Source; break }
}
if (-not $python) {
  [Console]::Error.WriteLine('pc-clean: python is required for the read-only scanner')
  exit 127
}

& $python -B (Join-Path $PSScriptRoot 'scan.py') @Arguments
exit $LASTEXITCODE
