#!/bin/sh

## Publish this Hugo blog to GitHub, same repo, 'master' branch.
##
##  adapted from:  https://gohugo.io/hosting-and-deployment/hosting-on-github/#deployment-from-your-gh-pages-branch
##
## run from the top of the hugo (source) repository
##  - directory "public" will be overwritten, it should be in .gitignore
##

# Upstream repository
#
UPSTR="origin"

# Publication branch
#
PUB_BR="master"

## ######################################################################

if [ -z "$(git config --get user.name)" ]; then
    echo "'user.name' not set."
    exit 1;
fi

if [ -z "$(git config --get user.email)" ]; then
    echo "'user.email' not set."
    exit 1;
fi

if [[ $(git status -s) ]]
then
    echo "Dirty repository.  Please commit all pending changes."
    exit 1;
fi

HASH=$(git log -1 --pretty=format:"%h")

echo "Scrubbing previous publication (./public)"
rm -rf public
mkdir public
git worktree prune
rm -rf .git/worktrees/public/

echo "Checking out '$PUB_BR' into ./public"
git worktree add -B $PUB_BR public $UPSTR/$PUB_BR

echo "Removing existing files from ./public"
rm -rf public/*

echo "Generating site"
hugo

echo "Updating (commit) branch $PUB_BR"
cd public
git add --all
git commit -m "Publishing from $HASH (pub2gh.sh)"

echo "Success:  published content [$HASH] to $PUB_BR locally."
echo ""
echo " > cd public; git push $UPSTR $PUB_BR"
echo ""
echo "to push upstream."

