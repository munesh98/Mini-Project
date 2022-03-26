import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QTableWidgetItem
from PyQt6.uic import loadUi
import mysql.connector as mc
import random
import time
import re
# Home page ----------------------------------------------------------------------------

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("Welcome1.ui", self)
        self.Admin.clicked.connect(self.admin)
        self.C_teacher.clicked.connect(self.c_teacher)
        self.S_teacher.clicked.connect(self.s_teacher)

    def admin(self):
        adminacc = Admin_Login()
        widget.addWidget(adminacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def c_teacher(self):
        c_teacher_acc = c_teacher()
        widget.addWidget(c_teacher_acc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def s_teacher(self):
        s_teacher_acc = s_teacher()
        widget.addWidget(s_teacher_acc)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# Admin Login page -------------------------------------------------------------------------------------------------

class Admin_Login(QDialog):
    def __init__(self):
        super(Admin_Login, self).__init__()
        loadUi("Admin_Login.ui", self)
        self.create_acc.clicked.connect(self.gotocreate)
        self.Change_pswd.clicked.connect(self.gotocreate_C)
        # self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Back.clicked.connect(self.createaccfunction)
        self.Login_admin.clicked.connect(self.gotocreate_Login)

    def gotocreate(self):
        tblname="admin_login_table"
       #---------------------------------------------------stored procedure---------------------------------------------------------
        mydb = mc.connect(
            host="localhost",
            user="root",
            password="Muneshismyname",
            database="student_database"
        )
        cursor = mydb.cursor()
        cursor.callproc('admin_count')  #admin_count is the name of the stored procedure created in mysql server

        for result in cursor.stored_results(): #from stored procedure we are retrieving the data
            value = result.fetchall()

       #----------------------------------------------------------------------------------------------------------------------------------
        for each in value:
            #print(each)
            try:
                u, *v = each
                #print(u)
                if u == 0:
                    createacc = CreateAcc()
                else:
                    createacc = CreateAcc_new()

            except Exception as e :
                self.result_label.setText("")

        #createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate_C(self):
        createacc = Change_pswd()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate_Login(self):
        try:
            tblname = "admin_login_table"

            username = self.user_name.text()
            if username == "":
                self.user_name_label.setText("Missing Username")
            else:
                self.user_name_label.setText("")

            password_ad = self.password.text()
            if password_ad == "":
                self.password_label.setText("Missing Password")
            else:
                self.password_label.setText("")

            if username and password_ad != "":

                mydb = mc.connect(
                    host="localhost",
                    user="root",
                    password="Muneshismyname",
                    database="student_database"
                )

                mycursor = mydb.cursor()
                sql = "SELECT * from  admin_login_table "
                mycursor.execute(sql, )
                result = mycursor.fetchall()
                m = len(result)
                list_admin = []
                if m != 0:
                    for each in result:
                        slnum, ad_nam,  pswd, mail = each
                        list_admin.append(ad_nam.upper())
                try :
                    if m != 0 :
                        for each in result:
                            slnum, ad_nam,  pswd, mail = each

                            if username.upper() in list_admin :

                                if username.upper() == ad_nam.upper():

                                    if pswd.upper()  == password_ad.upper() :
                                        status = "ONLINE"
                                        time_n=time.ctime()
                                        sql = "INSERT into  admin_logn_details( Admin_name,Status ,login_time) VALUES (%s, %s,%s)"
                                        val = (ad_nam , status, time_n)
                                        mycursor.execute(sql, val)
                                        mydb.commit()
                                        login = Admin_logged_in()
                                        widget.addWidget(login)
                                        widget.setCurrentIndex(widget.currentIndex() + 1)

                                    else:
                                        if password_ad.upper() != pswd.upper() :
                                            self.password_label.setText("Wrong Password")
                                            self.result_label.setText("Enter The Correct Password In The Shown Field")


                            else :
                                self.user_name_label.setText("Wrong Username")
                                self.result_label.setText("No Admin Account Exists With The Given Username")

                    else :
                        self.result_label.setText("")

                except Exception as e :
                    self.result_label.setText("")


            else :
                self.result_label.setText("                   Enter The Data In  The Shown Field")

        except mc.Error as e:
            self.result_label.setText("")


    def createaccfunction(self):
        #print("Successfully created acc with email and password")
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Admin_logged_in(QDialog):
    def __init__(self):
        super(Admin_logged_in, self).__init__()
        loadUi("Admin_Logged_in.ui", self)
        # self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Logout.clicked.connect(self.createaccfunction)
        self.Create_teach_acc.clicked.connect(self.gotocreate_Create_teach_acc)
        self.generate_otp.clicked.connect(self.gotocreate_Generate_otp)
        self.view_stat.clicked.connect(self.gotocreate_View_Stat)
        self.delete_teach_acc.clicked.connect(self.gotocreate_Delete_acc)

    def gotocreate_Create_teach_acc(self):
        login = Create_teach_acc()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate_Delete_acc(self):
        login = Delete_teach_acc()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate_Generate_otp(self):
        login = Generate_otp()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate_View_Stat(self):
        login = View_Stat()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def createaccfunction(self):


        #print("Successfully Logged out")
        mydb = mc.connect(
            host="localhost",
            user="root",
            password="Muneshismyname",
            database="student_database"
        )
        tblname="admin_logn_details"
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM {} ".format(tblname))
        result = mycursor.fetchall()
        for each in result:
            slnum, nam, stat, login,logout= each
            if stat == "ONLINE" :
                status = "OFFLINE"
                time_out = time.ctime()
                time_out = str(time_out)
                sql = "UPDATE admin_logn_details SET Status = %s , logout_time = %s WHERE Sl_No = %s"
                val = (status,time_out, slnum)
                mycursor.execute(sql, val)
                login = Admin_Login()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex() + 1)
#----------------------------------------------------------------------------------------------------------
class Delete_teach_acc(QDialog):
    def __init__(self):
        super(Delete_teach_acc, self).__init__()
        loadUi("Delete_lect_new.ui", self)
        self.Back.clicked.connect(self.deleteacc_function)
        self.Delete.clicked.connect(self.delete_function)

    def delete_function(self):
        try :
            sub_data = self.subject.text()
            if sub_data == "":
                self.sub_label.setText("Missing Subject")
            else:
                self.sub_label.setText("")

            name_data = self.name.text()
            if name_data == "":
                self.name_label.setText("Missing name")
            else:
                self.name_label.setText("")

            sec_data = self.section.text()
            if sec_data == "":
                self.sec_label.setText("Missing section")
            else:
                self.sec_label.setText("")

            sem_data = self.semester.text()
            if sem_data == "":
                self.sem_label.setText("Missing semester")
            else:
                self.sem_label.setText("")

            if sub_data and name_data and sec_data and sem_data != "":

                mydb = mc.connect(
                    host="localhost",
                    user="root",
                    password="Muneshismyname",
                    database="student_database"
                )
                mycursor = mydb.cursor()

                #tble_name = "teacher_accounts_new"
                query = "SELECT Sl_No , Lecturer_name  from teacher_accounts_new Group By  Lecturer_name"
                mycursor.execute(query, )
                result_new = mycursor.fetchall()
                #print(result_new)
                list_lect = []
                list_slno = []
                for each in result_new:
                    sl_no,name_req, *no_need = each
                    list_lect.append(name_req.upper())
                    list_slno.append(sl_no)

                #print(list_lect)

                if name_data.upper() in list_lect :

                    query = "SELECT Sl_No,Subject, Semester,Section  from teacher_accounts_new where Lecturer_name = %s "
                    value = (name_data,)
                    mycursor.execute(query, value)
                    result_new_one = mycursor.fetchall()
                    #print(result_new_one)
                    for each in result_new_one:
                        sl_num,sub_req,sem_req,sec_req, *no_need = each

                    if sub_data.upper() == sub_req.upper() and sec_data.upper() == sec_req.upper() and sem_data == sem_req :

                        try:
                            query = "DELETE from teacher_accounts_new  WHERE  Sl_No = %s"
                            value = (sl_num,)
                            mycursor.execute(query, value)
                            self.Result_label.setText("                             ACCOUNT DELETEION IS SUCCESSFULL")

                        except Exception as e:
                            pass


                    else :
                        if sub_data.upper() != sub_req.upper():
                            self.sub_label.setText("Invalid Subject")
                            self.Result_label.setText("                         ENTER THE SUBJECT OF THE  MENTIONED TEACHER NAME")

                        if sem_data.upper() != sem_req.upper():
                            self.sem_label.setText("Invalid Semester")
                            self.Result_label.setText("                         ENTER THE SEMESTER OF THE  MENTIONED TEACHER NAME")

                        if sec_data.upper() != sec_req.upper():
                            self.sec_label.setText("Invalid Semester")
                            self.Result_label.setText("                         ENTER THE SECTION OF THE  MENTIONED TEACHER NAME")

                        if sub_data.upper() != sub_req.upper() and sem_data.upper() != sem_req.upper() and sec_data.upper() != sec_req.upper():
                            self.Result_label.setText("                         ENTER THE DETAILS OF THE MENTIONED TEACHER NAME")



                else:
                    self.name_label.setText("Invalid name")
                    self.Result_label.setText("                 NO TEACHER ACCOUNT EXIST WITH THE GIVEN NAME")

            else:
                self.Result_label.setText("                               ENTER THE MISSING FIELD")

        except Exception as e :
            pass


    def deleteacc_function(self):
        # print("Successfully created acc with email and password")
        login = Admin_logged_in()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


#----------------------------------------------------------------------------------------------------------
class Create_teach_acc(QDialog):
    def __init__(self):
        super(Create_teach_acc, self).__init__()
        loadUi("Account_creation.ui", self)
        # self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.Logout.clicked.connect(self.createaccfunction)
        self.create__acc.clicked.connect(self.createacc_teachers)
        self.Reset_buttton.clicked.connect(self.createacc_teachers_reset)
        self.BACK.clicked.connect(self.createaccfunction)

    def createacc_teachers(self):
        try :
            lectname = self.username.text()
            if lectname == "":
                self.User_label.setText("Missing Username")
            else:
                self.User_label.setText("")

            email = self.email.text()
            if email == "":
                self.mail_label.setText("Missing Email")
            else:
                self.mail_label.setText("")

            password = self.password.text()
            if password == "":
                self.password_label.setText("Missing Password ")
            else:
                self.password_label.setText("")

            Subject = self.subject.text()
            if Subject == "":
                self.sub_label.setText("Missing Subject")
            else:
                self.sub_label.setText("")

            Position = self.position.text()
            if Position == "":
                self.position_label.setText("Missing Position")
            else:
                self.position_label.setText("")

            Semester = self.sem.text()
            if Semester == "":
                self.Semester_label.setText("Missing Semester")
            else:
                self.Semester_label.setText("")

            section = self.sect.text()
            if section == "":
                self.sect_label.setText("Missing Section")
            else:
                self.sect_label.setText("")

            length = len(password)
            #print(length)
            if lectname and email and password and Subject and Position and Semester and section != "":

                if  length == 8 :

                    emial_new = self.email.text()
                    ip_address = r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"
                    list2_ip = re.findall(ip_address, emial_new)

                    if list2_ip != []:
                        #print(list2_ip)

                        Sem_len  = len(Semester)

                        if Semester.isdigit() and Sem_len == 1:

                            Sec_len = len(section)

                            if section.isalpha() and Sec_len == 1:


                                if Position.upper() == "CLASS TEACHER" or Position.upper() == "SUBJECT TEACHER" :

                                    try:
                                        mydb = mc.connect(
                                            host="localhost",
                                            user="root",
                                            password="Muneshismyname",
                                            database="student_database"
                                        )
                                        tblname="admin_login_table"
                                        stat = "ONLINE"
                                        mycursor = mydb.cursor()
                                        query = "SELECT Admin_name  FROM admin_logn_details where Status = %s"
                                        value = (stat,)
                                        mycursor.execute(query, value)
                                        result = mycursor.fetchall()
                                        #print(result)
                                        list_ad = []
                                        for each in result :
                                            admin_N , *no_need= each
                                            #print(admin_N)
                                            list_ad.append(admin_N)

                                        admin_nm , *no_need = list_ad
                                        query = "INSERT INTO teacher_accounts_new(admin_name,Lecturer_name,Subject,Semester ,Section ,Position  ,PASSWORD ,Email) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                        value = (admin_nm, lectname, Subject, Semester, section, Position, password, email)
                                        mycursor.execute(query, value)
                                        mydb.commit()
                                        self.result_label.setText("                               ACCOUNT  CREATED   SUCCESSFULLY")
                                        # self.label_result.setText("Data Inserted")



                                    except Exception as e:
                                        self.result_label.setText("")

                                else :
                                    self.position_label.setText("POSITION ERROR")
                                    self.result_label.setText("           POSITION CAN ONLY BE CLASS TEACHER OR SUBJECT TEACHER ")

                            else:
                                self.sect_label.setText("SECTION ERROR")
                                self.result_label.setText("                 SECTION CAN ONLY BE A SINGLE CHARCTER ")

                        else:
                            self.Semester_label.setText("SEMESTER ERROR")
                            self.result_label.setText("                SEMESTER CAN ONLY BE A SINGLE NUMBER ")

                    else:
                        self.mail_label.setText("EMAIL ERROR")
                        self.result_label.setText("                    EMAIL FORMAT IS XYW@XYZ.XYZ ")

                else:
                    self.password_label.setText("PASSWORD ERROR")
                    self.result_label.setText(" PASSWORD CHARACTER SHOULD CONTAIN EXACTLY 8 CHARACTERS ")

            else:
                self.result_label.setText("                 ENTER THE MISSING FIELD FOR ACCOUNT  CREATION")
                #value = self.result_label.text()

        except Exception as e :
            self.result_label.setText("")

    def createacc_teachers_reset(self):
        self.username.setText("")
        self.User_label.setText("")
        self.email.setText("")
        self.mail_label.setText("")
        self.password.setText("")
        self.password_label.setText("")
        self.subject.setText("")
        self.sub_label.setText("")
        self.position.setText("")
        self.position_label.setText("")
        self.result_label.setText("")
        self.sem.setText("")
        self.Semester_label.setText("")
        self.sect.setText("")
        self.sect_label.setText("")

    def createaccfunction(self):
        #print("Successfully created acc with email and password")
        login = Admin_logged_in()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Generate_otp(QDialog):
    def __init__(self):

        super(Generate_otp, self).__init__()
        loadUi("Admin_OTP.ui", self)
        self.OTP_generator.clicked.connect(self.createacc_admin_OTP_gen)
        self.view_otp.clicked.connect(self.view_admin_OTP)
        self.Back.clicked.connect(self.createaccfunction)

    def createacc_admin_OTP_gen(self):
        try :
            tblname = "admin_otp"
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="Muneshismyname",
                database="student_database"
            )

            mycursor = mydb.cursor()
            mycursor.execute("SELECT COUNT(sl_no) FROM {} ".format(tblname))

            result_otp = mycursor.fetchall()
            #print(result_otp)
            for each in result_otp :
                cunt , *no_need =each

            if cunt == 0 :
                str1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                str2 = "abcdefghijklmnopqrstuvwxyz"
                str3 = "0123456789"
                str4 = "~!@#$%^&*"
                list1 = random.sample(str1, 1)
                # print(list1)
                list2 = random.sample(str2, 1)
                # print(list2)
                list3 = random.sample(str3, 1)
                list4 = random.sample(str4, 1)
                list1.extend(list2)
                list1.extend(list3)
                list1.extend(list4)
                # print(list1)
                random.shuffle(list1)
                otp = "".join(list1)
                #print(otp)
                self.label_result.setText("               " + otp)
                self.result_label.setText("")
                try :
                    val = otp
                    sql = "INSERT INTO admin_otp (otp) VALUES (%s)"
                    value = (val,)  # when inserting only single value use comma after the the single value as written.
                    # print(m)
                    mycursor.execute(sql, value)

                except Exception as e :
                    self.result_label.setText("")

            else :
                self.label_result.setText("")
                self.result_label.setText("                          OTP CAN BE GENERATED ONLY ONCE")

        except Exception as e :
            self.label_result.setText("")


    def view_admin_OTP(self) :
        try :
            tblname = "admin_otp"
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="Muneshismyname",
                database="student_database"
            )

            mycursor = mydb.cursor()
            mycursor.execute("SELECT otp FROM {} ".format(tblname))

            result_new_otp = mycursor.fetchall()
            #print(result_new_otp)

            if len(result_new_otp) !=0:

                for each in result_new_otp :
                    otp_view , *no_need =each

                self.result_label.setText("")
                self.label_result.setText("               " + otp_view)

            else :
                self.result_label.setText("                          OTP IS YET TO BE CREATED BY THE ADMIN ")

        except Exception as e :
            self.result_label.setText("")

    def createaccfunction(self):
        #print("Successfully created acc with email and password")
        login = Admin_logged_in()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class View_Stat(QDialog):
    def __init__(self):
        super(View_Stat, self).__init__()
        loadUi("Admin_View_user.ui", self)
        # self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.show_data.clicked.connect(self.Show_data_function)
        self.Back.clicked.connect(self.createaccfunction)

    def Show_data_function(self):

        try :
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="Muneshismyname",
                database="student_database"
            )

            mycursor = mydb.cursor()
            query = "SELECT Lecturer_name ,Subject ,semester ,section ,Position  ,Status  ,login_time ,logout_time from teacher_details_new "
            mycursor.execute(query,)
            result_new = mycursor.fetchall()
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result_new):
                # print(row_number , row_data)
                self.tableWidget.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        except Exception as e :
            pass


    def createaccfunction(self):
        login = Admin_logged_in()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# -------------------------------------------------------------------------------------------------------------------
