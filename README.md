## MLT Gen AI Project

## Introduction
As part of the MLT Career Prep '27 cohort, I had the opportunity to expand my technical skills by building this project. Beyond learning the technologies listed in the tech stack below, I also developed experience with the full software development lifecycle — including project planning, meeting deadlines, code deployment, and overall project management. The project layout was created entirely by MLT, all credit to them.

## Tech Stack
- Python
- cURL
- AWS (Lambda, S3, EventBridge)

## What is the SEC & Its Use in This Project

The U.S. Securities and Exchange Commission (SEC) is the federal government agency that regulates the securities markets in the United States. Its mission is to protect investors, maintain fair and efficient markets, and facilitate capital formation — essentially acting as the referee of the stock market.

Public companies such as NVIDIA, Apple, and Microsoft are required to regularly submit financial reports to the SEC. These reports are stored in a large public database called **EDGAR**, which is the foundation of this project.

This project provides tools to pull and organize those reports so developers, investors, and analysts can access them quickly. Instead of manually digging through EDGAR, users can use this software to look up companies and grab their filings in a structured way.

The main reports supported are:
- **10-K (Annual Report)** — a company’s most detailed yearly filing.  
- **10-Q (Quarterly Report)** — shorter updates released throughout the year.  

## CIK Lookup Module

The first feature implemented was the CIK Lookup Module. This feature allows you to take a company name or ticker and return its CIK (Central Index Key). A CIK is the SEC’s unique identifier for each company in EDGAR.

### How it Works

1. Fetch the company data JSON from the SEC’s endpoint  
2. Parse the JSON into two dictionaries for O(1) lookups  
3. Standardize the input so lookups are reliable  
4. Provide helper functions for easy access  

### Improvement with AWS (currently tweaking)

After learning about cloud development with AWS, I began improving the lookup module.  

Originally, the module loaded the JSON directly from the SEC’s website at runtime.  

In the update, the module will be able to read from an S3 bucket, which is refreshed automatically via AWS (Lambda + EventBridge). This makes the lookup module faster, more reliable, and prevents overloading the SEC servers.

### Expanding the CIK Module

After building the initial lookup module, I expanded it by using the EDGAR API. Additional methods were added to retrieve **10-K (Annual Reports)** and **10-Q (Quarterly Reports)**.  

In the beginning, I experimented with the API using cURL to understand how it worked.  

1. The CIK that is looked up is passed into the desired function  
2. The CIK is used to build the URL for accessing the company submissions JSON. This JSON contains the company’s entire filing history. The `recent` filings section of the JSON is returned in `_get_filings_data`.  
3. In `_match_filing`, the `form`, `filingDate`, `accessionNumber`, and `primaryDocument` are extracted. The function iterates over all forms to find the one requested by the user, including its date, accession number, and primary document.  

Using the function **`annual_filing`**, you can obtain the 10-K of a company by providing its CIK and the desired year.  

Using the function **`quarterly_filing`**, you can obtain the 10-Q of a company by providing its CIK, year, and quarter.
