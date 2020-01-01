from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3


class Student:
    def __init__(self, master):
        self.txt_gender = StringVar()
        self.regNO=StringVar()
        self.Name=StringVar()
        self.Email=StringVar()
        self.emailvalid = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        self.master=master
        self.master.geometry("1000x600")
        self.title = Label(self.master, text="MANAGE STUDENT DETAILS", font=("Helvetica", 20))
        self.title.pack(side=TOP, fill=X)
        # -----------Manage Frame-------------
        self.std_Manage_Frame = Frame(self.master, bd=2, relief=RIDGE)
        self.std_Manage_Frame.place(x=20, y=50, width=300, height=500)

        self.lbl_RegNo = Label(self.std_Manage_Frame, text="REGISTER NO")
        self.lbl_RegNo.grid(row=1, column=0, padx=10, pady=10)
        self.txt_RegNo = Entry(self.std_Manage_Frame, textvariable=self.regNO, bd=2, width=25)
        self.txt_RegNo.grid(row=1, column=2)

        self.lbl_Name = Label(self.std_Manage_Frame, text="NAME")
        self.lbl_Name.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.txt_Name = Entry(self.std_Manage_Frame, textvariable=self.Name, bd=2, width=25)
        self.txt_Name.grid(row=2, column=2)

        self.lbl_Course = Label(self.std_Manage_Frame, text="COURSE")
        self.lbl_Course.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.txt_Course = ttk.Combobox(self.std_Manage_Frame, width=22, values=["BCA", "BBA", "BCA", "B-COM", "MBA", "MCA"])
        self.txt_Course.grid(row=3, column=2)

        self.lbl_Gender = Label(self.std_Manage_Frame, text="GENDER")
        self.lbl_Gender.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.radio_male = Radiobutton(self.std_Manage_Frame, text="Male", variable=self.txt_gender, value="Male")
        self.radio_male.place(x=90, y=130)
        self.radio_female = Radiobutton(self.std_Manage_Frame, text="Female", variable=self.txt_gender, value="Female")
        self. radio_female.place(x=150, y=130)

        self.lbl_Email = Label(self.std_Manage_Frame, text="E-MAIL")
        self.lbl_Email.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.txt_Email = Entry(self.std_Manage_Frame, textvariable=self.Email, bd=2, width=25)
        self.txt_Email.grid(row=5, column=2)
        # --------Form Control buttons-------------
        self.btn_Add = Button(self.std_Manage_Frame, text="ADD", width=15, command=self.insert)
        self.btn_Add.place(x=26, y=260)
        self.btn_Update = Button(self.std_Manage_Frame, text="UPDATE", width=15, command=self.update)
        self.btn_Update.place(x=160, y=260)
        self.btn_Delete = Button(self.std_Manage_Frame, text="DELETE", width=15, command=self.delete)
        self.btn_Delete.place(x=26, y=290)
        self.btn_Clear = Button(self.std_Manage_Frame, text="CLEAR", width=15, command=self.clear)
        self.btn_Clear.place(x=160, y=290)
        # ---------Details Frame-------------
        self.std_Details_Frame = Frame(window, bd=2, relief=RIDGE)
        self.std_Details_Frame.place(x=350, y=50, width=610, height=500)
        self.scroll_x = Scrollbar(self.std_Details_Frame, orient=HORIZONTAL)
        self.scroll_y = Scrollbar(self.std_Details_Frame, orient=VERTICAL)
        self.std_Table = ttk.Treeview(self.std_Details_Frame,
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

    def display(self):
        self.cursor.execute("SELECT * FROM students")
        records=self.cursor.fetchall()
        if len(records) !=0:
            self.std_Table.delete(*self.std_Table.get_children())
            for row in records:
                self.std_Table.insert('', END, values=row)

    def validation(self, status):
        if len(self.txt_RegNo.get())==0:
            self.txt_RegNo.focus
            messagebox.showerror("Validation Error", "You Muster Enter a Register Number")
            return 0
        if len(self.txt_Name.get())==0:
            self.txt_Course.focus
            messagebox.showerror("Validation Error", "You Must Enter a Name")
            return 0
        if len(self.txt_Course.get())==0:
            self.txt_Course.focus
            messagebox.showerror("Validation Error", "You Must Select a Course")
            return 0
        if len(self.txt_gender.get())==0:
            messagebox.showerror("Validation Error", "You Must Select Gender")
            return 0
        if len(self.txt_Email.get())==0:
            self.txt_Email.focus
            messagebox.showerror("Validation Error", "You Must Enter a Email Id")
            return 0
        if self.emailvalid.match(self.txt_Email.get()) is None:
            self.txt_Email.focus
            messagebox.showerror("Validation Error", "Please Enter a Valida Email-Id")
            return 0
        self.cursor.execute("SELECT * FROM students where RegNo=?", ((self.txt_RegNo.get()).upper(),))
        value=len(self.cursor.fetchall())
        print(status)
        if value > 0 and str(status)=="insert":
            messagebox.showerror("Integrity Error", "A student profile already exist with the given Register Number:"+self.txt_RegNo.get()+". Please try a new Register Number ")

            return 0
        if value<0 and str(status)=="update":
            messagebox.showerror("Integrity Error", "Student Profile Is Not Exist With The Given Register Number:"+self.txt_RegNo.get())
            return 0
        return 1

    def insert(self):
        if self.validation("insert")==1:
            self.cursor.execute("INSERT INTO students VALUES(?,?,?,?,?)", ((self.txt_RegNo.get()).upper(), self.txt_Name.get(), self.txt_Course.get(), self.txt_gender.get(), self.txt_Email.get()))
            self.con.commit()
            self.display()
            self.clear()

    def update(self):
        if self.validation("update")==1:
            self.cursor.execute("UPDATE students set Name=?, Course=?, Gender=?, Email=? ", (self.txt_Name.get(), self.txt_Course.get(), self.txt_gender.get(), self.txt_Email.get()))
            self.con.commit()
            self.clear()
            self.display()

    def delete(self):
        self.cursor.execute("DELETE FROM TABLE students WHERE RegNo=?", (self.txt_RegNo.get()))
        self.con.commit()
        self.clear()
        self.display()

    def clear(self):
        self.txt_Course.set("")
        self.txt_gender.set("")
        self.txt_RegNo.delete(0, END)
        self.txt_Name.delete(0, END)
        self.txt_Email.delete(0, END)

    def get_data(self, ev):
        row=self.std_Table.focus()
        contents=self.std_Table.item(row)
        data=contents['values']
        self.regNO.set(data[0])
        self.Name.set(data[1])
        self.txt_Course.set(data[2])
        self.txt_gender.set(data[3])
        self.Email.set(data[4])


window = Tk()
studObj = Student(window)
window.mainloop()
