import boto3
import requests

"""
Creating an AWS Lambda function for taking company ticker information JSON and storing it in an S3
bucket for use by the CIK lookup module. Print statements are added for CloudWatch Logs
"""
def lambda_handler(event, context):
    try:
        s3 = boto3.client('s3')
        url = "https://www.sec.gov/files/company_tickers.json"
        
        print("Starting the SEC downloading")
        headers = {'user-agent': 'MLT CPL cpierrelouis1114@gmail.com'}
        response = requests.get(url)
        print("Download completed, the file size is", len(response.content))

        print("uploading to s3")
        s3.put_object(Bucket='sec-edgar-data-cedric', Key='company_tickers.json', Body=response.content)
        return "successful! upload complete"
    except Exception as e:
        print(f"Error occured {e}")