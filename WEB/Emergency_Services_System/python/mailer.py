from email.message import EmailMessage
import smtplib


def send_mail(receiver_email, subject, body):
    # construct email
    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = 'emergencyservicessystem@gmail.com'
    email['To'] = str(receiver_email)
    email.set_content(body, subtype='html')

    # """Password recovery code : <b>{}</b>""".format(str(code))

    # Send
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('emergencyservicessystem@gmail.com', 'zdgeirrchbgnphev')
    server.send_message(email)
    server.quit()
