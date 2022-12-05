#%%
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from IPython.display import display

class TaskerSpyder:
    """Tasker Spyder - doc"""
    
    def __init__(self,url):
        self.url=url
        self.content_list = []
        self.case_dic = {
            "Title":[],
            "金額":[],
            "地點":[],
            "報價":[],
            "內容":[],
            "標籤":[],
            "更新時間":[],
        }
    
    def changeUrl(self,url_new):
        self.url=url_new
        self.driver.get(self.url)
        time.sleep(1.5)
    
    def setUp(self):
        """driver setting"""
        self.driver = webdriver.Firefox()
        self.driver.get(self.url)
        time.sleep(4)
    
    def caseContent(self):
        """gett content in one page"""
        # ele_length = len(self.driver.find_elements(By.TAG_NAME, "ul"))
        content_box=[]
        start_=0
        for i in range(11,31):
            print("====================================",i)
            each_content = self.driver.find_elements(By.TAG_NAME, "ul")[i].text
            self.content_list.append([])
            for word in each_content.split('\n'):
                print("------------------------")
                self.content_list[start_].append(word)
                # print(word)
            start_+=1
            # self.content_list.append(self.driver.find_elements(By.TAG_NAME, "ul")[i].text)
        return self.content_list
    
    def caseDataFrame(self):
        """target content of case"""
        for i in range(len(self.content_list)):
            each_case=self.content_list[i]
            # 加入到 dict
            self.case_dic['Title'].append(each_case[0])
            self.case_dic["金額"].append(each_case[1])
            self.case_dic["地點"].append(each_case[2])
            self.case_dic["報價"].append(each_case[3])
            self.case_dic["內容"].append(each_case[4])
            self.case_dic["標籤"].append(each_case[5])
            self.case_dic["更新時間"].append(each_case[6])
            
    def buildResult(self):
        df = pd.DataFrame(self.case_dic)
        display(df)
        return df
    
    def closerDriver(self):
        """driver close"""
        self.driver.close()

if __name__ == '__main__':
    url = "https://www.tasker.com.tw/case/list?ca=Brg"
    # url_page="https://www.tasker.com.tw/case/list?ca=Brg&page=2"#
    for i in range(1,22):#爬取1~21頁的case
        url_page="https://www.tasker.com.tw/case/list?ca=Brg&page="+str(i)#i=page number
        tasker_test = TaskerSpyder(url_page)# get driver//待修正
        tasker_test.setUp()#prepare driver//待修正
        tasker_test.caseContent()# 
        tasker_test.caseDataFrame()#
        tasker_res=tasker_test.buildResult() #
        tasker_res.to_csv("./tasker_"+"page"+str(i)+".csv") # save each page's result(csv)
        tasker_test.closerDriver()
    
#url= "https://www.tasker.com.tw/case/list"#首頁
#url= "https://www.tasker.com.tw/case/list?ca=Brg"#程式開發
#url= "https://www.tasker.com.tw/case/list?ca=MLZ"#翻譯寫作

# %%
