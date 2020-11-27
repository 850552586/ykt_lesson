from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as wait_wd
from selenium.webdriver.support import expected_conditions  as ec
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.common.exceptions import TimeoutException
import time
import os
import json

#全局变量（包含设置文件
'''
lessons (dict) name-课程名，value-目录url
answers (dict) name-课程名 value-答案文件
settings[lessons] 课程名
settings[answers]
'''
settings = {
    'lessons':[],
    'first_login':True
}
with open("./settings.txt",'r',encoding='utf8') as f:
    lessons = json.load(f)
    for lesson,url in lessons.items():
        settings['lessons'].append(lesson)

with open('./answer_settings.txt','r',encoding='utf8') as f:
    answers = json.load(f)

#返回课程类型
'''
0: 视频
1: 讨论
2：习题
3: 课件
'''
def lessonType(url):
    if "video" in url:
        return 0
    elif "homework" in url:
        return 2
    elif "forum" in url:
        return 1
    elif "graph" in url:
        return 3


#加载课程url列表（未生成完全 或 文件不存在 返回False
def getLessonList(lesson):
    if not os.path.isfile(lesson+".txt"):
        print("文件不存在")
        return False
    with open(lesson+".txt",'r',encoding='utf8') as f:
        urls = f.readlines()
    if len(urls)==0:
        return False
    if urls[-1] != "finish":
        return False
    return urls

#生成课程url列表，保存至txt文件
def generateLessonList(driver,lesson):
    result = getLessonList(lesson)
    if result == False:
        section_url = lessons[lesson]
        urls = []
        with open("./"+lesson+".txt",'w+',encoding='utf8') as f:
            driver.get(section_url)
            time.sleep(5)
            section  = driver.find_element(*(By.CLASS_NAME, 'section-fr'))
            lesson_title = section.find_elements(*(By.CLASS_NAME,'leaf-title'))
            lesson_num = len(lesson_title)
            for i in range(lesson_num):
                driver.get(section_url)
                driver.refresh()
                time.sleep(6)
                s = driver.find_element(*(By.CLASS_NAME, 'section-fr'))
                lt = s.find_elements(*(By.CLASS_NAME,'leaf-title'))
                lt[i].click()
                time.sleep(5)
                f.write(driver.current_url+"\n")
                urls.append(driver.current_url)
            f.write('finish')
        return urls
    else:
        return result

#课件完成进度（是否完成
def finishCondition(driver,lesson):
    section_url = lessons[lesson]
    driver.get(section_url)
    section = wait_wd(driver,20,0.5).until(ec.presence_of_element_located((By.CLASS_NAME,'section-fr')))
    time.sleep(10)
    infos = section.find_elements(*(By.CLASS_NAME, 'el-tooltip'))
    condition = []
    for info in infos:
        t = info.text
        if t=='已读' or t=='已完成' or t=='已发言' or t=='缺勤':
            condition.append(1)
        else:
            condition.append(0)
    return condition

#查看播放进度，如果播放完成返回True
def getVideoFinish(driver):
    time.sleep(2)
    cur_videotime = driver.find_element_by_xpath('//*[@id="video-box"]/div/xt-wrap/xt-controls/xt-inner/xt-time/span[1]').text
    videotime = driver.find_element_by_xpath('//*[@id="video-box"]/div/xt-wrap/xt-controls/xt-inner/xt-time/span[2]').text
    print("curtime:{},videotime:{}".format(cur_videotime,videotime))
    if cur_videotime=="" or videotime=="" or cur_videotime!=videotime:
        return False
    print("播放完毕")
    return True

#播放视频
def videoPlay(driver,url):
    print(url)
    driver.get(url)
    videoBtn = wait_wd(driver,30,0.5).until(ec.presence_of_element_located((By.XPATH,'//*[@id="video-box"]/div/xt-wrap/xt-controls/xt-inner/xt-playbutton')))
    volumeBtn = driver.find_element_by_xpath('//*[@id="video-box"]/div/xt-wrap/xt-controls/xt-inner/xt-volumebutton')
    videoBtn_text = driver.find_element_by_xpath('//*[@id="video-box"]/div/xt-wrap/xt-controls/xt-inner/xt-playbutton/xt-tip').text
    volumeBtn.click()
    videoBtn.click()
    while not getVideoFinish():
        time.sleep(10)

#读取课程答案
answer_dict = {}
def getAnswer(lesson):
    answerfile = answers[lesson]
    answer_list = []
    if answerfile=="":
        answer_dict[lesson] = []
        return False
    with open("./"+answerfile,'r',encoding='utf8')as f:
        lines = f.readlines()
        for i in range(0,len(lines),2):
            title = lines[i].strip('\n\t')
            ans = lines[i+1]
            ans = ans.strip().split(' ')
            ans.insert(0,title)
            answer_list.append(ans)
    answer_dict[lesson] = answer_list


#答题
def answer(driver,url,lesson):
    print(url)
    driver.get(url)
    driver.implicitly_wait(30) 
    question_list = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[2]/div[1]/div/div/div/ul')
    question_btn = question_list.find_elements(*(By.TAG_NAME, 'li'))
    title = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div/div[1]/div/div[2]/span').text
    cur_answer = []
    answer_list = answer_dict[lesson]
    for ans in answer_list:
        if ans[0] == title:
            cur_answer = ans
            break
    for i,qbtn in enumerate(question_btn):
        qbtn.click()
        question_type = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div[1]').text
        if "多选题" in question_type or "单选题" in question_type or "判断题" in question_type:
            answer_section = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div[2]/div/ul')
            answer = answer_section.find_elements(*(By.TAG_NAME, 'li'))
        if "主观题" in question_type:
            #切换至iframe
            driver.switch_to.frame("ueditor_0")
            content = cur_answer[i+1]
            driver.execute_script("document.getElementsByClassName('view')[1].innerText ="+"'"+content+"'")
            driver.switch_to.default_content()
            time.sleep(10)
        if "单选题" in question_type or "多选题" in question_type:
            if (i+1) < len(cur_answer):
                if 'A' in cur_answer[i+1]:
                    answer[0].click()
                if 'B' in cur_answer[i+1]:
                    answer[1].click()
                if 'C' in cur_answer[i+1]:
                    answer[2].click()
                if 'D' in cur_answer[i+1]:
                    answer[3].click()
                if 'E' in cur_answer[i+1]:
                    answer[4].click()
        if "判断题" in question_type:
            if (i+1) < len(cur_answer):
                if '1' == cur_answer[i+1]:
                    answer[0].click()
                if '0' == cur_answer[i+1]:
                    answer[1].click()
        if "填空题" in question_type:
            tk_ans = cur_answer[i+1].split(',')
            tk_section = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div[2]/div')
            tk = tk_section.find_elements(*(By.TAG_NAME, 'input'))
            for k in range(len(tk_ans)):
                tk[k].send_keys(tk_ans[k])
        answer_btn = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/ul/li/span/button/span')
        answer_btn.click()
        time.sleep(5)


#讨论
def talk(driver,url):
    driver.get(url)
    time.sleep(3)
    talk_content = driver.find_element_by_xpath('//*[@id="new_discuss"]/div/div').find_elements(*(By.TAG_NAME, 'dl'))[2].find_element_by_class_name('cont_detail').text
    talk_input = driver.find_element_by_xpath('//*[@id="publish"]/div/div[1]/textarea')
    talk_input.send_keys(talk_content)
    time.sleep(2)
    talk_input_sender = driver.find_element_by_xpath('//*[@id="publish"]/div/div[3]/button/span')
    talk_input_sender.click()
    time.sleep(2)