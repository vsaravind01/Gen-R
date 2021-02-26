import csv
import tkinter as tk
from subprocess import Popen, call
from tkinter import PhotoImage, ttk
from tkinter import messagebox
import datetime
import Tooltip
import json
import dbexport
import logger


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        root.title("Report Generator")
        logger.log(log=f"Logged into Report Generator : {datetime.datetime.now()}\n")

        self.database = "records.csv"
        # Menubar

        menu = tk.Menu(self)
        root.config(menu=menu)

        file = tk.Menu(menu, tearoff=False)
        file.add_command(label="Refresh", command=self.refresh, accelerator='(F5)')
        file.add_command(label="Exit", command=self.quit, accelerator='(Alt+F4)')
        menu.add_cascade(label="File", menu=file)

        edit = tk.Menu(menu, tearoff=False)
        edit.add_command(label="Upload Data", command=self.upload, accelerator='(Enter)')
        edit.add_command(label="Clear Entries", command=lambda:
        self.clear(
            [self.name,
             self.Class,
             self.section,
             self.admin,
             self.subject1_,
             self.subject2_,
             self.subject3_,
             self.subject4_,
             self.subject5_]
        ),
                         accelerator='(Alt+C)'
                         )
        edit.add_command(label="Edit Subject Details", command=self.CreateTop)
        edit.add_command(label="Data Backup", command=self.export)
        menu.add_cascade(label="Edit", menu=edit)

        run = tk.Menu(menu, tearoff=False)
        run.add_command(label="Open CSV file", command=self.openCsv, accelerator='(Ctrl+O)')
        run.add_command(label="Generate Report (PDF)", command=self.pdfGen, accelerator='(Ctrl+G)')
        menu.add_cascade(label="Run", menu=run)

        self.icon = PhotoImage(file='report_generator.jpg')

        self.pack(ipadx=200, ipady=200)
        self.createWidgets()

    # GUI Widgets management

    def createWidgets(self):

        # Validation Functions

        # Name can contain only Alphabets or Space(" ") or dot(".")
        def nameChk(value="", current=""):
            nameValidate = False
            self.statusbar.configure(text=f"Typing Name...")
            if value in (" ", ".") or value.isalpha():
                nameValidate = True
            return nameValidate

        def classChk(value="", current=""):
            self.statusbar.configure(text="Typing Class...")
            if len(current) > 2:
                return False
            else:
                return value.isdigit()

        def sectionChk(value="", current=""):
            self.statusbar.configure(text="Typing Section...")
            if len(current) <= 1:
                return value.isalpha()
            else:
                return False

        def adminChk(value=""):  # Admission_Number can contain only Numbers or frontslash("/")
            adminValidate = False
            self.statusbar.configure(text="Typing Admission Number...")
            if value == "/" or value.isdigit():
                adminValidate = True
            return adminValidate

        def marksChk(value="", current=""):  # Marks can contain any Numerical value
            self.statusbar.configure(text="Typing Marks...")
            if len(current) > 3:
                return False
            else:
                return value.isdigit()

        self.sub = []
        with open(self.database, "r") as file:
            read = csv.reader(file)
            self.sub = next(read)

        with open('data.json', 'r') as jsonFile:
            self.data = json.load(jsonFile)

        # Frames Creation
        self.container = tk.Frame(self)  # Principal Frame
        # Frame for Details Collection ==> (Principal Frame)
        self.details = tk.Frame(self.container)
        # Frame for Marks Collection ==> (Principal Frame)
        self.marks = tk.Frame(self.container)
        self.buttons = tk.Frame(self)  # Frame for Buttons

        # Tooltip for marks range
        Tooltip.CreateToolTip(self.marks, text=f"Range(0-{self.data['max']})")

        heading = tk.Label(self, text="Report Generator", fg="black", bg="grey65", width=200, height=3,
                           font=("Century", 16))
        heading.pack(side=tk.TOP, fill=tk.X)
        self.statusbar = tk.Label(self, text="Resources Build Successful…", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Details Collection

        self.nameLabel = ttk.Label(self.details, text="Name")  # Name Label
        self.nameLabel.grid(row=0, column=0)

        # Valiation variables for Details Entry

        self.nameValidation = self.container.register(nameChk)
        self.classStatus = self.container.register(classChk)
        self.sectionStatus = self.container.register(sectionChk)

        self.name = ttk.Entry(self.details, validate="key",validatecommand=(self.nameValidation, '%S', '%P'))  # Name Entry
        self.name.grid(row=0, column=1)

        self.classLabel = ttk.Label(self.details, text="class")  # Class Label
        self.classLabel.grid(row=1, column=0)

        self.Class = ttk.Entry(self.details, validate="key", validatecommand=(self.classStatus, '%S', "%P"))  # Class Entry
        self.Class.grid(row=1, column=1)

        self.sectionLabel = ttk.Label(self.details, text="section")  # Section Label
        self.sectionLabel.grid(row=2, column=0)

        self.section = ttk.Entry(self.details, validate="key",validatecommand=(self.sectionStatus, '%S', "%P"))  # Section Entry
        self.section.grid(row=2, column=1)

        self.adminLabel = ttk.Label(self.details, text="admin")  # Admission Number Label
        self.adminLabel.grid(row=3, column=0)

        # Validation varible for Admission Number Entry
        self.adminvalidation = self.container.register(adminChk)

        self.admin = ttk.Entry(self.details, validate="key", validatecommand=(self.adminvalidation, '%S'))  # Admission Number Entry
        self.admin.grid(row=3, column=1)

        # Marks Collection

        self.marksValidation = self.container.register(marksChk)  # Validation Variable for Marks Entry

        self.subject1_Label = ttk.Label(self.marks, text=self.sub[4].title())
        self.subject1_Label.grid(row=0, column=0)

        self.subject1_ = ttk.Entry(self.marks, validate="key", validatecommand=(self.marksValidation, "%S", "%P"))
        self.subject1_.grid(row=0, column=1)

        self.subject2_Label = ttk.Label(self.marks, text=self.sub[5].title())
        self.subject2_Label.grid(row=1, column=0)

        self.subject2_ = ttk.Entry(self.marks, validate="key", validatecommand=(self.marksValidation, "%S", "%P"))
        self.subject2_.grid(row=1, column=1)

        self.subject3_Label = ttk.Label(self.marks, text=self.sub[6].title())
        self.subject3_Label.grid(row=2, column=0)

        self.subject3_ = ttk.Entry(self.marks, validate="key", validatecommand=(self.marksValidation, "%S", "%P"))
        self.subject3_.grid(row=2, column=1)

        self.subject4_Label = ttk.Label(self.marks, text=self.sub[7].title())
        self.subject4_Label.grid(row=3, column=0)

        self.subject4_ = ttk.Entry(self.marks, validate="key", validatecommand=(self.marksValidation, "%S", "%P"))
        self.subject4_.grid(row=3, column=1)

        self.subject5_Label = ttk.Label(self.marks, text=self.sub[8].title())
        self.subject5_Label.grid(row=4, column=0)

        self.subject5_ = ttk.Entry(self.marks, validate="key", validatecommand=(self.marksValidation, "%S", "%P"))
        self.subject5_.grid(row=4, column=1)

        # Buttons

        # Button to Upload Entries to "records.csv"
        self.add = ttk.Button(self.buttons, text="Add", command=self.upload)
        self.add.grid(row=0, column=0)

        # Button to Clear all entry fields
        self.clearBtn = ttk.Button(self.buttons,
                                   text="Clear",
                                   command=lambda:
                                   self.clear(
                                       [self.name,
                                        self.Class,
                                        self.section,
                                        self.admin,
                                        self.subject1_,
                                        self.subject2_,
                                        self.subject3_,
                                        self.subject4_,
                                        self.subject5_]
                                    )
                                )
        self.clearBtn.grid(row=0, column=1)

        # Frame packing (Grid Method)

        self.container.pack()  # Principal Frame Packing
        cover1 = tk.Label(self.container, text="\n")
        cover1.grid(row=0, column=5)
        self.details.grid(row=2, column=5)
        self.marks.grid(row=2, column=6)
        cover3 = tk.Label(self.container, text="\n\n\n")
        cover3.grid(row=9, column=0)
        self.buttons.pack()

        self.logs = tk.Text(self, height=20, width=45)
        self.logs.insert(tk.END, "\t\tAction Logs\n\n")
        self.logs.configure(state="disabled")
        self.logs.pack()

    # Functions

    # Function to Upload the Entries to "records.csv" (Alt+A)

    def upload(self, event=None):
        name = self.name.get()
        Class = self.Class.get()
        section = self.section.get()
        admin = self.admin.get()

        details = [name.title(), Class, section.upper(), admin]
        subjects = [self.sub[x].title() for x in range(4, 9)]
        marks = [self.subject1_.get(), self.subject2_.get(), self.subject3_.get(),
                 self.subject4_.get(), self.subject5_.get()]
        data = details + marks
        markAllocation = dict(zip(subjects, marks))

        for detail in tuple(details + marks):
            if detail == "":
                messagebox.showwarning(
                    "Warning", "Please fill all the fields.")
                self.statusbar.configure(text="Please fill all the fields...")
                return

        rangeFail = False
        rangeFailSubjects = []
        for mark in markAllocation:
            if int(markAllocation[mark]) > self.data['max'] or int(markAllocation[mark]) < 0:
                rangeFail = True
                rangeFailSubjects.append(mark)

        if rangeFail:
            rangeFailSubjectsString = ""
            for subject in tuple(rangeFailSubjects):
                rangeFailSubjectsString += subject + ","
            messagebox.showwarning("Warning",
                                   f"{rangeFailSubjectsString[:-1]} mark does not meet the required range (0-100).")
            self.statusbar.configure(
                text=f"{rangeFailSubjectsString[:-1]} mark does not meet the required range (0-100)...")
            return

        try:
            with open(self.database, "r") as readFile:
                read = csv.DictReader(readFile)
                for record in read:
                    if (record["name"] == name) or (record["admin"] == admin):
                        duplicateEntry = messagebox.askquestion(
                            "Warning",
                            f"{record['name']} (Admin : {record['admin']}) already exists!\nDo you want to upload it again?")
                        if duplicateEntry == 'no':
                            self.statusbar.configure(text="Duplication escaped...")
                            return

            with open(self.database, "a", newline='\n') as file:
                write = csv.writer(file)
                write.writerow(data)
                self.logs.configure(state="normal")
                self.logs.insert(tk.END, f"{name}-{admin}\n")
                logger.log(log=f"{name}-{admin}   {datetime.datetime.now()}\n")
                for subject in markAllocation:
                    self.logs.insert(tk.END, f"{subject} : {markAllocation[subject]}\n")
                    logger.log(log=f"{subject} : {markAllocation[subject]}\n")
                self.logs.insert(tk.END, "\n")
                logger.log(log="\n")
                self.logs.configure(state="disabled")
                self.statusbar.configure(text="Details Uploaded to 'records.csv'...")

        except Exception as e:
            self.logs.configure(state="normal")
            self.logs.insert(tk.END, f"\nA {e.__class__.__name__} occured while \nopening 'records.csv'\n\n")
            logger.log(log=f"\nA {e.__class__.__name__} occured while opening 'records.csv'\n\n")
            self.logs.configure(state="disabled")

    # Function to clear all Entry Fields (Alt+C)

    def clear(self, entries=[], event=None):
        for entry in entries:
            entry.delete(0, 'end')

    # Function to call PDF generating program "report.py" (Ctrl+G)

    def pdfGen(self, event=None):  # Function to call PDF generating program "report.py" (Ctrl+G)
        repGen = messagebox.askquestion(
            "Generate Reports", "Do you want to generate the reports now?")
        if repGen == 'yes':
            self.logs.configure(state="normal")
            # PDF report Generation log
            self.logs.insert(
                tk.END, f"Pdf Generated :\n\t\t{datetime.datetime.now()}\n\n")
            logger.log(log=f"Pdf Generated :\t{datetime.datetime.now()}\n")
            self.logs.configure(state="disabled")
            print(datetime.datetime.now())
            call(["python", "report.py"])
            print(datetime.datetime.now())
            self.statusbar.configure(text="Reports Generated...")
        else:
            return

    # Function to Open CSV file with the default CSV viewing Software [Eg : 'Microsoft Excel'] (Ctrl+O)

    def openCsv(self, event=None):
        Popen(self.database, shell=True)
        self.logs.configure(state="normal")
        # CSV file request log
        self.logs.insert(tk.END, f"CSV request initiated :\n\t\t{datetime.datetime.now()}\n\n")
        logger.log(log=f"CSV request initiated :\t{datetime.datetime.now()}\n")
        self.logs.configure(state="disabled")
        self.statusbar.configure(text="CSV request initiated...")

    # Function to Quit Application

    def quit(self, event=None):
        self.statusbar.configure(text="Quit initiated...")
        quit_request = messagebox.askquestion("Confirm", "Do you want to quit?")
        if quit_request == 'yes':
            logger.log(log=f"Quitted Report Generator : {datetime.datetime.now()}\n\n")
            root.destroy()
        else:
            return

    # Function to refresh the window

    def refresh(self, event=None):
        self.destroy()
        self.__init__()

    def export(self):
        backuptrigger = messagebox.askquestion("Confirm",
                                               "Your backup data will be stored at 'DB-Backup/RG-backup.db'.\nIt's a Sqlite Database.\nAre you sure?")
        if backuptrigger == 'no':
            return
        else:
            dbexport.backup()
            self.logs.configure(state="normal")
            # PDF report Generation log
            self.logs.insert(tk.END, f"Backup Successful :\n\t\t{datetime.datetime.now()}\n\n")
            self.logs.configure(state="disabled")
            self.statusbar.configure(text="Data Backup Successful...")

    # Function to  create a Toplevel window to Edit the Subject details.

    def CreateTop(self):
        win = tk.Toplevel()
        win.iconphoto(False, self.icon)
        windowWidth = win.winfo_reqwidth()
        windowHeight = win.winfo_reqheight()
        # Gets both half the screen width/height and window width/height
        positionRight = int(win.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = int(root.winfo_screenheight() / 3 - windowHeight / 2)
        win.geometry("500x500+{}+{}".format(positionRight, positionDown))
        win.grab_set()
        buttons = tk.Frame(win)

        def subName(value=""):
            self.statusbar.configure(text="Typing Subject Name...")
            return value.isalnum()

        subjects = tk.Frame(win)
        SubName = subjects.register(subName)

        subject1_Label = ttk.Label(subjects, text=self.sub[4].title())
        subject1_Label.grid(row=0, column=0)

        subject1_ = ttk.Entry(subjects, validate="key", validatecommand=(SubName, "%S"))
        subject1_.grid(row=0, column=1)

        subject2_Label = ttk.Label(subjects, text=self.sub[5].title())
        subject2_Label.grid(row=1, column=0)

        subject2_ = ttk.Entry(subjects, validate="key", validatecommand=(SubName, "%S"))
        subject2_.grid(row=1, column=1)

        subject3_Label = ttk.Label(subjects, text=self.sub[6].title())
        subject3_Label.grid(row=2, column=0)

        subject3_ = ttk.Entry(subjects, validate="key", validatecommand=(SubName, "%S"))
        subject3_.grid(row=2, column=1)

        subject4_Label = ttk.Label(subjects, text=self.sub[7].title())
        subject4_Label.grid(row=3, column=0)

        subject4_ = ttk.Entry(subjects, validate="key", validatecommand=(SubName, "%S"))
        subject4_.grid(row=3, column=1)

        subject5_Label = ttk.Label(subjects, text=self.sub[8].title())
        subject5_Label.grid(row=4, column=0)

        subject5_ = ttk.Entry(subjects, validate="key", validatecommand=(SubName, "%S"))
        subject5_.grid(row=4, column=1)

        maxMarksLabel = ttk.Label(subjects, text="Maximum Marks")
        maxMarksLabel.grid(row=5, column=0)

        maxMarks = ttk.Entry(subjects, validate="key", validatecommand=(self.marksValidation, "%S", "%P"))
        maxMarks.grid(row=5, column=1)

        change = ttk.Button(buttons, text="Change",
                            command=lambda: Change(entries=[subject1_.get(), subject2_.get(), subject3_.get(),
                                                            subject4_.get(), subject5_.get()],
                                                   maxMarks=maxMarks.get()))
        change.grid(row=0, column=0)

        clear = ttk.Button(buttons, text="Clear", command=lambda: self.clear([self.name,
                                                                              self.Class,
                                                                              self.section,
                                                                              self.admin,
                                                                              subject1_,
                                                                              subject2_,
                                                                              subject3_,
                                                                              subject4_,
                                                                              subject5_,
                                                                              maxMarks]))
        clear.grid(row=0, column=1)

        fake = ttk.Label(win, text="\t\t\t")
        fake.grid(row=0, column=1)
        head = tk.Label(win, text="Edit Subjects", fg="black", font=("Century", 16))
        head.grid(row=0, column=1)
        fake = ttk.Label(win, text="\n\t\t")
        fake.grid(row=1, column=0)
        subjects.grid(row=1, column=1)
        buttons.grid(row=2, column=1)

        def Change(entries=[], maxMarks=""):
            oldSubjects = [self.sub[x].lower() for x in range(4, 9)]
            finalList = []
            for (entry, oldSubject) in zip(entries, oldSubjects):
                if entry == "":
                    finalList.append(oldSubject.title())
                else:
                    finalList.append(entry.title())
            finalListStr = ""
            for i in finalList:
                finalListStr += i + ","

            if maxMarks == "":
                self.statusbar.configure(text="Maximum Marks not specified...")
                maxNil = messagebox.askquestion("Confirm",
                                                f"You haven't given Maximum Mark!\nIf you don't Enter the maximum mark then the former maximum mark ({self.data['max']}).\n Are you sure?")
                if maxNil == 'no':
                    return
                else:
                    upload(finalList=finalList, maxMarks=str(self.data['max']))
                    self.statusbar.configure(
                        text="Subjects edited to " + finalListStr[:-1] + " and the Maximum mark now is " + str(
                            self.data['max']))
                    logger.log(
                        log=f"Subjects Names Updated :\t{datetime.datetime.now()}\nSubjects edited to " + finalListStr[
                                                                                                          :-1] + "\n\n")
            else:
                upload(finalList=finalList, maxMarks=maxMarks)
                logger.log(
                    log=f"Subjects Names Updated :\t{datetime.datetime.now()}\nSubjects edited to " + finalListStr[
                                                                                                      :-1] + "\n\n")
                self.statusbar.configure(
                    text="Subjects edited to " + finalListStr[:-1] + " and the Maximum mark now is " + str(maxMarks))

        def upload(finalList, maxMarks):
            temp = []
            try:
                with open('records.csv', 'r') as infile:
                    reader = csv.reader(infile, skipinitialspace=True)
                    temp.extend(reader)
                temp[0] = [self.sub[x] for x in range(0, 4)] + finalList
                with open('records.csv', 'w', newline="\n") as outfile:
                    writer = csv.writer(outfile, quoting=csv.QUOTE_NONE, skipinitialspace=True)
                    writer.writerows(temp)
                    self.logs.configure(state="normal")
                    # Subject names updation log
                    self.logs.insert(tk.END, f"Subjects Names Updated :\n\t\t{datetime.datetime.now()}\n\n")
                    self.logs.configure(state="disabled")
                del temp

                Max = {"max": int(maxMarks)}
                with open('data.json', 'w') as file:
                    json.dump(Max, file, ensure_ascii=False, indent=4)
                    self.logs.configure(state="normal")
                    # maximum marks updation log
                    self.logs.insert(tk.END, f"Maximum Mark Changed to {maxMarks} :\n\t\t{datetime.datetime.now()}\n\n")
                    logger.log(log=f"Maximum Mark Changed to {maxMarks} :\t{datetime.datetime.now()}\n")
                    self.logs.configure(state="disabled")
            except Exception as e:
                self.logs.configure(state="normal")
                self.logs.insert(tk.END, f"\nA {e.__class__.__name__} occured while \nopening 'records.csv'\n\n")
                logger.log(log=f"\nA {e.__class__.__name__} occured while opening 'records.csv'\n\n")
                self.logs.configure(state="disabled")


# main Method


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    app = Application(root)

    # Key-Bindings

    root.bind("<Alt-c>",
              lambda events:
              app.clear([
                  app.name,
                  app.Class,
                  app.section,
                  app.admin,
                  app.subject1_,
                  app.subject2_,
                  app.subject3_,
                  app.subject4_,
                  app.subject5_]
                  )
              )
    root.bind("<Alt-C>", app.clear)
    root.bind("<Return>", app.upload)
    root.bind("<Control-o>", app.openCsv)
    root.bind("<Control-O>", app.openCsv)
    root.bind("<Control-g>", app.pdfGen)
    root.bind("<Control-G>", app.pdfGen)
    root.bind("<F5>", app.refresh)
    root.bind("<Alt-F4>", app.quit)

    app.mainloop()