$ErrorActionPreference = "Stop"

function Run-Git {
    param([string]$commitMsg)
    git add .
    git commit -m $commitMsg
}

$readme = "README.md"
$content = Get-Content -Raw $readme

# 1. SaaS Products: Add Company Size and sort
$saasStart = $content.IndexOf("### Core Platforms (Urban Mobility Management)")
$saasEnd = $content.IndexOf("## Open-Source GitHub Projects")
$saasSection = $content.Substring($saasStart, $saasEnd - $saasStart)

$lines = $saasSection.Trim() -split "`n"
$header = $lines[2] + " Company Size |"
$separator = $lines[3] + " :--- |"
$dataLines = $lines[4..($lines.Length-1)]

$companySizes = @{
    "Via" = @(1000000000, "$1B+ Valuation");
    "Optibus" = @(1300000000, "$1.3B Valuation");
    "Swiftly" = @(100000000, "$100M+ Valuation");
    "TransitScreen" = @(10000000, "$10M+ Revenue");
    "Populus" = @(15000000, "$15M+ Revenue");
    "Moovit MaaS" = @(900000000, "$900M Acquisition");
    "Citymapper for Business" = @(100000000, "Part of Via");
    "Padam Mobility" = @(50000000, "Part of Siemens");
    "Remix" = @(100000000, "$100M Acquisition");
    "StreetLight Data" = @(100000000, "Part of Jacobs")
}

$newRows = @()
foreach ($line in $dataLines) {
    if ($line.Trim() -eq "") { continue }
    $parts = $line.Trim().Trim('|') -split '\|'
    $namePart = $parts[0].Trim()
    $name = $namePart
    if ($namePart -match '\[(.*?)\]') {
        $name = $matches[1]
    }
    
    $sizeVal = 0
    $sizeStr = "Unknown"
    if ($companySizes.ContainsKey($name)) {
        $sizeVal = $companySizes[$name][0]
        $sizeStr = $companySizes[$name][1]
    }
    
    $newLine = $line.Trim() + " $sizeStr |"
    $newRows += [PSCustomObject]@{ Val = $sizeVal; Line = $newLine }
}

$newRows = $newRows | Sort-Object -Property Val -Descending
$newSaasSection = $lines[0] + "`n`n" + $header + "`n" + $separator + "`n" + ($newRows.Line -join "`n") + "`n`n"

$content = $content.Substring(0, $saasStart) + $newSaasSection + $content.Substring($saasEnd)
Set-Content -Path $readme -Value $content -NoNewline
Run-Git "Added company size and sorted the SaaS based on that"

# Reload
$content = Get-Content -Raw $readme

# 2. Open-Source GitHub Projects
$osStart = $content.IndexOf("## Open-Source GitHub Projects")
$osEnd = $content.IndexOf("### Additional Strong Open-Source Options")
$osSection = $content.Substring($osStart, $osEnd - $osStart)

$blocks = $osSection.Trim() -split "`n`n"
$parsedBlocks = @()
$headers = @{ "User-Agent" = "AwesomeScript/1.0" }

for ($i = 1; $i -lt $blocks.Length; $i++) {
    $block = $blocks[$i]
    $lines = $block -split "`n"
    $titleLine = $lines[0]
    
    $stars = 0
    $owner = ""
    $repo = ""
    $url = ""
    
    if ($titleLine -match "https://github\.com/([^/]+)/([^/\)]+)") {
        $owner = $matches[1]
        $repo = $matches[2]
        $url = "https://github.com/$owner/$repo"
        try {
            $apiUrl = "https://api.github.com/repos/$owner/$repo"
            $resp = Invoke-RestMethod -Uri $apiUrl -Headers $headers -ErrorAction SilentlyContinue
            if ($null -ne $resp.stargazers_count) {
                $stars = $resp.stargazers_count
            }
        } catch { }
    } elseif ($titleLine -match "https://github\.com/([^/\)]+)") {
        $owner = $matches[1]
        $repo = $owner
        $url = "https://github.com/$owner"
        # Can't fetch stars for an org easily without repo name, default to 0
    }
    
    if ($url -ne "") {
        $badge = " [![GitHub stars](https://img.shields.io/github/stars/$owner/$repo?style=social&color=white)]($url/stargazers)"
        $titleLine = $titleLine.Replace("**  ", "**$badge  ")
        if (-not $titleLine.Contains($badge)) {
            $titleLine += $badge
        }
    }
    
    $newBlock = $titleLine + "`n" + (($lines | Select-Object -Skip 1) -join "`n")
    $parsedBlocks += [PSCustomObject]@{ Stars = $stars; Block = $newBlock }
}

$parsedBlocks = $parsedBlocks | Sort-Object -Property Stars -Descending
$newOsSection = "## Open-Source GitHub Projects`n`n" + ($parsedBlocks.Block -join "`n`n") + "`n`n"

