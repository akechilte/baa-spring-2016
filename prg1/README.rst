Dataset Name: 2016 Presidential Campaign - Candidate Disbursements

Dataset Source: http://www.fec.gov/data/CandidateDisbursement.do
Dataset FTP url: ftp://ftp.fec.gov/FEC/Presidential_Map/2016/P00000001/P00000001D-ALL.zip

Dataset Description: This file contains all itemized disbursements reported by a candidate for either the House or Senate during the current election cycle. This includes any candidate who ran in a regular House or Senate campaign, along with all candidates in special elections in either the odd numbered year or the election year.

Column List:
Committee ID
Committee Name
Candidate ID
Candidate name
Election year
Candidate Office
Candidate Office State
Candidate Office District
Line number from Detailed Summary Page of FEC Form 3
Link to image presentation
Recipient Committee ID
Recipient Name
Recipient Street Address
Apt. number or Suite number for recipient
recipient city
recipient state
recipient zip
date of disbursement
amount of disbursement
purpose description
memo code
memo text
category code
category description
transaction id
back reference id

Data fetch & cleansing using fetchdata.py:

This script is divided into different module and below is the description of each module.

download module:
1) downloads the 2016 campaign disbursement data from "Federal Election Commision" site via ftp protocol.
2) It unzips the compressed file

cleanse_data module:
1) reads the csv file and loads it into a pandas dataframe
2) disbursement date is standardized to yyyy-MM-dd
3) invalid date records are removed and filters only records for year 2015 & 2016
4) generates a new year-month column for aggregation in yy-MM format

put_line_csv module:
1) aggregates disbursement amount by year-mon column
2) writes the aggregated amount column and year-mon column to data-line csv file

put_hist_csv module:
1) aggregates disbursement amount by candidate
2) filters top 10 spend candidate records
2) writes the aggregated amount column and candidate column to data-hist csv file with "|" as separator as the candidate names has comma (",") in the names.