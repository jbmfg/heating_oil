import os
import requests
from bs4 import BeautifulSoup
import sqlite_connector
import datetime

cwd = os.getcwd()
db_file = os.path.join("/home/jbg/heating_oil", "heating_oil.db")
db = sqlite_connector.sqlite_db(db_file)

query = "update prices set current_price = 0;"
db.execute(query)

r = requests.get("https://www.maineoil.com/zone1.asp?type=0")
soup = BeautifulSoup(r.text, "html.parser")

table = soup.find_all("table")[0]
for row in table.find_all("tr"):
    row_data = [i for i in row.find_all("td")]
    if row_data:
        company, town, price, phone, date, calc = row_data
        price_dt = date.text.strip()
        price_dt = datetime.datetime.strptime(price_dt, "%m/%d/%Y")
        price_dt = datetime.datetime.strftime(price_dt, "%Y-%m-%d 00:00:00")
        insert = [{
            "company": company.text.strip(),
            "town": town.text.strip(),
            "price": price.text.strip(),
            "phone": phone.text.strip(),
            "price_date": date.text.strip(),
            "price_datetime": price_dt,
            "calc": calc.text.strip(),
            "current_price": 1
        }]


        db.insert_dict_list("prices", insert)

