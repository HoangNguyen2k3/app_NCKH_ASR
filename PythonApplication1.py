from ast import Lambda
from asyncio.windows_events import NULL
from cProfile import label
from ctypes import sizeof
from curses.ascii import isdigit
from logging import raiseExceptions
from msilib.schema import Icon
from textwrap import wrap
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from Database import *
import tkinter
import pyttsx3
import speech_recognition as sr
from pydub import AudioSegment
import time
from PIL import Image, ImageFilter, ImageTk


root=Tk()
robot_mount=pyttsx3.init()
voices = robot_mount.getProperty('voices')
robot_mount.setProperty('voice',voices[1].id)
arr_vanban=read()


def Thoat():
    robot_mount.say("Bạn có chắc chắn muốn thoát chương trình hay không")
    robot_mount.runAndWait()
    result=messagebox.askokcancel("Thông báo","Bạn có chắc chắn muốn thoát chương trình")    
    if(result):
          root.destroy()
def NhanDienAmThanh():
    robot_ear=sr.Recognizer()
    robot_mount.say("Xin chào, tôi có thể giúp gì cho bạn")
    robot_mount.runAndWait()
    
    while True: 
        bat_dau_nghe=time.time()
        with sr.Microphone() as mic:#sử dụng xong thì giải phóng bộ nhớ , mic
            print("Robot: I'm Listening ...") 
            audio=robot_ear.listen(mic) 
            print("Robot:...")
        thoi_gian_da_nghe=time.time()-bat_dau_nghe
        if(thoi_gian_da_nghe>10):
             robot_mount.say("Tôi không nghe rõ làm ơn nói lại")
             robot_mount.runAndWait()
             return    
        try:    
            you=robot_ear.recognize_google(audio,language='vi-VN')
        except:
            you="I can't hear that"  
        you=you.lower()
        if "hello" in you or "xin chào" in you:
            robot_brain="Xin chào a d min Hoàng Nguyễn"
        elif "thêm văn bản" in you:
            Them()
            root.update()
            robot_brain="đã thêm thành công"
        elif "mở file âm thanh" in you:
            Mofileamthanh()
            robot_brain="Đã mở file âm thanh thành công"
        elif "tìm kiếm văn bản" in you:           
            TimKiem()
            root.update()
            robot_brain="Tìm kiếm thành công"
        elif "chỉnh sửa văn bản" in you:
            ChinhSuaVanBan()
            root.update()
            robot_brain="Chỉnh sửa thành công"
        elif "xóa văn bản" in you:
            XoaVanBan()
            root.update()
            robot_brain="Xóa văn bản thành công"
        elif "thống kê dữ liệu văn bản" in you:
            robot_mount.say(f"Có {len(arr_vanban) } đoạn văn trong cơ sở dữ liệu")
            robot_mount.runAndWait()
            HienThi()
            robot_brain="Đã thống kê thành công"
        elif you in "goodbye" or you in "tạm biệt":
            robot_mount.say("Tạm biệt a d min Hoàng Nguyễn")
            robot_mount.runAndWait()
            break
        else:
            robot_brain="Tôi không nghe rõ làm ơn nói lại"       
        robot_mount.say(robot_brain)
        robot_mount.runAndWait()
        robot_brain=None  
def Mofileamthanh():
     file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3;*.wav")])
     if(file_path):
       try:
        # Chuyển đổi file âm thanh sang định dạng WAV
        sound = AudioSegment.from_file(file_path)
        sound.export("temp.wav", format="wav")

        # Sử dụng SpeechRecognition để nhận diện văn bản từ file âm thanh
        recognizer = sr.Recognizer()
        with sr.AudioFile("temp.wav") as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="vi-VN")

        # Hiển thị văn bản từng chữ từ từ
        textbox=Text(root,width=80,height=20)
        textbox.grid(row=5,columnspan=2)
        textbox.delete("1.0",END)
        arr=text.split(" ")
        for element in arr:
            textbox.insert(END,element+" ")          
            root.update()           
            root.after(100)
        robot_mount.say(text)
        robot_mount.runAndWait()
        #text_combined = ''.join(text)
        #listbox.insert(END, text_combined)
        
        #button_1 = Button(textbox, text="Thoát",command=textbox.destroy())       
        #button_1.pack(side=tkinter.RIGHT, padx=10, pady=10) 
        time.sleep(0.5)
        textbox.destroy()       
       except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
