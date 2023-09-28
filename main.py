import smtplib
import sqlite3
import ssl
import requests
import selectorlib

"INSERT INTO events VALUES ('Tigers', 'Tiger City', '2088.10.14')"

URL = "https://programmer100.pythonanywhere.com/tours/"

# connecting with the database
connection = sqlite3.connect("data.db")

def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "dzheng@terpmail.umd.edu"
    password = "abnplxgfhtacnoet"
    # password = os.getenv("PASSWORD")

    recipient = "dzheng@terpmail.umd.edu"

    my_context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=my_context) as server:
        server.login(username, password)
        server.sendmail(username, recipient, message)
    print("send email")

def store(extracted):
    new_row = [item.strip() for item in extracted.split(",")]
    print("new_row: ", new_row)
    # object that can execute sql queries
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", new_row)
    connection.commit()

def read(extracted):
    row = [item.strip for item in extracted.split(",")]
    band, city, date = row
    # object that can execute sql queries
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",(str(band), str(city), str(date)))
    rows = cursor.fetchall()
    print(rows)
    return rows

if __name__=="__main__":
    source = scrape(URL)
    extracted = extract(source)
    print(extracted)
    if extracted != "No upcoming tours":
        row = read(extracted)
        if not row:
            store(extracted)
            send_email(message="Hey, new event was found!")


