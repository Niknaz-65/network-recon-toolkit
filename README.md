# Network Recon Toolkit
Python wrapper for Nmap that generates clean **HTML** and **CSV** recon reports.

## ✨ Features
- Quick or full scan profiles (TCP; optional UDP)
- Service/OS detection, timing (`-t 0–5`), and `--min-rate`
- Timestamped output in `./reports/<YYYYMMDD_HHMMSS>/`
  - `report.html` (pretty table)
  - `results.csv` (tabular data)
  - `scan.xml` (raw Nmap XML)

## ✅ Requirements
- Python 3.8+
- [`nmap`](https://nmap.org/) installed and available in your PATH

## 🚀 Quick Start
```bash
git clone https://github.com/Niknaz-65/network-recon-toolkit.git
cd network-recon-toolkit

# Quick single-host scan (default TCP)
python3 recon.py 192.168.1.10

# Full profile on a /24 with higher min-rate
python3 recon.py 10.0.0.0/24 --profile full -t 4 --rate 500

# Include UDP (slower)
python3 recon.py 192.168.1.10 --udp
