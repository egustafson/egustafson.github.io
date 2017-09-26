Notes to myself on how to clone & publish:

## Cloning this repo

1. `git checkout hugo-source`
2. `cd theme/xmin`
3. `git submodule init`
4. `git submodule update`

## Publishing

1. Commit everything in the repo.  (script check for this)
2. `pub2gh.sh`
3. `cd public; git push origin master`  (echoed from pub2gh.sh)

