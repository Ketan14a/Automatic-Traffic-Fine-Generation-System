import smtplib

def sendEmail(EmailID):
	msg = "You have broken a traffic rule \n You will need to pay Rs 100 within 4 days."
	mail = smtplib.SMTP('smtp.gmail.com',587)
	mail.ehlo()
	mail.starttls()
	mail.login('iamketan14@gmail.com','tabu20111')
	mail.sendmail('iamketan14@gmail.com',EmailID, msg)
	mail.close()