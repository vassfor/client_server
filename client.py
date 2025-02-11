import socket
import threading
import tkinter
from tkinter import *

login=Tk()
login.configure(bg = "#2C3E50")
l1=Label(login,text="Choose a username: ", bg="#2C3E50",fg="#EAECEE")
l1.pack(side='top')
entry=Entry(login,bg="#17202A",fg = "#EAECEE")
entry.pack()

username=""
def usr_set():
    global username
    username=entry.get()
    login.destroy()

ok=Button(login,text='OK', command=usr_set,bg='orange',fg = "#EAECEE",relief="raised")
ok.pack(side='bottom')
login.mainloop()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9999))

def join():
    msg=f"JOIN {username}"
    snd(msg)
    update_clients()
    
def send_msg():
    txt.insert(END,"\n"+username+":"+e.get())
    msg="SEND MSG TO "+clicked.get()+" "+e.get()
    snd_thread = threading.Thread(target=snd,args=(msg,))
    snd_thread.start()

def leave():
    msg="LEAVE"
    snd(msg)
    root.destroy()

def recv():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message.startswith("CLIENTS CONNECTED:"):
               msg = message.split(":")
               cl=msg[1].split(",")
               clients=["ALL"]+cl
               drop['menu'].delete(0, 'end')
               for c in clients:
                   drop['menu'].add_command(label=c, command=lambda value=c: clicked.set(value))
               root.after(1000, update_clients)
            elif not message.startswith(username):
                txt.insert(END,"\n"+message)
                root.update_idletasks()
        except:
            print("An error occured!")
            client.close()
            break

def snd(msg):
    client.send(msg.encode("utf-8"))
    
def update_clients():
    snd("CLIENT LIST")


root = tkinter.Tk()
root.title('myCHAT')
root.geometry('760x460')
root.configure(bg = "#2C3E50") 

l1=Label(root,text='     T E X T     ', bg = "#17202A",fg = "#EAECEE")
l1.pack(side='top')

join_btn=Button(root,text="JOIN",command=join, bg = "#17202A",fg = "#EAECEE",relief="raised")
join_btn.place(x=710, y=20)

leave_btn=Button(root,text="LEAVE",command=leave, bg='orange',fg = "#EAECEE",relief="raised")
leave_btn.place(x=710, y=55)

txt=Text(root,bg = "#17202A",fg = "#EAECEE")
txt.pack(side='top',expand='yes')

e=Entry(root,bg="#17202A",fg = "#EAECEE")
e.pack(side='bottom',fill='both') 

options=["ALL"]
clicked = StringVar()
clicked.set( "ALL" )
drop = OptionMenu( root , clicked , *options)
drop.configure(bg = "#17202A",fg = "#EAECEE")
drop.pack(side='right')

send_btn=Button(root,text="SEND MSG TO",command=send_msg, bg = "#17202A",fg = "#EAECEE", relief="raised")
send_btn.pack(side='right') 

receive_thread = threading.Thread(target=recv)
receive_thread.start()

root.mainloop() 
