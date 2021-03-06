#import urllib.request
#import numpy as np
import os
import _thread
import time
import requests
import multiprocessing
from numpy import interp
#import tkinter as tk
from timeit import default_timer as timer

import sys

# init all global var ...

try:
    neg_images_link = 'https://nolp.dhl.de/nextt-online-public/de/search?piececode='
    t1_job = t1_actual =0
    t2_job = t2_actual =0
    t3_job = t3_actual =0
    t4_job = t4_actual =0
    t5_job = t5_actual =0
    t6_job = t6_actual =0
    t7_job = t7_actual =0
    t8_job = t8_actual =0
    Total_Job =0
    fest_Job =0
    positive_result = 0


except Exception as e:
    print(str(e))

def ThreadSetupScalable(interval_ref):

    pic_num = 1

    if not os.path.exists('neg'):
        os.makedirs('neg')
    print("number of Core this Computer  is : "+str(multiprocessing.cpu_count()))
    time.sleep(3)
    # Berechnung Thread Job
    job = int(round(interval_ref)/8) # durch anzahl von Threads = 8
    print(job)

    try:
        _thread.start_new_thread( Thread_find_refInfos, ("Thread-1", 0, job) )
        _thread.start_new_thread( Thread_find_refInfos, ("Thread-2", job+1, job*2 ) )
        _thread.start_new_thread( Thread_find_refInfos, ("Thread-3", job*2 +1, job*3 ) )
        _thread.start_new_thread( Thread_find_refInfos, ("Thread-4", job*3 +1, job*4) )
        _thread.start_new_thread( Thread_find_refInfos, ("Thread-5", job*4 +1, job*5 ) )
        _thread.start_new_thread( Thread_find_refInfos, ("Thread-6", job*5 +1, job*6) )
        _thread.start_new_thread( Thread_find_refInfos, ("Thread-7", job*6 +1, job*7) )
        _thread.start_new_thread( Thread_find_refInfos, ("Thread-8", job*7 +1, job*8) )


    except:
        print ("Error: unable to start thread")

    while(1):
        pass


def ThreadDispatcher(from_ , to_):
    global Total_Job
    global fest_Job
    interval = 0
    CoreNumber = 0
    print(interval)
    CoreNumber = multiprocessing.cpu_count()
    if (CoreNumber < 1):
        print("this Script cannot be processed with multiprocessing Option ...")
        print("the programm will be abort .....")
        time.sleep(5)
        sys.exit()
    else:
        print("number of Core this Computer  is : "+str(multiprocessing.cpu_count()))

    if(from_ < to_ ):
        interval = to_ - from_
        Total_Job = interval
        fest_Job = interval
    else:
        print ("you must enter a correct value .....the interval that you entered is not correct !")
        ###  stop the programm ...
        print("the programm will be abort .....")
        time.sleep(5)
        sys.exit()

    pic_num = 1

    if not os.path.exists('neg'):
        os.makedirs('neg')
    time.sleep(3)
    # Berechnung Thread Job
    job = int(interval/8) # durch anzahl von Threads = 8
    print(job)

    try:

        _thread.start_new_thread( Thread_find_refInfos, ("Thread-1", from_, from_ + job) )
        _thread.start_new_thread( Thread_find_refInfos, ("Thread-2", from_+job + 1, from_ +job*2 +1 ) )
        _thread.start_new_thread( Thread_find_refInfos, ("Thread-3", from_ +job*2 +2, from_ +job*3 +2 ) )
        _thread.start_new_thread( Thread_find_refInfos, ("Thread-4", from_ +job*3 +4, from_ +job*4 +4) )
        _thread.start_new_thread( Thread_find_refInfos, ("Thread-5", from_ +job*4 +5, from_ +job*5 +5) )
        _thread.start_new_thread( Thread_find_refInfos, ("Thread-6", from_ +job*5 +6, from_ +job*6 +6) )
        _thread.start_new_thread( Thread_find_refInfos, ("Thread-7", from_ +job*6 +7, from_ +job*7 +7) )
        _thread.start_new_thread( Thread_find_refInfos, ("Thread-8", from_ +job*7 +8, from_ +job*8 +8) )

        ## special Thread  to refresh all Threads Informations of the console ....
        _thread.start_new_thread(Infos_console, ("Thread_InfosPrinter" , 10) )

    except Exception as e:
            print(str(e))

    while(1):
        pass


def Infos_console(count, suffix='' ):
    global  Total_Job , fest_Job
    print("Total Job is  :"+str(Total_Job))
    while(1):
        time.sleep(0.2)
        #bar_len = 60
        #filled_len = int(round(bar_len * Total_Job / float(fest_Job)))
        #percents = round(100.0 * Total_Job / float(fest_Job), 1)
        #bar = '=' * filled_len + '-' * (bar_len - filled_len)
        #sys.stdout.write("\r%d of %d" % (read, num_lines))
        if(Total_Job < 20):
            print("Total Job finished ....")
            break
        sys.stdout.write(""+"\rJob Progression : %f%% # Positive_Result = %d " % (interp(fest_Job-Total_Job,[1,fest_Job],[0,100]),positive_result))
        #sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
        sys.stdout.flush()

def fct(code):
    val = "000000000"
    b_code = bytearray(code)
    b_val = bytearray(val)
    strSize = len(b_code)
    for i in range(strSize):
        b_val[8 - i] = b_code[strSize - 1 - i]
    s = str(b_val)
    return ("RR" + s + "DE")

def ConcatPre(Value):
    return "RR" + str(Value) + "DE"


# define a function for the thread .
def Thread_find_refInfos(ThreadName , begin_ , to_ ):
    # create global variable ...
    global  Total_Job
    global  positive_result
    print("Start Thread " + ThreadName)
    #print(t1_job)
    #time.sleep(3)
    file_thread = open(ThreadName+"_Result.txt", "w")
    #pic_num = begin_
    start = timer()
    for  i in range(begin_ , to_):

        try:
            #print(ThreadName +" actually process  url : "+ConcatPre(i))
            r = requests.get("https://nolp.dhl.de/nextt-online-public/de/search?piececode=" + ConcatPre(i))
            paste_url = r.text
            key_1 = paste_url.find("Belgien")
            key_2 = paste_url.find("Zustellung erfolgreich")
            if key_1 != -1 and key_2 ==-1:
            #if key_1 != -1 and key_2 !=-1:
                print(ConcatPre(i) + "\n")
                file_thread.write(ConcatPre(i)+ "\n")
                positive_result = positive_result +1
            Total_Job = Total_Job -1
        except Exception as e:
            print(str(e))
    print(ThreadName+ " Job finished .")
    file_thread.close()
    end = timer()
    print(ThreadName+" needed " + str( end-start) + " Sek to make his job")
    #store_raw_images()
    #create_pos_n_neg()
    #file_thread.write(id + "\n")
ThreadDispatcher(611000000,612000000)
#progress(10, 100, "jui")
