import time
import MySQLdb as mdb
import os
import xlsxwriter



global count1,count2
count1=count2=1


con = mdb.connect('localhost', 'it', 'itdep', 'it_branch_attendabce');

############# First DB  ################

def first_db():
    with con:
        
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS first_db")

        firstdb = """CREATE TABLE first_db(Id INT , first_name CHAR(20), mark_att CHAR(20))"""

        cur.execute(firstdb)


def update_first_db(id_loc,f_n,attendace):
    global count1,count2
    id_loc = int(id_loc)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM first_db")
        
        #cur.execute ("INSERT into first_year_db (Id,fs_position, full_name2, semester,usn) values('%s','%s',%s,%s,%s)",(s_id_loc,s_id_loc, s_name, sem,us))

        cur.execute ("INSERT into first_db(Id,first_name,mark_att) values('%s',%s,%s)",(id_loc,f_n,attendace))
                
        con.commit()
        #print id_loc,f_n,attendace

def update_db(m,n):
    with con:
        cur = con.cursor()
        cur.execute ("""UPDATE first_db SET mark_att=%s WHERE first_name=%s""", (m,n))
        

def delete_first_db(position):
    position = int(position)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM first_db")
        cur.execute("delete from first_db where finger_position='%s'",(position,))
        con.commit()
        print 'deleted'

    
def mysqltoexcel():
    import xlsxwriter
    cursor = con.cursor()
    cursor.execute("SELECT * FROM first_db")

    attendance_sheet = xlsxwriter.Workbook('attendance_sheet.xlsx')
    sheet1 = attendance_sheet.add_worksheet()
    for r, row in enumerate(cursor.fetchall()):
        for c, col in enumerate(row):
            sheet1.write(r, c, col)

    attendance_sheet.close()





