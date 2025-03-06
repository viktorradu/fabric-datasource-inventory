from lib import *
import os, csv
from math import ceil
from pathlib import Path

path = './output'
Path(path).mkdir(parents=True, exist_ok=True)

client = Client()
scan = Scan(client)

workspaces = scan.list_workspaces()
if 'error' not in workspaces:
    batch_size = 100
    batch_count = ceil(len(workspaces) / batch_size)
    for batch in range(0, len(workspaces), batch_size):
        batch_workspaces = workspaces[batch:batch + batch_size]
        workspace_ids = [workspace['id'] for workspace in batch_workspaces]
        print(f"Scaning workspace batch {batch + 1} out of {batch_count}")
        scan_result = scan.scan_workspaces(workspace_ids)
        print(f"Scan completed for {len(workspace_ids)} workspaces.")
        
        for collection in scan_result.keys():      
            file_path = f'{path}/{collection}.csv'
            is_new = not os.path.exists(file_path)
            with open(file_path, 'a', newline='', encoding="utf-8") as file:
                writer = csv.DictWriter(file,fieldnames=scan_result[collection][0].keys(),extrasaction='ignore', quoting=csv.QUOTE_ALL, lineterminator='\n')
                if is_new:
                    writer.writeheader()
                writer.writerows(scan_result[collection])
else:
    print(workspaces.error)
