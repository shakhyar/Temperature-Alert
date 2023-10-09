import smtplib


class Mail():
    def __init__(self, email, password):
        self.m = smtplib.SMTP('smtp.gmail.com', 587)
        self.email = email
        self.password = password
 
        


    def send(self, mail, msg):
        # this function just sends mail, nothing much to explain here too

        self.msg = msg
        self.mail = mail

        self.m = smtplib.SMTP('smtp.gmail.com', 587)
        self.m.starttls()

        self.m.login(self.email, self.password)

        self.m.sendmail(self.mail, self.mail, self.msg)
        self.m.quit()