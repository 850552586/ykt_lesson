from selenium import webdriver
import lesson as ls
import json


ifFirst = input("是否是第一次登录：")
if  ifFirst == '1':
    ls.settings['first_login'] = True
else:
    ls.settings['first_login'] = False
driver = webdriver.Chrome()
driver.maximize_window()# 最大化窗口
#模拟登录
home_url="https://***.yuketang.cn/pro/portal/home/" #记得填写自己学校雨课堂地址~
driver.get(home_url)
driver.delete_all_cookies()
if ls.settings['first_login']:
    time.sleep(10)
    with open('cookies.txt','w') as cookief:
        cookief.write(json.dumps(driver.get_cookies()))
else:
    with open('cookies.txt','r') as cookief:
        #使用json读取cookies 注意读取的是文件 所以用load而不是loads
        cookieslist = json.load(cookief)
        # 方法1 将expiry类型变为int
        for cookie in cookieslist:
            #并不是所有cookie都含有expiry 所以要用dict的get方法来获取
            if isinstance(cookie.get('expiry'), float):
                cookie['expiry'] = int(cookie['expiry'])
            driver.add_cookie(cookie)


if __name__ == '__main__':
    #根据配置文件 添加课程url到队列
    all_urls = {}
    for lesson in ls.settings['lessons']:
        url = ls.generateLessonList(driver,lesson)
        condition = ls.finishCondition(driver,lesson)
        all_urls[lesson] = [url,condition]
    

    #开始干活了！
    #lesson = input("请输入你想刷的课:")
    for lesson in ls.settings['lessons']:
        #例如：lesson = "工程伦理"
        ls.getAnswer(lesson)
        l_urls = all_urls[lesson][0]
        l_condition = all_urls[lesson][1] 
        print(l_condition)
        for i,condi in enumerate(l_condition):
            if condi == 1:
                continue
            url = l_urls[i]
            if ls.lessonType(url) == 0:
                continue
                ls.videoPlay(driver,url)
            elif ls.lessonType(url) == 1:
                ls.talk(driver,url)
            elif ls.lessonType(url) == 2:
                ls.answer(driver,url,lesson)
            else:
                driver.get(url)
    driver.quit()
