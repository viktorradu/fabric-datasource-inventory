from lib import *
import os, csv, argparse
from math import ceil
from pathlib import Path


parser = argparse.ArgumentParser(description='--output parameter parser')
parser.add_argument('--output', type=str, help='Output directory for the scan results')
parser.add_argument('--tenant', type=str, help='Tenant ID for the Service Principal')
parser.add_argument('--client', type=str, help='Client ID for the Service Principal')
parser.add_argument('--secret', type=str, help='Client secret for the Service Principal')
args = parser.parse_args()  
if args.output:
    output = args.output
else:
    output = 'output'

Path(output).mkdir(parents=True, exist_ok=True)

client = Client()
if args.tenant and args.client and args.secret:
    client.set_sp_credentials(tenant_id=args.tenant, client_id=args.client, client_secret=args.secret)
scan = Scan(client)

workspaces = scan.list_workspaces()
if 'error' not in workspaces:
    batch_size = 100
    batch_count = ceil(len(workspaces) / batch_size)
    for batch in range(0, batch_count):
        batch_workspaces = workspaces[batch:batch + batch_size]
        workspace_ids = [workspace['id'] for workspace in batch_workspaces]
        print(f"Scaning workspace batch {batch + 1} out of {batch_count}")
        scan_result = scan.scan_workspaces(workspace_ids)
        print(f"Scan completed for {len(workspace_ids)} workspaces.")
        
        for collection in scan_result.keys():      
            if len(scan_result[collection]) > 0:
                file_path = f'{output}/{collection}.csv'
                is_new = not os.path.exists(file_path)
                with open(file_path, 'a', newline='', encoding="utf-8") as file:
                    writer = csv.DictWriter(file,fieldnames=scan_result[collection][0].keys(),extrasaction='ignore', quoting=csv.QUOTE_ALL, lineterminator='\n')
                    if is_new:
                        writer.writeheader()
                    writer.writerows(scan_result[collection])
else:
    print(workspaces.error)
