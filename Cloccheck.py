import email
import os
import re
import smtplib
import ssl
import subprocess
import sys
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import git

timestr =time.strftime("%m%d%Y")
currentDir = "./"
clockexe = ("cloc-1.92.exe")
repourl = input("Please enter repository address: ")           
#"https://github.com/navdeep-G/setup.py.git" for testing


#remove all but repo name 
def repoURLpull(): 
    return(repourl.strip(".git").split("/")[-1]) 


#https://stackoverflow.com/questions/2514859/regular-expression-for-git-repository
def checkrepovalidity():
            if not re.match(r"((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(\/)?", repourl): 
                print(repourl + " is not a valid github URL please try again.")
                sys.exit(0) # exit if the url is not valid
            else:
                print(repourl +"/n   is a valid URL ")


# clone repo , check file, update repo
# https://stackoverflow.com/questions/2472552/python-way-to-clone-a-git-repository
def clonerepo():
        if not os.path.exists(currentDir+reponame):  # check if file exists 
            print("Cloning repo..")
            try:   # way to clone git repo in python 
                git.Git(currentDir).clone(repourl)
            except git.exc.GitError:
                print( "Unable to pull repository, please try again")
                sys.exit()

        #https://stackoverflow.com/questions/47179167/open-an-exe-file-and-give-it-input-parameters-in-python
        print("Generating clock report ...." + reponame)
        proc = subprocess.Popen([clockexe,currentDir+reponame,"--csv","--out" , clockoutput, "--quiet"],stdout=subprocess.PIPE)
        proc.stdout.read()
        print( "Your report has been saved as: " + clockoutput)
        


# https://stackoverflow.com/questions/23171140/how-do-i-send-an-email-with-a-csv-attachment-using-python
# https://realpython.com/python-send-email/#code-example
def Sendemail():
        subject = "Cloc report attached"
        body = "The report is attached to your email."
        sender = input("Email address:")
        receiver = input("Receiver email address:")
        #password = input("Type your password and press enter:")

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = receiver
        message["Subject"] = subject
        #message["Bcc"] = receiver  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        filename = str(clockoutput)  # In same directory as script

        # Open csv file in binary mode
        with open(filename, "rb") as file:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.read())


        # Add header as key/value pair to attachment part
        part.add_header("Content-Disposition",f"file; filename= {filename}",)

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()
        
        
        # https://stackoverflow.com/questions/57715289/how-to-fix-ssl-sslerror-ssl-wrong-version-number-wrong-version-number-ssl
        # Log in to server using secure context and send email
        # Mailtrap.IO credentials required to test 
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.mailtrap.io", 587) as server:
            server.starttls(context=context)
            server.login("login", "loginpass")   # enter creds for MAILTRAP 
            server.sendmail(sender, receiver, text)
            server.quit()


repoURLpull()

reponame = repoURLpull()
clockoutput = timestr+"-"+reponame+ ".csv"
checkrepovalidity()

clonerepo()
    
print("Press 1 to exit now ...")
print("Press 2 to send email with Mailtrap")
value = input('1.Exit  2. Mailtrap:  ')

if value == '1' or value == 'q ':
    print('Your Cloc report is located in ./ ') ##
    print('Goodbye!')
elif value == '2' or value == 'mail':
    print('Sending email with Mailtrap.io...')
    Sendemail()
    print('Email sent....')
    print('Exiting')
else:
    print('Please try again and respond with 1 or 2.')




sys.exit
