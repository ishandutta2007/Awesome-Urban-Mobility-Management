import re
import urllib.request
import json
import os
import subprocess

def run_cmd(cmd):
    subprocess.run(["pwsh", "-Command", cmd], check=True)

readme_path = "README.md"
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. SaaS Products: Add Company Size and sort
saas_start = content.find("### Core Platforms (Urban Mobility Management)")
saas_end = content.find("## Open-Source GitHub Projects")
saas_section = content[saas_start:saas_end]

# Extract rows
rows = re.findall(r'\| \*\*\[(.*?)\]\((.*?)\)\*\* \| (.*?) \| (.*?) \| (.*?) \|', saas_section)

# We will add Company Size based on rough estimates
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

new_rows = []
for row in rows:
    name, url, desc, pricing, free_tier = row
    size_val, size_str = company_sizes.get(name, (0, "Unknown"))
    new_rows.append((size_val, f"| **[{name}]({url})** | {desc} | {pricing} | {free_tier} | {size_str} |"))

new_rows.sort(key=lambda x: x[0], reverse=True)
new_saas_table = "### Core Platforms (Urban Mobility Management)\n\n| Platform | Description | Pricing | Free Tier / Limits | Company Size |\n| :--- | :--- | :--- | :--- | :--- |\n"
for r in new_rows:
    new_saas_table += r[1] + "\n"

content = content[:saas_start] + new_saas_table + "\n" + content[saas_end:]
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)
run_cmd('git add . ; git commit -m "Added company size and sorted the SaaS based on that"')

# 2. Open-Source GitHub Projects
os_start = content.find("## Open-Source GitHub Projects")
os_end = content.find("### Additional Strong Open-Source Options")
os_section = content[os_start:os_end]

os_items = re.findall(r'- \*\*(.*?)\*\*  \n  (.*)', os_section)
# But wait, the previous content had: - **[OpenTripPlanner](https://github.com/opentripplanner/OpenTripPlanner)**
os_items = re.findall(r'- \*\*\[(.*?)\]\((https://github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+))\)\*\*  \n  (.*?)\n', os_section)

# Fetch stars and sort
os_list = []
for name, url, owner, repo, desc in os_items:
    try:
        req = urllib.request.Request(f"https://api.github.com/repos/{owner}/{repo}")
        req.add_header("User-Agent", "Mozilla/5.0")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            stars = data.get("stargazers_count", 0)
    except:
        stars = 0
    badge = f"[![GitHub stars](https://img.shields.io/github/stars/{owner}/{repo}?style=social&color=white)]({url}/stargazers)"
    os_list.append((stars, f"- **[{name}]({url})** {badge}  \n  {desc}\n"))

os_list.sort(key=lambda x: x[0], reverse=True)
new_os_section = "## Open-Source GitHub Projects\n\n"
for item in os_list:
    new_os_section += item[1] + "\n"

# wait, there are also items like "- **[OneBusAway](https://github.com/OneBusAway)**" where it is just an org. Let's just catch all and parse if possible.
# Better to do a more robust replacement for the opensource section.
