# -*- coding: utf-8 -*-

import pandas as pd
import csv
import os
import copy
from bs4 import BeautifulSoup

class read_csv:

  def __init__(self):
    self.file_name1 = ""    #  存放路徑1的檔案名稱
    self.file_name2 = ""    #  存放路徑1的檔案名稱
    self.list_without_same_in_list1 = []    #  存放篩選後的MAC列表

  def find_data_in_list(self,_list:list,_str:str):  
    
    #  從 _list中尋找_str位置，若沒有找到則回傳-1
    #  從0開始

    cur_pos = -1

    for tmp in _list:
      if tmp == _str:
        cur_pos = _list.index(_str)

    return cur_pos

  def set_file_name( self,_filename:str, _option:int ):

  #  從別的檔案讀取到的路徑傳給此程式的filename，由_option決定存到哪一個filename

    if _option == 1:
      self.file_name1 = _filename
    elif _option == 2:
      self.file_name2 = _filename

  def run(self,mode:int):    #  執行篩選MAC的功能
    df1 = pd.read_csv(self.file_name1)    #  將第一個檔案存成dataframe
    df2 = pd.read_csv(self.file_name2)    #  將第二個檔案存成dataframe

    mac_pos1 = 0    #  第一個檔案中，MAC欄位位置
    mac_pos2 = 0    #  第二個檔案中，MAC欄位位置

    title1 = list(df1.iloc[0:])   #  第一個檔案中，標題的list
    title2 = list(df2.iloc[0:])   #  第二個檔案中，標題的list

    mac_pos1 = self.find_data_in_list(title1,"MAC Address")   #  尋找 MAC Address 的欄位位置
    mac_pos2 = self.find_data_in_list(title2, "MAC地址")      #  尋找 MAC地址 的欄位位置

    if mac_pos1 == -1:
      print( "找不到 MAC Address 欄位!" )
      return self.list_without_same_in_list1

    if mac_pos2 == -1:
      print( "找不到 MAC地址 欄位!" )
      return self.list_without_same_in_list1

    list1 = list(df1.iloc[:,mac_pos1])   #  forescout的MAC
    list2 = list(df2.iloc[:,mac_pos2])  #  GCB的MAC

    is_nan1 = (df1.iloc[:,mac_pos1]).isna().sum()  #  紀錄list1中的nan數量
    is_nan2 = (df2.iloc[:,mac_pos2]).isna().sum()  #  紀錄list2中的nan數量
    len1 = len(list1)
    len2 = len(list2)

    i = 0

    for i in range(len1):     #  裡面的資料要轉成string才能使用下面的一些功能
      list1[i] = str(list1[i])

    i = 0
    for i in range(len2):
      list2[i] = str(list2[i]).replace('-','')  #  轉換成string的同時，去掉'-'

    list1.sort()  # 排序
    list2.sort()  # 排序

    #  排序後，空白會在後面

    del list1[(len1-is_nan1):len1]  #  扣掉空白資料
    del list2[(len2-is_nan2):len2]  #  扣掉空白資料

    list_the_same = set(list1) & set(list2)  #  找兩個list中相同的資料並存到 list_the_same

    self.list_without_same_in_list1 = [ x for x in list1 if x not in list_the_same ]  #  list1中扣掉list_the_same後的資料
    
    if mode == 1:
      self.output_file()  #  如果是手動執行版本，會輸出一個MAC列表的csv檔

    print( "Result:\n", self.list_without_same_in_list1[0:10] )
    print( "\nLength:", len(self.list_without_same_in_list1) )
    
    return self.list_without_same_in_list1

  def output_file(self):
    output_file = "output.csv"    #  輸出的檔案名稱，可按需求修改
    with open(output_file,"w",newline = "") as csvfile:
      writer = csv.writer( csvfile )
      writer.writerow(["MAC","Name"])
      rows = [[data] for data in self.list_without_same_in_list1 ]  # 轉為二維list，輸出資料後可存成同一欄
      writer.writerows(rows)
      print("輸出完成")

  def list_item_to_string(self,_list:list):

    #  將_list內容轉換成string型態

    _len = len( _list ) 
    for i in range(_len):
      _list[i] = str(_list[i])

  def combine_forescout_file(self,_columnName):
    
    #  此函式功能為：將填好廠商資料的output.csv讀進來，然後回填至檔案一的欄位中。

    df = pd.read_csv("output.csv")
    df_forescout = pd.read_csv(self.file_name1)

    title = list(df_forescout.iloc[0:])

    list_mac = list(df.iloc[:,0])  #  mac列表
    
    self.list_item_to_string( list_mac )

    list_names = list(df.iloc[:,1])  #  mac資料對應的廠商名稱

    self.list_item_to_string( list_names )

    common_pos = self.find_data_in_list(title, _columnName)   #  目前廠商資料回填欄位為 _columnName
                                                              #  _columnName 為使用者輸入
    
    if common_pos == -1:
      return False

    mac_pos = self.find_data_in_list(title,"MAC Address")
    print( "mac_pos:",mac_pos )
    
    if mac_pos == -1:
      print( "無此欄位!" )
      return False
    else:
      df_forescout = df_forescout.sort_values(by="MAC Address",ascending=True)
      org_mac_list = list( df_forescout.iloc[:,mac_pos])  #  原始資料中MAC address欄位的資料
      print( "len:", len(org_mac_list) )
      print( "data:", org_mac_list[0:10] )
      
    self.list_item_to_string( org_mac_list )

    #  print( type(org_mac_list[0]) )
    #  for i in range(len( org_mac_list )):
    #    org_mac_list[i] = str( org_mac_list[i] )

    pos_list = []  #  存放 mac_list 中的資料在原版資料中的位置資訊
    
    for index, element in enumerate( org_mac_list ):
      if element in list_mac:
        pos_list.append(index)  # 從原本的MAC欄位中找到要填入的位置，將位置資訊存進 pos_list中
        
    print( "len:", len(pos_list) )
    #  print( pos_list[0:10] )
    #  print( list_names[0:10] )

    i = 0
    for pos in pos_list:
      df_forescout.iloc[ pos, common_pos ] = list_names[i]  #  將已知的MAC的廠商資料回填至 comment 欄位
      i += 1

    df_forescout.to_csv("output2.csv",index=False)
    return True

  def combine_forescout_file_with_two_lists(self,_macList:list,_nameList:list,_columnName:str):
    
    df_forescout = pd.read_csv(self.file_name1)
    
    title = list(df_forescout.iloc[0:])  #  抓第一行資料

    list_mac = _macList  #  mac列表
    
    self.list_item_to_string( list_mac )

    list_names = _nameList  #  mac資料對應的廠商名稱

    self.list_item_to_string( list_names )

    common_pos = self.find_data_in_list(title, _columnName)   #  目前廠商資料回填欄位為 _columnName
                                                              #  _columnName 為使用者輸入
    
    if common_pos == -1:
      return False

    mac_pos = self.find_data_in_list(title,"MAC Address")
    
    if mac_pos == -1:
      print( "無此欄位!" )
      return False
    else:
      df_forescout = df_forescout.sort_values(by="MAC Address",ascending=True)
      org_mac_list = list( df_forescout.iloc[:,mac_pos])  #  原始資料中MAC address欄位的資料

      #  print( "len:", len(org_mac_list) )
      #  print( "data:", org_mac_list[0:10] )
      
    self.list_item_to_string( org_mac_list )

    #  print( type(org_mac_list[0]) )
    #  for i in range(len( org_mac_list )):
    #    org_mac_list[i] = str( org_mac_list[i] )

    pos_list = []  #  存放 mac_list 中的資料在原版資料中的位置資訊
    
    for index, element in enumerate( org_mac_list ):
      if element in list_mac:
        pos_list.append(index)

    #  print( "len:", len(pos_list) )
    #  print( pos_list[0:10] )

    i = 0
    for pos in pos_list:
      df_forescout.iloc[ pos, common_pos ] = list_names[i]  #  將已知的MAC的廠商資料回填至 comment 欄位
      i += 1

    df_forescout.to_csv("output2.csv",index=False)
    return True

  def output_mac_list_with_names(self,_macList:list,_macNames:list):
    # print(_macList)
    # print(_macNames)
    df = pd.DataFrame({ "MAC":_macList,"Names":_macNames})
    # print(df)
    df.to_csv("mac_list_result.csv", index=None, encoding="utf-8")
