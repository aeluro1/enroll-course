from bs4 import BeautifulSoup
from email.message import EmailMessage
from Naked.toolshed.shell import execute_js, muterun_js
import requests
import time
import smtplib
import pandas
import numpy

# Initialize variables
url_root = r"https://oscar.gatech.edu/bprod/bwckschd.p_disp_detail_sched?term_in=202102&crn_in="
with open("crn.txt") as f:
    content = f.readlines()
url_ext = [x.strip() for x in content]
addr_from = "openseatbot@gmail.com"
addr_to = "john924xps@gmail.com"
summary = "This layout table is used to present the seating numbers."
link = "https://login.gatech.edu/cas/login?service=https%3A%2F%2Fsso.sis.gatech.edu%3A443%2Fssomanager%2Fc%2FSSB%3Bjsessionid%3D403F9BD6538B23A170ECB95AEE275F69"

# Email notification
# def notify(subj, bod):
    # msg = EmailMessage()
    # msg['Subject'] = subj
    # msg['From'] = addr_from
    # msg['To'] = addr_to
    # msg.set_content(bod)
    
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server.ehlo()
    # server.starttls()
    # server.login(addr_from, r"5$Ay*3h!9YK*rR")
    # server.send_message(bod)
    # server.quit()
    # msg.clear()

# Loop continuously
while True:  
    for each in url_ext:
        source = requests.get(url_root + str(each))
        soup = BeautifulSoup(source.text, "lxml")
        table = soup.find("table", {"summary": summary})
        desc = soup.find("th", {"class": "ddlabel"}).text
        df = pandas.read_html(str(table))[0]
        print(desc)
        print(df)
        s_a, s_w = df.to_numpy()[1:]
        if int(s_a[3]) != 0:
            print("SEAT AVAILABLE: CRN ID {0}\nOpen seat: {1}".format(each, s_a[3]))
            result = execute_js('enroll/enroll.js', arguments=str(each))
        #elif int(s_w[3]) != 0:
        #    print("SEAT AVAILABLE: CRN ID {0}\nWaitlist seat: {1}".format(each, s_w[3]))
        #    result = execute_js('enroll/enroll.js', arguments=str(each))
        print("\n")
    print("Pass complete.\n\n")
    
    time.sleep(20)
    continue