def Tim_Kiem_Nhi_Phan(chuoi, cum_tu):
    left, right = 0, len(chuoi) - len(cum_tu)
    
    while left <= right:
        mid = (left + right) // 2
        
        # Kiểm tra xem chuỗi ở vị trí mid có bắt đầu bằng cum_tu hay không
        if chuoi[mid:mid+len(cum_tu)] == cum_tu:
            return mid
        # Nếu chuỗi ở vị trí mid nhỏ hơn cum_tu, tìm kiếm ở nửa bên phải
        elif chuoi[mid:mid+len(cum_tu)] < cum_tu:
            left = mid + 1
        # Ngược lại, tìm kiếm ở nửa bên trái
        else:
            right = mid - 1
    
    # Trả về -1 nếu không tìm thấy
    return -1
def TimKiem():
     ask=messagebox.askyesnocancel("Thông báo","Tìm kiếm qua giọng nói (yes) và Tìm kiếm qua nhập văn bản(no)")
     if ask==YES :
         robot_mount.say("Vui lòng nhập từ hoặc văn bản bạn cần tìm kiếm")
         robot_mount.runAndWait()
         bat_dau_nghe=time.time()
         recognizer = sr.Recognizer()
         with sr.Microphone() as mic:
                #listbox.insert(END,"Robot: I'm Listening ...") 
                print("Robot: I'm Listening for your searching...")   
                audio_data = recognizer.listen(mic)
         thoi_gian_da_nghe=time.time()-bat_dau_nghe
         if(thoi_gian_da_nghe>10):
             robot_mount.say("Tôi không nghe rõ vui lòng tìm kiếm lại")
             robot_mount.runAndWait()
             return
         try:
            text = recognizer.recognize_google(audio_data, language="vi-VN")
         except:
            robot_mount.say("Tôi không nghe rõ")
            robot_mount.runAndWait()
            return
         #listbox.insert(END,"Từ cần tìm: "+text)
         print("Từ cần tìm: "+text)
         robot_mount.say("Bạn muốn tìm kiếm từ "+text)
         robot_mount.runAndWait()
         i=0
         """ for index, element in enumerate(arrr):
            if(TimKiemNhiPhan(element[0],text)!=-1):
                 listbox.insert(END, element[0])
                 i=i+1"""
         listbox.delete(0, END)     
         for index,element in enumerate(arr_vanban):
             if TimKiemThongThuong(element,text):
              #if(Tim_Kiem_Nhi_Phan(element,text)!=-1):
               listbox.insert(END, element)
               i=i+1
         if(i==0):
             robot_mount.say("Tôi không tìm thấy từ đó trong cơ sở dữ liệu")
             robot_mount.runAndWait()
             listbox.insert(END,"Không tìm thấy đoạn văn nào trong cơ sở dữ liệu chứ từ bạn cần tìm")
         else:
             robot_mount.say(f"Tôi tìm thấy '{i}' đoạn văn chứa từ đó trong cơ sở dữ liệu")
             robot_mount.runAndWait()
             listbox.insert(END,f"--Đã tìm được {i} đoạn văn chứa từ hoặc cụm từ bạn cần tìm: {text}--")
         #num=len(result)
         #print(num)
         #for index in result:
              # Kiểm tra xem chuỗi text có nằm trong phần tử item không
                 # Thêm phần tử item vào Listbox tìm lỗi sai
     elif ask==NO:       
         #robot_mount.say("Vui lòng nhập từ hoặc văn bản bạn cần tìm kiếm")
         #robot_mount.runAndWait()
         text=simpledialog.askstring("Nhập dữ liệu","Vui lòng nhập từ cần tìm kiếm")        
         if(text is not None and text !=''):
             i=0
             listbox.delete(0, END)     
             for index,element in enumerate(arr_vanban):
                 if TimKiemThongThuong(element,text):
                 #if(Tim_Kiem_Nhi_Phan(element,text)!=-1):
                   listbox.insert(END, element)
                   i=i+1
             if(i==0):
                 robot_mount.say("Tôi không tìm thấy từ này trong cơ sở dữ liệu")
                 robot_mount.runAndWait()
                 listbox.insert(END,"Không tìm thấy đoạn văn nào trong cơ sở dữ liệu chứ từ bạn cần tìm")
             else:
                 robot_mount.say(f"Tôi tìm thấy '{i}' đoạn văn chứa từ đó trong cơ sở dữ liệu")
                 robot_mount.runAndWait()
                 listbox.insert(END,f"--Đã tìm được {i} từ chứa từ bạn cần tìm {text}--")
         else:
             messagebox.showinfo("Thông báo","Người dùng đã hủy hoặc không nhập dữ liệu")       
