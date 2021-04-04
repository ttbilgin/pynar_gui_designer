# pynar_gui_designer

## Resim sürükleyerek yapılan çalışma (kaydet yıklayınca json olarak pozisyonları üretir)

![image](https://user-images.githubusercontent.com/854154/113482847-210fce80-94a9-11eb-8008-e3f14f86f102.png)

## Gerçek gui objeler ile yapılan çalışma (buton gibi şeylerin üzerindeki yazının değişitirilebilmesi açısında daha avantajlı)

![image](https://user-images.githubusercontent.com/854154/113505248-430b5e80-9546-11eb-8d94-44fcf701bf18.png)


üretilmesi gereken Tkinter kodu:

  
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
 
 ## istediğim GUI design 
 
 ![image](https://user-images.githubusercontent.com/854154/113505596-7f3fbe80-9548-11eb-907d-217bbca4901e.png)

