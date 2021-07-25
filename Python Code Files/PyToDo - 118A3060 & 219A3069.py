import tkinter
import tkcalendar
import time
from tkcalendar import *
from tkinter import *
from tkinter import messagebox
import dbfunctions
from dbfunctions import conn
import os
from win10toast import ToastNotifier
from datetime import date
from datetime import datetime
import pygame
from pygame import mixer


def add():
    if(len(addtask.get()) == 0):
        messagebox._show("ERROR", "No data Available\nPlease Enter Some Task")
    else:
        dbfunctions.insertdata(addtask.get(), "", "")
        addtask.delete(0, END)
        populate()


def populate():
    listbox.delete(0, END)
    for rows in dbfunctions.show():
        listbox.insert(END, rows[1])


def deletetask(event):
    dbfunctions.deletebytask(listbox.get(ANCHOR))
    populate()


main = tkinter.Tk()
main.title("PYTODO")
main.geometry("600x600")

main.configure(background="#1d1d1d")

lbl1 = Label(
    main,
    text="Python Task Manager",
    background="#1d1d1d",
    foreground="#eeeeee",
    font=("Verdana 20")
).pack(pady=10)

addframe = tkinter.Frame(
    main,
    bg="#1d1d1d",
)
addframe.pack()

addtask = tkinter.Entry(
    addframe,
    font=("Verdana"),
    background="#eeeeee",
)
addtask.pack()


def addtsk():
    if(len(addtask.get()) == 0):
        messagebox._show(
            "ERROR", "Please copy and paste the task in the textbox.")
    else:

        taskframe.destroy()
        lbl2.destroy()
        listbox.destroy()

        addbtn.destroy()
        addbtn2.destroy()
        newpage()


def newpage():

    def msg():

        caldate = cal.get_date()
        update()
        today = date.today()
        d4 = today.strftime("%m/%d/%Y")
        print(d4)
        print(caldate)

        if(d4 > cal.get_date()):
            messagebox.showinfo("ERROR", "Wrong date selected")
        else:

            if (d4 == cal.get_date()):

                root = Tk()
                root.title("Alarm clock")

                def SubmitButton():
                    AlarmTime = addtaskval.get()
                    Message1()
                    CurrentTime = time.strftime("%H:%M")
                    print("the alarm time is: {}".format(AlarmTime))

                    while AlarmTime != CurrentTime:

                        CurrentTime = time.strftime("%H:%M")
                        time.sleep(1)
                    if AlarmTime == CurrentTime:
                        print("now Alarm Musing Playing")

                        mixer.init()
                        mixer.music.load("Music.mp3")
                        mixer.music.play()
                        label2.config(text="Alarm music playing.....")
                        messagebox.showinfo(
                            title='Alarm Message', message="{}".format(entry2.get()))
                        Notification()

                def Message1():
                    AlarmTimeLable = addtaskval.get()
                    label2.config(text="the Alarm time is Counting...")

                    messagebox.showinfo(
                        title='Alarm clock', message='Alarm will Ring at {}'.format(AlarmTimeLable))

                frame1 = ttk.Frame(root)
                frame1.pack()
                frame1.config(height=100, width=100)

                label1 = ttk.Label(frame1, text="Enter the Alarm time :")
                label1.pack()
                entry1 = ttk.Entry(frame1, width=30)
                entry1.pack()
                entry1.insert(3, addtaskval.get())

                labelAlarmMessage = ttk.Label(frame1, text="Alarm Message:")
                labelAlarmMessage.pack()

                entry2 = ttk.Entry(frame1, width=30)
                entry2.pack()
                entry2.insert(3, addtask.get())

                button1 = ttk.Button(frame1, text="submit",
                                     command=SubmitButton)
                button1.pack()

                label2 = ttk.Label(frame1)
                label2.pack()

                root.mainloop()

            else:
                from twilio.rest import Client

                account_sid = '**************'
                auth_token = '****************'
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                    from_='whatsapp:+*********',
                    body='Reminder for :\n' + addtask.get() + '\nDate (M/D/Y) : ' +
                    cal.get_date() + '\nTime : ' + addtaskval.get(),
                    to='whatsapp:+*************'
                )

                print(message.sid)
                messagebox.showinfo(
                    "DONE", "Reminder message sent on WhatsApp.")

    def Notification():
        now = datetime.now()

        print("now =", now)

        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
        print("date and time =", dt_string)

        print(addtask.get())
        query = "SELECT dateoftask, timeoftask FROM todo where task=?;"
        conn.execute(query, (addtask.get(),))
        for rows in conn.execute(query, (addtask.get(),)):
            print(rows)

        def convertTuple(tup):
            str = ''.join(tup)
            return str

        str = convertTuple(rows)
        print(str)

        ans = str >= dt_string
        print(ans)
        if(ans == True):
            toaster = ToastNotifier()
            a = addtask.get()
            toaster.show_toast("Task Reminder\n", a, duration=12)
            print("I'm in if")
        else:
            print("I'm in else")

    def update():
        dbfunctions.updatedata(addtask.get(), addtaskval.get(), cal.get_date())

    messagebox.showinfo("Select a Date:", "Select a Date ")
    cal = Calendar(addframe, selectmode="day", date_pattern='mm/dd/y')
    cal.pack()

    sett = Label(addframe, text="SET TIME:", background="#1d1d1d", foreground="#eeeeee", relief="flat",
                 font=("Verdana"), highlightcolor="#000000", activebackground="goldenrod1", border=0,
                 activeforeground="#eeeeee", )
    sett.pack()
    messagebox.showinfo("Select a time", "Enter the reminder time.")
    addtaskval = Entry(addframe, font=("Century"), background="#eeeeee")
    addtaskval.pack(padx=20, ipadx=20, ipady=5)
    btn = Button(addframe, text="Submit", command=msg)
    btn.pack(padx=20, ipadx=20, ipady=5)


