from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_with_edge(_str_list:list):
  
  str_result = []
  options = Options()
  options.add_argument("--disable-notifications")   # 這邊的用意是取消掉彈出視窗
  options.add_argument("headless")    #  隱藏操作視窗，在背景執行
  options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 關掉警告訊息

  edge = webdriver.Edge('./msedgedriver', options=options )

  edge.get("https://wintelguy.com/bulkmac.pl")

  input_area = edge.find_element(By.NAME,"tbx")
  for tmp in _str_list:
    input_area.send_keys(tmp)
    input_area.send_keys("\n")

  submit = edge.find_element(By.NAME,".submit")
  submit.submit()

  soup = BeautifulSoup(edge.page_source,"html.parser")

  table1 = soup.find("table",{
    'class': 'w3-table w3-bordered'
  })
  
  i = 1

  for tmp in table1.find_all("td"):
    if i%2 == 0:
      #  print("[{0}]: {1}".format(i, tmp.text ))
      str_result.append( tmp.text )
    i += 1

  i = 0

  for i in range( len(str_result) ):
    str_result[i] = str_result[i].replace("\n","")
    #  print(str_result[i])

  return str_result

    
def test_function():

  #  測試用的MAC，由於避免機密外洩之疑已經將此資料內的MAC改過了。
  
  macList = [
    "000001001100",
    "00000102948f",
    "000029999999",
    "999999999999",
    "111111111111",
    ]
  

  str_result = []
  options = Options()
  options.add_argument("--disable-notifications")   # 這邊的用意是取消掉彈出視窗
  #  options.add_argument("headless")    #  隱藏操作視窗，在背景執行
  options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 關掉警告訊息
  edge = webdriver.Edge('./msedgedriver', options=options )
  edge.get("https://wintelguy.com/bulkmac.pl")

  input_area = edge.find_element(By.NAME,"tbx")
  for tmp in macList:
    input_area.send_keys(tmp)
    input_area.send_keys("\n")

  submit = edge.find_element(By.NAME,".submit")
  submit.submit()

  soup = BeautifulSoup(edge.page_source,"html.parser")

  table1 = soup.find("table",{
    'class': 'w3-table w3-bordered'
  })
  
  i = 1

  for tmp in table1.find_all("td"):
    if i%2 == 0:
      #  print("[{0}]: {1}".format(i, tmp.text ))
      str_result.append( tmp.text )
    i += 1

  
  for i in range( 0,len(str_result) ):
    str_result[i] = str_result[i].replace("\n","")
    print("[{0}]\t{1}".format(i+1,str_result[i]))

  
  reset = WebDriverWait(edge,5).until(
    EC.presence_of_element_located((By.NAME,"rst"))
  )
  reset.submit()

  time.sleep(5)

#  test_function()