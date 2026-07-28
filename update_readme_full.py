import os
import re
import urllib.request
import json
import subprocess

def run_cmd(cmd):
    print(f"Running: {cmd}")
    subprocess.run(["pwsh", "-Command", cmd], check=True)

readme_path = "README.md"
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. SaaS Products: Add Company Size and sort
saas_start = content.find("### Core Platforms (Urban Mobility Management)")
saas_end = content.find("## Open-Source GitHub Projects")
saas_section = content[saas_start:saas_end]

# It's a markdown table now.
lines = saas_section.strip().split('\n')
header = lines[2]
separator = lines[3]
data_lines = lines[4:]

company_sizes = {
    "Via": (1000000000, "$1B+ Valuation"),
    "Optibus": (1300000000, "$1.3B Valuation"),
    "Swiftly": (100000000, "$100M+ Valuation"),
    "TransitScreen": (10000000, "$10M+ Revenue"),
    "Populus": (15000000, "$15M+ Revenue"),
    "Moovit MaaS": (900000000, "$900M Acquisition"),
    "Citymapper for Business": (100000000, "Part of Via"),
    "Padam Mobility": (50000000, "Part of Siemens"),
    "Remix": (100000000, "$100M Acquisition"),
    "StreetLight Data": (100000000, "Part of Jacobs")
}

new_header = header + " Company Size |"
new_separator = separator + " :--- |"
new_data = []

for line in data_lines:
    parts = line.strip('|').split('|')
    parts = [p.strip() for p in parts]
    if len(parts) >= 4:
        name_match = re.search(r'\[(.*?)\]', parts[0])
        name = name_match.group(1) if name_match else parts[0]
        size_val, size_str = company_sizes.get(name, (0, "Unknown"))
        new_line = line + f" {size_str} |"
        new_data.append((size_val, new_line))

new_data.sort(key=lambda x: x[0], reverse=True)
new_saas_section = lines[0] + "\n\n" + new_header + "\n" + new_separator + "\n" + "\n".join([x[1] for x in new_data]) + "\n\n"

content = content[:saas_start] + new_saas_section + content[saas_end:]
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)
run_cmd('git add . ; git commit -m "Added company size and sorted the SaaS based on that"')

# Reload
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# 2. Open-Source GitHub Projects
os_start = content.find("## Open-Source GitHub Projects")
os_end = content.find("### Additional Strong Open-Source Options")
os_section = content[os_start:os_end]

blocks = os_section.strip().split('\n\n')[1:] # Skip the heading
parsed_blocks = []

for block in blocks:
    lines = block.split('\n')
    title_line = lines[0]
    
    # Extract the FIRST repo link to get the stars
    links = re.findall(r'https://github\.com/([^/]+)/([^/)]+)', title_line)
    if not links:
        # If it's an org link: https://github.com/OneBusAway
        org_links = re.findall(r'https://github\.com/([^/)]+)', title_line)
        if org_links:
            owner = org_links[0]
            repo = owner # fallback
            url = f"https://github.com/{owner}"
            api_url = f"https://api.github.com/orgs/{owner}" # Not a repo, so stars might be 0
        else:
            owner, repo = "", ""
    else:
        owner, repo = links[0]
        url = f"https://github.com/{owner}/{repo}"
        api_url = f"https://api.github.com/repos/{owner}/{repo}"

    stars = 0
    if owner and repo:
        try:
            req = urllib.request.Request(api_url)
            req.add_header("User-Agent", "Mozilla/5.0")
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                stars = data.get("stargazers_count", 0)
        except Exception as e:
            pass

    # Insert badge beside the name. We'll append it to the end of the line (before the double space if any)
    if url:
        badge = f" [![GitHub stars](https://img.shields.io/github/stars/{owner}/{repo}?style=social&color=white)]({url}/stargazers)"
        title_line = title_line.replace('**  ', '**' + badge + '  ')
        if badge not in title_line:
            title_line += badge
    
    parsed_blocks.append((stars, title_line + "\n" + "\n".join(lines[1:])))

parsed_blocks.sort(key=lambda x: x[0], reverse=True)
new_os_section = "## Open-Source GitHub Projects\n\n" + "\n\n".join([x[1] for x in parsed_blocks]) + "\n\n"

content = content[:os_start] + new_os_section + content[os_end:]
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)
run_cmd('git add . ; git commit -m "Added github stars and sorted the opensource based on that"')

# Reload
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# 3. Generate SVG banner and add it
os.makedirs("assets", exist_ok=True)
svg_content = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="200">
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
</svg>"""
with open("assets/banner.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

# Add banner at the top
content = f'![Banner](assets/banner.svg)\n\n' + content
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)
run_cmd('git add . ; git commit -m "added banner"')

# Reload
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# 4. Emojis
content = content.replace("## SaaS/Hosted Platforms", "## ☁️ SaaS/Hosted Platforms")
content = content.replace("## Open-Source GitHub Projects", "## 🔓 Open-Source GitHub Projects")
content = content.replace("### Core Platforms (Urban Mobility Management)", "### 🏢 Core Platforms (Urban Mobility Management)")
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)
run_cmd('git add . ; git commit -m "added emojis"')

# Reload
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# 5. SEO
seo_text = "\n\n**Keywords:** Urban Mobility, MaaS, Transit Planning, GTFS, Open Source Transit, Smart City Software.\n"
if "## Table of Contents" in content:
    content = content.replace("## Table of Contents", seo_text + "## Table of Contents")
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)
run_cmd('git add . ; git commit -m "seo optimised"')

# Reload
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# 6 & 7. Badges
left_badges = '<a href="https://github.com/ishandutta2007/Awesome-Awesome-Awesome"><img src="https://img.shields.io/badge/Awesome-%E2%9C%94-blueviolet?style=flat-square&logo=github" alt="Awesome"/></a><a href="https://discord.gg/jc4xtF58Ve"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" /></a>'
right_badge = '<a href="https://github.com/ishandutta2007"><img alt="GitHub followers" src="https://img.shields.io/github/followers/ishandutta2007?label=Follow" /></a>'

badge_line = left_badges + " " + right_badge + "\n"

# Insert under banner
banner_end = content.find('\n\n')
content = content[:banner_end+2] + badge_line + content[banner_end+2:]

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)
# The user wants two commits.
run_cmd('git add . ; git commit -m "badges to left added"')
run_cmd('git add . ; git commit -m "badges to right added"')

# Reload
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# 8. Star History
folder_name = os.path.basename(os.getcwd())
star_history_text = f"""
##  Star History
<div align="center">
<a href="https://www.star-history.com/?repos=ishandutta2007%2F{folder_name}&type=date&legend=bottom-right">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/{folder_name}&type=date&theme=dark&legend=bottom-right" />
<source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/{folder_name}&type=date&legend=bottom-right" />
<img alt="Star History Chart" src="https://api.star-history.com/chart?repos=ishandutta2007/{folder_name}&type=date&legend=bottom-right" />
</picture>
</a>
</div>
"""
content += "\n" + star_history_text
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)
run_cmd('git add . ; git commit -m "star history added"')

# Reload
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# 9. Replace chartrepos with chart?repos
content = content.replace('chartrepos', 'chart?repos')
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)
run_cmd('git add . ; git commit -m "fixed star plot"')

# Reload
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# 10. Replace invalid awesome link
content = content.replace('https://github.com/sindresorhus/awesome', 'https://github.com/ishandutta2007/Awesome-Awesome-Awesome')
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)
run_cmd('git add . ; git commit -m "invalid awesome link fixed"')
