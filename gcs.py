from google.cloud import storage
#import dask.dataframe as dd
import os
import pandas as pd

def save_df(df, bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    bucket.blob('online_test.csv').upload_from_string(df.to_csv(), 'text/csv')

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def create_bucket(bucket_name):
    """Creates a new bucket."""
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.create_bucket(bucket_name)

    print("Bucket {} created".format(bucket.name))

def list_buckets():
    """Lists all buckets."""
    storage_client = storage.Client()
    buckets = storage_client.list_buckets()
    bucket_names = []
    for bucket in buckets:
        print(bucket.name)
        bucket_names.append(bucket.name)
    return bucket_names
