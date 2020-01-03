from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import re


class Student:
    def __init__(self, master):
        self.txt_gender = StringVar()
        self.regNO=StringVar()
        self.Name=StringVar()
        self.Email=StringVar()
        self.emailvalid = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        self.master=master
        self.master.title("STUDENT MANAGEMENT SYSTEM")
        w = 1000
        h = 600
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.title = Label(self.master, text="MANAGE STUDENT DETAILS", font=("Helvetica", 20))
        self.title.pack(side=TOP, fill=X)
        # -----------Manage Frame-------------
        self.std_Manage_Frame = Frame(self.master, bd=2, relief=RIDGE)
        self.std_Manage_Frame.place(x=20, y=50, width=300, height=500)

        self.lbl_RegNo = Label(self.std_Manage_Frame, text="REGISTER NO", font=("Helvetica", 10), fg="grey1")
        self.lbl_RegNo.grid(row=1, column=0, padx=10, pady=10)
        self.txt_RegNo = Entry(self.std_Manage_Frame, textvariable=self.regNO, bd=2, width=25)
        self.txt_RegNo.grid(row=1, column=2)
        self.lbl_Name = Label(self.std_Manage_Frame, text="NAME", font=("Helvetica",10), fg="grey1")
        self.lbl_Name.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.txt_Name = Entry(self.std_Manage_Frame, textvariable=self.Name, bd=2, width=25)
        self.txt_Name.grid(row=2, column=2)

        self.lbl_Course = Label(self.std_Manage_Frame, text="COURSE", font=("Helvetica", 10), fg="grey1")
        self.lbl_Course.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.txt_Course = ttk.Combobox(self.std_Manage_Frame, width=22, values=["BCA", "BBA", "BCA", "B-COM", "MBA", "MCA"])
        self.txt_Course.grid(row=3, column=2)

        self.lbl_Gender = Label(self.std_Manage_Frame, text="GENDER", font=("Helvetica", 10), fg="grey1")
        self.lbl_Gender.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.radio_male = Radiobutton(self.std_Manage_Frame, text="Male", variable=self.txt_gender, value="Male", fg="grey1", tristatevalue="x")
        self.radio_male.place(x=110, y=130)
        self.radio_female = Radiobutton(self.std_Manage_Frame, text="Female", variable=self.txt_gender, value="Female", fg="grey1", tristatevalue="x")
        self. radio_female.place(x=180, y=130)

        self.lbl_Email = Label(self.std_Manage_Frame, text="E-MAIL", font=("Helvetica", 10), fg="grey1")
        self.lbl_Email.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.txt_Email = Entry(self.std_Manage_Frame, textvariable=self.Email, bd=2, width=25)
        self.txt_Email.grid(row=5, column=2)
        # --------Form Control buttons-------------
        self.btn_Add = Button(self.std_Manage_Frame, text="ADD", width=15, command=self.insert,  font=("Helvetica", 10, "bold"), fg="grey1", background = 'white')
        self.btn_Add.place(x=22, y=260)
        self.btn_Update = Button(self.std_Manage_Frame, text="UPDATE", width=15, command=self.update, font=("Helvetica", 10, "bold"), fg="grey1", background = 'white')
        self.btn_Update.place(x=160, y=260)
        self.btn_Delete = Button(self.std_Manage_Frame, text="DELETE", width=15, command=self.delete, font=("Helvetica", 10, "bold"), fg="grey1", background = 'white')
        self.btn_Delete.place(x=22, y=295)
        self.btn_Clear = Button(self.std_Manage_Frame, text="CLEAR", width=15, command=self.clear, font=("Helvetica", 10, "bold"), fg="grey1", background = 'white')
        self.btn_Clear.place(x=160, y=295)
        # ---------Details Frame-------------
        self.std_Details_Frame = Frame(window, bd=2, relief=RIDGE)
        self.std_Details_Frame.place(x=350, y=50, width=610, height=500)
        self.scroll_x = Scrollbar(self.std_Details_Frame, orient=HORIZONTAL)
        self.scroll_y = Scrollbar(self.std_Details_Frame, orient=VERTICAL)
        self.std_Table = ttk.Treeview(self.std_Details_Frame, height=400,
                                 columns=("column-1", "column-2", "column-3", "column-4", "column-5"),
                                 xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.scroll_x.pack(side=BOTTOM, fill=X)
        self.scroll_y.pack(side=RIGHT, fill=Y)
        self.scroll_x.config(command=self.std_Table.xview)
        self.scroll_y.config(command=self.std_Table.yview)
        self.std_Table.heading("column-1", text="REGISTER-NO")
        self.std_Table.heading("column-2", text="NAME")
        self.std_Table.heading("column-3", text="COURSE")
        self.std_Table.heading("column-4", text="GENDER")
        self.std_Table.heading("column-5", text="EMAIL")
        self.std_Table['show'] = 'headings'
        self.std_Table.column("column-1", width=90)
        self.std_Table.column("column-2", width=140)
        self.std_Table.column("column-3", width=90)
        self.std_Table.column("column-4", width=90)
        self.std_Table.column("column-5", width=180)
        self.std_Table.pack()
        self.std_Table.bind("<ButtonRelease-1>", self.get_data)

        self.con=sqlite3.connect("studentDb.db")
        self.cursor=self.con.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS students (RegNo TEXT, Name TEXT, Course TEXT, Gender TEXT, 
        Email TEXT)""")
        self.con.commit()
        self.display()

    def __del__(self):
        self.con.close()

    # function for displaying data from database
    def display(self):
        self.cursor.execute("SELECT * FROM students")
        records=self.cursor.fetchall()
        if len(records) !=0:
            self.std_Table.delete(*self.std_Table.get_children())
            for row in records:
                self.std_Table.insert('', END, values=row)

    # function to concatenate error message based on condition
    def addmessage(self, container, content):
        if container=="":
            return content
        else:
            return container+","+content

    # function for validating the user data
    def validation(self, status):
        flag=0
        message=""
        if len(self.txt_RegNo.get())==0:
            flag+=1
            message=self.addmessage(message, "Register Number")
        if len(self.txt_Name.get())==0:
            flag += 1
            message = self.addmessage(message, "Name")
        if len(self.txt_Course.get())==0:
            flag += 1
            message = self.addmessage(message, "Course")
        if len(self.txt_gender.get())==0:
            flag += 1
            message = self.addmessage(message, "Gender")
        if len(self.txt_Email.get())==0:
            flag += 1
            message = self.addmessage(message, "Email")
        if flag>1 and status=="insert":
            messagebox.showerror("Validation Error", message + " fields are mandatory")
            return 0
        elif flag>0 and status=="insert":
            messagebox.showerror("Validation Error", message + " field is mandatory")
            return 0
        if len(self.txt_RegNo.get())==0 and (status=="delete" or status=="update"):
            messagebox.showerror("Validation Error", " Please select a student profile before performing the " + status
                                 +" operation")
            return 0

        if re.findall(r'[0-9]', self.txt_Name.get()) and str(status)=="insert":
            self.txt_Name.focus()
            messagebox.showerror("Validation Error", "Please enter a valid Name")
            return 0
        if re.findall(r'[0-9]', self.txt_Course.get()) and str(status)=="insert":
            self.txt_Course.set("")
            self.txt_Course.focus()
            messagebox.showerror("Validation Error", "Please select a valid Course")
            return 0
        # Validation the email address
        if self.emailvalid.match(self.txt_Email.get()) is None and  str(status)=="insert":
            self.txt_Email.focus()
            messagebox.showerror("Validation Error", "Please Enter a Valida Email-Id")
            return 0

        self.cursor.execute("SELECT * FROM students where RegNo=?", ((self.txt_RegNo.get()).upper(),))
        count_value=len(self.cursor.fetchall())
        # Avoiding the Register Number duplication in DataBase
        if count_value > 0 and str(status)=="insert":
            messagebox.showerror("Integrity Error", "A student profile already exist with the given Register Number:"+self.txt_RegNo.get()+". Please try a new Register Number ")
            self.txt_RegNo.focus()
            return 0
        # Ensuring that a student profile is exist in the DataBase before performing the update and delete operations
        if count_value==0 and (str(status)=="update" or str(status)=="delete"):
            messagebox.showerror("Integrity Error", "No Student profile is exist with the given Register Number:"+self.txt_RegNo.get())
            self.txt_RegNo.focus()
            return 0
        # Code for avoiding the Email duplication
        self.cursor.execute("SELECT * FROM students WHERE RegNo!=? and Email=?",((self.txt_RegNo.get()).upper(),self.txt_Email.get()))
        count_value=len(self.cursor.fetchall())
        if count_value>0 and (str(status)=="update" or str(status)=="insert"):
            messagebox.showerror("Integrity Error", "A student profile is already exist with the given Email id:" + self.txt_Email.get())
            self.txt_Email.focus()
            return 0
        return 1

    # function for performing insertion, deletion  and update execution operations
    def execute_function(self, query, values, message):
        self.cursor.execute(query, values)
        self.con.commit()
        self.display()
        self.clear()
        messagebox.showinfo("Success", "Successfully" + " " + message +" "+ "the student profile")

    # function for performing validation and execution for insert operation
    def insert(self):
        if self.validation("insert")==1:
            query="INSERT INTO students VALUES(?,?,?,?,?)"
            values=((self.txt_RegNo.get()).upper(), self.txt_Name.get(), self.txt_Course.get(), self.txt_gender.get(), self.txt_Email.get())
            self.execute_function(query, values, "Inserted")

    # function for performing validation and execution for update operation
    def update(self):
        if self.validation("update")==1:
            query="UPDATE students set Name=?, Course=?, Gender=?, Email=? WHERE RegNo=?"
            values=(self.txt_Name.get(), self.txt_Course.get(), self.txt_gender.get(), self.txt_Email.get(), (self.txt_RegNo.get()).upper())
            self.execute_function(query, values, "updated")

    # function for performing validation and execution for delete operation
    def delete(self):
        if self.validation("delete")==1:
            msgbox=messagebox.askquestion("Confirmation", "Are you sure you want to delete this profile:"+self.txt_RegNo.get(), icon='warning')
            if msgbox=='yes':
                query = "DELETE FROM students WHERE RegNo=?"
                values = ((self.txt_RegNo.get()).upper(),)
                self.execute_function(query, values, "deleted")

    # function for clearing the values in the all input form widgets
    def clear(self):
        self.txt_RegNo.config(state='normal')
        self.txt_Course.set("")
        self.txt_gender.set("")
        self.txt_RegNo.delete(0, END)
        self.txt_Name.delete(0, END)
        self.txt_Email.delete(0, END)
        self.std_Table.selection_remove(self.std_Table.focus())
        self.std_Table.selection_clear()

    # function for assigning the selected row in the student list to input form
    def get_data(self, ev):
        row=self.std_Table.focus()
        contents=self.std_Table.item(row)
        data=contents['values']
        self.regNO.set(data[0])
        self.Name.set(data[1])
        self.txt_Course.set(data[2])
        self.txt_gender.set(data[3])
        self.Email.set(data[4])
        self.txt_RegNo.config(state='disabled')


window = Tk()
studObj = Student(window)
window.mainloop()