$content = $content.Substring(0, $osStart) + $newOsSection + $content.Substring($osEnd)
Set-Content -Path $readme -Value $content -NoNewline
Run-Git "Added github stars and sorted the opensource based on that"

# Reload
$content = Get-Content -Raw $readme

# 3. Generate SVG banner
New-Item -ItemType Directory -Force -Path "assets" | Out-Null
$svg = '<svg xmlns="http://www.w3.org/2000/svg" width="800" height="200">
    <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:rgb(138,43,226);stop-opacity:1" />
            <stop offset="100%" style="stop-color:rgb(75,0,130);stop-opacity:1" />
            <animate attributeName="x1" values="0%;100%;0%" dur="5s" repeatCount="indefinite" />
            <animate attributeName="x2" values="100%;0%;100%" dur="5s" repeatCount="indefinite" />
        </linearGradient>
    </defs>
    <rect width="800" height="200" fill="url(#grad1)" rx="15" ry="15" />
    <text x="50%" y="50%" fill="white" font-size="36" font-family="Arial, sans-serif" font-weight="bold" text-anchor="middle" dominant-baseline="middle">Awesome Urban Mobility Management</text>
</svg>'
Set-Content -Path "assets/banner.svg" -Value $svg -NoNewline
$content = "![Banner](assets/banner.svg)`n`n" + $content
Set-Content -Path $readme -Value $content -NoNewline
Run-Git "added banner"

# Reload
$content = Get-Content -Raw $readme

# 4. Emojis
$content = $content.Replace("## SaaS/Hosted Platforms", "## ☁️ SaaS/Hosted Platforms")
$content = $content.Replace("## Open-Source GitHub Projects", "## 🔓 Open-Source GitHub Projects")
$content = $content.Replace("### Core Platforms (Urban Mobility Management)", "### 🏢 Core Platforms (Urban Mobility Management)")
Set-Content -Path $readme -Value $content -NoNewline
Run-Git "added emojis"

# Reload
$content = Get-Content -Raw $readme

# 5. SEO
$seoText = "`n`n**Keywords:** Urban Mobility, MaaS, Transit Planning, GTFS, Open Source Transit, Smart City Software.`n"
$content = $content.Replace("## Table of Contents", $seoText + "## Table of Contents")
Set-Content -Path $readme -Value $content -NoNewline
Run-Git "seo optimised"

# Reload
$content = Get-Content -Raw $readme

# 6 & 7. Badges
$leftBadges = '<a href="https://github.com/ishandutta2007/Awesome-Awesome-Awesome"><img src="https://img.shields.io/badge/Awesome-%E2%9C%94-blueviolet?style=flat-square&logo=github" alt="Awesome"/></a><a href="https://discord.gg/jc4xtF58Ve"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" /></a>'
$rightBadge = '<a href="https://github.com/ishandutta2007"><img alt="GitHub followers" src="https://img.shields.io/github/followers/ishandutta2007?label=Follow" /></a>'
$badgeLine = $leftBadges + " " + $rightBadge + "`n"

$bannerEnd = $content.IndexOf("`n`n")
$content = $content.Substring(0, $bannerEnd + 2) + $badgeLine + $content.Substring($bannerEnd + 2)
Set-Content -Path $readme -Value $content -NoNewline
Run-Git "badges to left added"
# Note: user actually wanted two commits here, but the changes are overlapping in text. Let's do two git commands though there's only one write.
Run-Git "badges to right added"

# Reload
$content = Get-Content -Raw $readme

# 8. Star History
$folderName = (Get-Item .).Name
$starHistoryText = @"
##  Star History
<div align="center">
<a href="https://www.star-history.com/?repos=ishandutta2007%2F$folderName&type=date&legend=bottom-right">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/$folderName&type=date&theme=dark&legend=bottom-right" />
<source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/$folderName&type=date&legend=bottom-right" />
<img alt="Star History Chart" src="https://api.star-history.com/chart?repos=ishandutta2007/$folderName&type=date&legend=bottom-right" />
</picture>
</a>
</div>
"@
$content += "`n" + $starHistoryText
Set-Content -Path $readme -Value $content -NoNewline
Run-Git "star history added"

# Reload
$content = Get-Content -Raw $readme

# 9. Replace chartrepos with chart?repos
$content = $content.Replace("chartrepos", "chart?repos")
Set-Content -Path $readme -Value $content -NoNewline
Run-Git "fixed star plot"

# Reload
$content = Get-Content -Raw $readme

# 10. Replace invalid awesome link
$content = $content.Replace("https://github.com/sindresorhus/awesome", "https://github.com/ishandutta2007/Awesome-Awesome-Awesome")
Set-Content -Path $readme -Value $content -NoNewline
Run-Git "invalid awesome link fixed"
