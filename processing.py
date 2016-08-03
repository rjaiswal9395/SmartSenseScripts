import csv
import re
import datetime
import time
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

def war_error_checker(text_found,color,filevariable):
    writer = csv.writer(open('dict.csv', 'w'))
    set_variable=set()
    dictionary_variable={}
    filevariable.seek(0);
    for line in filevariable:
        str_list=("".join(line))
        str_list.lower()
        if text_found in str_list:
            index=str_list.index(text_found)
            str_list=str_list[index:]
            if (str_list in set_variable):

                incremented = dictionary_variable[str_list] + 1
                dictionary_variable[str_list] = incremented
            else:
                set_variable.add(str_list)
                dictionary_variable[str_list] = 1
    # print("\n"+color+ text_found+"\n")
    # for key, value in dictionary_variable.items():
    #     print(color + key, "\t", value)
        for key, value in dictionary_variable.items():
            writer.writerow([key, value])

def time_jvm_gc_checker(text_found,color,filevariable):
    jvm_writer = csv.writer(open('jvm_gc.csv', 'w'))
    filevariable.seek(0);
    jvm_writer.writerow({"Date","Time","Halt-Time"})
    for line in filevariable:
        str_list = ("".join(line))
        date,time =date_timestamp_extractor(str_list)


        if text_found in str_list:
            halt = str_list.rsplit(" ",1)[1]
            halt = "".join(halt)
            halt_time=int(re.search(r'\d+', halt).group())
            index = str_list.index(text_found)
            jvm_writer.writerow ({date,time,halt_time})
            str_list = str_list[index:]

            # if (str_list in set_variable):
            #
            #     incremented = dictionary_variable[str_list] + 1
            #     dictionary_variable[str_list] = incremented
            # else:
            #     set_variable.add(str_list)
            #     dictionary_variable[str_list] = 1
                # print("\n"+color+ text_found+"\n")
                # for key, value in dictionary_variable.items():
                #     print(color + key, "\t", value)
        # for key, value in dictionary_variable.items():
        #     writer.writerow([key, value])


def date_timestamp_extractor(input_string):
    match_date = re.search(r'\d{4}-\d{2}-\d{2}', input_string)
    match_time = re.search(r'(?:[01]\d|2[0123]):(?:[012345]\d):(?:[012345]\d)', input_string)
    if match_date and match_time is not None:
        return datetime.datetime.strptime(match_date.group(), '%Y-%m-%d').date(),datetime.datetime.strptime(match_time.group(), '%H:%M:%S').time()




def parser(file):

    time_jvm_gc_checker("JVM",tcolors.WARNING,file)

def main():
    path="hadoop-hdfs-datanode-sandbox.hortonworks.com.log"
    opened_file=reader(path)
    parser(opened_file)

main()
