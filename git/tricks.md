## Tricks for using git

### fetch branch one by one

```bash
$ mkdir ProjectName
$ cd ProjectName
$ git init
$
$ git remote add origin RemoteProjectURL(http://xxx.git)
$ git remote -v show origin
$
$ git remote set-branches origin MissingBranchName1
$ git fetch
$ git checkout -b LocalBranchName origin/MissingBranchName1
$
$ git remote set-branches --add origin MissingBranchName2
$ git fetch
$ git branch -a
$ git checkout -b LocalBranchName origin/MissingBranchName2
```

