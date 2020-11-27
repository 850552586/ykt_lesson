# ykt_lesson
**intro:用于完成雨课堂的视频播放/答题等功能的自动化脚本。**
<img src='https://img-blog.csdnimg.cn/20201127224206491.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hqbTg1MDU1MjU4Ng==,size_16,color_FFFFFF,t_70' width="50%">
## 如何使用？
从该地址clone完整项目。

settings.txt是设置文档，在settings.txt下填写你想刷的课程信息，格式为：课程名称:url地址。
（切记该url地址是课程打开后的目录地址！）
然后脚本在执行时便会根据该设置文件打开课程目录url地址，然后爬取该课程所有课件的url地址，存储在txt文件中（以课程名称命名）。

answer_settings.txt是答案设置文档，在这里填写需要答题的课程信息，格式为：课程名称：答案文件地址。
(切记这里的课程名称要与settings.txt对应！)
然后需要在答案文件txt中填写好答案。

p.s.：其中答案文件txt可以为空，但是answer_settings.txt必须需要有相关信息。



## 其他

日后继续补充。