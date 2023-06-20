import git
import tempfile
import os
import argparse
import shutil
import datetime
import stat
import re


parser = argparse.ArgumentParser(description='Small GIT OSINT program')
repo_source_type = parser.add_mutually_exclusive_group(required=True)
repo_source_type.add_argument("-u", "--url", help="Url to repo")
repo_source_type.add_argument("-r","--repo", help="Path to repo")
parser.add_argument("-s","--search", help="Strings to search for. A single string or multiple seperated by comma")

args = vars(parser.parse_args())

temp_path = tempfile.gettempdir()

git_url = args["url"]

if git_url:
    git_name = git_url.rsplit('/', 1)[1]
    osint_path = os.path.join(temp_path, "gitosint")
    repo_path = os.path.join(osint_path, git_name)
    repo = git.Repo.clone_from(git_url, repo_path)
elif args["repo"]:
    repo_path =  os.path.realpath(args["repo"])
    git_name = os.path.basename(os.path.normpath(repo_path))
    repo = git.Repo(repo_path)

# print(repo_path)

# heads = repo.heads
# master = heads.master


# TODO create first/latest commit

def get_commit_info():

    commits = repo.iter_commits()

    committers = dict()

    for commit in commits:
        commit_date = commit.committed_datetime
        date = datetime.datetime(commit_date.year, commit_date.month, commit_date.day, commit_date.hour, commit_date.minute, commit_date.second)
        commit_data = {"hex": commit.hexsha, "date": commit_date}

        if commit.author in committers:
            committers[commit.author].append(commit_data)
        else:
            committers[commit.author] = [commit_data]

    return committers


def find_text_in_repo():

    strings_to_find = str(args["search"]).split(",")
    commits = repo.iter_commits()
    for commit in commits:

        for blob in commit.tree.blobs:
            file_content = blob.data_stream.read().decode("utf-8")

            for string in strings_to_find:
                find_str = f"({string}.*\\n)"
                # print(find_str)
                regex = re.findall(find_str, file_content)

                print(commit.hexsha, find_str, blob.path, regex)

find_text_in_repo()


commits = get_commit_info()
# TODO make it possible to change the values that are outputed
print("Email,Username,Number of commits")
print("--------------------------------")
for key, value in commits.items():
    print(f"{key.email},{key.name},{len(value)}")

repo.close()

def onerror(func, path, exc_info):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

if args["url"]:
    shutil.rmtree(osint_path, onerror=onerror)


# TODO use https://github.com/ishepard/pydriller instead of gitpython. It seems alot easier to use