import os
import xlsxwriter
import time
import MySQLdb as mdb
import time
import subprocess

global admin_menu,admin_menu_dummy,admin_window,admin_label
global result_btn,run_voting,yr1,yr2,yr3,yr4,back,ok,msg
global result,voting,excel
result=voting=0

con = mdb.connect('localhost', 'it', 'itdep', 'it_branch_attendabce');
cursor = con.cursor()

class adminMyOptionMenu(tk.OptionMenu):
        def __init__(self, master, status, *options):
                self.var = tk.StringVar(master)
                self.var.set(status)
                tk.OptionMenu.__init__(self, master, self.var, *options)
                self.config(font=('calibri', (10)), bg='white', width=12, fg='dark red')
                self['menu'].config(font=('calibri', (10)), bg='white', fg='dark blue')
                      

        def progress(self,x):
                global admin_menu,admin_menu_dummy,admin_window,admin_label
                global result_btn,run_voting,yr1,yr2,yr3,yr4,back,ok,msg
                global result,voting,excel

                import Voting_Data_Base
                import voting_result_db
                import delete

                back.config(state='disabled')
                ok.config(state='disabled')
                
                Voting_Data_Base.first_year_db()
                Voting_Data_Base.second_year_db()
                Voting_Data_Base.third_year_db()
                Voting_Data_Base.fourth_year_db()
                Voting_Data_Base.candidate_db()

                voting_result_db.first_year_resultdb()
                voting_result_db.second_year_resultdb()
                voting_result_db.third_year_resultdb()
                voting_result_db.fourth_year_resultdb()

                msg = delete.delete_template_finger_image(x)

                print x

                admin_label = tk.Label(admin_window,background="white",text='                                                                                                                                       ', font=('calibri', (14)),
                                       fg='dark blue').place(relx=0.5, rely=0.8, anchor="c")

                admin_label = tk.Label(admin_window,background="white",text=msg, font=('calibri', (14)),
                                       fg='dark blue').place(relx=0.5, rely=0.8, anchor="c")


        def mysqltoexcel(self):
                global result,voting,excel
                global admin_menu,admin_menu_dummy,admin_window,admin_label
                global result_btn,run_voting,yr1,yr2,yr3,yr4,back,ok,msg
                
                import MySQLdb as mdb
                import xlsxwriter
                
                con = mdb.connect('localhost', 'voting_user', 'votesym', 'voting_system');
                cursor = con.cursor()

                cursor.execute("SELECT * FROM first_year_db")
                
                first_yearworkbook = xlsxwriter.Workbook('/home/pi/Desktop/Student_Projects/Voting_System/Exported_excel_data/firstyear.xlsx')
                sheet1 = first_yearworkbook.add_worksheet()
                for r, row in enumerate(cursor.fetchall()):
                        for c, col in enumerate(row):
                                sheet1.write(r, c, col)

                first_yearworkbook.close()


                cursor.execute("SELECT * FROM second_year_db")               

                second_yearworkbook = xlsxwriter.Workbook('/home/pi/Desktop/Student_Projects/Voting_System/Exported_excel_data/secondyear.xlsx')
                sheet2 = second_yearworkbook.add_worksheet()
                for r, row in enumerate(cursor.fetchall()):
                        for c, col in enumerate(row):
                                sheet2.write(r, c, col)

                second_yearworkbook.close()
                

                cursor.execute("SELECT * FROM third_year_db")

                third_yearworkbook = xlsxwriter.Workbook('/home/pi/Desktop/Student_Projects/Voting_System/Exported_excel_data/thirdyear.xlsx')
                sheet3 = third_yearworkbook.add_worksheet()
                for r, row in enumerate(cursor.fetchall()):
                        for c, col in enumerate(row):
                                sheet3.write(r, c, col)

                third_yearworkbook.close()


                cursor.execute("SELECT * FROM fourth_year_db")
                
                fourth_yearworkbook = xlsxwriter.Workbook('/home/pi/Desktop/Student_Projects/Voting_System/Exported_excel_data/fourthyear.xlsx')
                sheet4 = fourth_yearworkbook.add_worksheet()
                for r, row in enumerate(cursor.fetchall()):
                        for c, col in enumerate(row):
                                sheet4.write(r, c, col)

                fourth_yearworkbook.close()


                cursor.execute("SELECT * FROM candidate_db")

                candidate_workbook = xlsxwriter.Workbook('/home/pi/Desktop/Student_Projects/Voting_System/Exported_excel_data/candidate.xlsx')
                sheet5 = candidate_workbook.add_worksheet()
                for r, row in enumerate(cursor.fetchall()):
                        for c, col in enumerate(row):
                                sheet5.write(r, c, col)

                candidate_workbook.close()

                excel.config(state='disabled')

                admin_label = tk.Label(admin_window,background="white",text='                                                                                                                                       ', font=('calibri', (14)),
                                       fg='dark blue').place(relx=0.5, rely=0.8, anchor="c")

                admin_label = tk.Label(admin_window,background="white",text='Excell sheet generated successfully', font=('calibri', (14)),
                                       fg='dark blue').place(relx=0.5, rely=0.8, anchor="c")
                time.sleep(1)

                admin_label = tk.Label(admin_window,background="white",text='                                                                                                                                       ', font=('calibri', (14)),
                                       fg='dark blue').place(relx=0.5, rely=0.8, anchor="c")

                admin_label = tk.Label(admin_window,background="white",text='click OK to clear data-base, wait for few minutes', font=('calibri', (14)),
                                       fg='dark blue').place(relx=0.5, rely=0.8, anchor="c")

                ok.config(state='active')
                


