import requests
import threading
import time
import queue as Queue
 
# url列表，这里是虚构的,现实情况这个列表里有大量的url
link_list = ['http://localhost:7777/Fight.aspx',]
test_url = 'http://localhost:7777/Fight.aspx'


start = time.time()
 
class myThread(threading.Thread):
    def __init__(self,name,q):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q
    def run(self):
        print("Starting " + self.name)
        while True:
            try:
                crawler(self.name,self.q)
            except:
                break
        print("Exiting " + self.name)
 
def crawler(threadName,q):
    # 从队列里获取url
    url = q.get(timeout=2)
    try:
        r = requests.get(url,timeout = 20)
        # 打印：队列长度，线程名，响应吗，正在访问的url
        print(q.qsize(),threadName,r.status_code,url)
    except Exception as e:
        print(q.qsize(),threadName,"Error: ",e)
 
# 创建5个线程名
threadList = ["Thread-1","Thread-2","Thread-3","Thread-4","Thread-5","Thread-6","Thread-7","Thread-8"]
 
# 设置队列长度
workQueue = Queue.Queue(300)
#将url填充到队列
for url in link_list:
    workQueue.put(url)


# 线程池
threads = []
 
#创建新线程
for tName in threadList:
    thread = myThread(tName,workQueue)
    thread.start()
    threads.append(thread)
 

 
for x in range(1,1000):
    workQueue.put(test_url)
    pass

#等待所有线程完成
for t in threads:
    t.join()
 
end = time.time()
print('Queue多线程爬虫总时间为：',end-start)
print('Exiting Main Thread')