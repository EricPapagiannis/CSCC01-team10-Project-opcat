from subprocess import Popen
from subprocess import PIPE
from subprocess import call


files = [];
direc = "gittut";

def initGit():
    link = input("Please type github branch link:\n");
    
    call(["git", "--bare", "clone", link]);
    link = link.split('/')[-1][0:-4];
    call(["git", "push", "--set-upstream", "origin", "master"], cwd=link);
    return link;
    


# check for local github repo
out = Popen(["cd", "gittut"], stderr=PIPE);
if("" != out.stderr.read()):
    direct = initGit();

# updating github repo
call(["git", "pull"], cwd='gittut');

# commit process
call(["git", "add", "."] + files, cwd='gittut');
call(["git", "commit", "-m", "automated commit"], cwd='gittut');
call(["git", "push"], cwd='gittut');
