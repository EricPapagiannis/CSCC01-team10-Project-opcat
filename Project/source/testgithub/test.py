# sudo apt install python3-pip
# pip install PyGithub
# to be able to use github api

from github import Github
from github import PullRequest

g = Github("71eac6c43870f21a267b3ebee5afbf1482695e88")
# pull = repo.create_pull("Pull request created by PyGithub", "Body of the pull request", "source/testgithub", "eric:master")
# pull = repo.create_pull("Pull request created by PyGithub", "Body of the pull request", "topic/RewriteWithGeneratedCode", "BeaverSoftware:master")
# Then play with your Github objects:
for repo in g.get_user().get_repos():
    if repo.name == "team10-Project":
        repo.create_pull("Pull request test created by PyGithub", "Body of the pull request", "eric", "master")
        # issue = repo.create_issue("Issue created by PyGithub. TEST TEST TEST")
    print(repo.name)