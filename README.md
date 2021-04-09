# pynar_gui_designer


## Taslak çalışma

![image](https://user-images.githubusercontent.com/854154/114240448-2fba2200-9990-11eb-8abf-cafc97715dad.png)

## Ne yapılacak?

Yukarıdaki pencereye bir Toolbar eklenecek. Toolbar üzerinde bir "Kod üret" butonu olacak. Bu butona tıklayınca ekranda (Örneğin)  3 label 3 Entry 2 buton var ise şu şekilde onların konumları ile birlikte aşağıdaki gibi bir Tkinter kodu üretecek.

  
  from tkinter import *  

  top = Tk()  

  top.geometry("400x250")  

  name = Label(top, text = "Name").place(x = 30,y = 50)  

  email = Label(top, text = "Email").place(x = 30, y = 90)  

  password = Label(top, text = "Password").place(x = 30, y = 130)  

  sbmitbtn = Button(top, text = "Submit",activebackground = "pink", activeforeground = "blue").place(x = 30, y = 170)  

  e1 = Entry(top).place(x = 80, y = 50)  


  e2 = Entry(top).place(x = 80, y = 90)  


  e3 = Entry(top).place(x = 95, y = 130)  

  top.mainloop()  
  
 Kaynak: https://www.javatpoint.com/python-tkinter-entry
 


