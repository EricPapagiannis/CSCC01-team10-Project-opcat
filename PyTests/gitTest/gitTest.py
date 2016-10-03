from subprocess import call

# 'static' vars
files = [];
direc = "gittut";

def initGit():
    link = input("Please type github branch link:\n");
    
    call(["git", "--bare", "clone", link]);
    link = link.split('/')[-1][0:-4];
    call(["git", "push", "--set-upstream", "origin", "master"], cwd=link);
    return link;
    
def saveDirName(direc):
    file = open('dirname', 'w');
    file.write(direc);
    file.close();

def getDirName():
    try:
        file = open('dirname', 'r');
        return file.read();
    except IOError:
        return None;

# check for local github repo
direc = getDirName();
if(direc == None):
    direc = initGit();
    saveDirName(direc);

# updating github repo
call(["git", "pull"], cwd=direc);

# commit process
call(["git", "add", "."] + files, cwd=direc);
call(["git", "commit", "-m", "automated commit"], cwd=direc);
call(["git", "push"], cwd=direc);
