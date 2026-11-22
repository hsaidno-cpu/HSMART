$ErrorActionPreference = "Stop"

$pythonCommand = Get-Command py -ErrorAction SilentlyContinue
if ($pythonCommand) {
    $pythonArgs = @("-3.12")
    & py @pythonArgs -c "import sys; assert sys.version_info[:2] == (3, 12), sys.version"
    if ($LASTEXITCODE -ne 0) { throw "Python 3.12 is required." }
    if (-not (Test-Path ".venv")) { & py @pythonArgs -m venv .venv }
} else {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCommand) { throw "Python 3.12 is required." }
    & python -c "import sys; assert sys.version_info[:2] == (3, 12), sys.version"
    if ($LASTEXITCODE -ne 0) { throw "Expected Python 3.12." }
    if (-not (Test-Path ".venv")) { & python -m venv .venv }
}

& .\.venv\Scripts\python.exe -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "Failed to upgrade pip." }
& .\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
if ($LASTEXITCODE -ne 0) { throw "Failed to install development requirements." }

Write-Host "HSMART contract-validation environment is ready. Run: .\.venv\Scripts\python.exe -m pytest -q"
