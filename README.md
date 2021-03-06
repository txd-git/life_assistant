### 项目名称：智能生活小助手



### 1.项目描述：

实现个人生活助理工作：

1.》语音识别

2.》查询天气

​	用户点击或者语音识别后实现查询未来一周天气，并对出行交通工具和穿衣等做出建议。		

3.》一夜暴富（双色球生成及往期查询）

​	用户点击或者语音识别后实现生成一组双色球号码，提供查询往期双气球中奖号码的查看。

4.》个人随身便签

​	用户点击或者语音识别后实现对个人生活的便签功能

5.》新闻查看

用户点击或者语音识别后实现新闻的查询查看

6.》日常日记

用户点击或者语音识别后实现可以做日常日记的功能（增删改查）

### 2.架构介绍：

本项目使用前后端分离技术。前端使用nginx代理，后端使用Django框架进行数据交互。



### 3.软件环境及技术栈：

操作系统Ubuntu18.04 

编译器：Pycharm

Python版本     3.6

Django版本    Django2.2.2



## 生活小助手使用说明文档

##### 1.准备工作：

<1>项目开始前先创建数据库Life_assistant

​		生成后迁移数据表

<2>迁移数据表完成后，找到城市转化代码文件夹，在

pycharm上运行01.py文件，提前将需要的数据放入数据表中。

<3>保证运行环境中有以下第三方库

​		1>   baidu-aip

​		2>   bs4

​		3>  Beatiful Soup

​		4> fake-useragent

​		5>django

​		6>nigx(待定)

<4>创建超级管理员用户，用以管理后台（管理已写）

<5>保证系统中redis数据库处于解放状态（解除哨兵主从控制）

##### 2.启动项目：

​	通过django项目启动命令启动项目	

##### 3.使用说明：

​	1>注册：注册注意用户名不要超过11位，用户名不能重复，一个用户只能绑定一个邮箱号用于修改信息，如果用qq邮箱注册则在qq邮箱垃圾箱查看验证码。

​	2>忘记密码：如果用qq邮箱则在qq邮箱垃圾箱查看验证码，必须保证用户名和邮箱一致。

​	3>主页：进入主页必须保证登录状态下，否则会自动跳转登录页面。

​	4>天气：进入天气功能会自动定位，弹窗定位允许请求，点确定，会自动定位（定位有点慢）

​	5.>语音识别：说出包含其他功能的名字能自己跳转要进入的页面，说话前先点击话筒按钮，说完再次点击。简单的对话可以实现智障聊天。弹窗是否允许话筒，点击允许，否则该功能无法使用

​	6>日记书写：进入生活日记页面，导航栏有标签点击可以书写，修改在笔记主页点击要修改的笔记即可，删除同上。

​	7>吐槽论坛：进入论坛可以编辑，修改，点击详情可以评论回复。非编辑用户不可修改该论坛。

​	8>后台管理：运用django自带的后台管理，在各个app中设置，可以做到对日记，用户，论坛的管理等等。