# Class teacher Login
# -------------------------------------------------------------------------------------------------------------------


class c_teacher(QDialog):
    def __init__(self):
        super(c_teacher, self).__init__()
        loadUi("Login_CT.ui", self)
        # Form.resize(650, 500)
        # self.Create_acc.clicked.connect(self.gotocreate)
        self.Back.clicked.connect(self.createaccfunction)
        self.Change_pswd.clicked.connect(self.gotocreate_C)
        self.Login.clicked.connect(self.gotoLogin_CT)
        # self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def gotocreate_C(self):
        createacc = Change_pswd_c_teacher()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def createaccfunction(self):
        #print("Successfully created acc with email and password")
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoLogin_CT(self):

        try:
            tblname = "teacher_accounts_new"

            username = self.username.text()

            if username == "":
                self.username_label.setText("Missing Username")
            else:
                self.username_label.setText("")

            password = self.password.text()

            if password == "":
                self.password_label.setText("Missing Password")
            else:
                self.password_label.setText("")

            if username and password != "":
                #print(f"Successfully {username} created acc with email {email} and password {password}")
                mydb = mc.connect(
                    host="localhost",
                    user="root",
                    password="Muneshismyname",
                    database="student_database"
                )

                mycursor = mydb.cursor()
                Pos = "class Teacher"
                sql = "SELECT * from teacher_accounts_new  WHERE Position = %s"
                val = (Pos,)
                mycursor.execute(sql , val)
                result = mycursor.fetchall()
                m = len(result)
                list_ct = []
                if m != 0 :
                    for each in result:
                        slnum,ad_nam,lect,sub,sem,sec,postn,pswd,mail = each
                        list_ct.append(lect.upper())

                        if username.upper() in list_ct:

                            if username.upper() == lect.upper():

                                if  pswd.upper() == password.upper() :
                                    status = "ONLINE"
                                    time_cur = time.ctime()
                                    query = "INSERT INTO teacher_details_new(Lecturer_name,Subject,semester ,section ,Position	,Status ,login_time) VALUES (%s, %s, %s,%s,%s, %s, %s)"
                                    value = (lect, sub,sem,sec,postn,status,time_cur)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                    createacc = c_teacher_Login()
                                    widget.addWidget(createacc)
                                    widget.setCurrentIndex(widget.currentIndex() + 1)
                                else:
                                    if pswd.upper() != password.upper():
                                        self.password_label.setText("Wrong Password")

                                    self.result_label.setText("                       ENTER THE CORRECT PASSWORD IN THE SHOWN FIELD")

                        else:
                            self.username_label.setText("Wrong Username")
                            self.result_label.setText("              ACCOUNT WITH THE GIVEN USERNAME DOES NOT EXISTS ")



                else :
                    self.result_label.setText("")


            else :
                self.result_label.setText("                   ENTER THE DATA IN THE SHOWN FIELD")

        except mc.Error as e:
            pass



class c_teacher_Login(QDialog):
    def __init__(self):
        super(c_teacher_Login, self).__init__()
        loadUi("Class_Teacher.ui", self)
        #self.out.setText("WELCOME  TO STUDENT ATTENDENCE MANAGEMENT SYSTEM ")
        self.Logout.clicked.connect(self.createaccfunction)
        self.View_A_S_Sub.clicked.connect(self.goto_Specific_subject_Attendence)
        self.View_A_S_Student_Sub.clicked.connect(self.goto_View_Specific_student_Attendence)


    def goto_Specific_subject_Attendence(self):
        createacc = ViewAttendence_specific_subject_CT()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_View_Specific_student_Attendence(self):
        createacc = View_Specific_student_Attendence_CT()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def createaccfunction(self):

        mydb = mc.connect(
            host="localhost",
            user="root",
            password="Muneshismyname",
            database="student_database"
        )
        mycursor = mydb.cursor()
        Pos = "class Teacher"
        sql = "SELECT * from teacher_details_new  WHERE Position = %s"
        val = (Pos,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        for each in result:
            slnum, lectnam, sub, sem, sec, pos, stat, login, logout = each
            # print(slnum,lectnam,sub,pos,stat,login ,logout)
            if stat == "ONLINE":
                # print(stat)
                lout_time = time.ctime()
                status = "OFFLINE"
                sql = "UPDATE teacher_details_new SET Status = %s , logout_time = %s WHERE Sl_no = %s"
                val = (status, lout_time, slnum)
                mycursor.execute(sql, val)
                #result = mycursor.fetchall()
                # print(result)
                login = c_teacher()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex() + 1)

        #print("Successfully created acc with email and password")


