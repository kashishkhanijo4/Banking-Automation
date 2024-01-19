from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from datetime import datetime
import time
import sqlite3
try:
    conobj=sqlite3.connect(database="banking.sqlite")
    curobj=conobj.cursor()
    curobj.execute("create table accounts(acn integer primary key autoincrement,name text,pass text,email text,mob text,bal float,type text,opendate text)")
    conobj.commit()
    print("table created")
except:
    print("something went wrong,might be table already exists")
conobj.close()

win=Tk()
win.state("zoomed")
win.configure(bg="powder blue")
win.resizable(width=False,height=False)


title=Label(win,text="Banking Automation",font=('Arial',60,'bold','underline'),bg='powder blue')
title.pack()

date=Label(win,text=f"{datetime.now().date()}",font=('Arial',15,'bold'),bg='powder blue')
date.place(relx=.9,rely=.12)

def mainscreen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)

    def new():
        frm.destroy()
        newuserscreen()
        
    def fp():
        frm.destroy()
        fpscreen()
    def reset():
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_acn.focus()
        
    def login():
        acn=e_acn.get()
        pwd=e_pass.get()
        if len(acn)==0 or len(pwd)==0:
            messagebox.showerror("Login","Empty fields are not allowed!")
        else:
            conobj=sqlite3.connect(database="banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select * from accounts where acn=? and pass=?",(acn,pwd))
            tup=curobj.fetchone()
            if tup==None:
                messagebox.showerror("Login","Invalid ACN/Pass")
            else:
                global uname,uacn
                uacn=tup[0]
                uname=tup[1]
                frm.destroy()
                homescreen()
        
    lbl_acn=Label(frm,text="ACN",font=('arial',20,'bold'),fg='blue',bg='pink')
    lbl_acn.place(relx=.3,rely=.1)
    
    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.4,rely=.1)
    e_acn.focus()
    
    lbl_pass=Label(frm,text="Pass",font=('arial',20,'bold'),fg='blue',bg='pink')
    lbl_pass.place(relx=.3,rely=.2)
    
    e_pass=Entry(frm,font=('arial',20,'bold'),bd=5,show="*")
    e_pass.place(relx=.4,rely=.2)
    
    login_btn=Button(frm,command=login,font=('arial',20,'bold'),bd=5,text="login")
    login_btn.place(relx=.42,rely=.3)
    
    reset_btn=Button(frm,font=('arial',20,'bold'),bd=5,text="reset",command=reset)
    reset_btn.place(relx=.52,rely=.3)
    
    fp_btn=Button(frm,command=fp,font=('arial',20,'bold'),bd=5,text="forgot password",width=16)
    fp_btn.place(relx=.4,rely=.4)

    new_btn=Button(frm,font=('arial',20,'bold'),bd=5,text="open new account",width=19,command=new)
    new_btn.place(relx=.38,rely=.5)


