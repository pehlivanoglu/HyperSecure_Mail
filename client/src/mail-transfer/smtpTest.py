import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = 587 # port number
smtp_server = "smtp.gmail.com" # gmail server name
login = "example" # mail user ID (everything before @)
password = "abcd efgh ijkl mnop" # 16-digit application-specific password

sender_email = "senderemail@gmail.com"
receiver_email = "receiveremail@gmail.com"
message = MIMEMultipart("alternative") # to combine plain text and HTML
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

# plain text part
text = """\
"""

# HTML part
html = """\
<html>
  <body>
    <p>SLM,<br>
      BİR ŞEY DENİYORUM</p>
    <p> bu mesajı aldıysan bir şey deniyorum </p>
  </body>
</html>
"""

# convert both parts to MIMEText objects and add them to the MIMEMultipart message
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")
message.attach(part1)
message.attach(part2)

# send the email
with smtplib.SMTP(smtp_server, port) as server:
    server.connect(smtp_server, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(login, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
    server.quit()

print('Sent')