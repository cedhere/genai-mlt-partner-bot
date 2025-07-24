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
    
# testing class and methods
se = SecEdgar('https://www.sec.gov/files/company_tickers.json')
print(se.name_to_cik('Nvidia Corp'))
print(se.ticker_to_cik('MSFT'))
print(se.name_to_cik('Fake Corp'))
print(se.ticker_to_cik('FAKE'))