def newuserscreen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    def back():
        frm.destroy()
        mainscreen()
        
    def openaccountdb():
        name=e_name.get()
        pwd=e_pass.get()
        email=e_email.get()
        mob=e_mob.get()
        actype=cb_acn.get()
        bal=0
        opendate=time.ctime()
        
        conobj=sqlite3.connect(database="banking.sqlite")
        curobj=conobj.cursor()
        curobj.execute("insert into accounts(name,pass,email,mob,bal,type,opendate) values(?,?,?,?,?,?,?)",(name,pwd,email,mob,bal,actype,opendate))
        conobj.commit()
        curobj.close()
        
        curobj=conobj.cursor()
        curobj.execute("select max(acn) from accounts")
        tup=curobj.fetchone()
        conobj.close()
        messagebox.showinfo("open account",f"Account opened with ACN:{tup[0]}")
        
        
    back_btn=Button(frm,font=('arial',20,'bold'),bd=5,text="back",command=back)
    back_btn.place(relx=0,rely=0)
    
    lbl_name=Label(frm,text="Name",font=('arial',20,'bold'),fg='blue',bg='pink')
    lbl_name.place(relx=.3,rely=.1)
    
    e_name=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_name.place(relx=.4,rely=.1)
    e_name.focus()
    
    lbl_pass=Label(frm,text="Pass",font=('arial',20,'bold'),fg='blue',bg='pink')
    lbl_pass.place(relx=.3,rely=.2)
    
    e_pass=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_pass.place(relx=.4,rely=.2)
    
    lbl_email=Label(frm,text="Email",font=('arial',20,'bold'),fg='blue',bg='pink')
    lbl_email.place(relx=.3,rely=.3)
    
    e_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_email.place(relx=.4,rely=.3)
    
    lbl_mob=Label(frm,text="Mob",font=('arial',20,'bold'),fg='blue',bg='pink')
    lbl_mob.place(relx=.3,rely=.4)
    
    e_mob=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_mob.place(relx=.4,rely=.4)
    
    lbl_type=Label(frm,text="Type",font=('arial',20,'bold'),fg='blue',bg='pink')
    lbl_type.place(relx=.3,rely=.5)
    
    cb_acn=Combobox(frm,font=('arial',20,'bold'),values=['Saving','Current'])
    cb_acn.current(0)
    cb_acn.place(relx=.4,rely=.5)
    
    open_btn=Button(frm,font=('arial',20,'bold'),bd=5,text="open",command=openaccountdb)
    open_btn.place(relx=.42,rely=.6)
    
    reset_btn=Button(frm,font=('arial',20,'bold'),bd=5,text="reset")
    reset_btn.place(relx=.52,rely=.6)
    
    
def fpscreen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    def back():
        frm.destroy()
        mainscreen()
       
    def getpassdb():
        acn=e_acn.get()
        email=e_email.get()
        mob=e_mob.get()
        
        conobj=sqlite3.connect(database="banking.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select pass from accounts where acn=? and email=? and mob=?",(acn,email,mob))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror("Forgot Password","Invalid Details!")
        else:
            messagebox.showinfo("Forgot Password",f"Your Pass:{tup[0]}")
            
            
    def reset():
        e_acn.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")
        e_acn.focus()
        
    back_btn=Button(frm,font=('arial',20,'bold'),bd=5,text="back",command=back)
    back_btn.place(relx=0,rely=0)
    
    lbl_acn=Label(frm,text="ACN",font=('arial',20,'bold'),fg='blue',bg='pink')
    lbl_acn.place(relx=.3,rely=.2)
    
    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.4,rely=.2)
    e_acn.focus()
    
    lbl_email=Label(frm,text="Email",font=('arial',20,'bold'),fg='blue',bg='pink')
    lbl_email.place(relx=.3,rely=.3)
    
    e_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_email.place(relx=.4,rely=.3)
    
    lbl_mob=Label(frm,text="Mob",font=('arial',20,'bold'),fg='blue',bg='pink')
    lbl_mob.place(relx=.3,rely=.4)
    
    e_mob=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_mob.place(relx=.4,rely=.4)
    
    recvr_btn=Button(frm,font=('arial',20,'bold'),bd=5,text="recover",command=getpassdb)
    recvr_btn.place(relx=.42,rely=.5)
    
    reset_btn=Button(frm,font=('arial',20,'bold'),bd=5,text="reset",command=reset)
    reset_btn.place(relx=.54,rely=.5)
    
