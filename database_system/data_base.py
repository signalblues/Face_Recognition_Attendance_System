import time
import MySQLdb as mdb


global count1,count2
count1=count2=1


con = mdb.connect('localhost', 'it', 'itdep', 'it_branch_attendabce');


def get_attendance(case,data):
    case = int(case)
    
    def student_db_get(inf1):
        inf1 = int(inf1)
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM student_db")
            for i in range(cur.rowcount):
                s_id,s_f_p,s_name,s_sem,s_usn = cur.fetchone()

            if s_f_p == inf1:
                return (str(s_id),str(s_f_p),s_name,s_sem,s_usn)

            else:
                m='no_db'
                return(m,' ',' ',' ',' ')
                

    def faculty_db_get(inf2):
        inf2 = int(inf2)
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM lecturer_db")
            for i in range(cur.rowcount):
                f_id,f_f_p,f_name = cur.fetchone()

            if f_f_p==inf2:
                return(str(f_id),str(f_f_p),f_name,' ',' ')

            else:
                m='no_db'
                return(m,' ',' ',' ',' ')

    if case==0:
        msg1,msg2,msg3,msg4,msg5=faculty_db_get(data)
        return(msg1,msg2,msg3,msg4,msg5)

    elif case==1:
        msg1,msg2,msg3,msg4,msg5=student_db_get(data)
        return(msg1,msg2,msg3,msg4,msg5)
    




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
        print id_loc,f_n,attendace
        

def delete_first_db(position):
    position = int(position)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM first_db")
        cur.execute("delete from first_db where finger_position='%s'",(position,))
        con.commit()
        print 'deleted'

'''
first_year_db()
update_firstyear_db(0,'chetan','A')
'''



