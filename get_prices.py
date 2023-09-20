import requests
from bs4 import BeautifulSoup
import sqlite_connector

db = sqlite_connector.sqlite_db("heating_oil.db")

r = requests.get("https://www.maineoil.com/zone1.asp?type=0")
soup = BeautifulSoup(r.text)

table = soup.find_all("table")[0]
for row in table.find_all("tr"):
    row_data = [i for i in row.find_all("td")]
    if row_data:
        company, town, price, phone, date, calc = row_data
        insert = [{
            "company": company.text,
            "town": town.text,
            "price": price.text,
            "phone": phone.text,
            "price_date": date.text,
            "calc": calc.text,
        }]
        db.insert_dict_list("prices", insert)

