import requests
import os
import boto3

s3 = boto3.client('s3', region_name='us-east-1')

def download_file(url, file_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded to {file_path}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading: {e}")

# Example usage:
image_url = "https://upload.wikimedia.org/wikipedia/commons/3/3b/Triclinic_Lattice_type_1a_%28Brillouin_zone%29.png"
file = "downloaded_image.gif"
path = os.path.join(os.getcwd(), file) # Saves to current directory

download_file(image_url, path)

# vars needed
bucket_name = "ds2002-gzy5jd"
object_name = "downloaded_image.gif"
expires_in = 30 

# upload to s3 bucket
with open(file, "rb") as data:
            s3.put_object(
                Body=data,
                Bucket=bucket_name,
                Key=file,
                ACL='public-read'
            )
            print(f"File uploaded to S3: s3://{bucket_name}/{file}")

response = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket_name, 'Key': object_name},
    ExpiresIn=expires_in
)

print(f'Generated presigned url: {response}')