def homescreen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
        
    def logout():
        frm.destroy()
        mainscreen()
            
    def details():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)
        
        lbl=Label(ifrm,text="This is Details Screen",font=('arial',25,'bold'),fg='blue',bg='white')
        lbl.pack()
        
        conobj=sqlite3.connect(database="banking.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from accounts where acn=?",(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        
        lbl_acn=Label(ifrm,text=f"Account No\t{tup[0]}",font=('arial',12,'bold'),bg='white')
        lbl_acn.place(relx=.3,rely=.15)
        
        lbl_bal=Label(ifrm,text=f"ACN Balance\t{tup[5]}",font=('arial',12,'bold'),bg='white')
        lbl_bal.place(relx=.3,rely=.25)
        
        lbl_type=Label(ifrm,text=f"Account Type\t{tup[6]}",font=('arial',12,'bold'),bg='white')
        lbl_type.place(relx=.3,rely=.35)
        
        lbl_opendate=Label(ifrm,text=f"ACN opened date\t{tup[7]}",font=('arial',12,'bold'),bg='white')
        lbl_opendate.place(relx=.3,rely=.45)
        
    def profile():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)
        
        
        def updatedb():
            name=e_name.get()
            pwd=e_pass.get()
            email=e_email.get()
            mob=e_mob.get()
            
            conobj=sqlite3.connect(database="banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update accounts set name=?,pass=?,email=?,mob=? where acn=?",(name,pwd,email,mob,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update Profile","Record Updated")
            global uname
            uname=name
            ifrm.destroy()
            homescreen()
        
        lbl=Label(ifrm,text="This is Update Profile Screen",font=('arial',25,'bold'),fg='blue',bg='white')
        lbl.pack()
        
        lbl_name=Label(ifrm,text="Name",font=('arial',15,'bold'),bg='white')
        lbl_name.place(relx=.2,rely=.15)
        
        e_name=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_name.place(relx=.2,rely=.2)
        
        
        lbl_pass=Label(ifrm,text="Pass",font=('arial',15,'bold'),bg='white')
        lbl_pass.place(relx=.2,rely=.4)
        
        e_pass=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_pass.place(relx=.2,rely=.45)
        
        
        lbl_email=Label(ifrm,text="Email",font=('arial',15,'bold'),bg='white')
        lbl_email.place(relx=.5,rely=.15)
        
        e_email=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_email.place(relx=.5,rely=.2)
        
        lbl_mob=Label(ifrm,text="Mob",font=('arial',15,'bold'),bg='white')
        lbl_mob.place(relx=.5,rely=.4)
        
        e_mob=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        e_mob.place(relx=.5,rely=.45)
        
        btn=Button(ifrm,font=('arial',20,'bold'),bd=5,text="update",command=updatedb)
        btn.place(relx=.6,rely=.6)
        
        conobj=sqlite3.connect(database="banking.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from accounts where acn=?",(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        
        e_name.insert(0,tup[1])
        e_pass.insert(0,tup[2])
        e_email.insert(0,tup[3])
        e_mob.insert(0,tup[4])
        
        
        
    def deposit():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)
        
        def depositdb():
            amt=float(e_amt.get())
            conobj=sqlite3.connect(database="banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select bal from accounts where acn=?",(uacn,))
            bal=curobj.fetchone()[0]
            curobj.close()
            
            curobj=conobj.cursor()
            curobj.execute("update accounts set bal=bal+? where acn=?",(amt,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Deposit",f"Amt {amt} deposited,Updated Bal:{bal+amt}")
        
        lbl=Label(ifrm,text="This is Deposit Screen",font=('arial',25,'bold'),fg='blue',bg='white')
        lbl.pack()
        
        lbl_amt=Label(ifrm,text="Amount",font=('arial',20,'bold'),fg='black',bg='white')
        lbl_amt.place(relx=.2,rely=.2)
    
        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.35,rely=.2)
    
    
        btn=Button(ifrm,font=('arial',20,'bold'),bd=5,text="deposit",command=depositdb)
        btn.place(relx=.55,rely=.35)
        
    def withdraw():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)
        
        def withdrawdb():
            
            amt=float(e_amt.get())
            conobj=sqlite3.connect(database="banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select bal from accounts where acn=?",(uacn,))
            bal=curobj.fetchone()[0]
            curobj.close()
            if bal>=amt:
                curobj=conobj.cursor()
                curobj.execute("update accounts set bal=bal-? where acn=?",(amt,uacn))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Withdraw",f"Amt {amt} withdrawn,Updated Bal:{bal-amt}")
            else:
                messagebox.showwarning("Withdraw",f"Insufficient Bal:{bal}")
                
        lbl=Label(ifrm,text="This is Withdraw Screen",font=('arial',25,'bold'),fg='blue',bg='white')
        lbl.pack()
    
        lbl_amt=Label(ifrm,text="Amount",font=('arial',20,'bold'),fg='black',bg='white')
        lbl_amt.place(relx=.2,rely=.2)
    
        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.35,rely=.2)
    
    
        btn=Button(ifrm,font=('arial',20,'bold'),bd=5,text="withdraw",command=withdrawdb)
        btn.place(relx=.55,rely=.35)
        
    
    def transfer():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6)
        
        def transferdb():
            to=e_to.get()
            amt=float(e_amt.get())
            
            conobj=sqlite3.connect(database="banking.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select * from accounts where acn=?",(to,))
            tup=curobj.fetchone()
            curobj.close()
            if tup==None:
                messagebox.showerror("Transfer","To ACN does not exist!")
            else:
                curobj=conobj.cursor()
                curobj.execute("select bal from accounts where acn=?",(uacn,))
                bal=curobj.fetchone()[0]
                curobj.close()
                if bal>=amt:
                    curobj=conobj.cursor()
                    curobj.execute("update accounts set bal=bal-? where acn=?",(amt,uacn))
                    curobj.execute("update accounts set bal=bal+? where acn=?",(amt,to))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Transfer",f"Amt {amt} transfered to ACN:{to}")
                else:
                    messagebox.showwarning("Transfer",f"Insufficient Bal:{bal}")
             
            
        lbl=Label(ifrm,text="This is Transfer Screen",font=('arial',25,'bold'),fg='blue',bg='white')
        lbl.pack()
    
        lbl_to=Label(ifrm,text="To",font=('arial',20,'bold'),fg='black',bg='white')
        lbl_to.place(relx=.2,rely=.2)
    
        e_to=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_to.place(relx=.35,rely=.2)
    
        lbl_amt=Label(ifrm,text="Amount",font=('arial',20,'bold'),fg='black',bg='white')
        lbl_amt.place(relx=.2,rely=.3)
    
        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.35,rely=.3)
    
        btn=Button(ifrm,font=('arial',20,'bold'),bd=5,text="transfer",command=transferdb)
        btn.place(relx=.55,rely=.45)
        
        
    logout_btn=Button(frm,font=('arial',20,'bold'),bd=5,text="logout",command=logout)
    logout_btn.place(relx=.9,rely=0)
    
    lbl_wel=Label(frm,text=f"Welcome,{uname}",font=('arial',15,'bold'),fg='blue',bg='pink')
    lbl_wel.place(relx=0,rely=0)
      
    details_btn=Button(frm,command=details,font=('arial',20,'bold'),bd=5,text="details",width=12)
    details_btn.place(relx=0,rely=.15)
    
    profile_btn=Button(frm,command=profile,font=('arial',20,'bold'),bd=5,text="update profile",width=12)
    profile_btn.place(relx=0,rely=.3)
    
    dep_btn=Button(frm,command=deposit,font=('arial',20,'bold'),bd=5,text="deposit",width=12)
    dep_btn.place(relx=0,rely=.45)
    
    withdraw_btn=Button(frm,command=withdraw,font=('arial',20,'bold'),bd=5,text="withdraw",width=12)
    withdraw_btn.place(relx=0,rely=.6)

    trans_btn=Button(frm,command=transfer,font=('arial',20,'bold'),bd=5,text="transfer",width=12)
    trans_btn.place(relx=0,rely=.75)  
    
mainscreen()
win.mainloop()
