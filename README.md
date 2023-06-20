# small-gitosint-project
A small python project that extract data from git repos


## Usage

Get a repo from an url with the ```--url``` or ```-u``` flag
```
gitosint.py --url https://github.com/zamomfg/small-gitosint-project
```
Use a repo from a file with the ```--repo``` or ```-r``` flag
```
gitosint.py -r ./small-gitosint-project
```

Output:
```
Email,Username,Number of commits
--------------------------------
37627447+zamomfg@users.noreply.github.com,Zamomfg,1
```