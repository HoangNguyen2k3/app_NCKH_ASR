import os
file_name = "Quanlyvanban.txt"
current_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_dir, file_name)
def save(line):
    try:
        f=open(path,'a',encoding='utf8')
        f.writelines(line)
        f.writelines('\n')
        f.close()
    except:
        pass
def read():
    arr_vanban=[]
    try:
        f=open(path,'r',encoding='utf8')
        for i in f:
            data=i.strip()
            arr_vanban.append(data)
        f.close()
    except:
        pass
    return arr_vanban
if not os.path.exists(path):
    try:
        with open(path, 'w', encoding='utf8'):
            pass
    except Exception as e:
        print("Error:", e)
