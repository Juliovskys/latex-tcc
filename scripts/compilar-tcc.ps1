param(
    [string]$Tectonic = 'tectonic',
    [string]$Pandoc = 'pandoc',
    [string]$Python = 'python'
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$buildDirectory = Join-Path $projectRoot 'tmp/pdfs/build'
$outputDirectory = Join-Path $projectRoot 'output/pdf'
New-Item -ItemType Directory -Force -Path $buildDirectory, $outputDirectory | Out-Null

& $Python (Join-Path $PSScriptRoot 'sincronizar_tcc.py') --pandoc $Pandoc
if ($LASTEXITCODE -ne 0) { throw 'A sincronização do manuscrito falhou.' }

Push-Location (Join-Path $projectRoot 'latex')
try {
    & $Tectonic --keep-logs --keep-intermediates --outdir $buildDirectory tcc.tex
    if ($LASTEXITCODE -ne 0) { throw 'A compilação do documento falhou.' }
    $pdfPath = Join-Path $outputDirectory 'TCC_Avaliacao_Contextual_Curto_Prazo.pdf'
    Copy-Item -LiteralPath (Join-Path $buildDirectory 'tcc.pdf') -Destination $pdfPath
    Write-Output "PDF atualizado: $pdfPath"
} finally {
    Pop-Location
}
