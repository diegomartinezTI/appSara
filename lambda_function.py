import os
import gnupg
import boto3
from botocore.exceptions import (
    ClientError
)

session = boto3.Session( aws_access_key_id='AKIAQJZNGEWMWYXNQ3GX', aws_secret_access_key='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')
s3 = session.resource('s3')
ssm = boto3.client("ssm")

def handler(event, context):
    my_bucket = s3.Bucket('merchantkey')
    my_bucket.download_file("XX_AP_UPL_MERCHANT_DOCS_NPRD_.key", "/tmp/XX_AP_UPL_MERCHANT_DOCS_NPRD_.key") 
    print("algo")
    

    items = []
    
    for my_bucket_object in my_bucket.objects.all():
        file = my_bucket_object.key
        items.append(file)
        my_bucket.download_file(f"{file}", f"/tmp/{file}") 
    
    for file in items:
        result = encrypt_file(f"/tmp/{file}") 
        print(result)
    
    return f'Gpg encrypt ok'       


def encrypt_file(file_name):
    gpg_homeshort = "/tmp"
    gpg = gnupg.GPG(gnupghome=gpg_homeshort, verbose=True)
    key = open("XX_AP_UPL_MERCHANT_DOCS_NPRD_.key", "rb").read()
    gpg.import_keys(key)
    gpg.list_keys() 
    with open(file_name, "rb") as f:
        status = gpg.encrypt_file(
            f,
            recipients=["Luis.Salazar@Millicom.com"],
            output=f"/tmp/{file_name}.gpg",
            always_trust=True,
            extra_args=["--yes"],
        )
        print(status) 
    lst = os.listdir("/tmp")
    
    return lst


 

 
