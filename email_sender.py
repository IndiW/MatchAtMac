import os
import smtplib
import csv
import random
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

count = 0
with open("final_output.csv", newline='') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        for row in csv_reader:
            #if count < 82:
            #    count += 1
            #    continue
            send1 = row[0]
            send2 = row[1]
            score = row[2]
            shared = [val for val in row[3:]]

            body = "Hello " + send1 + " and " + send2 + "!\n\nAfter analyzing over 1000 submissions, our algorithm has determined that you two are a Match at Mac!\n\n"

            if int(score) > 18:
                body += "You answered an amazing " + score + " of the 25 questions the EXACT same! Are you the same person?\n\n"

            if len(shared) > 5:
                body += "You two have a lot in common! For example, you both: \n\n"
                for i in random.sample(shared,5):
                    body += "- " + i + "\n"
                body += "\n"
            else:
                body += "You two stood out from the rest!\n\n"

            body += "And now, our job is done, and you're on your own! Why not start off by introducing yourselves, sharing social media, and see where it goes from there?\n\n"
            body += "Remember to follow us on facebook @MatchAtMac and let us know how we did! And be on the lookout for the next round of Match at Mac in the school year!\n\n"

            body +="Good luck and best wishes you two!\nYour Match at Mac Team"

            print(send1, send2)
            

            subject = 'You have a Match at Mac!'

            msg = f'Subject: {subject}\n\n{body}'

            smtp.sendmail(EMAIL_ADDRESS, [send1,send2], msg) #change second email to recipient

            count += 1
            print("Emails Sent: ", count)
            #break
        

