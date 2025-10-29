# Multi-Cloud Cost Analyzer (AWS vs Azure vs GCP)

Compares real-time costs using official pricing APIs.

## Features
- Fetch VM, storage & data transfer prices
- Supports AWS, Azure, GCP
- CLI + CSV export
- No third-party tools

## Setup
```bash
pip install -r requirements.txt
Set credentials:

AWS: aws configure
GCP: export GOOGLE_APPLICATION_CREDENTIALS=key.json

Run
bashpython analyzer.py --vm t3.medium D2s_v5 e2-medium --storage 100 --egress 1
Output
textAWS: $122.67 | Azure: $144.86 | GCP: $146.46 → AWS wins
Files

analyzer.py – Main script
pricing.py – API clients
utils.py – Cost logic
