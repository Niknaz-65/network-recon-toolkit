# Network Recon Toolkit
Python wrapper for Nmap that generates an HTML recon report.

## Requirements
- Python 3.8+
- `nmap` installed and available in your PATH

## Usage
```bash
python3 recon.py <target-or-cidr>
# example
python3 recon.py 192.168.1.10
python3 recon.py 10.0.0.0/24 --profile full -t 4 --rate 500
python3 recon.py target1 target2 target3 --udp
