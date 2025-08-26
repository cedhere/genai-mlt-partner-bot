import json
import cik

bucket = "sec-edgar-data-cedric"
key = "company_tickers.json"
def lambda_handler(event, context):
    try:
        sec = cik.SecEdgar(bucket, key)

        # gets the json input and parses
        request_type = event.get("request_type")
        company_ticker = event.get("company")
        year = event.get("year")
        
        if not request_type or not company_ticker or not year:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "missing fields"})
            }
        

        year = int(year)

        # handling the annual requests
        if request_type == "Annual":
            doc = sec.annual_filing(sec.ticker_to_cik(company_ticker), year)
        
        # handling the quarterly requests
        elif request_type == "Quarter":
            quarter = event.get("quarter")
            quarter = int(quarter)
            doc = sec.quarterly_filing(sec.ticker_to_cik(company_ticker), year, quarter)
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "request type must be 'Annual' or 'Quarter'"})
            }
        
        # handlng if no filing was found
        if doc == "Not found":
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "no doc found"})
            }
        
        return {
            "statusCode": 200,
            "body": json.dumps(doc)
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': "server error"
        }