# import library (if these are not installed then install them using requirements.txt)
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import sqlite3
import datetime
import logging

# get the current time
cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

# get current directory path
cur_dir = os.path.dirname(os.path.realpath(__file__))

# setting the logging level
logging.basicConfig(filename=cur_dir+"/logs/indian_political_donors.log",
                    level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")

# sqlite3 db path
db = sqlite3.connect(cur_dir + '/db/property_price.db')

# myneta.info website url's
myneta_url = 'http://myneta.info'
myneta_all_donors_url = 'http://myneta.info/party/index.php?action=all_donors&id=1'

# pandas data frame display options on terminal (this is helpful while debugging)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 400)

# initializing a data frame
df_myneta_donors = pd.DataFrame()

# initializing lists (these are columns in data frame)
scrape_time = []
donor_name = []
donor_address = []
donor_pan = []
donor_amount = []
donor_contribution_mode = []
donor_financial_year = []

# headers (simulate a html browser. get this details from https://www.whoishostingthis.com/tools/user-agent/)
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }

# get the response
response = requests.get(myneta_all_donors_url, headers=headers, stream=True)
logging.debug(f"Received GET Response from {myneta_all_donors_url}")


# get the html content from the response
soup = BeautifulSoup(response.content, "html.parser")
donor_table = soup.find('thead', attrs={'class': 'tableFloatingHeaderOriginal'})

print("=================================")
print(donor_table)

