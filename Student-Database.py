from tkinter import *
from customtkinter import *
import sqlite3
from tkinter import messagebox

def update():
    con =sqlite3.connect('students.db')
    c = con.cursor()
    c.execute('UPDATE STUDENTS SET sid=:id,name=:n,phone=:p WHERE sid=:r',{
        'id':sid2.get(),
        'n':name2.get(),
        'p':phone2.get(),
        'r':rid2.get()
    })
    c.close()
    con.commit()
    con.close()
    sid2.delete(0,END)
    name2.delete(0,END)
    phone2.delete(0,END)
    rid2.delete(0,END)

def edit():
    global sid2,name2,phone2,rid2
    top = CTkToplevel()
    l1 = CTkLabel(top,text='Student ID:')
    l2 = CTkLabel(top,text='Name:')
    l3 = CTkLabel(top,text='Phone:')
    l4 = CTkLabel(top,text='Target Student ID:')

    sid2 = CTkEntry(top,width=500)
    name2 = CTkEntry(top,width=500)
    phone2 = CTkEntry(top,width=500)
    rid2 = CTkEntry(top,width=500)

    l1.grid(row=0,column=0,padx=10,pady=5)
    sid2.grid(row=0,column=1,padx=10)
    l2.grid(row=1,column=0,pady=5)
    name2.grid(row=1,column=1)
    l3.grid(row=2,column=0,pady=5)
    phone2.grid(row=2,column=1)

    CTkLabel(top).grid(row=3,column=0,pady=5) # divider
    l4.grid(row=4,column=0,padx=10,pady=5)
    rid2.grid(row=4,column=1)
    
    CTkButton(top,text='update',command=update).grid(row=5,column=0,columnspan=2,padx=10,pady=5,sticky=W+E)

def create():
    con = sqlite3.connect('students.db')
    c = con.cursor()
    try:
        c.execute('''create table students(
        sid TEXT(10),
        name TEXT(20),
        phone INT
        )''')
        messagebox.showinfo('Info','Table Successfully Created')
    except sqlite3.OperationalError:
        messagebox.showerror('Error','Table Already Exists')
    c.close()
    con.commit()
    con.close()

def droptable():
    try:
        con = sqlite3.connect('students.db')
        c = con.cursor()
        try:
            if messagebox.askyesno('Delete Table','Do you Want to Delete the Student Table? All Your data will be Lost'):
                c.execute('drop table students')
        except sqlite3.OperationalError:
            messagebox.showerror('Error',"Table Doesn't Exist")
        c.close()
        con.commit()
        con.close()
    except:
        pass


def delete():
    con = sqlite3.connect('students.db')
    c = con.cursor()
    try:
        c.execute('DELETE FROM students WHERE sid=:place',{
        'place':rid.get()        
        }).fetchall()
    except sqlite3.OperationalError:
        messagebox.showerror('Error',"Table Doesn't Exist")
    rid.delete(0,END)
    c.close()
    con.commit()
    con.close()

def submit():
    con = sqlite3.connect('students.db')
    c = con.cursor()
    # inserting
    try:
        c.execute('INSERT INTO students VALUES(:sid,:name,:phone)',{
            'sid':sid.get(),'name':name.get(),'phone':phone.get()
        })
    except sqlite3.OperationalError:
        messagebox.showerror('Error',"Table Doesn't Exist")
    c.close()
    con.commit()
    con.close()
    sid.delete(0,END)
    name.delete(0,END)
    phone.delete(0,END)

def query():
    con = sqlite3.connect('students.db')
    c = con.cursor()
    try:
        o = c.execute('SELECT oid,* from students').fetchall()
    except sqlite3.OperationalError:
        messagebox.showerror('Error',"Table Doesn't Exist")
        c.close()
        con.commit()
        con.close()
        return
    if len(o)==0:
        messagebox.showinfo('Info','Table consists 0 record(s)')
        c.close()
        con.commit()
        con.close()
        return
    top = CTkToplevel()
    for i in range(len(o)):
        CTkLabel(top,text=o[i][0]).grid(row=i,column=0,pady=3,padx=10)
        CTkLabel(top,text=o[i][1]).grid(row=i,column=1,pady=3,padx=10)
        CTkLabel(top,text=o[i][2]).grid(row=i,column=2,pady=3,padx=10)
        CTkLabel(top,text=o[i][3]).grid(row=i,column=3,pady=3,padx=10)
    c.close()
    con.commit()
    con.close()

root = CTk()
root.title('Student Form')

l1 = CTkLabel(root,text='Student ID:')
l2 = CTkLabel(root,text='Name:')
l3 = CTkLabel(root,text='Phone:')
l4 = CTkLabel(root,text='Student ID:')

sid = CTkEntry(root,width=500)
name = CTkEntry(root,width=500)
phone = CTkEntry(root,width=500)
rid = CTkEntry(root,width=500)

l1.grid(row=0,column=0,padx=10,pady=5)
sid.grid(row=0,column=1,padx=10)
l2.grid(row=1,column=0,pady=5)
name.grid(row=1,column=1)
l3.grid(row=2,column=0,pady=5)
phone.grid(row=2,column=1)
CTkButton(root,text='Submit',command=submit).grid(row=3,column=0,columnspan=2,sticky=W+E,padx=10,pady=5)
CTkButton(root,text='Show Database',command=query).grid(row=4,column=0,columnspan=2,sticky=W+E,padx=10,pady=5)
l4.grid(row=5,column=0,pady=5)
rid.grid(row=5,column=1)
CTkButton(root,text='Delete record',command=delete).grid(row=6,column=0,columnspan=2,sticky=W+E,padx=10,pady=5)
CTkButton(root,text='Edit record',command=edit).grid(row=7,column=0,columnspan=2,sticky=W+E,padx=10,pady=5)
CTkButton(root,text='Create Table',command=create).grid(row=8,column=0,columnspan=2,sticky=W+E,padx=10,pady=5)
CTkButton(root,text='Delete Table',command=droptable).grid(row=9,column=0,columnspan=2,sticky=W+E,padx=10,pady=5)

root.mainloop()