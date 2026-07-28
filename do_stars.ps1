$ErrorActionPreference = 'Stop'

$readme = 'README.md'
$content = Get-Content -Raw $readme

$osStart = $content.IndexOf('## 🔓 Open-Source GitHub Projects')
$osEnd = $content.IndexOf('### Additional Strong Open-Source Options')
$osSection = $content.Substring($osStart, $osEnd - $osStart)

$blocks = $osSection.Trim() -split "

"
$parsedBlocks = @()
$headers = @{ 'User-Agent' = 'AwesomeScript/1.0' }

for ($i = 1; $i -lt $blocks.Length; $i++) {
    $block = $blocks[$i]
    $lines = $block -split "
"
    $titleLine = $lines[0]
    
    $stars = 0
    $owner = ''
    $repo = ''
    $url = ''
    
    if ($titleLine -match 'https://github\.com/([^/]+)/([^/\)]+)') {
        $owner = $matches[1]
        $repo = $matches[2]
        $url = 'https://github.com/' + $owner + '/' + $repo
        try {
            $apiUrl = 'https://api.github.com/repos/' + $owner + '/' + $repo
            $resp = Invoke-RestMethod -Uri $apiUrl -Headers $headers -ErrorAction SilentlyContinue
            if ($null -ne $resp.stargazers_count) {
                $stars = $resp.stargazers_count
            }
        } catch { }
    } elseif ($titleLine -match 'https://github\.com/([^/\)]+)') {
        $owner = $matches[1]
        $repo = $owner
        $url = 'https://github.com/' + $owner
    }
    
    if ($url -ne '') {
        $badge = ' [![GitHub stars](https://img.shields.io/github/stars/' + $owner + '/' + $repo + '?style=social&color=white)](' + $url + '/stargazers)'
        $titleLine = $titleLine.Replace('**  ', '**' + $badge + '  ')
        if (-not $titleLine.Contains($badge)) {
            $titleLine += $badge
        }
    }
    
    $newBlock = $titleLine + "
" + (($lines | Select-Object -Skip 1) -join "
")
    $parsedBlocks += [PSCustomObject]@{ Stars = $stars; Block = $newBlock }
}

$parsedBlocks = $parsedBlocks | Sort-Object -Property Stars -Descending
$newOsSection = "## 🔓 Open-Source GitHub Projects

" + ($parsedBlocks.Block -join "

") + "

"

$content = $content.Substring(0, $osStart) + $newOsSection + $content.Substring($osEnd)
Set-Content -Path $readme -Value $content -NoNewline
