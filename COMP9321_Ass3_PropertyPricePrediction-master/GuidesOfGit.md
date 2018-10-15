This is just a general guides for using git repo to teamwork, it doesn't contain  much details on command of git, you can search and learn them.

## Basic Command

To operate git, there are some basic command
 
 - Local repo control: `git add`, `git commit`, `git checkout`
 - Status check: `git log`, `git status`
 - Remote repo control: `git remote`, `git push`, `git pull`
 
## Cooperation

### Flow
 
 - First Step: Fork my git [repo](https://github.com/luckybuzhi/COMP9321_Ass3_PropertyPricePrediction)
 ![](https://ws1.sinaimg.cn/large/006tNbRwly1fvv27beqa4j30s2042mxq.jpg)
 
 - Second Step: `git clone` into your local repo
 - Third Step: modify local files and operate local repo
 - Special Step: see below   
 - Forth Step: after modification of your local repo, `git push` into your remote repo.
 - Fifth Step: Make a new pull request
 
 ![](https://ws4.sinaimg.cn/large/006tNbRwly1fvv2dyadouj30rq07cgmk.jpg)
 
 and I will check and merge your request.
 
 ### Update local repo
 
There is another important thing you need to do, update your local repo to the latest one as same as the repo your forked before `git push` for avoiding merge conflict.

You can use 

 - `git remote upstream https://github.com//username_you_forked//repo_your_fork.git` add remote connection
 - `git fetch upstream master` get latest repo
 - `git checkout master` switch to master branch
 - `git merge upstream/master` merge latest one into your local repo

By the way, the last three steps can be replaced by `git pull upstream master`, but it is not safe.

 
 