addbtn = tkinter.Button(
    addframe,
    text="ADD TASK",
    command=add,
    background="#1d1d1d",
    foreground="#eeeeee",
    relief="flat",
    font=("Verdana"),
    highlightcolor="#000000",
    activebackground="goldenrod1",
    border=0,
    activeforeground="#eeeeee",
)
addbtn.pack(padx=20, ipadx=20, ipady=5)

addbtn2 = Button(
    addframe,
    text="Set Reminder",
    command=addtsk,
    background="#1d1d1d",
    foreground="#eeeeee",
    relief="flat",
    font=("Verdana"),
    highlightcolor="#000000",
    activebackground="#1d1d1d",
    border=0,
    activeforeground="#eeeeee",
)
addbtn2.pack(padx=20, ipadx=20, ipady=5)

tkinter.Label(
    addframe,
    text="Your Tasks",
    background="#1d1d1d",
    foreground="#eeeeee",
    font=("Calibri", 18, "bold", "underline"),
).pack(pady=10)

taskframe = tkinter.Frame(
    main,
    bg="#1d1d1d",
)
taskframe.pack(fill=BOTH, expand=300)
scrollbar = Scrollbar(taskframe)
scrollbar.pack(side=RIGHT, fill=Y)
listbox = Listbox(
    taskframe,
    font=("Verdana 18 bold"),
    bg="#1d1d1d",
    fg="#eeeeee",
    selectbackground="#eeeeee",
    selectforeground="#1d1d1d",
)
listbox.pack(fill=BOTH, expand=300)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

listbox.bind("<Double-Button-1>", deletetask)
listbox.bind("<Delete>", deletetask)

populate()

lbl2 = tkinter.Label(
    taskframe,
    text="TIP : Double Click On A Task to Delete",
    background="#1d1d1d",
    foreground="#FFEB3B",
    font=("Calibri 18"),
)

lbl2.pack(side=BOTTOM, pady=10)

main.mainloop()
