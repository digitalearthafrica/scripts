import boto3
import json
import gzip
import csv
import os.path as op
from copy import deepcopy
from datetime import datetime, timedelta

class s3(object):
    def __init__(self, url, suffix=''):
        self.url = url
        self.suffix = suffix
        self.s3 = boto3.client('s3') 
        self.bucket = self.urlparse(self.url)['bucket']        

    # Modified derived from https://alexwlchan.net/2018/01/listing-s3-keys-redux/
    def find(self, url, sub_key):
        """
        Generate objects in an S3 bucket.
        :param: sub_key: string to be present in the object name
        :param url: The URL of the bucket      
        """
        
        parts = self.urlparse(url)
        kwargs = {'Bucket': parts['bucket']}

        while True:
            # The S3 API response is a large blob of metadata.
            # 'Contents' contains information about the listed objects.
            resp = self.s3.list_objects_v2(**kwargs)           
            try:
                contents = resp['Contents']
            except KeyError:
                return
       
            for obj in contents:
                key = obj['Key']    
                if sub_key in key and key.endswith(self.suffix):                   
                    yield f"s3://{parts['bucket']}/{obj['Key']}"

            # The S3 API is paginated, returning up to 1000 keys at a time.
            # Pass the continuation token into the next response, until we
            # reach the final page (when this field is missing).
            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break

    def latest_manifest(self):   
        """
        Return a dictionary of a manifest file"
        """     
        parts = self.urlparse(self.url)
        # get latest manifest file
        today = datetime.now()
        manifest_url = None
        for dt in [today, today - timedelta(1)]:
            _key = op.join(parts['key'], dt.strftime('%Y-%m-%d'))
            _url = 's3://%s' % (parts['bucket'])           
            manifests = [k for k in self.find(_url, _key)]                 
            if len(manifests) == 1:                
                manifest_url = manifests[0]
                parts = self.urlparse(manifest_url)    
                break
        if manifest_url:         
            s3_clientobj = self.s3.get_object(Bucket=parts['bucket'], Key=parts['key'])               
            return json.loads(s3_clientobj['Body'].read().decode('utf-8'))
        else:
            return None        


    def urlparse(self, url):
        """ Split S3 URL into bucket, key, filename """
        _url = deepcopy(url)
        if url[0:5] == 'https':
            _url = cls.https_to_s3(url)
        if _url[0:5] != 's3://':
            raise Exception('Invalid S3 url %s' % _url)

        url_obj = _url.replace('s3://', '').split('/')

        # remove empty items
        url_obj = list(filter(lambda x: x, url_obj))
        return {
            'bucket': url_obj[0],
            'key': '/'.join(url_obj[1:])
        }

    def list_keys(self):                     
        manifest = self.latest_manifest()
        for obj in manifest['files']:    
            print(obj['key'])                                   
            gzip_obj = self.s3.get_object(Bucket=self.bucket, Key=obj['key'])             
            buffer = gzip.open(gzip_obj["Body"], mode='rt')
            reader = csv.reader(buffer)
            for row in reader:
                yield row 