class ViewAttendence_specific_subject_CT(QDialog):
    def __init__(self):
        super(ViewAttendence_specific_subject_CT, self).__init__()
        loadUi("View_att_CT_new1.ui", self)
        self.Back.clicked.connect(self.createaccfunction)
        self.show_data.clicked.connect(self.Show_function)
    # -----------------------------------------------------------------------------------------------------------

    def Show_function(self):

        sub_data = self.subject.text()
        if sub_data == "":
            self.sub_label.setText("Missing Subject")
        else:
            self.sub_label.setText("")

        sem_data = self.semester.text()
        if sem_data == "":
            self.sem_label.setText("Missing Semester")
        else:
            self.sem_label.setText("")

        sec_data = self.section.text()
        if sec_data == "":
            self.sec_label.setText("Missing Section")
        else:
            self.sec_label.setText("")

        date_data = self.date_opt.text()
        if date_data == "":
            self.date_label.setText("Missing Date")
        else:
            self.date_label.setText("")

        formt = self.date_opt.text()
        tup = re.findall("\d\d-\d\d-\d\d\d\d", formt)
        if len(tup) == 1:
            ok_date, *no_need = tup
        else:
            ok_date = ""

        try :
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="Muneshismyname",
                database="student_database"
            )
            mycursor = mydb.cursor()

            Pos = "subject teacher"

            query = "SELECT Subject  from teacher_accounts_new where Position = %s "
            value = (Pos,)
            mycursor.execute(query, value)
            result = mycursor.fetchall()
            list_sub=[]
            for each in result:
                Subject_one, *no_need = each
                list_sub.append(Subject_one.upper())

            if sub_data and sem_data and sec_data != "" and date_data == "":

                try:
                    mydb = mc.connect(
                        host="localhost",
                        user="root",
                        password="Muneshismyname",
                        database="student_database"
                    )

                    mycursor = mydb.cursor()

                    sub_data = sub_data.upper()
                    #print(list_sub)

                    if sub_data in list_sub:


                        Pos = "ONLINE"

                        query = "SELECT semester ,section  from teacher_details_new where Status = %s "
                        value = (Pos,)
                        mycursor.execute(query, value)
                        result = mycursor.fetchall()
                        for each in result:
                            sem_name, sec_name, *no_need = each

                        try:
                            if sem_data == sem_name and sec_data.upper() == sec_name.upper():

                                query = "SELECT Subject ,USN ,Status ,Semester ,Section ,Date from attendence_new  where   Subject = %s and Section = %s "
                                value = (sub_data,sec_data)
                                mycursor.execute(query, value)
                                result_new = mycursor.fetchall()
                                self.date_label.setText("")
                                self.Result_label.setText("")
                                if len(result_new) !=0 :
                                    self.tableWidget.setRowCount(0)
                                    for row_number, row_data in enumerate(result_new):
                                        self.tableWidget.insertRow(row_number)
                                        for column_number, data in enumerate(row_data):
                                            self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                                else :
                                    self.sub_label.setText("NO RECORD")
                                    self.Result_label.setText("THERE IS NO DATA STORED IN THAT SUBJECT")

                            else:

                                if sem_data != sem_name:
                                    self.date_label.setText("")
                                    self.sem_label.setText("ENTER CURRENT SEM")
                                    result_new = ""
                                    self.tableWidget.setRowCount(0)
                                    for row_number, row_data in enumerate(result_new):
                                        self.tableWidget.insertRow(row_number)
                                        for column_number, data in enumerate(row_data):
                                            self.tableWidget.setItem(row_number, column_number,
                                                                     QTableWidgetItem(str(data)))

                                if sec_data.upper() != sec_name.upper():
                                    self.date_label.setText("")
                                    self.sec_label.setText("ENTER CURRENT SECT")
                                    result_new = ""
                                    self.tableWidget.setRowCount(0)
                                    for row_number, row_data in enumerate(result_new):
                                        self.tableWidget.insertRow(row_number)
                                        for column_number, data in enumerate(row_data):
                                            self.tableWidget.setItem(row_number, column_number,
                                                                     QTableWidgetItem(str(data)))

                                self.date_label.setText("")
                                self.Result_label.setText("         ENTER THE CORRECT DETAILS IN THE FIELDS SHOWN")

                        except Exception as e:
                            pass

                    else:
                        result_new = ""
                        self.tableWidget.setRowCount(0)
                        for row_number, row_data in enumerate(result_new):
                            self.tableWidget.insertRow(row_number)
                            for column_number, data in enumerate(row_data):
                                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                        self.date_label.setText("")
                        self.sub_label.setText("ENTER 5th SEM SUBS")
                        self.Result_label.setText("         ENTER THE CORRECT DETAILS IN THE FIELDS SHOWN")

                except Exception as e:
                    pass

            elif sub_data and sem_data and sec_data and date_data != "":

                sub_data =sub_data.upper()

                if sub_data in  list_sub :

                    Pos = "ONLINE"

                    query = "SELECT semester ,section  from teacher_details_new where Status = %s "
                    value = (Pos,)
                    mycursor.execute(query, value)
                    result = mycursor.fetchall()
                    #print(result)
                    for each in result:
                        sem_name, sec_name , *no_need = each

                    query = "SELECT Date  from attendence_new where Subject = %s  GROUP BY Date"
                    value = (sub_data,)
                    mycursor.execute(query, value)
                    result_new = mycursor.fetchall()
                    list_dt =[]
                    for each in result_new:
                        curr_sub_date , *no_need = each
                        list_dt.append(curr_sub_date)

                    #print(list_dt)

                    if date_data == ok_date :

                        date_fmt = str(date_data)
                        ruslt = date_fmt.split("-")
                        dy, mn, yr, *no_need = ruslt
                        # print(dy, mn, yr, *no_need)

                        if int(dy) >= 1 and int(dy) <= 31 and int(mn) >= 1 and int(mn) <= 12:

                            if  date_data in list_dt :

                                try:
                                    if  sem_data == sem_name and sec_data.upper() == sec_name.upper()  :
                                        query = "SELECT Subject ,USN ,Status ,Semester ,Section ,Date from attendence_new where   Subject = %s and Date = %s"
                                        value = ( sub_data, ok_date)
                                        mycursor.execute(query, value)
                                        result_new = mycursor.fetchall()
                                        self.date_label.setText("")
                                        self.Result_label.setText("")
                                        if len(result_new) != 0 :
                                            self.tableWidget.setRowCount(0)
                                            for row_number, row_data in enumerate(result_new):
                                                self.tableWidget.insertRow(row_number)
                                                for column_number, data in enumerate(row_data):
                                                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                                        else :
                                            self.sub_label.setText("NO RECORD")
                                            self.Result_label.setText("                THERE IS NO DATA STORED IN THAT DATE")
                                            result_new = ""
                                            self.tableWidget.setRowCount(0)
                                            for row_number, row_data in enumerate(result_new):
                                                self.tableWidget.insertRow(row_number)
                                                for column_number, data in enumerate(row_data):
                                                    self.tableWidget.setItem(row_number, column_number,
                                                                             QTableWidgetItem(str(data)))

                                    else:
                                        if sem_data != sem_name:
                                            self.sem_label.setText("ENTER CURRENT SEM")
                                            result_new = ""
                                            self.tableWidget.setRowCount(0)
                                            for row_number, row_data in enumerate(result_new):
                                                self.tableWidget.insertRow(row_number)
                                                for column_number, data in enumerate(row_data):
                                                    self.tableWidget.setItem(row_number, column_number,
                                                                             QTableWidgetItem(str(data)))

                                        if sec_data.upper() != sec_name.upper():
                                            self.sec_label.setText("ENTER CURRENT SECT")
                                            result_new = ""
                                            self.tableWidget.setRowCount(0)
                                            for row_number, row_data in enumerate(result_new):
                                                self.tableWidget.insertRow(row_number)
                                                for column_number, data in enumerate(row_data):
                                                    self.tableWidget.setItem(row_number, column_number,
                                                                             QTableWidgetItem(str(data)))

                                        self.Result_label.setText("         ENTER THE CORRECT DETAILS IN THE FIELDS SHOWN")

                                except Exception as e:
                                    pass

                            else:
                                self.date_label.setText("NO RECORD ")
                                self.Result_label.setText("               THERE IS NO DATA STORED IN THAT DATE")
                                result_new = ""
                                self.tableWidget.setRowCount(0)
                                for row_number, row_data in enumerate(result_new):
                                    self.tableWidget.insertRow(row_number)
                                    for column_number, data in enumerate(row_data):
                                        self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                        else:
                            self.date_label.setText(" WRONG FORMAT ")
                            self.Result_label.setText("           DAY BETWEEN 0 TO 31 AN MONTH BETWEEN 1 TO 12")
                            result_new = ""
                            self.tableWidget.setRowCount(0)
                            for row_number, row_data in enumerate(result_new):
                                self.tableWidget.insertRow(row_number)
                                for column_number, data in enumerate(row_data):
                                    self.tableWidget.setItem(row_number, column_number,
                                                             QTableWidgetItem(str(data)))

                    else :
                        self.date_label.setText("WRONG FORMAT")
                        self.Result_label.setText("                 CORRECT FORMAT IS DD-MM-YYYY")
                        result_new = ""
                        self.tableWidget.setRowCount(0)
                        for row_number, row_data in enumerate(result_new):
                            self.tableWidget.insertRow(row_number)
                            for column_number, data in enumerate(row_data):
                                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))


                else:
                    self.sub_label.setText("ENTER 5th SEM SUBS")
                    self.Result_label.setText("         ENTER THE CORRECT DETAILS IN THE FIELDS SHOWN")
                    result_new = ""
                    self.tableWidget.setRowCount(0)
                    for row_number, row_data in enumerate(result_new):
                        self.tableWidget.insertRow(row_number)
                        for column_number, data in enumerate(row_data):
                            self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            else :
                self.Result_label.setText("         ENTER THE CORRECT DETAILS IN THE FIELDS SHOWN")

        except Exception as e:
            pass

    # ------------------------------------------------------------------------------------------------------------

    def createaccfunction(self):
        #print("Successfully created acc with email and password")
        login = c_teacher_Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class View_Specific_student_Attendence_CT(QDialog):
    def __init__(self):
        super(View_Specific_student_Attendence_CT, self).__init__()
        loadUi("View_att_CT_usn.ui", self)
        self.Back.clicked.connect(self.createaccfunction)
        self.show_data.clicked.connect(self.Show_att_student_function)
    # -----------------------------------------------------------------------------------------------------------
    def Show_att_student_function(self):

        sub_data = self.subject.text()
        if sub_data == "":
            self.sub_label.setText("Missing Subject")
        else:
            self.sub_label.setText("")

        sem_data = self.semester.text()
        if sem_data == "":
            self.sem_label.setText("Missing Semester")
        else:
            self.sem_label.setText("")

        sec_data = self.section.text()
        if sec_data == "":
            self.sec_label.setText("Missing Section")
        else:
            self.sec_label.setText("")

        date_data = self.date_opt.text()
        if date_data == "":
            self.date_label.setText("Missing Date")
        else:
            self.date_label.setText("")

        usn_data = self.usn.text()
        if usn_data == "":
            self.usn_label.setText("Missing USN")
        else:
            self.usn_label.setText("")

        formt = self.date_opt.text()
        tup = re.findall("\d\d-\d\d-\d\d\d\d", formt)
        if len(tup) == 1:
            ok_date, *no_need = tup
        else:
            ok_date = ""

        try:
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="Muneshismyname",
                database="student_database"
            )
            mycursor = mydb.cursor()

            Pos = "subject teacher"

            query = "SELECT Subject  from teacher_accounts_new where Position = %s "
            value = (Pos,)
            mycursor.execute(query, value)
            result = mycursor.fetchall()
            list_sub = []
            for each in result:
                Subject_one, *no_need = each
                list_sub.append(Subject_one.upper())

            if sub_data and sem_data and usn_data and sec_data != "" and date_data == "":

                try:
                    mydb = mc.connect(
                        host="localhost",
                        user="root",
                        password="Muneshismyname",
                        database="student_database"
                    )

                    mycursor = mydb.cursor()

                    sub_data = sub_data.upper()

                    if sub_data in list_sub:

                        Pos = "ONLINE"

                        query = "SELECT semester ,section  from teacher_details_new where Status = %s "
                        value = (Pos,)
                        mycursor.execute(query, value)
                        result = mycursor.fetchall()
                        for each in result:
                            sem_name, sec_name, *no_need = each

                        query = "SELECT USN  from attendence_new where Subject = %s and Semester = %s and Section = %s GROUP BY USN "
                        value = (sub_data,sem_name,sec_name)
                        mycursor.execute(query, value)
                        result_new = mycursor.fetchall()

                        list_usn = []
                        for each_new in result_new:
                            usn_num , *no_need = each_new
                            list_usn.append(usn_num.upper())

                        if len(list_usn) != 0 :

                            if usn_data.upper() in list_usn :

                                try:
                                    if sem_data == sem_name and sec_data.upper() == sec_name.upper() :

                                        usn_data = usn_data.upper()
                                        query = "SELECT Subject ,USN ,Status ,Semester ,Section ,Date from attendence_new  where   USN = %s "
                                        value = (usn_data,)
                                        mycursor.execute(query, value)
                                        result_new_one = mycursor.fetchall()
                                        self.date_label.setText("")
                                        self.Result_label.setText("")
                                        if len(result_new_one) != 0:
                                            self.tableWidget.setRowCount(0)
                                            for row_number, row_data in enumerate(result_new_one):
                                                self.tableWidget.insertRow(row_number)
                                                for column_number, data in enumerate(row_data):
                                                    self.tableWidget.setItem(row_number, column_number,
                                                                             QTableWidgetItem(str(data)))
                                        else:
                                            self.sub_label.setText("NO RECORD")
                                            self.Result_label.setText("                  THERE IS NO DATA STORED IN THAT USN")
                                            result_new = ""
                                            self.tableWidget.setRowCount(0)
                                            for row_number, row_data in enumerate(result_new):
                                                self.tableWidget.insertRow(row_number)
                                                for column_number, data in enumerate(row_data):
                                                    self.tableWidget.setItem(row_number, column_number,
                                                                             QTableWidgetItem(str(data)))

                                    else:

                                        if sem_data != sem_name:
                                            self.date_label.setText("")
                                            self.sem_label.setText("ENTER CURRENT SEM")
                                            result_new = ""
                                            self.tableWidget.setRowCount(0)
                                            for row_number, row_data in enumerate(result_new):
                                                self.tableWidget.insertRow(row_number)
                                                for column_number, data in enumerate(row_data):
                                                    self.tableWidget.setItem(row_number, column_number,
                                                                             QTableWidgetItem(str(data)))

                                        if sec_data.upper() != sec_name.upper():
                                            self.date_label.setText("")
                                            self.sec_label.setText("ENTER CURRENT SECT")
                                            result_new = ""
                                            self.tableWidget.setRowCount(0)
                                            for row_number, row_data in enumerate(result_new):
                                                self.tableWidget.insertRow(row_number)
                                                for column_number, data in enumerate(row_data):
                                                    self.tableWidget.setItem(row_number, column_number,
                                                                             QTableWidgetItem(str(data)))

                                        self.date_label.setText("")
                                        self.Result_label.setText("        ENTER THE CORRECT DETAILS IN THE FIELDS SHOWN")

                                except Exception as e:
                                    pass

                            else:
                                self.date_label.setText("")
                                self.usn_label.setText("WRONG USN")
                                self.Result_label.setText("        ENTER THE CORRECT DETAILS IN THE FIELDS SHOWN")
                                result_new = ""
                                self.tableWidget.setRowCount(0)
                                for row_number, row_data in enumerate(result_new):
                                    self.tableWidget.insertRow(row_number)
                                    for column_number, data in enumerate(row_data):
                                        self.tableWidget.setItem(row_number, column_number,
                                                                 QTableWidgetItem(str(data)))

                        else:
                            self.date_label.setText("")
                            self.sub_label.setText("NO DATA")
                            self.Result_label.setText("           NO DATA IS PRESENT FOR THE SUBJECT ENTERED")
                            result_new = ""
                            self.tableWidget.setRowCount(0)
                            for row_number, row_data in enumerate(result_new):
                                self.tableWidget.insertRow(row_number)
                                for column_number, data in enumerate(row_data):
                                    self.tableWidget.setItem(row_number, column_number,
                                                             QTableWidgetItem(str(data)))

                    else:
                        self.date_label.setText("")
                        self.sub_label.setText("ENTER 5th SEM SUBS")
                        self.Result_label.setText("        ENTER THE CORRECT DETAILS IN THE FIELDS SHOWN")
                        result_new = ""
                        self.tableWidget.setRowCount(0)
                        for row_number, row_data in enumerate(result_new):
                            self.tableWidget.insertRow(row_number)
                            for column_number, data in enumerate(row_data):
                                self.tableWidget.setItem(row_number, column_number,
                                                         QTableWidgetItem(str(data)))

                except Exception as e:
                    pass

            elif sub_data and sem_data and sec_data and usn_data and date_data != "":

                sub_data = sub_data.upper()

                if sub_data in list_sub:

                    Pos = "ONLINE"

                    query = "SELECT semester ,section  from teacher_details_new where Status = %s "
                    value = (Pos,)
                    mycursor.execute(query, value)
                    result = mycursor.fetchall()
                    #print(result)
                    for each in result:
                        sem_name, sec_name, *no_need = each

                    query = "SELECT Date  from attendence_new where Subject = %s  GROUP BY Date"
                    value = (sub_data,)
                    mycursor.execute(query, value)
                    result_new = mycursor.fetchall()
                    list_dt = []
                    for each in result_new:
                        curr_sub_date, *no_need = each
                        list_dt.append(curr_sub_date)

                    #print(list_dt)

                    if date_data == ok_date:

                        query = "SELECT USN  from attendence_new where Subject = %s and Semester = %s and Section = %s  GROUP BY USN "
                        value = (sub_data, sem_name, sec_name )
                        mycursor.execute(query, value)
                        result_new = mycursor.fetchall()
                        #print(result_new)
                        list_usn = []
                        for each_new in result_new:
                            usn_num, *no_need = each_new
                            list_usn.append(usn_num.upper())

                        #print(list_usn)
                        date_fmt = str(date_data)
                        ruslt = date_fmt.split("-")
                        dy, mn, yr, *no_need = ruslt
                        # print(dy, mn, yr, *no_need)

                        if int(dy) >= 1 and int(dy) < 32 and int(mn) >= 1 and int(mn) <= 12:

                            if date_fmt in list_dt:

                                if usn_data.upper() in list_usn :

                                    try:
                                        if sem_data == sem_name and sec_data.upper() == sec_name.upper():
                                            query = "SELECT Subject ,USN ,Status ,Semester ,Section ,Date from attendence_new where   USN = %s and Date = %s"
                                            value = (usn_data, date_data)
                                            mycursor.execute(query, value)
                                            result_new = mycursor.fetchall()
                                            self.date_label.setText("")
                                            self.Result_label.setText("")
                                            if len(result_new) != 0:
                                                self.tableWidget.setRowCount(0)
                                                for row_number, row_data in enumerate(result_new):
                                                    self.tableWidget.insertRow(row_number)
                                                    for column_number, data in enumerate(row_data):
                                                        self.tableWidget.setItem(row_number, column_number,
                                                                                 QTableWidgetItem(str(data)))

                                            else:
                                                result_new = ""
                                                self.tableWidget.setRowCount(0)
                                                for row_number, row_data in enumerate(result_new):
                                                    self.tableWidget.insertRow(row_number)
                                                    for column_number, data in enumerate(row_data):
                                                        self.tableWidget.setItem(row_number, column_number,
                                                                                 QTableWidgetItem(str(data)))
                                                self.date_label.setText("NO RECORD")
                                                self.Result_label.setText("THERE IS NO DATA STORED ABOUT GIVEN  USN IN THAT DATE")


                                        else:
                                            if sem_data != sem_name:
                                                self.sem_label.setText("ENTER CURRENT SEM")
                                                result_new = ""
                                                self.tableWidget.setRowCount(0)
                                                for row_number, row_data in enumerate(result_new):
                                                    self.tableWidget.insertRow(row_number)
                                                    for column_number, data in enumerate(row_data):
                                                        self.tableWidget.setItem(row_number, column_number,
                                                                                 QTableWidgetItem(str(data)))

                                            if sec_data.upper() != sec_name.upper():
                                                self.sec_label.setText("ENTER CURRENT SECT")

                                                result_new = ""
                                                self.tableWidget.setRowCount(0)
                                                for row_number, row_data in enumerate(result_new):
                                                    self.tableWidget.insertRow(row_number)
                                                    for column_number, data in enumerate(row_data):
                                                        self.tableWidget.setItem(row_number, column_number,
                                                                                 QTableWidgetItem(str(data)))

                                            self.Result_label.setText("        ENTER THE CORRECT DETAILS IN THE FIELDS SHOWN")

                                    except Exception as e:
                                        pass

                                else :
                                    self.usn_label.setText("WRONG USN")
                                    self.Result_label.setText("        ENTER THE CORRECT DETAILS IN THE FIELDS SHOWN")
                                    result_new = ""
                                    self.tableWidget.setRowCount(0)
                                    for row_number, row_data in enumerate(result_new):
                                        self.tableWidget.insertRow(row_number)
                                        for column_number, data in enumerate(row_data):
                                            self.tableWidget.setItem(row_number, column_number,
                                                                     QTableWidgetItem(str(data)))


                            else:
                                self.date_label.setText("NO RECORD ")
                                self.Result_label.setText("           THERE IS NO DATA STORED IN THAT DATE")
                                result_new = ""
                                self.tableWidget.setRowCount(0)
                                for row_number, row_data in enumerate(result_new):
                                    self.tableWidget.insertRow(row_number)
                                    for column_number, data in enumerate(row_data):
                                        self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                        else:
                            self.date_label.setText(" DD-MM-YYYY")
                            self.Result_label.setText("        DAY BETWEEN 0 TO 31 AN MONTH BETWEEN 1 TO 12")
                            result_new = ""
                            self.tableWidget.setRowCount(0)
                            for row_number, row_data in enumerate(result_new):
                                self.tableWidget.insertRow(row_number)
                                for column_number, data in enumerate(row_data):
                                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))


                    else:
                        self.date_label.setText("WRONG FORMAT")
                        self.Result_label.setText("               CORRECT FORMAT IS DD-MM-YYYY")
                        result_new = ""
                        self.tableWidget.setRowCount(0)
                        for row_number, row_data in enumerate(result_new):
                            self.tableWidget.insertRow(row_number)
                            for column_number, data in enumerate(row_data):
                                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))


                else:
                    self.sub_label.setText("ENTER 5th SEM SUBS")
                    self.Result_label.setText("           ENTER THE SUBJECTS OF 5TH SEM ONLY")
                    result_new = ""
                    self.tableWidget.setRowCount(0)
                    for row_number, row_data in enumerate(result_new):
                        self.tableWidget.insertRow(row_number)
                        for column_number, data in enumerate(row_data):
                            self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            else:
                self.Result_label.setText("      ENTER THE CORRECT DETAILS IN THE FIELDS SHOWN")

        except Exception as e:
            pass
    # ------------------------------------------------------------------------------------------------------------

    def createaccfunction(self):
        #print("Successfully created acc with email and password")
        login = c_teacher_Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# -------------------------------------------------------------------------------------------------------------------
