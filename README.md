# Network Recon Toolkit – Automated Nmap Reporting

## Overview
Python-based reconnaissance toolkit that automates Nmap scanning, parses results, and generates analyst-ready HTML and CSV reports.  
Designed to support SOC investigations, validation, and escalation by standardizing network reconnaissance output.

## Environment / Tools
- OS: Linux, macOS, Windows
- Tools: Python 3.8+, Nmap
- Data Sources: Nmap TCP/UDP scans, service detection, OS fingerprinting
- Frameworks: SOC investigation workflow

## Results / Findings (SOC Notes)
- Identified active hosts and exposed TCP/UDP services across target networks
- Extracted service versions and banners for vulnerability and risk assessment
- Generated structured HTML reports for rapid analyst review
- Produced CSV output suitable for tracking, comparison, or SIEM enrichment
- Retained raw Nmap XML for validation, correlation, and follow-on analysis

## Architecture
Target Network → Nmap Scan Profiles → Python Parser → HTML / CSV Reports

## Repository Structure
```text
/reports        → generated scan reports (HTML, CSV, XML)
recon.py        → main reconnaissance script
README.md       → project documentation
```

## Usage
```bash
git clone https://github.com/Niknaz-65/network-recon-toolkit.git
cd network-recon-toolkit

# Quick TCP scan
python3 recon.py 192.168.1.10

# Full scan profile
python3 recon.py 10.0.0.0/24 --profile full -t 4 --rate 500

# Include UDP scanning
python3 recon.py 192.168.1.10 --udp
```

## Author
**Niknaz Sadehvandi**  
**Cybersecurity Analyst**

