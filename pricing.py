import boto3
import requests
from google.cloud import billing_v1

# Hardcoded fallbacks & regions (us-east-1 / eastus / us-east1)
REGIONS = {'aws': 'US East (N. Virginia)', 'azure': 'eastus', 'gcp': 'us-east1'}

def get_aws_price(instance_type):
    try:
        client = boto3.client('pricing', region_name='us-east-1')
        resp = client.get_products(
            ServiceCode='AmazonEC2',
            Filters=[
                {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
                {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': REGIONS['aws']},
                {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Linux'},
                {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'}
            ]
        )
        if resp['PriceList']:
            data = eval(resp['PriceList'][0])
            return float(list(data['terms']['OnDemand'].values())[0]['priceDimensions'].values())[0]['pricePerUnit']['USD']
    except: pass
    return 0.0416  # t3.medium fallback

def get_azure_price(instance_type):
    try:
        url = "https://prices.azure.com/api/retail/prices"
        query = f"armRegionName eq '{REGIONS['azure']}' and contains(skuName, '{instance_type.split('_')[0]}')"
        resp = requests.get(url, params={'$filter': query}).json()
        for item in resp['Items']:
            if instance_type.lower() in item['skuName'].lower():
                return item['retailPrice'] / 1000  # per hour
    except: pass
    return 0.0768  # D2s v5 fallback

def get_gcp_price(instance_type):
    try:
        client = billing_v1.CloudBillingClient()
        skus = client.list_skus(parent="services/6F81-5844-456A")  # Compute Engine
        for sku in skus:
            if instance_type in sku.description and 'Hourly' in sku.category.resource_group:
                rate = sku.pricing_info[0].pricing_expression.tiered_rates[0]
                return rate.unit_price.units + rate.unit_price.nanos / 1e9
    except: pass
    return 0.0335  # e2-medium fallback

def get_prices(aws_vm, azure_vm, gcp_vm):
    return {
        'aws': {'vm': get_aws_price(aws_vm), 'storage': 0.023, 'egress': 0.09},
        'azure': {'vm': get_azure_price(azure_vm), 'storage': 0.018, 'egress': 0.087},
        'gcp': {'vm': get_gcp_price(gcp_vm), 'storage': 0.020, 'egress': 0.12}
    }
