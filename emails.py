import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

subject = "SRB COVID-19 izveštaj na dan"
body = "Izveštaj se nalazi u prilogu."
sender_email = "covid19.srb@gmail.com"
receiver_email = ["covid19.srb@gmail.com",
                  "bandukaaa@gmail.com"]
password = input("Type your password and press enter:")

# Create a multipart message and set headers
message = MIMEMultipart()
message["Subject"] = subject

# Add body to email
message.attach(MIMEText(body, "plain"))

filename = "Poslednji_izveštaj.png"  # In same directory as script

# Open PDF file in binary mode
img_data = open(filename, 'rb').read()
image = MIMEImage(img_data, name=os.path.basename(filename))

# Add attachment to message and convert message to string
message.attach(image)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    for email in receiver_email:
        server.sendmail(sender_email, email, text)