def TimKiemThongThuong(arr, x):
    if x.lower() in arr.lower():
          return True
    return False    
def Them():
    result=messagebox.askquestion("Thông báo","Bạn có muốn thêm 1 văn bản đã có (yes) hay thêm 1 văn bản mới (no) ?")
    if(result=='yes'):
        file_path_sound = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3;*.wav;*txt"),("Text files", "*.txt")])
        if(file_path_sound):
            if(file_path_sound.endswith(('.mp3', '.wav'))):
               try:
                # Chuyển đổi file âm thanh sang định dạng WAV
                sound = AudioSegment.from_file(file_path_sound)
                sound.export("temp.wav", format="wav")
                # Sử dụng SpeechRecognition để nhận diện văn bản từ file âm thanh
                recognizer = sr.Recognizer()
                with sr.AudioFile("temp.wav") as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language="vi-VN")
               except Exception as e:
                    messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
               for element in arr_vanban:
                   if text == element :
                       messagebox.showinfo("Thông báo","Đã tồn tại văn bản")
                       return
               arr_vanban.append(text)
               save(text)
               messagebox.showinfo("Announcement","Add successfull")          
               Label(root,text=f"Có tổng cộng {len(arr_vanban)} đoạn văn bản trong cơ sở dữ liệu").grid(row=4)
               HienThi() 
               return 
            elif(file_path_sound.endswith(('.txt'))):
                try:
                    # Mở tệp và đọc nội dung
                    with open(file_path_sound, 'r', encoding='utf-8') as file:
                        content = file.read().strip()
                        
                        for element in arr_vanban:
                           if element == content :
                               messagebox.showinfo("Thong bao","Da ton tai van ban")
                               return  
                        
                        arr_vanban.append(content)
                        save(content)
                        messagebox.showinfo("Announcement","Add successfull")          
                        Label(root,text=f"Có tổng cộng {len(arr_vanban)} đoạn văn bản trong cơ sở dữ liệu").grid(row=4)
                        HienThi() 
                        return
                except Exception as e:
                    print("Đã xảy ra lỗi khi mở hoặc đọc tệp:", e)
            else:
                messagebox.showinfo("Thông báo","Định dạng file không hợp lệ")
    else:
        window1 = tkinter.Tk()
        window1.geometry(f"{app_width}x{app_height}+{x}+{y}") 
        window1.title("Ứng dụng quản lý văn bản")
        text_editor = tkinter.Text(window1)
        text_editor.pack(fill=tkinter.BOTH, expand=True)        
        add_button = tkinter.Button(window1, text="Thêm văn bản",command=lambda: ThemDuLieu(text_editor,window1))       
        add_button.pack(side=tkinter.RIGHT, padx=10, pady=10)
        window1.mainloop()               
def ThemDuLieu(text_editor,window1):
    
    text = text_editor.get(1.0, tkinter.END).strip()  # Lấy văn bản từ trình soạn thảo và loại bỏ dấu cách thừa
    if text: # Kiểm tra xem văn bản có dữ liệu không
        for element in arr_vanban:
               if element == text :
                   messagebox.showinfo("Thong bao","Da ton tai van ban")
                   return  
        #for ky_tu in text:
            #if not (ky_tu.isdigit() and ky_tu.isalpha()):
                #messagebox.showinfo("Thông báo","Vui lòng chỉ nhập kí tự ")
                #return
        arr_vanban.append(text)  # Thêm văn bản vào mảng
        save(text)
        messagebox.showinfo("Thông báo", "Thêm văn bản mới thành công")
        Label(root,text=f"Có tổng cộng {len(arr_vanban)} đoạn văn bản trong cơ sở dữ liệu").grid(row=4)
        window1.destroy()
    else:
        messagebox.showinfo("Cảnh báo", "Vui lòng nhập dữ liệu trước khi thêm!")
    HienThi()
def HienThi():
    listbox.delete(0,END)
    arr_vanban.sort()
    for index,element in enumerate(arr_vanban):
        listbox.insert(END,element+"\n")
        root.update()
        root.after(100)    
