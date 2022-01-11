import subprocess
import os, sys
import re
import os
import time
import git 


timestr =time.strftime("%m%d%Y")
currentDir = "./"
clockexe = ("./bin/cloc-1.90.exe")
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
        else: # update repo
            print (" Updating repo ..." )
            Repo = git.Repo(reponame)
            g = git.Cmd.Git(reponame)
            g.pull()
            print( " You repo has been updated")

        print("Generating clock report ...." + reponame)
        proc = subprocess.Popen([clockexe,currentDir+reponame,"--csv","--out" , clockoutput, "--quiet"],stdout=subprocess.PIPE)
        proc.stdout.read()
        print( "Your report has been saved as: " + clockoutput)
        



# https://realpython.com/python-send-email/#code-example



repoURLpull()

reponame = repoURLpull()
clockoutput = timestr+"-"+reponame+ ".csv"

clonerepo()

