git config credential.helper store
git add .
git commit -m 'update'
git push -u origin master

## git filter-branch --index-filter 'git rm -r --cached --ignore-unmatch <file/dir>' HEAD