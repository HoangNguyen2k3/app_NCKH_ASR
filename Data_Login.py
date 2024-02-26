import os
file_name = "Quanlytaikhoan.txt"
current_dir = os.path.dirname(os.path.abspath(__file__))
path1 = os.path.join(current_dir, file_name)
if not os.path.exists(path1):
    try:
        with open(path1, 'w', encoding='utf8'):
            pass
    except Exception as e:
        print("Error:", e)
def save_account_info(line):
    try:
        f=open(path1,'a',encoding='utf8')
        f.writelines(line)
        f.writelines('\n')
        f.close()
    except:
        pass
"""def read():
    arr_vanban=[]
    try:
        f=open(path,'r',encoding='utf8')
        for i in f:
            data=i.strip().split("-")            
            arr_vanban.append(data)
        f.close()
    except:
        pass
    return arr_vanban"""
def read_account_info():
    accounts = {} 
    with open(path1, 'r') as file:
        for line in file:
            account, password, status = line.strip().split("-")

            # Thêm thông tin vào từ điển
            accounts[account] = {
                'password': password,
                'status': status
            }

    return accounts
