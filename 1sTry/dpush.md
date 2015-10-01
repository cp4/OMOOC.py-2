gitbook-github double push 设置。

一期时这一关虐了不少人，二期难度反而增加，操作过程中更深入理解了git
操作，记录下来，和学员的尝试做对比。

我的尝试及理解
--------------

gitbook 和 github 内置了相互关联的机制，但是只能关联master
默认分支，而二期使用新建分支 primer2， 那么就不能使用内置机制，恰好gitbook
又支持分支编译，手动双推可行。

双推就是把本地仓库的改动，同时更新到github
和gitbook。关键点在于三个库要保持一致，否则容易引发不必要的麻烦。

仓库的基本框架已经在github上被大妈建立好，fork 这个仓库到私人帐号下就得到 github
仓库初始版本。gitbook
则通过新建一本书来获得初始仓库，这个仓库是空的。本地仓库从gitbook
中clone，获得一个空的初始版本。 如果从 github 中clone
理论上也应该可以，但是gitbook 或许不够灵活，追加对 gitbook 的关联可能更困难？
未尝试。

接下来用github 仓库同步gitbook 和本地仓库，这样三者取得一致。

### 一 clone gitbook 仓库

-   仓库的git 地址是这样的：git.gitbook.com/omoocpy/cp4tutornotes.git

clone需认证，gitbook 只支持https 明文口令认证，格式是这样的

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
git clone https://<用户名>:<口令>@git.gitbook.com/omoocpy/cp4tutornotes.git
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   口令不是登录gitbook所用的密码，而是API Token，进入gitbook -\> personal
    settings -\> Profile -\> API 下可以看到该选项，复制其中字符串即可。

-   clone 成功后确认

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  $ git remote -vv
  origin  https://<用户名>:<口令>@git.gitbook.com/omoocpy/cp4tutornotes.git (fetch)
  origin  https://<用户名>:<口令>@git.gitbook.com/omoocpy/cp4tutornotes.git (push)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### 二 为本地增加分支

-   为本地增加分支

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  $git checkout -b primer2
  Switched to a new branch 'primer2'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### 三 追加上游仓库

-   大妈的追加方式是

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  $git remote add hub git@github.com:OpenMindClub/OMOOC.py.git
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

经尝试，如果未使用SSH
方式，这种方法会出现认证失败。如果使用口令认证，可以这样追加

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  $git remote add hubs https://github.com/cp4/OMOOC.py-2.git 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   确认

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  $ git branch --all
  master 
  * primer2
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  $ git remote -vv
  hubs    https://github.com/cp4/OMOOC.py-2.git (fetch)
  hubs    https://github.com/cp4/OMOOC.py-2.git (push)
  origin  https://<用户名>:<口令>@git.gitbook.com/omoocpy/cp4tutornotes.git (fetch)
  origin  https://<用户名>:<口令>@git.gitbook.com/omoocpy/cp4tutornotes.git (push)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  $ git remote show hubs
  * remote hubs
  Fetch URL: https://github.com/cp4/OMOOC.py-2.git
  Push  URL: https://github.com/cp4/OMOOC.py-2.git
  HEAD branch: master
  Remote branches:
    master  new (next fetch will store in remotes/hubs)
    primer2 new (next fetch will store in remotes/hubs)
  Local refs configured for 'git push':
    master  pushes to master  (local out of date)
    primer2 pushes to primer2 (local out of date)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  $ git fetch hubs
  remote: Counting objects: 467, done.
  remote: Compressing objects: 100% (17/17), done.
  Receiving objectsremo:  te: 91% (425/Total 467467), 76.01 KiB | 5 (d6.00 elta 2), reused 0 (delta 0), pack-reused 450
  Receiving objects: 100% (467/467), 156.23 KiB | 56.00 KiB/s, done.
  Resolving deltas: 100% (228/228), done.
  From https://github.com/cp4/OMOOC.py-2
  * [new branch]      master     -> hubs/master
  * [new branch]      primer2    -> hubs/primer2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  $ git branch --all
  master
* primer2
  remotes/hubs/master
  remotes/hubs/primer2
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### 四 本地仓库同步 github 仓库

-   merge primer2 仓库

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$ git merge hubs/primer2
error: merge is not possible because you have unmerged files.
hint: Fix them up in the work tree, and then use 'git add/rm <file>'
hint: as appropriate to mark resolution and make a commit.
fatal: Exiting because of an unresolved conflict.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   查看冲突

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$ git status
On branch primer2
You have unmerged paths.
  (fix conflicts and run "git commit")

Changes to be committed:

        modified:   .gitignore
        new file:   .travis.yml
        ……

Unmerged paths:
  (use "git add <file>..." to mark resolution)

        both modified:   README.md
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   解决冲突

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$ git add README.md
$ git commit -am "init with primer2"
$ git merge hubs/primer2
Already up-to-date.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### 五 尝试双推

-   配置 .git/config

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[remote "origin"]
    url = https://cp4:7bf2f864-364d-43ba-a705-8f9176552a80@git.gitbook.com/omoocpy/cp4tutornotes.git
    url = https://github.com/cp4/OMOOC.py-2.git
    fetch = +refs/heads/*:refs/remotes/origin/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   git push 的默认模式配置

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
warning: push.default is unset; its implicit value has changed in
Git 2.0 from 'matching' to 'simple'.
……
When push.default is set to 'matching', git will push local branches
to the remote branches that already exist with the same name.

Since Git 2.0, Git defaults to the more conservative 'simple'
behavior, which only pushes the current branch to the corresponding
remote branch that 'git pull' uses to update the current branch.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

似乎配置称simple 影响范围更精确，但是，总之，我配置成了 matching 模式。

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$ git config --global push.default matching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   double push

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$ git push
Everything up-to-date
Username for 'https://github.com': cp4
Password for 'https://cp4@github.com':
Counting objects: 9, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (9/9), done.
Writing objects: 100% (9/9), 915 bytes | 0 bytes/s, done.
Total 9 (delta 6), reused 0 (delta 0)
To https://github.com/cp4/OMOOC.py-2.git
   784ada7..d39ef59  primer2 -> primer2
 ! [rejected]        master -> master (non-fast-forward)
error: failed to push some refs to 'https://github.com/cp4/OMOOC.py-2.git'
hint: Updates were rejected because a pushed branch tip is behind its remote
hint: counterpart. Check out this branch and integrate the remote changes
hint: (e.g. 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

可以看到，matching 模式把 master 推给 master， primer2 推给 primer2，而且 github
的 master推送出现错误。这是因为，本地的master 仓库还和
gitbook一致，是空的（前面只merge了 github 的
primer2），落后于github，所以想github
推送时出现错误。但是可以看到，双推机制已经配置成功。

##### 附：其他git 操作

-   在matching 模式下，也可以通过指定分支精准push。

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$ git push origin primer2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   尝试改变gitbook 的默认版本时，学到设置remote HEAD

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$ git remote set-head origin primer2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   使用远程覆盖当前版本

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$ git fetch hubs
$ git reset --hard hubs/master
HEAD is now at e05fd17 add in README.md
$ git pull hubs master
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   当前版本覆盖远程

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$ git push -f origin master
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
