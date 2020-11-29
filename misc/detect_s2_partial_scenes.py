"""
Generate a report on scenes in deafrica-sentinel-2 bucket which have incomplete data
E.g command: python generate_report.py "s3://deafrica-sentinel-2-inventory/deafrica-sentinel-2/deafrica-sentinel-2-inventory/2020-11-24T00-00Z/manifest.json"
                                        africa_account report.txt

"""

from datetime import datetime
from pathlib import Path
import boto3
import csv
import gzip
import click
import json

MANIFEST_SUFFIX = "manifest.json"
SRC_BUCKET_NAME = "deafrica-sentinel-2"
INVENTORY_BUCKET_NAME = "s3://deafrica-sentinel-2-inventory/"


@click.command()
@click.argument("manifest-file")
@click.argument("aws-profile")
@click.argument("output-filepath")
def generate_report(manifest_file, aws_profile, output_filepath):
    """
    Compare Sentinel-2 buckets in US and Africa and detect differences
    A report containing missing keys will be written to s3://deafrica-sentinel-2/monthly-status-report
    """
    session = boto3.session.Session(profile_name=aws_profile)
    s3 = session.client("s3", region_name="af-south-1")
    manifest_file = manifest_file

    def read_manifest():
        bucket, key = manifest_file.replace("s3://", "").split("/", 1)
        s3_clientobj = s3.get_object(Bucket=bucket, Key=key)
        return json.loads(s3_clientobj["Body"].read().decode("utf-8"))

    def list_keys():
        manifest = read_manifest()
        for obj in manifest["files"]:
            bucket = "deafrica-sentinel-2-inventory"
            gzip_obj = s3.get_object(Bucket=bucket, Key=obj["key"])
            buffer = gzip.open(gzip_obj["Body"], mode="rt")
            reader = csv.reader(buffer)
            for row in reader:
                yield row

    keys = set()
    partial_scenes = set()

    for bucket, key, *rest in list_keys():
        scene_key = str(Path(key).parent)
        if scene_key not in keys:
            keys.add(scene_key)
            count = len(
                s3.list_objects_v2(Bucket=bucket, Prefix=scene_key + "/")["Contents"]
            )
            if count != 18:
                partial_scenes.add(scene_key)
                print("Partial scene: ", scene_key)

    print(f"{len(partial_scenes)} partial scenes found in {SRC_BUCKET_NAME}")

    with open(output_filepath, "w") as f:
        f.write("\n".join(partial_scenes))


if __name__ == "__main__":
    generate_report()