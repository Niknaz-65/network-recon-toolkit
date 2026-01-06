# Network Recon Toolkit – Automated Nmap Reporting

## Overview
Python-based network reconnaissance tool that wraps Nmap to automate service discovery and generate analyst-ready HTML and CSV reports.  
The project supports SOC and security operations by standardizing reconnaissance output for investigation, validation, and handoff.

## Why This Project Matters to SOC Teams
- Accelerates reconnaissance during investigations and incident response
- Produces consistent, readable reports for analyst review and escalation
- Supports vulnerability assessment and network visibility without manual parsing

## Environment
- OS: Linux / macOS / Windows
- Tools: Python 3.8+, Nmap
- Data Sources: Nmap scan results (TCP/UDP, service detection, OS fingerprinting)
- Frameworks: SOC investigation workflow

## Data Collected / Artifacts
- Open ports and exposed services
- Service versions and banners
- OS fingerprinting results
- Network host availability
- Scan timestamps and metadata

## Detection Logic / Analysis Steps
1. Executed Nmap scans using predefined profiles (quick or full)
2. Performed TCP service discovery with optional UDP scanning
3. Applied timing and rate controls for scan optimization
4. Parsed Nmap XML output using Python
5. Generated structured reports for analyst consumption

## Findings
- Identified active hosts and exposed services across target networks
- Generated clean HTML reports for rapid review
- Produced CSV output suitable for tracking, comparison, or SIEM enrichment

## Outcome
- Reconnaissance workflow automated and standardized
- Reduced manual effort during investigations
- Reports suitable for escalation, documentation, or follow-on scanning

## Evidence
- Sample HTML and CSV reports stored in `/reports`
- Raw Nmap XML retained for validation

## Repository Structure
```text
/reports        → generated scan reports (HTML, CSV, XML)
recon.py        → main reconnaissance script
README.md       → project documentation

## Usage
```bash
git clone https://github.com/Niknaz-65/network-recon-toolkit.git
cd network-recon-toolkit

# Quick TCP scan
python3 recon.py 192.168.1.10

# Full scan profile with rate tuning
python3 recon.py 10.0.0.0/24 --profile full -t 4 --rate 500

# Include UDP scanning
python3 recon.py 192.168.1.10 --udp

## Author
**Niknaz Sadehvandi**  
**Cybersecurity Analyst**

