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
clockexe = ("./bin/cloc-1.92.exe")
repourl = input("Please enter repository address: ")           
#"https://github.com/navdeep-G/setup.py.git" # input("Please enter the address for the repositories:") 


#remove all but repo name 
def repoURLpull(): 
    return(repourl.strip(".git").split("/")[-1]) 


#https://stackoverflow.com/questions/2514859/regular-expression-for-git-repository
def checkRepoValidity():
        if not re.match(r"((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(\/)?", repourl): 
            print(repourl + " is not a valid github URL please check your url and re-run again")
            sys.exit() # exit if the url is not valid
        else:
            print(repourl +" is a valid URL ")


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


        print("Generating clock report ...." + reponame)
        proc = subprocess.Popen([clockexe,currentDir+reponame,"--csv","--out" , clockoutput, "--quiet"],stdout=subprocess.PIPE)
        proc.stdout.read()
        print( "Your report has been saved as: " + clockoutput)
        



# https://realpython.com/python-send-email/#code-example
def Sendemail():
        subject = "Cloc report attached"
        body = "The report is attached to your email."
        sender_email = input("Email address:")
        receiver_email = input("Receiver email address:")
        password = input("Type your password and press enter:")

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        filename = clockoutput  # In same directory as script

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)

repoURLpull()

reponame = repoURLpull()
clockoutput = timestr+"-"+reponame+ ".csv"

clonerepo()

print("Press 1 to send email with AWS.")
print("Press 2 to send email with Gmail")
value = input('1.AWS  2.Gmail:  ')

if value == '1' or value == 'AWS':
    print('In progress') ##
    print('Complete!')
elif value == '2' or value == 'gmail':
    print('Sending email with Gmail')
    Sendemail()
    print('Exiting')
else:
    print('Please try again and respond with 1 or 2.')




sys.exit