# Subject teacher Login
# -------------------------------------------------------------------------------------------------------------------


class s_teacher(QDialog):
    def __init__(self):
        super(s_teacher, self).__init__()
        loadUi("Login.ui", self)
        self.Change_pswd.clicked.connect(self.gotocreate_C)
        self.Login.clicked.connect(self.gotoLogin_ST)  # self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Back.clicked.connect(self.createaccfunction)

    def gotocreate_C(self):
        createacc = Change_pswd_s_teacher()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoLogin_ST(self):
        try:
            tblname = "teacher_accounts_new"

            username = self.username.text()

            if username == "":
                self.username_label.setText("Missing Username")
            else:
                self.username_label.setText("")

            password = self.password.text()

            if password == "":
                self.password_label.setText("Missing Password")
            else:
                self.password_label.setText("")

            if username and password != "":
                #print(f"Successfully {username} created acc with email {email} and password {password}")
                mydb = mc.connect(
                    host="localhost",
                    user="root",
                    password="Muneshismyname",
                    database="student_database"
                )

                mycursor = mydb.cursor()
                Pos = "subject Teacher"
                sql = "SELECT * from teacher_accounts_new  WHERE Position = %s"
                val = (Pos,)
                mycursor.execute(sql , val)
                result = mycursor.fetchall()
                #print(result)
                m = len(result)
                list_lct = []
                if m != 0 :
                    for each in result:
                        slnum,ad_nam,lect,sub,sem,sec,postn,pswd,mail = each
                        list_lct.append(lect.upper())

                        if username.upper() in list_lct :

                            if username.upper() == lect.upper() :

                                if  pswd.upper() == password.upper() :
                                    status = "ONLINE"
                                    time_cur = time.ctime()
                                    query = "INSERT INTO teacher_details_new(Lecturer_name,Subject,semester ,section ,Position	,Status ,login_time) VALUES (%s, %s, %s,%s,%s, %s, %s)"
                                    value = (lect, sub,sem,sec,postn,status,time_cur)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                    createacc = s_teacher_Login()
                                    widget.addWidget(createacc)
                                    widget.setCurrentIndex(widget.currentIndex() + 1)

                                else:
                                    if password.upper() != pswd.upper() :
                                        self.password_label.setText("Wrong Password")
                                    self.result_label.setText("                Enter The Correct Password In The Shown Field")

                        else :
                            self.username_label.setText("Wrong Username")
                            self.result_label.setText("                No Subject Teacher Account Exists With The Given Username")

                else :
                    self.result_label.setText("")


            else :
                self.result_label.setText("                  Enter The Data In  The Shown Field")

        except mc.Error as e:
            pass

    def createaccfunction(self):
        #print("Successfully created acc with email and password")
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class s_teacher_Login(QDialog):
    def __init__(self):
        super(s_teacher_Login, self).__init__()
        loadUi("Sub_Teacher.ui", self)
        self.Logout.clicked.connect(self.createaccfunction_logout)
        self.Mark_A.clicked.connect(self.goto_MarkAttendence)
        self.View_A.clicked.connect(self.goto_ViewAttendence)
        #self.out.setText("WELCOME  TO STUDENT ATTENDENCE MANAGEMENT SYSTEM")
        self.Edt_att.clicked.connect(self.goto_EditAttendence)

    def goto_MarkAttendence(self):
        createacc = MarkAttendence()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_ViewAttendence(self):
        createacc = ViewAttendence()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goto_EditAttendence(self):
        createacc = EditAttendence()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def createaccfunction_logout(self):
        mydb = mc.connect(
            host="localhost",
            user="root",
            password="Muneshismyname",
            database="student_database"
        )
        #tblname = "teacher_login"
        mycursor = mydb.cursor()
        Pos = "subject Teacher"
        sql = "SELECT * from teacher_details_new  WHERE Position = %s"
        val = (Pos,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        for each in result:
            slnum, lectnam, sub,sem,sec, pos ,stat, login ,logout = each
            #print(slnum,lectnam,sub,pos,stat,login ,logout)
            if stat == "ONLINE" :
                #print(stat)
                lout_time = time.ctime()
                status="OFFLINE"
                sql = "UPDATE teacher_details_new SET Status = %s , logout_time = %s WHERE Sl_no = %s"
                val = (status, lout_time, slnum)
                mycursor.execute(sql, val)
                #result = mycursor.fetchall()
                #print(result)
                login = s_teacher()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex() + 1)

