import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


def __tmp0(__tmp2: <FILL>, __tmp1) :
    """Sends an email when a new connection is created"""

    fromaddr = ""
    toaddr = ""
    msg = MIMEMultipart()
    msg["From"] = fromaddr
    msg["To"] = toaddr
    msg["Subject"] = "HoneyDock Attack Alert"

    if __tmp1 == 1:
        body = "HoneyDock just received a new connection from: " + __tmp2
    else:
        body = "HoneyDock just received another connection from: " + __tmp2

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("", 587)
    server.starttls()
    server.login("", "")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
