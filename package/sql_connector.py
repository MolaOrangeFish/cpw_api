import mysql.connector
from time import sleep

def connect_to_db():
    while True:
        try:
            connection = mysql.connector.connect(host="localhost",
                                                user="root",
                                                password="",
                                                database="cpw_sql")
            return connection
        except Exception as e:
            print("Error: " + str(e))
            print("Will reconnect to db in 3 sec.")
            sleep(3)

def format_time(time):
    return time.strftime('%Y-%m-%d %H:%M:%S')  #นำเวลาที่ได้รับมาแล้วแปลงเป็นสตริง

def insert_text_and_type(message, message_group, reply, user_id,user_type="bot"):
    try:
        connection = connect_to_db()
        db_cursor = connection.cursor()

        if(user_type == "contacter"):
            # คำสั่ง SQL สำหรับเพิ่มข้อมูล
            sql_command = "INSERT INTO contacter_message (message_id,message, message_group, reply, c_id) VALUES (UUID(), %s, %s, %s, %s)"
            # ทำการ execute คำสั่ง SQL
            db_cursor.execute(sql_command, (message, message_group, int(reply), user_id))
        elif(user_type == "admin"):  ##ยังทำไม่ได้ทำๆไวก่อน อย่าพึ่งไปสนใจ
            # คำสั่ง SQL สำหรับเพิ่มข้อมูล
            sql_command = "INSERT INTO admin_message (`a_message_id`,`message`,`userID`,`last_interact`,`c_id`) VALUES (UUID(),%s,1,%s,%s)"
            # ทำการ execute คำสั่ง SQL
            db_cursor.execute(sql_command, (message, message_group, int(reply), user_id))
        else:
            # คำสั่ง SQL สำหรับเพิ่มข้อมูล
            sql_command = "INSERT INTO admin_message (`a_message_id`,`message`,`userID`,`c_id`) VALUES (UUID(),%s,9999,%s)"
            # ทำการ execute คำสั่ง SQL
            db_cursor.execute(sql_command, (message,user_id))

        connection.commit()
        connection.close()

        print("Insertion successful.")
        update_interact_contacter(user_id,user_type)
        
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")

def search_contacter(c_id):
    try:
        print("Get in search_contacter <<")
        connection = connect_to_db()
        db_cursor = connection.cursor()

        # คำสั่ง SQL สำหรับเพิ่มข้อมูล
        sql_command = "select * from contacter where c_id = %s"
        # ทำการ execute คำสั่ง SQL
        db_cursor.execute(sql_command, (c_id,))

        res = db_cursor.fetchall()
        print(f"search_contacter result {res}")
        return res
        # connection.close()

    except Exception as e:
        print(f"Error: {e}")

def get_answer(message_group,main_question_type = None):
    try:
        print("Get in get_answer <<")
        connection = connect_to_db()
        db_cursor = connection.cursor()

        # คำสั่ง SQL สำหรับเพิ่มข้อมูล
        if message_group != "question":
            sql_command = "SELECT answer FROM `answer_question` WHERE message_group = %s"
            # ทำการ execute คำสั่ง SQL
            db_cursor.execute(sql_command, (message_group))
        else:
            sql_command = "SELECT answer FROM `answer_question` WHERE message_group = %s AND question_type = %s"
            # ทำการ execute คำสั่ง SQL
            db_cursor.execute(sql_command, (message_group, main_question_type))

        res = db_cursor.fetchone()
        print(f"get_answer result {res[0]}")
        return res[0]

    except Exception as e:
        print(f"Error: {e}")

def get_main_question_type(c_id):
    try:
        print("Get in get_main_question_type <<")
        connection = connect_to_db()
        db_cursor = connection.cursor()

        # คำสั่ง SQL สำหรับเพิ่มข้อมูล
        sql_command = "select main_question_type from contacter where c_id = %s"
        # ทำการ execute คำสั่ง SQL
        db_cursor.execute(sql_command, (c_id,))

        res = db_cursor.fetchone()
        print(f"get_main_question_type result {res[0]}")
        return res[0]
        # connection.close()

    except Exception as e:
        print(f"Error: {e}")    

