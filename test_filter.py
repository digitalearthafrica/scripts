import json
import sys
import csv
import gzip
import boto3
import pandas as pd
from time import process_time
import inventory

if __name__ == '__main__':

    url = 's3://sentinel-cogs-inventory'
    suffix = "manifest.json"
    africa_tile_ids_path = ("data/africa-mgrs-tiles.csv")
    output_filepath = "C://temp/out_side_africa_extent.csv"
                               
    africa_tile_ids = pd.read_csv(africa_tile_ids_path, header=None)[0]    

    buckets = []
    keys = [] 
    s3_inventory = inventory.s3(url, suffix)
    for bucket, key, *rest in s3_inventory.list_keys():
        keys.append(key)
        buckets.append(bucket)

    tile_ids = pd.Series(keys).str.split("/", expand=True)[2].str.split("_", expand=True)[1]    
    filter = tile_ids.isin(africa_tile_ids)       
    outside_africa_extent = tile_ids[~filter]

    print(f"{len(outside_africa_extent)} objects out of {len(tile_ids[filter])} fall outside Africa: ") 
    pd.DataFrame({"ids": outside_africa_extent, 
                  "keys" : pd.Series(keys)[~filter]}).to_csv(output_filepath)

    