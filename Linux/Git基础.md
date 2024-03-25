[toc]
#### 基本命令
###### git安装
```
sudo apt-get install git
```
###### 配置用户名
```
sudo git config --global user.name Uranus
```
###### 配置用户邮箱
```
git config --global user.email hanming_qin@qq.com
```
###### 查看本地仓库
```
cat ~/.gitconfig
```
###### git init
```
git init
ls -a --查看隐藏目录(.git是项目的根目录，删掉即可不受git管理)
```
###### 查看本地仓库状态
```
git status
```
###### 将工作内容记录到暂存区
```
git add file1 file2 ...
git add *
```
###### 取消文件暂存记录
```
git rm --cached file1 file2 ...
git rm --cached *
```
###### 将文件同步到本地仓库
```
git commit file1 file2 ... -m '文件描述'
git commit -m '文件描述' 将暂存区所有记录同步到仓库区
```
###### 查看commit日志记录
```
git log
git log --pretty=oneline
```
###### 将暂存区或者commit点文件恢复到工作区
```
git chechkout -- file1 file2 ...
```
###### 移动或者删除文件
```
git mv file1 file2 ... [path]
git rm file1 file2 ...
```
#### 版本控制
###### 退回到上一个commit节点
```
git reset --hard HEAD^
```
###### 退回到指定得commit_id 节点
```
git reset --hard [commit_id前七位即可]
```
###### 查看所有操作记录
```
git reflog
```
###### 创建标签
```
git tag [tag_name] [commit_id] -m [message]
说明: commit_id可以不写则默认标签表示最新的commit_id位置，message也可以不写，但是最好添加。
例子：git tag v1.0 -m '版本1'
```
###### 去往某个节点
```
git reset --hard [tag]
```
###### 删除标签
```
git tag -d [tag]
```
#### 保存工作区
###### 保存工作内容
```
git stash save [message]
例：git stash save '第一种方案'
```
###### 查看工作区列表
```
git stash list
```
###### 应用某个工作区
```
git stash apply stash@{n}
```
###### 删除工作区
```
git stash drop stash@{n}
git stash clear --删除所有保存的工作区
```
#### 分支管理
###### 查看分支情况
```
git branch
```

###### 查看所有分支
```
git branch -a
```

###### 创建分支
```
git branch [branch_name]
```
###### 切换工作分支
```
git checkout [branch_name]
git checkout -b [branch_name]  --创建并切换分支
```
###### 合并分支
```
git merge [branch_name]
```
###### 删除分支
```
git branch -d [branch_name] --删除分支
git branch -D [branch_name] --删除没有被合并的分支
```
#### GitHub远程仓库
###### 绑定到哪个仓库
```
git remote add origin https://github.com/xxxxx
```
###### 在本地使用git clone方法获取
```
git clone https://github.com/xxxxxxxxx
```
###### 查看连接的主机
```
git remote
```
###### 删除远程主机
```
git remote rm [origin]
```
###### 将本地分支推送给远程仓库
```
git push -u origin master
git push
```
###### 推送标签
```
git push origin [tag] --推送本地标签到远程
git push origin --tags 推送本地所有标签到远程
```
###### 推送旧的版本
```
git push --force origin
```
###### 删除远程分支和标签
```
git push origin :branch_name 删除远程分支
git push origin --delete tag [tagname] 删除远程仓库标签
```
###### 从远程获取代码
```
git pull
```

#### Git clone远程分支

- git clone http://xxx.com/project/.git
- cd project
- git branch -a（列出所有分支名称）
- git checkout -b dev origin/dev（作用是checkout远程的dev分支，在本地起名为dev分支，并切换到本地的dev分支）

###### 克隆分支的另一个方法：

```
git clone -b (分支项目名) http://myrepo.xxx.com/project/.git
```

@[toc]
##### 基本命令

- clone远程分支：

  ```
  git clone -b (分支项目名) http://myrepo.xxx.com/project/.git
  ```

- 要先commit之后才会真正建立master分支，此时才可以建立其它分支

  ```
  建立分支 git branch name(分支名稱)
  ```

- 切換分支 git checkout name（分支名稱）

- 綁定遠程倉庫 git remote add origin https://xxxx

- git init(ls -a)

- 设置全局用户名和码云上预留的email

  ```
  git config --global user.name "fortunamajor"
  git config --global user.email "17682310652@163.com"
  ```

##### 將代碼推送至遠程倉庫的分支

```
- 獲取遠程倉庫代碼 git clone https://xxx
	注意：代碼文件獲取下來之後，再進入代碼文件打開git bash here，不然無法向遠程倉庫推送（獲取不到文件裡的隱藏文件.git）
- git add *
- git commit -m "名稱描述"
- 建立分支 git branch name(分支名稱)
- 切換分支 git checkout name（分支名稱）
- git status
- 将本地分支推送到远程分支下以test命名 git push --set-upstream origin Frandis
```

##### 將代碼推送到遠程倉庫

```
git status
git add .
git commit -m "introduce"
git push
```

##### 遠程倉庫新建的新項目時，第一次將本地代碼推送至遠程倉庫

```
cd existing_folder
git init
git remote add origin ssh://git@10.156.148.63:2289/FrandisHMQin/my-autoupdater.git
git add .
git commit -m "Initial commit"
git push -u origin master
```

##### 使用pycharm中的git模塊

```
1. 創建一個新的文件夾
2. 在此文件夾下打開終端
3. 在終端中clone遠端的文件：git clone xxxx
4. 在clone好的文件夾下使用pycharm打開
5. 在pycharm中切換分支，分支名字和遠端的分支名保持一致
6. 在pycharm的菜單欄中找到pull，選擇對應的分支
這樣，就能將遠端對應的分支複製到本地了
```
##### 强制解决冲突，保持和线上一致
1. 切换分支：`git checkout 分支名`
2. 拉取远程分支并强制覆盖本地分支：`git fetch origin 分支名` `git reset --hard origin/分支名`
3. 清理未跟踪的文件和目录：git clean -fd