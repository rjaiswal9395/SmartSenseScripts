import csv
error_file = open("error_sheet.csv")
error_file = csv.reader(error_file)
company_names = open("company_names.csv")
company_names = csv.reader(company_names)
company_list = list(company_names)
flag=1
bug_list=[]
summary=[]
namelist=[]
mydict={'key':'value'}

for rows in error_file:
    k = rows[1]
    k = k.lower()
    k = k + " "
    summary.append(rows[1])
    bug_list.append(rows[0])
    f=1
    for element in company_list:
        list = str(element)
        name = list.replace("['", "")
        name = name.replace("']", "")
        name = name.lower()
        if name in k:
            x=int(k.index(name)) + len(name)
            y=int(k.index(name)) -1
            if k[x].isalpha() or k[y].isalpha():
                v='Not Found'
                namelist.append('Not Found')
            else:
                namelist.append(name)
                v = name
            mydict[k]=v
            flag=0
            break
    if flag==1:
        mydict[k] = 'Not Found'
        namelist.append('Not Found')

writer = csv.writer(open('final.csv', 'wb'))
for element1,element2,element3 in zip(bug_list,summary,namelist):
   writer.writerow([element1, element2, element3])