class MarkAttendence(QDialog):
    def __init__(self):
        super(MarkAttendence, self).__init__()
        loadUi("Attendence_Layout.ui", self)
        self.Load.clicked.connect(self.load_data_sec_A_B_C)
        self.Submit.clicked.connect(self.submit_data)
        self.Back_t.clicked.connect(self.createaccfunction)

    # ------------------------------------------------------------------------------------------------------------
    # load attendece code
    def load_data_sec_A_B_C(self):
        try:
            tblname = "base_table"
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="Muneshismyname",
                database="student_database"
            )

            mycursor = mydb.cursor()

            subject = self.sub.text()
            if subject == "":
                self.sub_label.setText("Missing Subject")
            else:
                self.sub_label.setText("")

            semester = self.sem.text()
            if semester == "":
                self.sem_label.setText("Missing Semester")
            else:
                self.sem_label.setText("")

            section = self.sec.text()
            if section == "":
                self.sec_label.setText("Missing Section")
            else:
                self.sec_label.setText("")

            if subject and semester and section != "" :

                sql = "SELECT * from teacher_details_new  WHERE Status = %s"
                Pos = "ONLINE"
                val = (Pos,)
                mycursor.execute(sql, val)
                result = mycursor.fetchall()
                for each in result :
                    slnum, lectnam, sub, sem, sec, pos, stat, login, logout = each
                #print(result)

                if subject.upper() == sub.upper() and semester.upper() == sem.upper() and section.upper() == sec.upper() :
                    sql = "SELECT * from base_table  WHERE Semester = %s and Section = %s"
                    val = (sem,sec)
                    mycursor.execute(sql, val)
                    result = mycursor.fetchall()
                    list_v=[]
                    for each in result :
                        slnum ,f_name ,l_name , usn, *no_need = each
                        list_v.append(usn)

                    try :
                        USN_1,USN_2,USN_3,USN_4,USN_5,USN_6,USN_7,USN_8,USN_9,USN_10,USN_11,USN_12,USN_13,USN_14,USN_15,USN_16,USN_17,USN_18,USN_19,USN_20 = list_v
                        self.labels = [self.label_one , self.label_two , self.label_three, self.label_four, self.label_five, self.label_six, self.label_seven, self.label_eight, self.label_nine, self.label_ten ,self.label_101,self.label_102,self.label_103,self.label_104,self.label_105,self.label_106,self.label_107,self.label_108,self.label_109,self.label_110]
                        #count = len(self.labels)
                        #print(count)
                        for labels in self.labels:
                            #print(labels)
                            self.Result_label.setText("")
                            if labels == self.label_one:
                                self.label_one.setText(USN_1)
                            if labels == self.label_two:
                                self.label_two.setText(USN_2)
                            if labels == self.label_three:
                                self.label_three.setText(USN_3)
                            if labels == self.label_four:
                                self.label_four.setText(USN_4)
                            if labels == self.label_five:
                                self.label_five.setText(USN_5)
                            if labels == self.label_six:
                                self.label_six.setText(USN_6)
                            if labels == self.label_seven:
                                self.label_seven.setText(USN_7)
                            if labels == self.label_eight:
                                self.label_eight.setText(USN_8)
                            if labels == self.label_nine:
                                self.label_nine.setText(USN_9)
                            if labels == self.label_ten:
                                self.label_ten.setText(USN_10)
                            if labels == self.label_101:
                                self.label_101.setText(USN_11)
                            if labels == self.label_102:
                                self.label_102.setText(USN_12)
                            if labels == self.label_103:
                                self.label_103.setText(USN_13)
                            if labels == self.label_104:
                                self.label_104.setText(USN_14)
                            if labels == self.label_105:
                                self.label_105.setText(USN_15)
                            if labels == self.label_106:
                                self.label_106.setText(USN_16)
                            if labels == self.label_107:
                                self.label_107.setText(USN_17)
                            if labels == self.label_108:
                                self.label_108.setText(USN_18)
                            if labels == self.label_109:
                                self.label_109.setText(USN_19)
                            if labels == self.label_110:
                                self.label_110.setText(USN_20)

                    except Exception as e:
                        pass

                else :
                    if subject.upper() != sub.upper() :
                        self.sub_label.setText("ENTER CURRENT SUB")
                    if semester.upper() != sem.upper() :
                        self.sem_label.setText("ENTER CURRENT SEM")
                    if section.upper() != sec.upper() :
                        self.sec_label.setText("ENTER CURRENT SECTION")

                    self.Result_label.setText("        ENTER THE CORRECT DATA IN THE SHOWN FIELD")

            else:
                self.Result_label.setText("                          ENTER THE MISSING FIELDS")

        except Exception as e:
            pass
    #-------------------------------------------------------------------------------------------------------------
    # store attendence code
    def submit_data(self):

        new = time.time()
        t9 = time.localtime(new)
        dote = time.strftime("%d-%m-%Y", t9)

        subject = self.sub.text()
        if subject == "":
            self.sub_label.setText("Missing Subject")
        else:
            self.sub_label.setText("")

        semester = self.sem.text()
        if semester == "":
            self.sem_label.setText("Missing Semester")
        else:
            self.sem_label.setText("")

        section = self.sec.text()
        if section == "":
            self.sec_label.setText("Missing Section")
        else:
            self.sec_label.setText("")


        if subject and semester and section != "" :
            try :
                mydb = mc.connect(
                    host="localhost",
                    user="root",
                    password="Muneshismyname",
                    database="student_database"
                )

                mycursor = mydb.cursor()

                Pos = "ONLINE"
                query = "SELECT Lecturer_name,Subject,Semester,Section from teacher_details_new where Status = %s "
                value = (Pos,)
                mycursor.execute(query, value)
                result = mycursor.fetchall()
                for each in result:
                    lect_name, sub_n, sem, sec, *no_need = each

                t2 = time.time()
                t9 = time.localtime(t2)
                date = time.strftime("%d-%m-%Y", t9)
                query = "SELECT Time  from submit_timings where Subject = %s and Date = %s "
                date_nw = str(date)
                value = (sub_n, date_nw)
                mycursor.execute(query, value)
                result_new_n = mycursor.fetchall()
                list_n=[]
                for each in result_new_n :
                    #print(each)
                    new , *no_need = each
                    #type(new)
                    list_n.append(new)



                #print(list_n)
                reqird = list_n
                new_m  = reqird[-1]
                #print(new_m)
                new1 = float(new_m)
                min_time = new1 + 1800
                min_time_new = str(min_time)
                #print(type(min_time_new))

                result_time = time.time()
                result_time = str(result_time)
                #print(type(result_time) , result_time)

            except Exception as e :
                pass

            try:

                Pos ="ONLINE"
                query = "SELECT Lecturer_name,Subject,Semester,Section from teacher_details_new where Status = %s "
                value = (Pos,)
                mycursor.execute(query, value)
                result = mycursor.fetchall()
                for each in result :
                    lect_name,sub,sem,sec,*no_need = each

                if subject.upper() == sub.upper() and semester.upper() == sem.upper() and section.upper() == sec.upper():

                    try :

                        query = "SELECT Date  from attendence_new where Subject = %s  GROUP BY Date"
                        value = (sub,)
                        mycursor.execute(query, value)
                        result_new = mycursor.fetchall()
                        list_dt_n = []
                        for each in result_new:
                            curr_sub_date, *no_need = each
                            list_dt_n.append(curr_sub_date)

                        #print(list_dt_n)
                        t2 = time.time()
                        t9 = time.localtime(t2)
                        t3 = time.strftime("%d-%m-%Y", t9)
                        todate=str(t3)

                        result_att = todate not in list_dt_n
                        #print(result_att)

                    except Exception as e :
                        pass

                    if result_att :

                        #print(result_att)
                        new = time.time()
                        t9 = time.localtime(new)
                        dte = time.strftime("%d-%m-%Y", t9)
                        query = "INSERT INTO submit_timings (Time,Subject,Date) VALUES (%s, %s, %s)"
                        value = (new, subject, dte)
                        mycursor.execute(query, value)
                        mydb.commit()

                        USN_1= self.label_one.text()
                        USN_2 = self.label_two.text()
                        USN_3 = self.label_three.text()
                        USN_4 = self.label_four.text()
                        USN_5 = self.label_five.text()
                        USN_6 = self.label_six.text()
                        USN_7 = self.label_seven.text()
                        USN_8 = self.label_eight.text()
                        USN_9 = self.label_nine.text()
                        USN_10 = self.label_ten.text()
                        USN_11 = self.label_101.text()
                        USN_12 = self.label_102.text()
                        USN_13 = self.label_103.text()
                        USN_14 = self.label_104.text()
                        USN_15 = self.label_105.text()
                        USN_16 = self.label_106.text()
                        USN_17 = self.label_107.text()
                        USN_18 = self.label_108.text()
                        USN_19 = self.label_109.text()
                        USN_20 = self.label_110.text()
                        #print("-------------------------------------------------")
                        self.labels = [self.label_one, self.label_two, self.label_three,self.label_four ,self.label_five, self.label_six, self.label_seven, self.label_eight, self.label_nine, self.label_ten, self.label_101, self.label_102, self.label_103, self.label_104, self.label_105, self.label_106, self.label_107, self.label_108, self.label_109,self.label_110]
                        for labels in self.labels:
                            # print(labels)
                            if labels == self.label_one:
                                usn = self.label_one.text()
                                if self.radioButton_1.isChecked():
                                    txt=self.radioButton_1.text()
                                else :
                                    txt = self.radioButton_2.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section ,dote ,new )
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_two:
                                usn = self.label_two.text()
                                if self.radioButton_1.isChecked():
                                    txt = self.radioButton_3.text()
                                else:
                                    txt = self.radioButton_4.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_three:
                                usn = self.label_three.text()
                                if self.radioButton_5.isChecked():
                                    txt = self.radioButton_5.text()
                                else:
                                    txt = self.radioButton_6.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_four:
                                usn = self.label_four.text()
                                if self.radioButton_7.isChecked():
                                    txt = self.radioButton_7.text()
                                else:
                                    txt = self.radioButton_8.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_five:
                                usn = self.label_five.text()
                                if self.radioButton_9.isChecked():
                                    txt = self.radioButton_9.text()
                                else:
                                    txt = self.radioButton_10.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_six:
                                usn = self.label_six.text()
                                if self.radioButton_11.isChecked():
                                    txt = self.radioButton_11.text()
                                else:
                                    txt = self.radioButton_12.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_seven:
                                usn = self.label_seven.text()
                                if self.radioButton_13.isChecked():
                                    txt = self.radioButton_13.text()
                                else:
                                    txt = self.radioButton_14.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_eight:
                                usn = self.label_eight.text()
                                if self.radioButton_15.isChecked():
                                    txt = self.radioButton_15.text()
                                else:
                                    txt = self.radioButton_16.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_nine:
                                usn = self.label_nine.text()
                                if self.radioButton_17.isChecked():
                                    txt = self.radioButton_17.text()
                                else:
                                    txt = self.radioButton_18.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_ten:
                                usn = self.label_ten.text()
                                if self.radioButton_19.isChecked():
                                    txt = self.radioButton_19.text()
                                else:
                                    txt = self.radioButton_20.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_101:
                                usn = self.label_101.text()
                                if self.radioButton_21.isChecked():
                                    txt = self.radioButton_21.text()
                                else:
                                    txt = self.radioButton_22.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_102:
                                usn = self.label_102.text()
                                if self.radioButton_23.isChecked():
                                    txt = self.radioButton_23.text()
                                else:
                                    txt = self.radioButton_24.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_103:
                                usn = self.label_103.text()
                                if self.radioButton_25.isChecked():
                                    txt = self.radioButton_25.text()
                                else:
                                    txt = self.radioButton_26.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_104:
                                usn = self.label_104.text()
                                if self.radioButton_27.isChecked():
                                    txt = self.radioButton_27.text()
                                else:
                                    txt = self.radioButton_28.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_105:
                                usn = self.label_105.text()
                                if self.radioButton_29.isChecked():
                                    txt = self.radioButton_29.text()
                                else:
                                    txt = self.radioButton_30.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_106:
                                usn = self.label_106.text()
                                if self.radioButton_31.isChecked():
                                    txt = self.radioButton_31.text()
                                else:
                                    txt = self.radioButton_32.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_107:
                                usn = self.label_107.text()
                                if self.radioButton_33.isChecked():
                                    txt = self.radioButton_33.text()
                                else:
                                    txt = self.radioButton_34.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_108:
                                usn = self.label_108.text()
                                if self.radioButton_35.isChecked():
                                    txt = self.radioButton_35.text()
                                else:
                                    txt = self.radioButton_36.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_109:
                                usn = self.label_109.text()
                                if self.radioButton_37.isChecked():
                                    txt = self.radioButton_37.text()
                                else:
                                    txt = self.radioButton_38.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_110:
                                usn = self.label_110.text()
                                if self.radioButton_39.isChecked():
                                    txt = self.radioButton_39.text()
                                else:
                                    txt = self.radioButton_40.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    print(e)

                        self.Result_label.setText("              ATTENDENCE MARKED SUCCESSFULLY")

                    elif t3 in list_dt_n and result_time > min_time_new :
                        

                        #print(result_att)
                        new = time.time()
                        t9 = time.localtime(new)
                        dte = time.strftime("%d-%m-%Y", t9)
                        query = "INSERT INTO submit_timings (Time,Subject,Date) VALUES (%s, %s, %s)"
                        value = (new, subject, dte)
                        mycursor.execute(query, value)
                        mydb.commit()

                        USN_1 = self.label_one.text()
                        USN_2 = self.label_two.text()
                        USN_3 = self.label_three.text()
                        USN_4 = self.label_four.text()
                        USN_5 = self.label_five.text()
                        USN_6 = self.label_six.text()
                        USN_7 = self.label_seven.text()
                        USN_8 = self.label_eight.text()
                        USN_9 = self.label_nine.text()
                        USN_10 = self.label_ten.text()
                        USN_11 = self.label_101.text()
                        USN_12 = self.label_102.text()
                        USN_13 = self.label_103.text()
                        USN_14 = self.label_104.text()
                        USN_15 = self.label_105.text()
                        USN_16 = self.label_106.text()
                        USN_17 = self.label_107.text()
                        USN_18 = self.label_108.text()
                        USN_19 = self.label_109.text()
                        USN_20 = self.label_110.text()
                        # print("-------------------------------------------------")
                        self.labels = [self.label_one, self.label_two, self.label_three, self.label_four,
                                       self.label_five, self.label_six, self.label_seven, self.label_eight,
                                       self.label_nine, self.label_ten, self.label_101, self.label_102, self.label_103,
                                       self.label_104, self.label_105, self.label_106, self.label_107, self.label_108,
                                       self.label_109, self.label_110]
                        for labels in self.labels:
                            # print(labels)
                            if labels == self.label_one:
                                usn = self.label_one.text()
                                if self.radioButton_1.isChecked():
                                    txt = self.radioButton_1.text()
                                else:
                                    txt = self.radioButton_2.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_two:
                                usn = self.label_two.text()
                                if self.radioButton_1.isChecked():
                                    txt = self.radioButton_3.text()
                                else:
                                    txt = self.radioButton_4.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_three:
                                usn = self.label_three.text()
                                if self.radioButton_5.isChecked():
                                    txt = self.radioButton_5.text()
                                else:
                                    txt = self.radioButton_6.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_four:
                                usn = self.label_four.text()
                                if self.radioButton_7.isChecked():
                                    txt = self.radioButton_7.text()
                                else:
                                    txt = self.radioButton_8.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_five:
                                usn = self.label_five.text()
                                if self.radioButton_9.isChecked():
                                    txt = self.radioButton_9.text()
                                else:
                                    txt = self.radioButton_10.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_six:
                                usn = self.label_six.text()
                                if self.radioButton_11.isChecked():
                                    txt = self.radioButton_11.text()
                                else:
                                    txt = self.radioButton_12.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_seven:
                                usn = self.label_seven.text()
                                if self.radioButton_13.isChecked():
                                    txt = self.radioButton_13.text()
                                else:
                                    txt = self.radioButton_14.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_eight:
                                usn = self.label_eight.text()
                                if self.radioButton_15.isChecked():
                                    txt = self.radioButton_15.text()
                                else:
                                    txt = self.radioButton_16.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_nine:
                                usn = self.label_nine.text()
                                if self.radioButton_17.isChecked():
                                    txt = self.radioButton_17.text()
                                else:
                                    txt = self.radioButton_18.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_ten:
                                usn = self.label_ten.text()
                                if self.radioButton_19.isChecked():
                                    txt = self.radioButton_19.text()
                                else:
                                    txt = self.radioButton_20.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_101:
                                usn = self.label_101.text()
                                if self.radioButton_21.isChecked():
                                    txt = self.radioButton_21.text()
                                else:
                                    txt = self.radioButton_22.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_102:
                                usn = self.label_102.text()
                                if self.radioButton_23.isChecked():
                                    txt = self.radioButton_23.text()
                                else:
                                    txt = self.radioButton_24.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_103:
                                usn = self.label_103.text()
                                if self.radioButton_25.isChecked():
                                    txt = self.radioButton_25.text()
                                else:
                                    txt = self.radioButton_26.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_104:
                                usn = self.label_104.text()
                                if self.radioButton_27.isChecked():
                                    txt = self.radioButton_27.text()
                                else:
                                    txt = self.radioButton_28.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_105:
                                usn = self.label_105.text()
                                if self.radioButton_29.isChecked():
                                    txt = self.radioButton_29.text()
                                else:
                                    txt = self.radioButton_30.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_106:
                                usn = self.label_106.text()
                                if self.radioButton_31.isChecked():
                                    txt = self.radioButton_31.text()
                                else:
                                    txt = self.radioButton_32.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_107:
                                usn = self.label_107.text()
                                if self.radioButton_33.isChecked():
                                    txt = self.radioButton_33.text()
                                else:
                                    txt = self.radioButton_34.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_108:
                                usn = self.label_108.text()
                                if self.radioButton_35.isChecked():
                                    txt = self.radioButton_35.text()
                                else:
                                    txt = self.radioButton_36.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_109:
                                usn = self.label_109.text()
                                if self.radioButton_37.isChecked():
                                    txt = self.radioButton_37.text()
                                else:
                                    txt = self.radioButton_38.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                            if labels == self.label_110:
                                usn = self.label_110.text()
                                if self.radioButton_39.isChecked():
                                    txt = self.radioButton_39.text()
                                else:
                                    txt = self.radioButton_40.text()
                                try:
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lect_name, usn, subject, txt, semester, section, dote, new)
                                    mycursor.execute(query, value)
                                    mydb.commit()
                                except Exception as e:
                                    pass

                        self.Result_label.setText("              ATTENDENCE MARKED SUCCESSFULLY")

                    else:
                        self.Result_label.setText("                      ATTENDENCE MARKED ALREADY")

                else :
                    if subject.upper() != sub.upper() :
                        self.sub_label.setText("ENTER CURRENT SUB")
                    if semester.upper() != sem.upper() :
                        self.sem_label.setText("ENTER CURRENT SEM")
                    if section.upper() != sec.upper() :
                        self.sec_label.setText("ENTER CURRENT SECTION")

                    self.Result_label.setText("        ENTER THE CORRECT DATA IN THE SHOWN FIELD")

            except Exception  as e:
               pass

        else :
            self.Result_label.setText("                          ENTER THE MISSING FIELDS")

    # ------------------------------------------------------------------------------------------------------------
    def createaccfunction(self):
        #print("Successfully created acc with email and password")
        login = s_teacher_Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# ------------------------------------------------------------------------------------------------------------
# edit attendence page
# ------------------------------------------------------------------------------------------------------------

