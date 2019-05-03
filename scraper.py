import threading
import time
import requests
from bs4 import BeautifulSoup
import re
from importlib import reload
import sys


db = []

def scraper (list_index):
  global db
  for index in list_index:
    if index < 100:
      continue

    url = 'http://application.ditp.go.th/exporter/index/companydetail?catid=101&subid=102&id=' + str(index)
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    soup.decode("utf-8")
    content = soup.find_all('p')
    string = ''
    try:
      string = string + str(index) + '\t'
      for c in content:
        c_strip = c.get_text().strip()
        c_strip = c_strip.replace('\n', '')
        c_strip = c_strip.replace('\n', '')
        c_strip = c_strip.replace('\r', '')
        c_strip = c_strip.replace('\r\n', '')
        c_strip = c_strip.replace('\t', '')
        c_strip = c_strip.replace('	', '')
        c_strip = c_strip.replace('\
', '')

        string = string + c_strip + '\t'
      db.append(string)
    except:
      continue


def createThread():
    n = 20000
    n_thread = 20
    n_length = int(n/n_thread)


    f = [[] for i in range(int(n/n_thread))]

    thread_list = []

    for sub in range(n_thread):
      f = range((sub*n_length), ((sub+1)*(n_length)))

      t = threading.Thread(target=scraper, args=(f,))
      thread_list.append(t)
    
    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()
        
    
if __name__ == "__main__":

  createThread()
  fp = open('output.txt', 'w', encoding="utf-8")
  fp.write('id\tcontact_person\taddress\ttelephone\tfax\temail\twebsite\taddress\ttelephone\tfax\tregistered_capital\tyear_of_establishment\tproduct\n')

  for r in db:
    fp.write(r + '\n')
  
  fp.close()

  print( "Exiting Main Thread" )