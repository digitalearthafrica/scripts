import json
import sys
import os
import csv
import gzip
import boto3
import pandas as pd
from pathlib import Path
from time import process_time
import inventory

def delete_object(key, bucket_name):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        key = key + "/"
        bucket.objects.filter(Prefix=key).delete()
        print("Deleted: ", bucket_name +  '/' + key)

if __name__ == '__main__':

    url = 's3://deafrica-sentinel-2-inventory'
    suffix = "manifest.json"
    africa_tile_ids_path = ("data/africa-mgrs-tiles.csv")
    output_filepath = "C://temp/out_side_africa_extent.csv"

    africa_tile_ids = pd.read_csv(africa_tile_ids_path, header=None)[0]

    buckets = []
    keys = []

    s3_inventory = inventory.s3(url, suffix)
    for bucket, key, *rest in s3_inventory.list_keys():
            keys.append(os.path.dirname(key))

    keys_unique = pd.Series(keys).unique()
    tile_ids = pd.Series(keys_unique).str.split("/", expand=True)[2].str.split("_", expand=True)[1]

    filter = tile_ids.isin(africa_tile_ids)
    outside_africa_extent = tile_ids[~filter]
    print("Number of scenes falling outside Africa extent", len(outside_africa_extent))

    df = pd.DataFrame({"bucket": [bucket]*len(outside_africa_extent), "ids": outside_africa_extent,
                  "keys" : pd.Series(keys_unique)[~filter]})
    df.to_csv(output_filepath)
    # exclude files that are not S2 scenes and therefore have no tile IDs
    df = df[~df["ids"].isnull().values]
    for key, bucket in zip(df["keys"], df["bucket"]):
        delete_object(key, bucket)



