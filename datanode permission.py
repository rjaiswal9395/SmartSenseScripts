import csv
import re
import datetime
import subprocess
from datetime import *
from datetime import timedelta


class tcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def reader(filepath):
    print(tcolors.HEADER+filepath+" opened for processing\n")
    return open(filepath,"r")

def keyword_extractor(text_found,color,filevariable):
  jvm_writer = csv.writer(open('jvm_gc.csv', 'w'))
  filevariable.seek(0);
  for line in reversed(list(filevariable)):  # file is being read in reverse to obtain the recent date and time entry
    match = re.search(r'(^\d{4}-\d{2}-\d{2} [0-2][0-3]:[0-5][0-9]:[0-5][0-9])',line)  # searching for date and time in every line
    if match:
      endTime= datetime.strptime(match.group(), '%Y-%m-%d %H:%M:%S')

      break
  endTime=endTime
  count=0
  startTime = endTime - timedelta(days=1)
   # most recent date and time entry
  filevariable.seek(0);
  Startup_Messages=[]
  Errors=[]
  Dir=[]

  for line in reversed(list(filevariable)):
    str_list = ("".join(line))

    if "STARTUP_MSG:" in str_list:
      Startup_Messages.append(str_list)
      match = re.search(r'(^\d{4}-\d{2}-\d{2} [0-2][0-3]:[0-5][0-9]:[0-5][0-9])', str_list)  # searching for date and time in every line
      if match:
        currentTime = datetime.strptime(match.group(), '%Y-%m-%d %H:%M:%S')
        break
  filevariable.seek(0);
  for line in reversed(list(filevariable)):
    str_list = ("".join(line))
    if text_found in str_list:
      match = re.search(r'(^\d{4}-\d{2}-\d{2} [0-2][0-3]:[0-5][0-9]:[0-5][0-9])',str_list)  # searching for date and time in every line
      if match:
        currentTime = datetime.strptime(match.group(), '%Y-%m-%d %H:%M:%S')
        Errors.append(str_list)
        Dir.append((str_list.split("/",1)[1]).split(" ",1)[0])
        count=count+1
        if (currentTime < startTime or currentTime > endTime):
          break



  print(tcolors.BOLD + "Total ", count, " Instances Found\n")
  #
  # for line in Startup_Messages:
  #   print(tcolors.OKGREEN+line)
  # for line in Errors:
  #   print(tcolors.FAIL+line)
  # for line in Dir:
  #   print(tcolors.FAIL+"/"+line)
  return Startup_Messages,Errors,count,Dir

def date_timestamp_extractor(input_string):
    match_date = re.search(r'\d{4}-\d{2}-\d{2}', input_string)
    match_time = re.search(r'(?:[01]\d|2[0123]):(?:[012345]\d):(?:[012345]\d)', input_string)
    if match_date and match_time is not None:
        return datetime.datetime.strptime(match_date.group(), '%Y-%m-%d').date(),datetime.datetime.strptime(match_time.group(), '%H:%M:%S').time()
    else:
      return 0,0

def parser(file):
    startup_msg,errors,count,dir=keyword_extractor("Invalid dfs.datanode.data.dir",tcolors.WARNING,file)
    printer(startup_msg,errors,count,dir)

def printer(startup_msg,errors,count,dir):
    if (startup_msg is not None):
      print (tcolors.OKGREEN+"#### LATEST STARTUP MESSAGES ####\n")
      for line in reversed(startup_msg):
        print(tcolors.OKGREEN + line)
    if(errors is not None):
      print(tcolors.FAIL+"#####  DIRECTORIES BELOW SEEMS TO HAVE ACCESS PROBLEMS#####\nCHECK THE FOLLOWING\n1.PERMISSION\n2.OWNERSHIP\n")
      if (dir is not None):
        for line in dir:
          print(tcolors.FAIL +"/" +line)
          print(subprocess.call(["ls", "-ld","/"+line]),"\n")
      else:
          print("ERROR OCCURED BUT DIRECTORY COULD NOT BE FOUND")
    else:
      print(tcolors.OKGREEN+"NO INVALID DIRECTORY ERROR")



def main():
    path="hadoop-hdfs-datanode-hbs1.hwxblr.com.log"
    opened_file=reader(path)
    parser(opened_file)
main()
