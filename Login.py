from tkinter import messagebox
from PythonApplication1 import root
import tkinter as tk
from tkinter import *
import sys
from tkinter import ttk
from Data_Login import *


# Tạo cửa sổ đăng nhập
login_window = tk.Tk()
login_window.title("Đăng nhập")
login_window.minsize(150,150)
def DangKy():
    def register():
        username = entry_username.get()
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()
        #role = combo_role.get()

        if not (username and password and confirm_password):
            messagebox.showerror("Error", "Vui lòng điền đầy đủ thông tin.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Mật khẩu không khớp.")
            return

        # Xử lý việc lưu thông tin tài khoản ở đây
        
        account_list=read_account_info()
        if(account_list):
            for account,info in account_list.items():
                if(account==username):
                    messagebox.showinfo("Thông báo","Đã tồn tại tên tài khoản vui lòng nhập tên khác!")
                    return
        messagebox.showinfo("Thông báo","Đăng ký thành công!")
        save_account_info(username+"-"+password+"-"+"nhân viên")
    def Thoat():
        root_1.destroy()
    root_1 = tk.Tk()
    root_1.title("Đăng ký tài khoản")

    # Tạo các thành phần trong form đăng ký
    label_username = tk.Label(root_1, text="Tên đăng nhập:")
    label_username.grid(row=0, column=0, padx=10, pady=5)
    entry_username = tk.Entry(root_1)
    entry_username.grid(row=0, column=1, padx=10, pady=5)

    label_password = tk.Label(root_1, text="Mật khẩu:")
    label_password.grid(row=1, column=0, padx=10, pady=5)
    entry_password = tk.Entry(root_1, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=5)

    label_confirm_password = tk.Label(root_1, text="Nhập lại mật khẩu:")
    label_confirm_password.grid(row=2, column=0, padx=10, pady=5)
    entry_confirm_password = tk.Entry(root_1, show="*")
    entry_confirm_password.grid(row=2, column=1, padx=10, pady=5)
    """label_role = tk.Label(root_1, text="Chức vụ:")
    label_role.grid(row=3, column=0, padx=10, pady=5)
    combo_role = ttk.Combobox(root_1, values=["Nhân viên", "Admin"])
    combo_role.grid(row=3, column=1, padx=10, pady=5)
    combo_role.current(0) """
    button_register = tk.Button(root_1, text="Đăng ký", command=register)
    button_register.grid(row=4, column=0,columnspan=2, padx=10, pady=5)
    button_register = tk.Button(root_1, text="Thoát",command=Thoat)
    button_register.grid(row=4,column=1, columnspan=2, padx=10, pady=5)
    
def check_login(username, password):
    account_list=read_account_info()  
    for account,info in account_list.items():           
        if username == account and password == info['password']:
            return True
        else:
            return False
def Thoat_Login():
    kq=messagebox.askokcancel("Thông báo","Bạn có chắc chắn muốn thoát chương trình")    
    if(kq):
        #login_window.destroy()
        sys.exit()
def login():
    username = entry_username.get()
    password = entry_password.get()
    if check_login(username, password):
        login_window.withdraw()
        root.deiconify()  # Hiển thị cửa sổ root
    else:
        messagebox.showerror("Lỗi", "Tên người dùng hoặc mật khẩu không đúng!")


# Tạo các thành phần trong cửa sổ đăng nhập
label_username = tk.Label(login_window, text="Tên đăng nhập:")
label_username.grid(row=0, column=0, padx=10, pady=5)
entry_username = tk.Entry(login_window)
entry_username.grid(row=0, column=1, padx=10, pady=5)

label_password = tk.Label(login_window, text="Mật khẩu:")
label_password.grid(row=1, column=0, padx=10, pady=5)
entry_password = tk.Entry(login_window, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=5)
Label(root).grid(row=3)
button_login=Frame(login_window)

tk.Button(button_login, text="Đăng nhập",width=10,height=2, command=login).pack(side=LEFT)
Label(button_login, width=3).pack(side=LEFT)
tk.Button(button_login, text="Đăng ký",width=10,height=2, command=DangKy).pack(side=LEFT)
Label(button_login, width=3).pack(side=LEFT)
tk.Button(button_login, text="Thoát",width=10,height=2, command=Thoat_Login).pack(side=LEFT)
button_login.grid(row=4)

# Ẩn cửa sổ root ban đầu
root.withdraw()
login_window.mainloop()
