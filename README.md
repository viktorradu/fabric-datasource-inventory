# fabric-datasource-inventory

The script is designed to extract Microsoft Fabric workspace metadata along with users, semantic models, and datasources into flat csv files.

Run pip instll to ensure the dependencies are installed.
```
pip install -r .\requirements.txt 
```

The script will append data to files in the output folder (path variable in invenroty.py). Remove files from the output folder before running to avoid duplicate records.