def run_admin_page():
        global result,voting,excel
        global admin_menu,admin_menu_dummy,admin_window,admin_label
        global result_btn,run_voting,yr1,yr2,yr3,yr4,back,ok
        result=voting=0

        admin_window = tk.Toplevel()
        admin_window.geometry('800x479')
        admin_window.config(background="white")
        admin_window.wm_title("Clear DB")
        admin_window.columnconfigure(0, weight=1)
        admin_window.columnconfigure(1, weight=1)

        admin_logo_image = Image.open("LOGO.png")
        admin_logo_photo = ImageTk.PhotoImage(admin_logo_image)
        admin_label = tk.Label(admin_window,image=admin_logo_photo)
        admin_label.admin_logo_image = admin_logo_photo
        admin_label.place(relx=0.1, rely=0.08, anchor="c")

        admin_border_image1 = Image.open("BORDER.png")
        admin_border_photo1 = ImageTk.PhotoImage(admin_border_image1)
        admin_label = tk.Label(admin_window,image=admin_border_photo1)
        admin_label.admin_border_image1 = admin_border_photo1 # keep a reference!
        admin_label.place(relx=0.5, rely=0.95, anchor="c")

        mainlabel = tk.Label(admin_window,background="white",text='SMART VOTING SYSTEM-Clear Database System', font=('calibri', (14)),
                             fg='dark blue').place(relx=0.5, rely=0.1, anchor="c")


        admin_label = tk.Label(admin_window,background="white",text='                                                                                                                                       ', font=('calibri', (14)),
                         fg='dark blue').place(relx=0.5, rely=0.8, anchor="c")

        admin_label = tk.Label(admin_window,background="white",text='create excell file by clicking CREATE-EXCELL button', font=('calibri', (14)),
                         fg='dark blue').place(relx=0.5, rely=0.8, anchor="c")

        admin_menu_dummy = adminMyOptionMenu(admin_window, 'Select Option', '')

        back=tk.Button(admin_window,text="BACK",command=admin_menu_dummy.settings)
        back.place(relx=0.7, rely=0.3, anchor="c")
        back.config(width="10",height="5")

        ok=tk.Button(admin_window,text="OK",command=admin_menu_dummy.System_run)
        ok.place(relx=0.4, rely=0.3, anchor="c")
        ok.config(state='disabled',width="10",height="5")

        excel=tk.Button(admin_window,text="CREATE-EXCELL",command=admin_menu_dummy.mysqltoexcel)
        excel.place(relx=0.55, rely=0.5, anchor="c")
        excel.config(state='active',width="10",height="3")

