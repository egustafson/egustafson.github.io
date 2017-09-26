Notes to myself on how to clone & publish:

## Cloning this repo

+ `git clone --recursive -b hugo-source github.com:egustafson/egustafson.github.io`

(or)

1. `git clone github.com:egustafson/egustafson.github.io`
2. `cd egustafson.github.io`
3. `git checkout hugo-source`
4. `cd theme/xmin`
5. `git submodule init`
6. `git submodule update`

## Publishing

1. Commit everything in the repo.  (script check for this)
2. `pub2gh.sh`
3. `cd public; git push origin master`  (echoed from pub2gh.sh)

## Clean after Publishing

1. `rm -rf public`
2. `git worktree prune`
