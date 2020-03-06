from tkinter import *
from tkinter import filedialog
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3
# aditya.baravkar@gmail.com
# global variables
c=0
z=1
name=""
xy=''

# functions
def file():

    file.filename = filedialog.askopenfilename(filetypes =(("All Files","*.*"),("PY files","*.py")))
    name2=file.filename
    global name
    name=name2.split('/')
    global xy
    xy=name[-1]
  
    global c
    c=1
    Label(root, text="File :\t" + name[-1], bg="#17202A", fg="#F7F9F9", font=("calibri", 10, 'italic'),padx=10,pady=10).place(x=150,y=420)

def attach():
        attach.fname = name[-1]
        attachment = open(file.filename, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + attach.fname)
        send_mail.newmsg.attach(part)


def retrieve_input():
    return t.get("1.0",'end-1c')

#batch1.vit.infta@gmail.com
def status_success():
    Label(text="Sent successfully",fg="#05B647",bg="#17202A",font="calibri 9 italic").place(y=550,x=200,width=150)

def status_failure():
    Label(text="Unable to send",fg="#C12105",bg="#17202A").place(y=550, x=200, width=150)

def status_login():
    Label(text="Invalid credentials",fg="#C12105",bg="#17202A",font="calibri 9 italic").place(y=550, x=200, width=150)

def no_reply():
    Label(text="No reply from server",fg="#C12105",bg="#17202A").place(y=550, x=200, width=150)

def error_occured():
    Label(text="Error Occured",fg="#C12105",bg="#17202A").place(y=550, x=200, width=150)

def send_mail():
    server_connect = False # To check variable
    # handling exception
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(e1.get(), e2.get())
        server_connect = True

    except smtplib.SMTPHeloError:
        # print("No reply from server")
        no_reply()
    except smtplib.SMTPAuthenticationError:
        # print("Invalid email-id or password")
        status_login()
    except smtplib.SMTPException:
        # print("Error occured")
        error_occured()
    # if no exception raised from previous try block
    if server_connect == True:
        try:
            send_mail.newmsg = MIMEMultipart()
            send_mail.newmsg['From']=e1.get()
            send_mail.newmsg['To']=e3.get()
            send_mail.newmsg['Subject']=e4.get()
            send_mail.msg = retrieve_input()
            send_mail.newmsg.attach(MIMEText(send_mail.msg,'plain'))
            global c
            if c==1:
                attach()
            text = send_mail.newmsg.as_string()
            s.sendmail(e1.get(), e3.get(), text)
            # print("Sent successfully")
            status_success()

            conn = sqlite3.connect('femail.db')
            c = conn.cursor()
            global z
            if z>0:
                 c.execute('''CREATE TABLE data_table
                         (Sender_emial text, Receiver_emial text, File_send text,Subject text, Message_send text)''')
                z=0
            l=[]
            global xy
            a1=e1.get()
            a2=e3.get()
            a3=t.get("1.0", 'end-1c')
            a4=xy
            a5=e4.get()
            l.append((a1,a2,a4,a5,a3))
            c.executemany('INSERT INTO data_table VALUES (?,?,?,?,?)', l)
            conn.commit()
            for row in c.execute('SELECT * FROM data_table'):
                print(row)
            conn.close()
        except smtplib.SMTPException:
            status_failure()
            # print("Unable to send")
    s.quit()

# root
root=Tk()
root.geometry('600x700')
root.minsize(600,650)
root.maxsize(600,700)
root.title("Q Mail")
root.configure(background="#17202A",borderwidth='5px',relief=GROOVE)
root.maxsize(650,700)

# label
Label(root,text="Quick Mail",font=("comic sans ms",18,"bold"),pady=20,borderwidth='2px',relief=GROOVE,width=20,fg="wheat",bg="#494949").grid(row=0,column=1)
Label(root,text="From : ",bg="#17202A",fg="#F7F9F9",font=("calibri",13,'italic'),padx=10,pady=10).grid(row=2)
Label(root,text="Password : ",bg="#17202A",fg="#F7F9F9",font=("calibri",13,'italic'),padx=10,pady=10).grid(row=3)
Label(root,text="To : ",bg="#17202A",fg="#F7F9F9",font=("calibri",13,'italic'),padx=10,pady=10).grid(row=4)
Label(root,text="Subject : ",bg="#17202A",fg="#F7F9F9",font=("calibri",13,'italic'),padx=10,pady=10).grid(row=5)
Label(root,text="Message : ",bg="#17202A",fg="#F7F9F9",font=("calibri",13,'italic'),padx=10,pady=10).grid(row=6)

# textboxes
e1 = Entry(root,width=35,bg="#DCDCDC",fg="#1C2833",font="calibri 10 italic bold")
e2 = Entry(root,show='*',width=35,bg="#DCDCDC",fg="#AD0000",font="calibri 10 italic bold")
e3 = Entry(root,width=35,bg="#DCDCDC",fg="#1C2833",font="calibri 10 italic bold")
e4 = Entry(root,width=35,bg="#DCDCDC",fg="#1C2833",font="calibri 10 italic bold")
t = Text(root,width=35,height=10,bg="#DCDCDC",fg="#1C2833",font="calibri 10 italic bold")

e1.grid(row=2, column=1,pady=5)
e2.grid(row=3, column=1,pady=5)
e3.grid(row=4,column=1,pady=5)
e4.grid(row=5,column=1,pady=5)
t.grid(row=6,column=1,pady=5)

# button
Button(root,text="Quit",width=10,command=root.quit,fg="#F7F7F7",bg="#AD0000",borderwidth='2px',relief=RAISED,font=("calibri",10,'italic bold')).place(width=70,height=35,x=140,y=500)
Button(root,text="Send",width=10,command=send_mail,fg="#F7F7F7",bg="#117916",borderwidth='2px',relief=RAISED,font=("calibri",10,'italic bold')).place(width=70,height=35,x=325,y=500)
Button(root,text="Attach",width=10,command=file,fg="#17202A",bg="#E3E333",borderwidth='2px',relief=RAISED,font=("calibri",10,'italic bold')).place(width=70,height=35,x=230,y=500)

root.mainloop()