def insert_sub_answer(answer,sub_type):
    try:
        connection = connect_to_db()
        db_cursor = connection.cursor()

        
        sql_command = "INSERT INTO sub_answer (s_answer_id,answer, sub_type) VALUES (UUID(), %s, %s)"
            # ทำการ execute คำสั่ง SQL
        db_cursor.execute(sql_command, (answer, sub_type))

        connection.commit()
        connection.close()

        print("Insertion successful.")
        
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")

def update_main_question_type(type,c_id):
    try:   
        print("Get in update_main_question_type<<")
        connection = connect_to_db()
        db_cursor = connection.cursor()

        
        sql_command = "UPDATE `contacter` SET `main_question_type`=%s,`last_interact`= NOW() WHERE `c_id`=%s"

            # ทำการ execute คำสั่ง SQL
        db_cursor.execute(sql_command, (type,c_id))

        connection.commit()
        connection.close()

        print("Update successful.")
        
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")

def insert_contacter(c_id,c_name):
    try:
        connection = connect_to_db()
        db_cursor = connection.cursor()

        # คำสั่ง SQL สำหรับเพิ่มข้อมูล
        sql_command = "Insert into contacter (c_id,c_name) VALUES (%s,%s)"
    
        # ทำการ execute คำสั่ง SQL
        db_cursor.execute(sql_command, (c_id,c_name))

        connection.commit()
        connection.close()

        print("Insertion successful.")
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")

def update_interact_contacter(c_id,user_type):
    print(">>>Get in update_interact_contacter(c_id)<<<<")
    try:
        connection = connect_to_db()
        db_cursor = connection.cursor()

        if(user_type == "contacter"):
            # คำสั่ง SQL สำหรับดึงเวลลาที่มีการติดต่อล่าสุดของcontacter
            sql_command = "SELECT max(last_interact) FROM `contacter_message` WHERE c_id = %s"
        elif(user_type in ["admin","bot"]):
            sql_command = "SELECT max(last_interact) FROM `admin_message` WHERE c_id = %s"
    
        # ทำการ execute คำสั่ง SQL
        db_cursor.execute(sql_command, (c_id,))

        # ทำการformat datetime ให้อ่านออกใช้method fetchOne แล้วเลือกndex 0 ไปใส่ function format_time
        last_contacter_interact_time = format_time(db_cursor.fetchone()[0])

        print(f"get last_contacter_interact_time : {last_contacter_interact_time }")


        # คำสั่ง SQL สำหรับupdate ติดต่อล่าสุดของcontacter
        sql_command = "UPDATE contacter SET last_interact = %s WHERE c_id = %s"
        db_cursor.execute(sql_command, (last_contacter_interact_time,c_id,))

        connection.commit()
        connection.close()

        print(f"Update successful. Time :{last_contacter_interact_time} userId :{c_id}")
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")

    try:
        print("Get in get_current_reply_status <<")
        connection = connect_to_db()
        db_cursor = connection.cursor()

        # คำสั่ง SQL สำหรับเพิ่มข้อมูล
        sql_command =  "SELECT cm.last_interact last_interact,'contacter' as role "
        sql_command+=  "from contacter_message cm " 
        sql_command+=  "INNER join contacter c " 
        sql_command+=  "on c.c_id = cm.c_id  "
        sql_command+=  "WHERE cm.c_id = %s  "
        sql_command+=  "UNION  "
        sql_command+=  "SELECT am.last_interact last_interact,'admin' as role  "
        sql_command+=  "FROM admin_message am  "
        sql_command+=  "INNER JOIN cpw_user cu on cu.userID=am.userID  "
        sql_command+=  "WHERE am.c_id = %s ORDER BY last_interact Desc "
        sql_command+=  "Limit 1"
        # ทำการ execute คำสั่ง SQL
        db_cursor.execute(sql_command, (c_id,c_id,))

        res = db_cursor.fetchall()
        time = res[0][0]
        user_type = res[0][1]
        print(f"get_current_reply_status\n user_type: {user_type}\n time: {time}\n")
        return user_type
        # connection.close()

    except Exception as e:
        print(f"Error: {e}")