class EditAttendence(QDialog):
    def __init__(self):
        super(EditAttendence, self).__init__()
        loadUi("Edit_att.ui", self)
        self.Back.clicked.connect(self.createaccfunction)
        #self.To_delete.clicked.connect(self.Delete_attendence_value)
        self.To_Update.clicked.connect(self.Update_attendence_value)
        self.To_Insert.clicked.connect(self.Insert_attendence_value)


    def Update_attendence_value(self):
        createacc = Update_Attendence_Value()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Insert_attendence_value(self):
        createacc = Insert_Attendence_Value()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def createaccfunction(self):
        #print("Successfully created acc with email and password")
        login = s_teacher_Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class Update_Attendence_Value(QDialog):  # to Update the value in the DB
    def __init__(self):
        super(Update_Attendence_Value, self).__init__()
        loadUi("update_att_ST_new.ui", self)
        self.Back.clicked.connect(self.createaccfunction)
        self.update.clicked.connect(self.Update_function)
        self.show_data.clicked.connect(self.Show_Data_function)
        # self.To_delete.clicked.connect(self.Delete_attendence_value)

    def Update_function(self):

        try :

            sub_data = self.subject.text()
            if sub_data == "":
                self.sub_label.setText("Missing Subject")
            else:
                self.sub_label.setText("")

            sem_data = self.semester.text()
            if sem_data == "":
                self.sem_label.setText("Missing Semester")
            else:
                self.sem_label.setText("")

            sec_data = self.section.text()
            if sec_data == "":
                self.sec_label.setText("Missing Section")
            else:
                self.sec_label.setText("")

            usn_data = self.usn.text()
            if usn_data == "":
                self.usn_label.setText("Missing USN")
            else:
                self.usn_label.setText("")

            status_data = self.status.text()
            if status_data == "":
                self.status_label.setText("Missing Status")
            else:
                self.status_label.setText("")

            date_data = self.date_D.text()
            if date_data == "":
                self.date_D_label.setText("Missing Date")
            else:
                self.date_D_label.setText("")


            mydb = mc.connect(
                host="localhost",
                user="root",
                password="Muneshismyname",
                database="student_database"
            )

            mycursor = mydb.cursor()
            Pos = "ONLINE"
            query = "SELECT Lecturer_name , Subject ,semester ,section  from teacher_details_new where Status = %s "
            value = (Pos,)
            mycursor.execute(query, value)
            result = mycursor.fetchall()
            for each in result:
                lect_name, sub_name, sem_name ,sec_name ,*no_need = each

            query = "SELECT USN , Status from attendence_new where lecturer_name = %s and Subject = %s and semester =%s and section = %s "
            value1 = (lect_name, sub_name, sem_name, sec_name )
            mycursor.execute(query, value1)
            result_new1 = mycursor.fetchall()
            #print(result_new1)
            list_n = []
            list_s = []
            for each in result_new1:
                usn_name, status_s = each
                list_n.append(usn_name)
                list_s.append(status_s)


            if sub_data and sem_data and sec_data and usn_data and status_data != "" and date_data =="" :
                self.date_D_label.setText("")
                if  usn_data.upper() in list_n :

                    if status_data.upper() == "PRESENT" or status_data.upper() == "ABSENT" or status_data.upper() == "P" or status_data.upper() == "A":

                        try :

                            if sub_data.upper() == sub_name.upper() and sem_data == sem_name and sec_data.upper() == sec_name.upper() :

                                for each in result_new1:
                                    usn_name, status_s = each

                                    if usn_data.upper() == usn_name.upper() :
                                        self.usn_label.setText("")
                                        self.Result_label.setText("")

                                        #print(usn_data)
                                        status_data = status_data.upper()

                                        query = "SELECT Date  from attendence_new where Subject = %s  GROUP BY Date"
                                        value = (sub_name,)
                                        mycursor.execute(query, value)
                                        result_new = mycursor.fetchall()
                                        list_D = []
                                        for each in result_new:
                                            date_d, *no_need = each
                                            list_D.append(date_d)

                                        Current_time = time.time()
                                        local_time = time.localtime(Current_time)
                                        Current_date = time.strftime("%d-%m-%Y", local_time)

                                        if Current_date in list_D :
                                            self.date_D_label.setText("")
                                            sql = "UPDATE attendence_new SET Status = %s WHERE USN = %s and Date = %s"
                                            val = (status_data, usn_data, Current_date )
                                            mycursor.execute(sql, val)
                                            self.Result_label.setText("STATUS UPDATED SUCCESSSFULLY")
                                            self.date_D_label.setText("")
                                            mydb.commit()

                                        else :
                                            self.Result_label.setText("ATTENDENCE IS NOT MARKED FOR THAT USN TODAY")



                            else :
                                if sub_data.upper() != sub_name.upper():
                                    self.sub_label.setText("ENTER CURRENT SUB")
                                if sem_data != sem_name:
                                    self.sem_label.setText("ENTER CURRENT SEM")
                                if sec_data.upper() != sec_name.upper():
                                    self.sec_label.setText("ENTER CURRENT SEC")

                                self.Result_label.setText("   ENTER THE CORRECT DETAILS IN THE SHOWN FIELD")

                        except Exception as e:
                            pass

                    else :
                        self.status_label.setText("STATUS ERROR")
                        self.Result_label.setText("    STATUS CAN BE ONLY PRESENT/P OR ABSENT/A")

                else :
                    self.usn_label.setText("USN NOT FOUND")
                    self.Result_label.setText("               ENTER THE CORRECT USN")

            elif sub_data and sem_data and sec_data and usn_data and status_data and date_data != "" :

                formt = self.date_D.text()
                tup = re.findall("\d\d-\d\d-\d\d\d\d", formt)
                if len(tup) == 1:
                    ok_date, *no_need = tup
                else:
                    ok_date = ""

                if  usn_data.upper() in list_n :

                    if status_data.upper() == "PRESENT" or status_data.upper() == "ABSENT" or status_data.upper() == "P" or status_data.upper() == "A":

                        try :

                            if sub_data.upper() == sub_name.upper() and sem_data == sem_name and sec_data.upper() == sec_name.upper() :

                                if date_data == ok_date:

                                    date_fmt = str(date_data)
                                    ruslt = date_fmt.split("-")
                                    dy, mn, yr, *no_need = ruslt
                                    # print(dy, mn, yr, *no_need)

                                    if int(dy) >= 00 and int(dy) <= 31 and int(mn) >= 1 and int(mn) <= 12:

                                        for each in result_new1:
                                            usn_name, status_s = each

                                            if usn_data.upper() == usn_name.upper() :
                                                self.usn_label.setText("")
                                                self.Result_label.setText("")
                                                #print(usn_data)
                                                status_data = status_data.upper()

                                                query = "SELECT Date  from attendence_new where Subject = %s  GROUP BY Date"
                                                value = (sub_name,)
                                                mycursor.execute(query, value)
                                                result_new = mycursor.fetchall()
                                                list_D = []
                                                for each in result_new:
                                                    date_d, *no_need = each
                                                    list_D.append(date_d)

                                                '''Current_time = time.time()
                                                local_time = time.localtime(Current_time)
                                                Current_date = time.strftime("%d-%m-%Y", local_time)'''

                                                if date_data in list_D :

                                                    sql = "UPDATE attendence_new SET Status = %s WHERE USN = %s and Date = %s"
                                                    val = (status_data, usn_data, date_data )
                                                    mycursor.execute(sql, val)
                                                    self.Result_label.setText("                  STATUS UPDATED SUCCESSSFULLY")
                                                    self.date_D_label.setText("")
                                                    mydb.commit()

                                                else :
                                                    self.date_D_label.setText("NO RECORD")
                                                    self.Result_label.setText("        ATTENDENCE IS NOT MARKED IN THAT  DATE")

                                    else:
                                        self.date_D_label.setText(" DD-MM-YYYY")
                                        self.Result_label.setText("DAY BETWEEN 01 TO 31 AN MONTH BETWEEN 01 TO 12")

                                else:
                                    self.date_D_label.setText("WRONG FORMAT")
                                    self.Result_label.setText("                CORRECT FORMAT IS DD-MM-YYYY")

                            else :
                                if sub_data.upper() != sub_name.upper():
                                    self.sub_label.setText("ENTER CURRENT SUB")
                                    result_new = ""
                                    self.tableWidget.setRowCount(0)
                                    for row_number, row_data in enumerate(result_new):
                                        # print(row_number , row_data)
                                        self.tableWidget.insertRow(row_number)
                                        for column_number, data in enumerate(row_data):
                                            self.tableWidget.setItem(row_number, column_number,
                                                                     QTableWidgetItem(str(data)))

                                if sem_data != sem_name:
                                    self.sem_label.setText("ENTER CURRENT SEM")
                                    result_new = ""
                                    self.tableWidget.setRowCount(0)
                                    for row_number, row_data in enumerate(result_new):
                                        # print(row_number , row_data)
                                        self.tableWidget.insertRow(row_number)
                                        for column_number, data in enumerate(row_data):
                                            self.tableWidget.setItem(row_number, column_number,
                                                                     QTableWidgetItem(str(data)))

                                if sec_data.upper() != sec_name.upper():
                                    self.sec_label.setText("ENTER CURRENT SEC")
                                    result_new = ""
                                    self.tableWidget.setRowCount(0)
                                    for row_number, row_data in enumerate(result_new):
                                        # print(row_number , row_data)
                                        self.tableWidget.insertRow(row_number)
                                        for column_number, data in enumerate(row_data):
                                            self.tableWidget.setItem(row_number, column_number,
                                                                     QTableWidgetItem(str(data)))

                                self.Result_label.setText("            ENTER THE CORRECT DETAILS IN THE SHOWN FIELD")

                        except Exception as e:
                            pass

                    else :
                        self.status_label.setText("STATUS ERROR")
                        self.Result_label.setText("    STATUS CAN BE ONLY PRESENT/P OR ABSENT/A")
                else :
                    self.usn_label.setText("USN NOT FOUND")
                    self.Result_label.setText("               ENTER THE CORRECT USN")
            else :
                self.Result_label.setText("                ENTER THE DATA  IN THE SHOWN FIELD")

        except Exception as e:
            pass

    def Show_Data_function(self) :
        sub_data = self.subject.text()
        if sub_data == "":
            self.sub_label.setText("Missing Subject")
        else:
            self.sub_label.setText("")

        sem_data = self.semester.text()
        if sem_data == "":
            self.sem_label.setText("Missing Semester")
        else:
            self.sem_label.setText("")

        sec_data = self.section.text()
        if sec_data == "":
            self.sec_label.setText("Missing Section")
        else:
            self.sec_label.setText("")


        if sub_data and sem_data and sec_data != "" :
            try:
                mydb = mc.connect(
                    host="localhost",
                    user="root",
                    password="Muneshismyname",
                    database="student_database"
                )

                mycursor = mydb.cursor()
                Pos = "ONLINE"
                query = "SELECT Lecturer_name , Subject from teacher_details_new where Status = %s "
                value = (Pos,)
                mycursor.execute(query, value)
                result = mycursor.fetchall()
                for each in result:
                    lect_name, sub_name = each

                query = "SELECT Semester , Section from attendence_new where lecturer_name = %s and Subject = %s "
                value1 = (lect_name, sub_name)
                mycursor.execute(query, value1)
                result_new1 = mycursor.fetchall()
                for each in result_new1:
                    sem_name, sec_name = each
                try:
                    if sub_data.upper() == sub_name.upper() and sem_data == sem_name and sec_data.upper() == sec_name.upper() :
                        query = "SELECT Subject ,USN ,Status ,Semester ,Section ,Date from attendence_new where lecturer_name = %s and Subject = %s "
                        value = (lect_name, sub_name)
                        mycursor.execute(query, value)
                        result_new = mycursor.fetchall()
                        self.Result_label.setText("")
                        self.usn_label.setText("")
                        self.status_label.setText("")
                        self.date_D_label.setText("")
                        self.tableWidget.setRowCount(0)
                        for row_number, row_data in enumerate(result_new):
                            # print(row_number , row_data)
                            self.tableWidget.insertRow(row_number)

                            for column_number, data in enumerate(row_data):
                                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                    else:
                        result_new = ""
                        self.tableWidget.setRowCount(0)
                        for row_number, row_data in enumerate(result_new):
                            # print(row_number , row_data)
                            self.tableWidget.insertRow(row_number)
                            for column_number, data in enumerate(row_data):
                                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                        if sub_data.upper() != sub_name.upper():
                            self.sub_label.setText("ENTER CURRENT SUB")

                        if sem_data != sem_name:
                            self.sem_label.setText("ENTER CURRENT SEM")

                        if sec_data.upper() != sec_name.upper():
                            self.sec_label.setText("ENTER CURRENT SEC")


                        self.Result_label.setText("            ENTER THE CORRECT DETAILS IN THE SHOWN FIELD")

                except Exception as e:
                    pass

            except Exception as e:
                pass

        else:
            self.Result_label.setText("                ENTER THE DATA  IN THE SHOWN FIELD")

    def createaccfunction(self):
        #print("Successfully created acc with email and password")
        login = EditAttendence()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#--------------------------------------------------------------------------------------------

