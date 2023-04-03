from bs4 import BeautifulSoup
from email.message import EmailMessage
import requests
import time
import smtplib
import pandas
import numpy

# Initialize variables
url_root = r"https://oscar.gatech.edu/pls/bprod/bwckschd.p_disp_detail_sched?term_in=202008&crn_in="
summary = "This layout table is used to present the seating numbers."


# Loop continuously
while True:
    url_ext = input("CRN: ")
    source = requests.get(url_root + url_ext)
    soup = BeautifulSoup(source.text, "lxml")
    table = soup.find("table", {"summary": summary})
    try:
        desc = soup.find("th", {"class": "ddlabel"}).text
    except:
        print("CRN invalid.")
        continue
    df = pandas.read_html(str(table))[0]
    s_a, s_w = df.to_numpy()[1:]
    if int(s_a[3]) != 0:
        print("SEAT AVAILABLE: CRN ID {0}".format(url_ext), "| Open seat: {0}".format(s_a[3]) + "\n" + desc)
    elif int(s_w[3]) != 0:
        print("SEAT AVAILABLE: CRN ID {0}".format(url_ext), "| Waitlist seat: {0}".format(s_w[3]) + "\n" + desc)
    else:
        print("No seat available.")
    print("\n\n")

