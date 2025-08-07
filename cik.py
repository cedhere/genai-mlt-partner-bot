import requests

class SecEdgar:
    def __init__(self, fileurl):
        self.fileurl = fileurl
        self.name_dict = {}
        self.ticker_dict = {}
        self.data_dict = {}


        headers = {'user-agent': 'MLT CB cpierrelouis1114@gmail.com'}
        r = requests.get(self.fileurl, headers=headers)
        data = r.json()

        # parsing the data from the json into the respective dictionaries
        for entry in data.values():
            cik = int(entry["cik_str"])
            ticker = entry["ticker"]
            name = entry["title"]

            if not name or not ticker:
                continue

            self.data_dict[cik] = (cik, name, ticker)
            self.name_dict[name.lower()] = cik
            self.ticker_dict[ticker.lower()] = cik
        
    """
    Function that will look up a company's full CIK information using the company name
    """
    def name_to_cik(self, name):
        try:
            cik = self.name_dict[name.lower()]
            return self.data_dict[cik]
        except KeyError:
            return "Not found"

    """
    Function that will look up a company's full CIK information using the company stock
    ticker
    """
    def ticker_to_cik(self, ticker):
        try:
            cik = self.ticker_dict[ticker.lower()]
            return self.data_dict[cik]
        except KeyError:
            return "Not found"
    
    
    # SEC EDGAR API Library
    def annual_filing(self, cik, year):
        if not isinstance(cik, int):
            return "Not found"
        
        filing_info = self._match_filing(cik, "10-K", year)
        if not filing_info:
            return "Not found"
        
        cik_str = str(cik).zfill(10)
        return {
            "url": f"https://www.sec.gov/Archives/edgar/data/{cik_str}/{filing_info[0]}/{filing_info[2]}",
            "filing date": filing_info[1],
            "description": "10-K"
        }

    def quarterly_filing(self, cik, year, quarter):
        if not isinstance(cik, int):
            return "Not found"
        
        filing_info = self._match_filing(cik, "10-Q", year, quarter)
        if not filing_info:
            return "Not found"

        cik_str = str(cik).zfill(10)
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
        headers = {'user-agent': 'MLT CB cpierrelouis1114@gmail.com'}
        r = requests.get(url, headers=headers)
        data = r.json()
        return data["filings"]["recent"]
    
    """
    Private helper method for finding the matching form by year and quarter (if applicable)
    """
    def _match_filing(self, cik, form_type, year, quarter=None):
        data = self._get_filings_data(cik)
        forms = data["form"]
        accessionNumbers = data["accessionNumber"]
        dates = data["filingDate"]
        primaryDocuments = data["primaryDocument"]

        for i in range(len(forms)):
            if forms[i] != form_type:
                continue

            filing_year = int(dates[i][:4])
            if filing_year != year:
                continue

            if forms[i] == "10-Q" and quarter is not None:
                month = int(dates[i][5:7])
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


### Testing classes and methods ###
se = SecEdgar('https://www.sec.gov/files/company_tickers.json')
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

print(se.annual_filing(cik1, 2026))
print(se.quarterly_filing(cik1, 2025, 7))

# testing fail cases
print(se.annual_filing(cik2, 2024))
print(se.quarterly_filing(cik2, 2024, 1))