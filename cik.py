import requests
import boto3
import json

class SecEdgar:
    def __init__(self, bucket, key_name):
        self.s3 = boto3.client('s3')
        self.bucket = bucket
        self.key_name = key_name
        self.headers = {'user-agent': 'MLT CPL cpierrelouis1114@gmail.com'}
        
        obj =  self.s3.get_object(Bucket = self.bucket, Key = self.key_name)
        data = obj["Body"].read().decode("utf-8")
        self.filejson = json.loads(data)

        self.name_dict = {}
        self.ticker_dict = {}

        for value in self.filejson.values():
            cik = str(value["cik_str"]).zfill(10)
            name = value["title"].lower()
            ticker = value["ticker"].lower()

            self.name_dict[name] = (cik, value["title"], value["ticker"])
            self.ticker_dict[ticker] = (cik, value["title"], value["ticker"])
    
    """
    Function that will look up a company's full CIK information using the company name
    """
    def name_to_cik(self, name):
        try:
            return self.name_dict[name.lower()]
        except KeyError:
            return "Not found"

    """
    Function that will look up a company's full CIK information using the company stock
    ticker
    """
    def ticker_to_cik(self, ticker):
        try:
            return self.ticker_dict[ticker.lower()]
        except KeyError:
            return "Not found"
    
    
    # SEC EDGAR API Library
    def annual_filing(self, cik, year):
        cik_str = self._normalize_cik(cik)
        if not cik_str:
            return "Not found"

        filing_info = self._match_filing(cik_str, "10-K", int(year))
        if not filing_info:
            return "Not found"
        
        return {
            "url": f"https://www.sec.gov/Archives/edgar/data/{cik_str}/{filing_info[0]}/{filing_info[2]}",
            "filing date": filing_info[1],
            "description": "10-K"
        }

    def quarterly_filing(self, cik, year, quarter):
        cik_str = self._normalize_cik(cik)
        if not cik_str:
            return "Not found"
        
        filing_info = self._match_filing(cik_str, "10-Q", int(year), int(quarter))
        if not filing_info:
            return "Not found"

        return {
            "url": f"https://www.sec.gov/Archives/edgar/data/{cik_str}/{filing_info[0]}/{filing_info[2]}",
            "filing date": filing_info[1],
            "description": "10-Q"
        }

    # helper methods for SEC EDGAR API Library
    """
    Private helper method for fetching and parsing the submission json by CIK
    """
    def _get_filings_data(self, cik):
        cik_str = str(cik).zfill(10)
        url = f"https://data.sec.gov/submissions/CIK{cik_str}.json"
        headers = {'user-agent': 'MLT CPL cpierrelouis1114@gmail.com'}
        r = requests.get(url, headers=headers)
        data = r.json()
        return data["filings"]["recent"]
    
    """
    Private helper method for finding the matching form by year and quarter (if applicable)
    """
    def _match_filing(self, cik, form_type, year, quarter=None):
        data = self._get_filings_data(cik)
        forms = data.get("form", [])
        accessionNumbers = data.get("accessionNumber", [])
        dates = data.get("filingDate", [])
        primaryDocuments = data.get("primaryDocument", [])

        for i in range(len(forms)):
            if not forms[i].startswith(form_type):
                continue

            try:
                filing_year = int(dates[i][:4])
            except (ValueError, IndexError):
                continue

            if filing_year != year and filing_year != year + 1:
                continue

            if form_type == "10-Q" and quarter is not None:
                try:
                    month = int(dates[i][5:7])
                except (ValueError, IndexError):
                    continue
                if not self._match_quarter(month, quarter):
                    continue
            
            return (accessionNumbers[i].replace("-", ""), dates[i], primaryDocuments[i])
        
        return None
        

    """
    Helper method for making sure that the month matches the quarter correctly
    """
    def _match_quarter(self, month, quarter):
        if quarter == 1:
            return 1 <= month <= 3
        elif quarter == 2:
            return 4 <= month <= 6
        elif quarter == 3:
            return 7 <= month <= 9
        elif quarter == 4:
            return 10 <= month <= 12
    
    """
    Helper method to extract the cik
    """
    def _extract_cik_value(self, cik):
        if isinstance(cik, (tuple, list)) and cik:
            return cik[0]
        return cik

    """
    Helper method for normalizing the cik
    """
    def _normalize_cik(self, cik):
        try:
            return str(int(self._extract_cik_value(cik))).zfill(10)
        except (TypeError, ValueError):
            return None



### Testing classes and methods ###
se = SecEdgar("sec-edgar-data-cedric", "company_tickers.json")
print(se.name_to_cik('Nvidia Corp'))
print(se.ticker_to_cik('MSFT'))
print(se.name_to_cik('Fake Corp'))
print(se.ticker_to_cik('FAKE'))

# testing the annual and quarterly filing information
print("---------------------------")
cik_info1 = se.ticker_to_cik('AAPL')
cik_info2 = se.ticker_to_cik('FAKE')
cik1 = cik_info1[0]
cik2 = cik_info2[0]
print(se.annual_filing(cik1, 2024))
print(se.quarterly_filing(cik1, 2024, 1))

# testing fail cases
print(se.annual_filing(cik1, 2026))
print(se.quarterly_filing(cik1, 2025, 7))

print(se.annual_filing(cik2, 2024))
print(se.quarterly_filing(cik2, 2024, 1))