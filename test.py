def send_email():
            import smtplib

            gmail_user = "dabolink@gmail.com"
            gmail_pwd = "*************"
            FROM = 'dabolink@gmail.com'
            TO = ['dabolink@gmail.com'] #must be a list
            SUBJECT = "Testing sending using gmail"
            TEXT = "Testing sending mail using gmail servers"

            # Prepare actual message
            message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, message)
                #server.quit()
                server.close()
                print 'successfully sent the mail'
            except:
                print "failed to send mail"

if __name__ == "__main__":
    send_email()