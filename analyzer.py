#!/usr/bin/env python3
import argparse
from pricing import get_prices
from utils import calculate_costs, print_comparison, export_csv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vm', nargs=3, required=True, help='AWS Azure GCP instance types')
    parser.add_argument('--storage', type=int, default=100, help='GB')
    parser.add_argument('--egress', type=int, default=1, help='TB outbound')
    args = parser.parse_args()

    aws_vm, azure_vm, gcp_vm = args.vm
    prices = get_prices(aws_vm, azure_vm, gcp_vm)
    results = calculate_costs(prices, args.storage, args.egress)
    print_comparison(results)
    export_csv(results)

if __name__ == "__main__":
    main()
