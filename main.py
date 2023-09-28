import smtplib
import ssl
import requests
import selectorlib

"INSERT INTO events VALUES ('Tigers', 'Tiger City', '2088.10.14')"

URL = "https://programmer100.pythonanywhere.com/tours/"

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
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")

def read():
    with open("data.txt","r") as file:
        return file.read()

if __name__=="__main__":
    source = scrape(URL)
    extracted = extract(source)
    print(extracted)
    content = read()
    print("the content: ",content)
    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email(message="Hey, new event was found!")


