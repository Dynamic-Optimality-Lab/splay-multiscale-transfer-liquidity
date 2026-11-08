param([int]$RunnerProcessId)
$ErrorActionPreference = 'Stop'
$trackedPhases = @{}
$resourceRows = [System.Collections.Generic.List[object]]::new()
$outputPath = Join-Path $PSScriptRoot 'resource_monitor.json'
if (Test-Path -LiteralPath $outputPath) { throw 'Resource output already exists' }
while ($true) {
    $runnerPresent = $null -ne (Get-Process -Id $RunnerProcessId -ErrorAction SilentlyContinue)
    if ($runnerPresent) {
        $children = Get-CimInstance Win32_Process -Filter "ParentProcessId=$RunnerProcessId AND Name='python.exe'"
        foreach ($child in $children) {
            $key = [string]$child.ProcessId
            if (-not $trackedPhases.ContainsKey($key)) {
                try {
                    $phaseProcess = Get-Process -Id $child.ProcessId -ErrorAction Stop
                    $null = $phaseProcess.Handle
                    $trackedPhases[$key] = @{ Process=$phaseProcess; Command=$child.CommandLine; Recorded=$false }
                } catch {
                    $resourceRows.Add([pscustomobject]@{process_id=$child.ProcessId;command=$child.CommandLine;CPU_seconds=$null;error=$_.Exception.Message})
                }
            }
        }
    }
    foreach ($key in @($trackedPhases.Keys)) {
        $item = $trackedPhases[$key]
        if (-not $item.Recorded -and ($item.Process.HasExited -or -not $runnerPresent)) {
            try {
                $seconds = $item.Process.TotalProcessorTime.TotalSeconds
                $resourceRows.Add([pscustomobject]@{process_id=[int]$key;command=$item.Command;CPU_seconds=$seconds;error=$null})
            } catch {
                $resourceRows.Add([pscustomobject]@{process_id=[int]$key;command=$item.Command;CPU_seconds=$null;error=$_.Exception.Message})
            }
            $item.Recorded = $true
            $item.Process.Dispose()
        }
    }
    if (-not $runnerPresent) { break }
    Start-Sleep -Milliseconds 500
}
[pscustomobject]@{
    status='READ_ONLY_CHILD_CPU_OBSERVATIONS'
    runner_process_id=$RunnerProcessId
    source_queries=0
    evaluator_changes=0
    phases=$resourceRows.ToArray()
} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $outputPath -Encoding utf8
Write-Output ('Resource observations saved: '+$resourceRows.Count)