class Insert_Attendence_Value(QDialog):  # to alter the  table attribute value in the DB
    def __init__(self):
        super(Insert_Attendence_Value, self).__init__()
        loadUi("Insert_ST_new_one.ui", self)
        self.Back.clicked.connect(self.createaccfunction)
        self.insert_data.clicked.connect(self.Inert_ST_function)
        self.show_data.clicked.connect(self.Show_ST_function)
        # self.To_delete.clicked.connect(self.Delete_attendence_value)

    def Inert_ST_function(self):

        usn_data = self.usnn.text()
        if usn_data == "":
            self.usn_label.setText("Missing USN")
        else:
            self.usn_label.setText("")

        status_data = self.stati.text()
        if status_data == "":
            self.stat_label.setText("Missing Status")
        else:
            self.stat_label.setText("")

        date_data = self.datei.text()
        if date_data == "":
            self.date_label.setText("Missing Date")
        else:
            self.date_label.setText("")

        if  usn_data  and status_data and date_data !="" :
            try:
                mydb = mc.connect(
                    host="localhost",
                    user="root",
                    password="Muneshismyname",
                    database="student_database"
                )

                mycursor = mydb.cursor()

                Pos = "ONLINE"
                query = "SELECT Lecturer_name , Subject ,Semester ,Section from teacher_details_new where Status = %s "
                value = (Pos,)
                mycursor.execute(query, value)
                result = mycursor.fetchall()
                for each in result:
                    lectr_name, subjt_name ,semster_name,sectn_name,*no_need = each

                query = "SELECT USN  from attendence_new where lecturer_name = %s and Subject = %s and semester =%s and section = %s "
                value1 = (lectr_name, subjt_name, semster_name, sectn_name)
                mycursor.execute(query, value1)
                result_new1 = mycursor.fetchall()
                list_in = []
                for each in result_new1 :
                    usn_in ,*no_need = each
                    list_in.append(usn_in)
                #print(list_in)

                formt = self.datei.text()
                tup = re.findall("\d\d-\d\d-\d\d\d\d", formt)
                if len(tup) == 1:
                    ok_date, *no_need = tup
                else:
                    ok_date = ""

                if usn_data.upper() in list_in :

                    if status_data.upper() == "PRESENT" or status_data.upper() == "ABSENT" or status_data.upper() == "A" or status_data.upper() == "P":

                        if date_data == ok_date :

                            date_fmt = str(date_data)
                            ruslt = date_fmt.split("-")
                            dy, mn, yr, *no_need = ruslt
                            #print(dy, mn, yr, *no_need)

                            if int(dy) >= 00 and int(dy) <= 31 and int(mn) >= 1 and int(mn) <= 12:

                                try :
                                    #print("yes")
                                    tim = time.time()
                                    self.result_label.setText("                       DATA INSERTED SUCCESSFULLY")
                                    query = "INSERT INTO attendence_new(lecturer_name,USN,Subject,Status,Semester,Section,Date ,Time) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
                                    value = (lectr_name, usn_data, subjt_name, status_data, semster_name, sectn_name, date_data, tim)
                                    mycursor.execute(query, value)
                                    mydb.commit()


                                except Exception as e :
                                    pass

                            else:
                                self.date_label.setText(" DD-MM-YYYY")
                                self.result_label.setText("       DAY BETWEEN 0 TO 31 AN MONTH BETWEEN 1 TO 12")

                        else :
                            self.date_label.setText("ENTER CORRECT FORM")
                            self.result_label.setText("                CORRECT FORMAT IS DD-MM-YYYY")

                    else:
                        self.stat_label.setText("STATUS ERROR")
                        self.result_label.setText("           STATUS CAN BE ONLY PRESENT/P OR ABSENT/A")


                else :
                    self.usn_label.setText("USN NOT FOUND")
                    self.result_label.setText("                     ENTER THE CORRECT USN")

            except Exception as e :
                pass

        else :
            self.result_label.setText("                    ENTER THE DATA IN THE SHOWN FIELD")


    def Show_ST_function(self) :

        try:
            mydb = mc.connect(
            host="localhost",
            user="root",
            password="Muneshismyname",
            database="student_database"
            )

            mycursor = mydb.cursor()
            Pos = "ONLINE"
            query = "SELECT Lecturer_name , Subject from teacher_details_new where Status = %s "
            value = (Pos,)
            mycursor.execute(query, value)
            result = mycursor.fetchall()
            for each in result:
                lect_name, sub_name = each

            query = "SELECT Semester , Section from attendence_new where lecturer_name = %s and Subject = %s "
            value1 = (lect_name, sub_name)
            mycursor.execute(query, value1)
            result_new1 = mycursor.fetchall()
            for each in result_new1:
                sem_name, sec_name = each
            try:

                query = "SELECT Subject ,USN ,Status ,Semester ,Section ,Date from attendence_new where lecturer_name = %s and Subject = %s "
                value = (lect_name, sub_name)
                mycursor.execute(query, value)
                result_new = mycursor.fetchall()
                self.result_label.setText("")
                self.tableWidget.setRowCount(0)
                for row_number, row_data in enumerate(result_new):
                    # print(row_number , row_data)
                    self.tableWidget.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))


            except Exception as e:
                    pass

        except Exception as e:
            pass


    def createaccfunction(self):
        #print("Successfully created acc with email and password")
        login = EditAttendence()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# -----------------------------------------------------------------------------------------------------------------
class ViewAttendence(QDialog):
    def __init__(self):
        super(ViewAttendence, self).__init__()
        loadUi("view_att_ST_new.ui", self)
        self.Back.clicked.connect(self.createaccfunction)
        self.show_data.clicked.connect(self.View_attendence_status)
    # -----------------------------------------------------------------------------------------------------------
    # view attendence code will be here
    def View_attendence_status(self):
        tblname = "attendence_new"

        sub_data = self.subject.text()
        if sub_data == "":
            self.sub_label.setText("Missing Subject")
        else:
            self.sub_label.setText("")

        sem_data = self.semester.text()
        if sem_data == "":
            self.sem_label.setText("Missing semester")
        else:
            self.sem_label.setText("")

        sec_data = self.section.text()
        if sec_data == "":
            self.sec_label.setText("Missing section")
        else:
            self.sec_label.setText("")

        date_data = self.date_opt.text()
        if date_data == "":
            self.date_label.setText("Missing date")
        else:
            self.date_label.setText("")

        if sub_data and sem_data and sec_data != "" and date_data =="" :
            try:
                mydb = mc.connect(
                    host="localhost",
                    user="root",
                    password="Muneshismyname",
                    database="student_database"
                )

                mycursor = mydb.cursor()
                Pos = "ONLINE"
                query = "SELECT Lecturer_name , Subject from teacher_details_new where Status = %s "
                value = (Pos,)
                mycursor.execute(query, value)
                result = mycursor.fetchall()
                for each in result:
                    lect_name, sub_name = each

                query = "SELECT Semester , Section from attendence_new where lecturer_name = %s and Subject = %s "
                value1 = (lect_name,sub_name)
                mycursor.execute(query, value1)
                result_new1 = mycursor.fetchall()
                for each in result_new1:
                    sem_name, sec_name = each


                try :
                    if sub_data.upper() == sub_name.upper() and sem_data == sem_name and sec_data.upper() == sec_name.upper() and date_data == "":
                        query = "SELECT Subject ,USN ,Status ,Semester ,Section ,Date from attendence_new where lecturer_name = %s and Subject = %s "
                        value = (lect_name, sub_name)
                        mycursor.execute(query, value)
                        result_new = mycursor.fetchall()
                        self.date_label.setText("")
                        self.Result_label.setText("")
                        self.tableWidget.setRowCount(0)
                        for row_number, row_data in enumerate(result_new):
                            # print(row_number , row_data)
                            self.tableWidget.insertRow(row_number)

                            for column_number, data in enumerate(row_data):
                                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                    else :
                        self.date_label.setText("")
                        if sub_data.upper() != sub_name.upper():
                            self.sub_label.setText("ENTER CURRENT SUB")
                        if sem_data != sem_name:
                            self.sem_label.setText("ENTER CURRENT SEM")
                        if sec_data.upper() != sec_name.upper():
                            self.sec_label.setText("ENTER CURRENT SEC")

                        self.Result_label.setText("               ENTER THE CORRECT DETAILS IN THE SHOWN FIELD")

                except Exception as e:
                    pass

            except Exception as e:
                pass

        elif sub_data and sem_data and sec_data  and date_data !="" :
            try:
                mydb = mc.connect(
                    host="localhost",
                    user="root",
                    password="Muneshismyname",
                    database="student_database"
                )
                mycursor = mydb.cursor()
                Pos = "ONLINE"
                query = "SELECT Lecturer_name , Subject from teacher_details_new where Status = %s "
                value = (Pos,)
                mycursor.execute(query, value)
                result = mycursor.fetchall()
                for each in result:
                    lect_name, sub_name = each

                query = "SELECT Semester , Section from attendence_new where lecturer_name = %s and Subject = %s "
                value1 = (lect_name,sub_name)
                mycursor.execute(query, value1)
                result_new1 = mycursor.fetchall()
                for each in result_new1:
                    sem_name, sec_name = each

                formt = self.date_opt.text()
                tup = re.findall("\d\d-\d\d-\d\d\d\d", formt)
                if len(tup) == 1:
                    ok_date, *no_need = tup
                else:
                    ok_date = ""

                query = "SELECT Date  from attendence_new where Subject = %s  GROUP BY Date"
                value = (sub_name,)
                mycursor.execute(query, value)
                result_new = mycursor.fetchall()
                list_dt = []
                for each in result_new:
                    curr_sub_date, *no_need = each
                    list_dt.append(curr_sub_date)

                try :

                    if sub_data.upper() == sub_name.upper() and sem_data == sem_name and sec_data.upper() == sec_name.upper() and date_data == ok_date:

                        date_fmt = str(date_data)
                        ruslt = date_fmt.split("-")
                        dy, mn, yr, *no_need = ruslt
                        # print(dy, mn, yr, *no_need)

                        if int(dy) >= 00 and int(dy) <= 31 and int(mn) >= 1 and int(mn) <= 12:

                            if date_data in list_dt:

                                query = "SELECT Subject ,USN ,Status ,Semester ,Section ,Date from attendence_new where lecturer_name = %s and Subject = %s and Date = %s"
                                value = (lect_name, sub_name, date_data)
                                mycursor.execute(query, value)
                                result_new = mycursor.fetchall()
                                self.date_label.setText("")
                                self.Result_label.setText("")
                                self.tableWidget.setRowCount(0)
                                for row_number, row_data in enumerate(result_new):
                                    self.tableWidget.insertRow(row_number)
                                    for column_number, data in enumerate(row_data):
                                        self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                            else:
                                result_new = ""
                                self.tableWidget.setRowCount(0)
                                for row_number, row_data in enumerate(result_new):
                                    self.tableWidget.insertRow(row_number)
                                    for column_number, data in enumerate(row_data):
                                        self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                                self.date_label.setText("NO RECORD ")
                                self.Result_label.setText("                    THERE IS NO DATA STORED IN THAT DATE")

                        else:
                            result_new = ""
                            self.tableWidget.setRowCount(0)
                            for row_number, row_data in enumerate(result_new):
                                self.tableWidget.insertRow(row_number)
                                for column_number, data in enumerate(row_data):
                                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                            self.date_label.setText(" DD-MM-YYYY")
                            self.Result_label.setText("            DAY BETWEEN 0 TO 31 AN MONTH BETWEEN 1 TO 12")
                    else :
                        if sub_data.upper() != sub_name.upper():
                            self.sub_label.setText("ENTER CURRENT SUB")
                            result_new = ""
                            self.tableWidget.setRowCount(0)
                            for row_number, row_data in enumerate(result_new):
                                self.tableWidget.insertRow(row_number)
                                for column_number, data in enumerate(row_data):
                                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                        if sem_data != sem_name:
                            self.sem_label.setText("ENTER CURRENT SEM")
                            result_new = ""
                            self.tableWidget.setRowCount(0)
                            for row_number, row_data in enumerate(result_new):
                                self.tableWidget.insertRow(row_number)
                                for column_number, data in enumerate(row_data):
                                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                        if sec_data.upper() != sec_name.upper():
                            self.sec_label.setText("ENTER CURRENT SECT")
                            result_new = ""
                            self.tableWidget.setRowCount(0)
                            for row_number, row_data in enumerate(result_new):
                                self.tableWidget.insertRow(row_number)
                                for column_number, data in enumerate(row_data):
                                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                        if date_data != ok_date :
                            self.date_label.setText("WRONG FORMAT")
                            self.Result_label.setText("                    CORRECT FORMAT IS DD-MM-YYYY")
                            result_new = ""
                            self.tableWidget.setRowCount(0)
                            for row_number, row_data in enumerate(result_new):
                                self.tableWidget.insertRow(row_number)
                                for column_number, data in enumerate(row_data):
                                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                        self.Result_label.setText("               ENTER THE CORRECT DETAILS IN THE FIELDS SHOWN")

                except Exception as e:
                    pass


            except Exception as e:
                pass

        else:
            self.Result_label.setText("                   ENTER THE DATA IN THE SHOWN FIELD")

    # ------------------------------------------------------------------------------------------------------------

    def createaccfunction(self):
        login = s_teacher_Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# ---------------------------------------------------------------------------------------------------------------
# Account Creation page common to both admin ------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("Account_creation_modifd.ui", self)
        # self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.create__acc.clicked.connect(self.createaccfunction)
        #self.result_label.setText("account Created Successfully")
        self.Back.clicked.connect(self.createaccfunction_back)


    def createaccfunction(self):

        username = self.username.text()
        if username == "" :
            self.user_name_label.setText("Missing Username")
        else :
            self.user_name_label.setText("")

        email = self.email.text()
        if email =="" :
            self.email_label.setText("Missing Email")
        else :
            self.email_label.setText("")

        password = self.password.text()
        if password == "" :
            self.password_label.setText("Missing Password")
        else :
            self.password_label.setText("")

        if username and email and password != "" :
            #print(f"Successfully {username} created acc with email {email} and password {password}")

            emial_new = self.email.text()
            ip_address = r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"
            list2_ip = re.findall(ip_address, emial_new)

            if list2_ip != []:

                length = len(password)

                if length == 8:

                    try:
                        mydb = mc.connect(
                        host="localhost",
                        user="root",
                        password="Muneshismyname",
                        database="student_database"
                        )

                        mycursor = mydb.cursor()

                        a_name = self.username.text()
                        a_pswd = self.password.text()
                        a_email = self.email.text()

                        query = "INSERT INTO admin_login_table(Admin_name,Password,Email) VALUES (%s, %s, %s)"
                        value = (a_name, a_pswd, a_email)

                        mycursor.execute(query, value)

                        mydb.commit()
                        self.result_label.setText("                      Account Created Successfully")
                            # self.label_result.setText("Data Inserted")


                    except mc.Error as e:
                        self.result_label.setText("")
                        pass


                else:
                    self.password_label.setText("Password Error")
                    self.result_label.setText("                       Password Should Contain Exactly 8 Characters")

            else:
                self.email_label.setText("Email Error")
                self.result_label.setText("                          Email Format Is xyw@xyz.xyz")

        else :
            self.result_label.setText("                            Enter The Data In  The Shown Field")
            value = self.result_label.text()


    def createaccfunction_back(self):
        #username = self.username.text()
        #email = self.email.text()
        #password = self.password.text()
        #print("Successfully created acc with email and password")
        login = Admin_Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#-----------------------------to create 2nd admin acc

