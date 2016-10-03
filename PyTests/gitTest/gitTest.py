from subprocess import Popen
from subprocess import PIPE
from subprocess import call


files = [];

def initGit():
    link = input("Please type github branch link:\n");
    
    call(["git", "--bare", "clone", link]);
    call(["git", "--set-upstream", "origin", "master"]);
    #return link;
    


# check for local github repo
out = Popen(["cd", "gittut"], stderr=PIPE);
if("" != out.stderr.read()):
    initGit();

# updating github repo
call(["git", "pull"], cwd='gittut');

# commit process
call(["git", "add"] + files, cwd='gittut');
call(["git", "commit", "-m", "automated commit"], cwd='gittut');
call(["git", "push"], cwd='gittut');
