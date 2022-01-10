import subprocess
import os
import git
import sys 
from git import repo




currentDir = "./"
clocexe = ("./cloc-1.90.exe")
repourl = input("Please enter the address for the repositories:") 



def repoURLpull():
    return(repourl.strip(".git").split("/")[-1]) 

reponame = repoURLpull



def clonerepo():
    if not os.path.exists ( currentDir + repoURLpull):
        print("Cloning repo..")
        try: 
            git.git( currentDir ) .clone( repourl )
        except git.exc.giterror:
            print( "Unable to pull repository, please try again")
            sys.exit()
    else: #Todo add git pull code for update of repo
        print (" Updating repo ..." )
    

clocoutput =(repoURLpull ,   ".csv" )


def clocreport():

    print("Generating CLOC report. Please wait. ")
    proc = subprocess.Popen([clocexe,currentDir+reponame,"--csv","--out" , clocoutput, "--quiet"],stdout=subprocess.PIPE)
    proc.stdout.read(
        print( clocoutput + "Has been saved. ")
    )

repoURLpull()
clonerepo()
clocreport()
