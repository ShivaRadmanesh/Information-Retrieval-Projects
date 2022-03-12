from time import sleep, time

import threading
import queue
import logging
import csv

from selenium import webdriver
# from selenium.webdriver.firefox.options import Options

data = queue.Queue()
data_results = queue.Queue()
done = 0
queue_timeout = 2.5

fileHandler = logging.FileHandler(f"log/logs-{int(time())}.txt",encoding="utf-8")
streamHandler = logging.StreamHandler()
logging.basicConfig(
  format='[%(process)d] - {%(levelname)s} // %(message)s',
  level=logging.DEBUG,
  handlers=[
    fileHandler,
    streamHandler,
  ],
)

def db_thread(threads_num, fileName):
  global done
  logger = logging.getLogger(threading.current_thread().name)
  logger.info("DBThread Started")

  i = 0
  print(data)
  with open(f"output/{fileName}.csv", "w", encoding='utf-8') as outfile:
    writer = csv.writer(outfile,)
    writer.writerow(['id','pos','gloss','persian_gloss','checked'])
    # outfile.write("id,pos,gloss,persian_gloss,checked\n")
    logger.info("Added CSV Headers")
    while not data.empty() or not data_results.empty() or done < threads_num:
      if not data_results.empty():
        item = data_results.get(block=True,timeout=queue_timeout)
        q = [item[0],item[1],item[2],item[3],0]
        # outfile.write(q)
        writer.writerow(q)
        logger.info(f"New Row Added {i}")
        i += 1

  logger.info("DB Thread Finished:")


def main_thread():
  global done
  logger = logging.getLogger(threading.current_thread().name)

  logger.info(f"{threading.current_thread().name} started")
  options = webdriver.FirefoxOptions()
  # options.headless = True
  driver = webdriver.Firefox(options=options)
  
  driver.get("https://translate.google.com/?sl=en&tl=fa&text=IT%20IS%20A%20TEST&op=translate")
  ta = driver.find_element_by_xpath("""//*[@class="er8xn"]""")

  i = 0
  start = time()
  try:
    while not data.empty() :
      sleep(0.5)
      result = data.get(block=True,timeout=queue_timeout)
      logger.info(f"{threading.current_thread().name}: new datum {result[0]}")
      if not result:
        logger.info("NO MORE QUERY RESULT")
        break
      logger.info(result)
      ta.clear()
      ta.send_keys(result[2])
      sleep(len(result[2])/30 + 1)
      res_elem = driver.find_elements_by_xpath("""//*[@class="J0lOec"]/span[@class="VIiyi"]/span/span""")
      translated = ""
      for el in res_elem:
        translated += el.get_attribute('innerText')
      i += 1
      logger.info(f"{threading.current_thread().name}: {result[0]} & {i} & {result[2]} >>> {translated}")
      result = [result[0],result[1],result[2], translated]
      data_results.put(result)
      logger.info(f"{threading.current_thread().name} {result[0]} COMPLETED")
      
  except Exception as e:
    logger.error(e)
  finally:
    done += 1
    logger.info(f"finished translating Thread: {threading.current_thread().name}")
    
  totaltime = time() - start
  logger.info(f"{threading.current_thread().name}: Total Time: {totaltime}")

if __name__ == "__main__":
  fileName = input("file number: ")
  
  with open(f"csv/{fileName}.csv", "r") as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
      data.put(row)
  # data.put([0,'pos',"Joan likes eggs; Jennifer does not.Joan likes eggs;"])
  threads_num = 5
  threads = []
  dbt = threading.Thread(target=db_thread, args=(threads_num,fileName),name="DBThread")
  for i in range(threads_num):
    threads.append(threading.Thread(target=main_thread, name=f"Thread#{i}"))

  dbt.start()
  sleep(1)
  for t in threads:
    print("IN FOR")
    t.start()
    sleep(0.5)
  
  for t in threads:
    t.join()
  dbt.join()