class CreateAcc_new(QDialog):
    def __init__(self):
        super(CreateAcc_new, self).__init__()
        loadUi("Account_creation_admin.ui", self)
        self.create__acc.clicked.connect(self.createaccfunction_admin_new)
        self.BACK.clicked.connect(self.createaccfunction)
        self.clear.clicked.connect(self.clear_accfunction)

    def createaccfunction_admin_new(self):
        username_n = self.username.text()
        if username_n == "":
            self.usename.setText("Missing Username")
        else:
            self.usename.setText("")

        email = self.mail.text()
        if email == "":
            self.email_label.setText("Missing Email")
        else:
            self.email_label.setText("")

        password = self.password_p.text()
        if password == "":
            self.password_label.setText("Missing Password")
        else:
            self.password_label.setText("")

        otp_data = self.otp.text()
        if otp_data == "":
            self.otp_label.setText("Missing OTP")
        else:
            self.otp_label.setText("")

        if username_n and email and password  and otp_data != "":
            #print(f"Successfully {username} created acc with email {email} and password {password}")

            emial_new = self.mail.text()
            ip_address = r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"
            list2_ip = re.findall(ip_address, emial_new)

            if list2_ip != []:

                length = len(password)

                if length == 8:

                    try:
                        tblname = "admin_otp"
                        mydb = mc.connect(
                            host="localhost",
                            user="root",
                            password="Muneshismyname",
                            database="student_database"
                        )

                        mycursor = mydb.cursor()
                        mycursor.execute("SELECT otp FROM {} ".format(tblname))

                        result_new_otp = mycursor.fetchall()
                        #print(result_new_otp)

                        if len(result_new_otp) != 0 :

                            for each in result_new_otp:
                                otp_data_st, *no_need = each

                            if username_n and email and password and otp_data != "":

                                if str(otp_data) == otp_data_st :

                                    a_name = self.username.text()
                                    a_email = self.mail.text()
                                    a_pswd = self.password_p.text()

                                    try:
                                        query = "INSERT INTO admin_login_table(Admin_name,Password,Email) VALUES (%s, %s, %s)"
                                        value = (a_name, a_pswd, a_email)
                                        mycursor.execute(query, value)
                                        mydb.commit()
                                        self.label_result.setText("                      Account Created Successfully")
                                    except Exception as e:
                                        pass

                                    try:
                                        query = "DELETE  FROM admin_otp "
                                        mycursor.execute(query)

                                    except Exception as e:
                                        pass

                                else :
                                    self.label_result.setText("                  You Have Entered Invalid Otp")
                        else:
                            self.otp_label.setText("Invalid OTP")
                            self.label_result.setText("                Enter The Valid Otp Created By Admin")
                            # value = self.result_label.text()


                    except mc.Error as e:
                        self.label_result.setText("Error Storing the data")
                        pass

                else:
                    self.password_label.setText("Password Error")
                    self.label_result.setText("     Password Should Contain Exactly 8 Characters")

            else:
                self.email_label.setText("Email Error")
                self.label_result.setText("                     EMAIL FORMAT IS XYW@XYZ.XYZ")

        else:
            self.label_result.setText("                       Enter The Data In  The Shown Field")
            #value = self.result_label.text()

    def clear_accfunction(self):
        self.username.setText("")
        self.mail.setText("")
        self.password_p.setText("")
        self.otp.setText("")
        self.usename.setText("")
        self.email_label.setText("")
        self.password_label.setText("")
        self.otp_label.setText("")
        self.label_result.setText("")

    def createaccfunction(self):
        login = Admin_Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# --------------------------------------------------------------------------------------------------------------------
# Change password  page  for all ------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
class Change_pswd(QDialog):
    def __init__(self):
        super(Change_pswd, self).__init__()
        loadUi("Change_pswd_admin.ui", self)
        self.BACK.clicked.connect(self.createBACKfunction)
        self.change.clicked.connect(self.Change_password_admin_new)
        self.clear.clicked.connect(self.Clear_data)
        # self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def Change_password_admin_new(self) :
        try:
            tblname = "admin_login_table"

            username = self.username.text()
            if username == "":
                self.username_label.setText("Missing Username")
            else:
                self.username_label.setText("")
            #------------------------------------------------------------------
            password = self.password.text()
            if password == "":
                self.pass_label.setText("Missing Password")
            else:
                self.pass_label.setText("")
            # ------------------------------------------------------------------
            Confirm_password = self.conpassword.text()
            if Confirm_password == "":
                self.confrm_pass_label.setText("Missing Confirm Password")
            else:
                self.confrm_pass_label.setText("")
            #-----------------------------------------------------------------

            if username and password and Confirm_password != "" :

                Pass_len = len(password)


                try :

                    mydb = mc.connect(
                    host="localhost",
                    user="root",
                    password="Muneshismyname",
                    database="student_database"
                    )
                    mycursor = mydb.cursor()
                    mycursor.execute("SELECT * FROM {} ".format(tblname))
                    result_old = mycursor.fetchall()
                    mj=len(result_old)
                    list_ch_admin=[]
                    for each in result_old:
                        slno, name, *no_need = each
                        list_ch_admin.append(name.upper())

                    #print(list_ch_admin)
                    if mj!=0 :
                        user_data ={}
                        for each in result_old :
                            slno,name,*no_need = each
                            name= name.upper()
                            user_data.update({slno: name})

                            #print(user_data)

                        if username.upper() in list_ch_admin:
                            #print("yes")

                            if Pass_len == 8:

                                try :

                                    for each in list(user_data.items()) :
                                        sl_num , admin_name = each
                                        #print(type(admin_name))
                                        username = username.upper()

                                        if username == admin_name :
                                            sl_num_update = sl_num

                                            if password == Confirm_password :
                                                new_password = password
                                                sql = "UPDATE admin_login_table SET Password = %s WHERE Sl_No = %s"
                                                val = (new_password, sl_num_update)
                                                mycursor.execute(sql, val)
                                                mydb.commit()
                                                self.result_label.setText("                          Password Change Is Successfull")

                                            else:
                                                if password != Confirm_password :
                                                    self.confrm_pass_label.setText("Password Error")

                                                self.result_label.setText("                       Entered Password Is Not Matching ")



                                except Exception as e :
                                    pass

                            else:
                                self.pass_label.setText("Password Error")
                                # self.confrm_pass_label.setText("PASSWORD ERROR")
                                self.result_label.setText("                Password Should Contain Exactly 8 Characters")

                        else :
                            self.username_label.setText("Username Error")
                            self.result_label.setText("             No Admin Account Exists With The Given Username")

                    else :
                        self.result_label.setText()

                except Exception as e:
                    pass

            else :
                self.result_label.setText("                                 Enter The Missing Fields")

        except Exception as e:
            pass

    def Clear_data(self):
        self.username.setText("")
        self.password.setText("")
        self.conpassword.setText("")
        self.result_label.setText("")
        self.username_label.setText("")
        self.confrm_pass_label.setText("")
        self.pass_label.setText("")

    def createBACKfunction(self):
        #print("Successfully created acc with email and password")
        login = Admin_Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Change_pswd_c_teacher(QDialog):
    def __init__(self):
        super(Change_pswd_c_teacher, self).__init__()
        loadUi("Change_pswd_CT.ui", self)
        self.change.clicked.connect(self.Change_acc_pass_function)
        self.clear.clicked.connect(self.Clear_data_CT)
        self.BACK.clicked.connect(self.createaccfunction)
        # self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def Change_acc_pass_function(self):

        try:
            tblname = "teacher_accounts_new"

            username = self.username.text()
            if username == "":
                self.username_label.setText("Missing username")
            else:
                self.username_label.setText("")
                # ------------------------------------------------------------------
            password = self.password.text()
            if password == "":
                self.pass_label.setText("Missing password")
            else:
                self.pass_label.setText("")
            # ------------------------------------------------------------------
            Confirm_password = self.conpassword.text()
            if Confirm_password == "":
                self.confrm_pass_label.setText("Missing Confirm password")
            else:
                self.confrm_pass_label.setText("")
            # ------------------------------------------------------------------

            # ------------------------------------------------------------------teacher_accounts_new
            if username and password and Confirm_password != "":

                mydb = mc.connect(
                    host="localhost",
                    user="root",
                    password="Muneshismyname",
                    database="student_database"
                )
                pos = "class teacher"
                mycursor = mydb.cursor()
                sql = "SELECT * FROM teacher_accounts_new WHERE Position = %s"
                val = (pos,)
                mycursor.execute(sql, val)
                # mycursor.execute("SELECT * FROM {} ".format(tblname))
                result_old = mycursor.fetchall()
                #print(result_old)
                mj = len(result_old)
                list_ch_ct = []

                for each in result_old:
                    slno1,not_need, name1, *no_need = each
                    #print(slno1,not_need,name1)
                    list_ch_ct.append(name1.upper())

                #print(list_ch_ct)

                if mj != 0:

                    user_data_ct = {}
                    for each in result_old:
                        slno, name,name2, *no_need = each
                        name2 = name2.upper()
                        user_data_ct.update({slno: name2})

                    #print(user_data_ct)

                    if username.upper() in list_ch_ct:
                        #print("yes")

                        pass_len = len(password)

                        if pass_len == 8 :

                            try:

                                for each in list(user_data_ct.items()):
                                    sl_num, admin_name = each
                                    #print(type(admin_name))
                                    username = username.upper()

                                    if username == admin_name:
                                        sl_num_update = sl_num

                                        if password == Confirm_password:
                                            new_password = password
                                            sql = "UPDATE teacher_accounts_new SET Password = %s WHERE Sl_No = %s"
                                            val = (new_password, sl_num_update)
                                            mycursor.execute(sql, val)
                                            mydb.commit()
                                            self.result_label.setText("                          Password Change Is Successfull")

                                        else:
                                            if password != Confirm_password:
                                                self.confrm_pass_label.setText("Password Error")

                                            self.result_label.setText("                       Entered Password Is Not Matching")



                            except Exception as e:
                                pass

                        else:
                            self.pass_label.setText("Password Error")
                            self.result_label.setText("                Password Should Contain Exactly 8 Characters")

                    else:
                        self.username_label.setText("Username Error")
                        self.result_label.setText("          No Class Teacher Account Exists With The Given Username")
                else:
                    self.result_label.setText()

            else:
                self.result_label.setText("                                 Enter The Missing Fields")

        except Exception as e:
            self.result_label.setText()

    def Clear_data_CT(self):
        self.username.setText("")
        self.username_label.setText("")
        self.password.setText("")
        self.pass_label.setText("")
        self.conpassword.setText("")
        self.confrm_pass_label.setText("")
        self.result_label.setText("")


    def createaccfunction(self):
        login = c_teacher()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Change_pswd_s_teacher(QDialog):
    def __init__(self):
        super(Change_pswd_s_teacher, self).__init__()
        loadUi("Change_pswd_ST.ui", self)
        self.change.clicked.connect(self.createaccfunction)
        self.BACK.clicked.connect(self.createaccfunction_back)
        self.clear.clicked.connect(self.Clear_data_S)
        # self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def createaccfunction(self):
        try:
            tblname = "teacher_accounts_new"

            username=self.username.text()
            if username == "":
                self.username_label.setText("Missing username")
            else:
                self.username_label.setText("")
            #------------------------------------------------------------------
            password = self.password.text()
            if password == "":
                self.pass_label.setText("Missing password")
            else:
                self.pass_label.setText("")
            # ------------------------------------------------------------------
            Confirm_password = self.conpassword.text()
            if Confirm_password == "":
                self.confrm_pass_label.setText("Missing Confirm password")
            else:
                self.confrm_pass_label.setText("")
            #------------------------------------------------------------------

            if username and password and Confirm_password != "":

                mydb = mc.connect(
                host="localhost",
                user="root",
                password="Muneshismyname",
                database="student_database"
                )
                pos = "subject teacher"
                mycursor = mydb.cursor()
                sql = "SELECT * FROM teacher_accounts_new WHERE Position = %s"
                val = (pos,)
                mycursor.execute(sql, val)
                #mycursor.execute("SELECT * FROM {} ".format(tblname))
                result_old = mycursor.fetchall()
                #print(result_old)
                mj=len(result_old)
                list_ch_st = []
                for each in result_old:
                    slno11,noneed ,name11, *no_need = each
                    list_ch_st.append(name11.upper())

                if mj!=0 :
                    user_data_st = {}
                    for each in result_old:
                        slnum1, name,name12, *no_need = each
                        name12 = name12.upper()
                        user_data_st.update({slnum1: name12})

                    #print(user_data_st)

                    if username.upper() in list_ch_st:
                        #print("yes")

                        pass_lenS = len(password)

                        if pass_lenS == 8:

                            try:

                                for each in list(user_data_st.items()):
                                    sl_num, admin_name = each
                                    #print(type(admin_name))
                                    username = username.upper()

                                    if username == admin_name:
                                        sl_num_update = sl_num

                                        if password == Confirm_password:
                                            new_password = password
                                            sql = "UPDATE teacher_accounts_new SET Password = %s WHERE Sl_No = %s"
                                            val = (new_password, sl_num_update)
                                            mycursor.execute(sql, val)
                                            mydb.commit()
                                            self.result_label.setText("                          Password Change Is Successfull")

                                        else:
                                            if password != Confirm_password:
                                                self.confrm_pass_label.setText("Password Error")

                                            self.result_label.setText("                       Entered Password Is Not Matching")



                            except Exception as e:
                                pass

                        else:
                            self.pass_label.setText("Password Error")
                            self.result_label.setText("                Password Should Contain Exactly 8 Characters")

                    else:
                        self.username_label.setText("Username Error")
                        self.result_label.setText("           No Subject Teacher Account Exists With The Given Username")

                else :
                    self.result_label.setText()

            else :
                self.result_label.setText("                                 Enter The Missing Fields")

        except mc.Error as e:
            pass

    def Clear_data_S(self):
        self.username.setText("")
        self.username_label.setText("")
        self.password.setText("")
        self.pass_label.setText("")
        self.conpassword.setText("")
        self.confrm_pass_label.setText("")
        self.result_label.setText("")


    def createaccfunction_back(self):
        #print("Successfully created acc with email and password")
        login = s_teacher()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# ------------------------------------------------------------------------------------------------------

app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1500)
widget.setFixedHeight(750)
widget.show()
app.exec()