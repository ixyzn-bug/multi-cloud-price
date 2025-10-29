import pandas as pd
from datetime import datetime

HOURS = 730

def calculate_costs(prices, storage_gb, egress_tb):
    results = {}
    for provider, p in prices.items():
        vm_cost = p['vm'] * HOURS
        storage_cost = p['storage'] * storage_gb
        egress_cost = p['egress'] * egress_tb * 1024
        total = vm_cost + storage_cost + egress_cost
        results[provider] = {
            'vm_hourly': round(p['vm'], 5),
            'vm_monthly': round(vm_cost, 2),
            'storage': round(storage_cost, 2),
            'egress': round(egress_cost, 2),
            'total': round(total, 2)
        }
    return results

def print_comparison(results):
    print("\nProvider | VM ($/hr) | VM Cost | Storage | Egress | Total")
    print("-" * 65)
    for prov, cost in results.items():
        print(f"{prov.upper():8} | {cost['vm_hourly']:8.5f} | ${cost['vm_monthly']:6} | ${cost['storage']:6} | ${cost['egress']:5} | **${cost['total']}**")
    winner = min(results, key=lambda x: results[x]['total'])
    print(f"\n→ {winner.upper()} is the cheapest.")

def export_csv(results):
    df = pd.DataFrame(results).T
    df = df[['vm_hourly', 'vm_monthly', 'storage', 'egress', 'total']]
    df.to_csv(f"cost_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv")
    print(f"\nExported to CSV")
