# ykt_lesson
**intro:用于完成雨课堂的视频播放/答题等功能的自动化脚本。**
<img src='https://img-blog.csdnimg.cn/20201127224206491.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hqbTg1MDU1MjU4Ng==,size_16,color_FFFFFF,t_70' width="50%">

**免责声明**

<font color="red">**本项目仅用于分享脚本经验，一切使用该脚本的用户所作出的行为与本项目无关！请勿应用于商业途径，请勿擅自转载！如有侵权，请issues告知！**</font>

[项目介绍](https://ericam.top/post/jiao-ben-yu-ke-tang-zi-dong-hua-python-jiao-ben/)



## Usage

**1.环境配置**

chrome浏览器+chromedriver下载

chromedriver下载地址：[here](https://registry.npmmirror.com/binary.html?path=chromedriver/)

将chromedriver.exe放到chrome安装位置（Aplication文件夹），然后添加环境变量。

p.s：chromedriver下载的版本记得大于chrome浏览器的版本



**2.文件介绍**

settings.txt是设置文档，在settings.txt下填写你想刷的课程信息，格式为：课程名称:url地址。
（切记该url地址是课程打开后的目录地址！）
然后脚本在执行时便会根据该设置文件打开课程目录url地址，然后爬取该课程所有课件的url地址，存储在txt文件中（以课程名称命名）。

answer_settings.txt是答案设置文档，在这里填写需要答题的课程信息，格式为：课程名称：答案文件地址。
(切记这里的课程名称要与settings.txt对应！)
然后需要在答案文件txt中填写好答案。

p.s.：其中答案文件txt可以为空，但是answer_settings.txt必须需要有相关信息。



**3.运行**

```shell
python main.py
```

询问是否首次登录时，输入0或1。（1代表首次，0代表非首次）

当首次运行时，需要当自动化脚本打开浏览器，进入首页时，手动点击登录按钮，扫码登录即可。



**4.代码需要注意修改的地方**

`main.py`

```python
home_url="https://***.yuketang.cn/pro/portal/home/" #记得填写自己学校雨课堂地址~
```

`settings.txt`

改成你的课程名称与对应地址

```
{
    "工程伦理":"https://.yuketang.cn/pro/lms/8An9nREbzDS/5640353/studycontent"
}
```



**5.其他**

本项目以xx学校雨课堂作为测试点进行开发，不同学校版本可能有所不同。

请自行更改部分代码即可。

欢迎二次开发，但请勿应用于商业用途！