def XoaVanBan():
    if(listbox.size()<len(arr_vanban)):
        HienThi()
        robot_mount.say("Đã hiển thị danh sách văn bản vui lòng chọn một văn bản cần xóa")
        robot_mount.runAndWait()
    else:
        selected_index=listbox.curselection() 
        if(selected_index):
            for index in selected_index[::-1]:  # Lặp qua các chỉ mục từ cuối lên đầu
                listbox.delete(index)
                arr_vanban.pop(index)
            f=open(path,'w',encoding='utf8')
            for element in arr_vanban:
                f.writelines(element)
                f.writelines('\n')
            f.close()
            messagebox.showinfo("Thông báo","Xóa đoạn văn thành công")
            Label(root,text=f"Có tổng cộng {len(arr_vanban)} đoạn văn bản trong cơ sở dữ liệu").grid(row=4)
            
        else:
            messagebox.showinfo("Thông báo","vui lòng chọn một văn bản cần xóa")
def ChinhSuaVanBan():
    #listbox.delete(0,END)
    if(listbox.size()<len(arr_vanban)):
        HienThi()
        robot_mount.say("Đã hiển thị danh sách văn bản vui lòng chọn một văn bản cần chỉnh sửa")
        robot_mount.runAndWait()
    else:       
        selected_index=listbox.curselection()
        if selected_index:
            text_selected=listbox.get(selected_index)
            new_text=simpledialog.askstring("Nhập dữ liệu","Chỉnh sửa văn bản mới:",initialvalue=text_selected)
            if(new_text):      
                for index in selected_index[::-1]:  # Lặp qua các chỉ mục từ cuối lên đầu
                    listbox.delete(index)
                    arr_vanban.pop(index)
                    listbox.insert(index,new_text)
                arr_vanban.append(new_text)
                #arr_vanban.sort()
                f=open(path,'w',encoding='utf8')
                for element in arr_vanban:
                    f.writelines(element)
                    f.writelines('\n')
                f.close()
                messagebox.showinfo("Thông báo","Chỉnh sửa đoạn văn thành công")                
        else:
            messagebox.showinfo("Thông báo","Vui lòng chọn 1 văn bản để chỉnh sửa")
    
            

#goi cua so
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
app_width = 600
app_height = 600
x = (screen_width - app_width) // 2
y = (screen_height - app_height) // 2

# Đặt kích thước và vị trí cho cửa sổ
root.geometry(f"{app_width}x{app_height}+{x}+{y}") 
root.title('QUẢN LÝ VĂN BẢN')
root.minsize(height=650,width=600)
Label(root,text="Ứng dụng quản lý văn bản",fg='red',font=('cambria',22),width=30).grid(row=0)
Label(root).grid(row=1)
Label(root).grid(row=2)
Button(root,text='NHAN DIEN AM THANH',width=20,height=4,fg='blue',command=NhanDienAmThanh,bg='#FFCDD2').grid(row=3)
label_numvb=Label(root,text=f"Có tổng cộng {len(arr_vanban)} đoạn văn bản trong cơ sở dữ liệu").grid(row=4)
listbox=Listbox(root,width=100,height=20,bg='#ADD8E6')
listbox.grid(row=5,columnspan=2)
button=Frame(root)
Button(button,text='Thêm',width=10,height=2,command=Them,bg='#E0E0E0').pack(side=LEFT)
Label(button, width=3).pack(side=LEFT)
Button(button,text='Chỉnh sửa',width=10,height=2,command=ChinhSuaVanBan,bg='#E0E0E0').pack(side=LEFT)
Label(button, width=3).pack(side=LEFT)
Button(button,text='Xóa văn bản',width=10,height=2,command=XoaVanBan,bg='#E0E0E0').pack(side=LEFT)
Label(button, width=3).pack(side=LEFT)
Button(button,text='Hiển thị',width=10,height=2,command=HienThi,bg='#E0E0E0').pack(side=LEFT)
Label(button, width=3).pack(side=LEFT)
button_1=Frame(root)
Button(button_1,text='Tìm kiếm',width=10,height=2,command=TimKiem,bg='#E0E0E0').pack(side=LEFT)
Label(button_1, width=3).pack(side=LEFT)
Button(button_1,text='Mở file âm thanh',width=15,height=2,command=Mofileamthanh,bg='#E0E0E0').pack(side=LEFT)
Label(button_1, width=3).pack(side=LEFT)
Button(button_1,text='Thoát',width=10,height=2,command=Thoat,bg='#E0E0E0').pack(side=LEFT)
Label(button_1, width=3).pack(side=LEFT)
Label(root).grid(row=6)
button.grid(row=7)
Label(root).grid(row=8)
button_1.grid(row=9)
root.mainloop()

