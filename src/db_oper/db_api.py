import psycopg2


class QueryAPI():

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="postgres",
            port=5432
        )
        self.cur = self.conn.cursor()

    def add_member(self, username, password):
        try:
            self.cur.execute("INSERT INTO members (username, password) VALUES (%s, %s)", (username, password))
            self.conn.commit()
        except:
           print("Adding memeber didn't work for some reason")
           
    def get_member_username_by_username(self, username):
        self.cur.execute("SELECT username FROM members WHERE username = (%s)", (username,))
        return self.cur.fetchone()

    def get_member_password_by_username(self, username):
        self.cur.execute("SELECT password FROM members WHERE username = (%s)", (username,))
        return self.cur.fetchone()[0]
    
    def get_member_id_by_username(self, username):
        self.cur.execute("SELECT member_id FROM members WHERE username = (%s)", (username,))
        return self.cur.fetchone()[0]
    
    def get_member_username_by_id(self, id):
        self.cur.execute("SELECT username FROM members WHERE member_id = (%s)", (id,))
        return self.cur.fetchone()
    
    def get_member_password_by_id(self, id):
        self.cur.execute("SELECT password FROM members WHERE member_id = (%s)", (id,))
        return self.cur.fetchone()

    def update_member_username_by_id(self, username, id):
        self.cur.execute("UPDATE members SET username = (%s) WHERE member_id = (%s)", (username, id))
        self.conn.commit()

    def update_member_password_by_id(self, password, id):
        self.cur.execute("UPDATE members SET password = (%s) WHERE member_id = (%s)", (password, id))
        self.conn.commit()

    def add_exercise_entry_by_id(self, id, *args):
        if len(args[2]) == 0 and len(args[3]) == 0:
            self.cur.execute("INSERT INTO dashboard (member_id, exercise, exercise_routine) VALUES (%s, %s, %s)", (id, args[0], args[1]))
        elif len(args[3]) == 0:
            self.cur.execute("INSERT INTO dashboard (member_id, exercise, exercise_routine, personal_best) VALUES (%s, %s, %s, %s)", (id, args[0], args[1], args[2]))
        elif len(args[2]) == 0:
            self.cur.execute("INSERT INTO dashboard (member_id, exercise, exercise_routine, body_weight) VALUES (%s, %s, %s, %s)", (id, args[0], args[1], args[3]))
        else:
            self.cur.execute("INSERT INTO dashboard (member_id, exercise, exercise_routine, personal_best, body_weight) VALUES (%s, %s, %s, %s, %s)", (id, args[0], args[1], args[2], args[3]))
        self.conn.commit()

    def delete_exercise_by_exercise(self, id, exercise):
        self.cur.execute("DELETE FROM dashboard WHERE member_id = (%s) AND exercise = (%s)", (id, exercise))
        self.conn.commit()

    def get_exercise_by_exercise(self, id, exercise):
        self.cur.execute("SELECT exercise FROM dashboard WHERE member_id = (%s) and exercise = (%s)", (id, exercise))
        return self.cur.fetchone()
    
    def update_exercise_by_exercise(self, id, *args):
        if len(args[2]) == 0 and len(args[3]) == 0:
            self.cur.execute("UPDATE dashboard SET exercise_routine = (%s) WHERE member_id = (%s) AND exercise = (%s)", (args[1], id, args[0]))
        elif len(args[3]) == 0:
            self.cur.execute("UPDATE dashboard SET exercise_routine = (%s), personal_best = (%s) WHERE member_id = (%s) AND exercise = (%s)", (args[1], args[2], id, args[0]))
        elif len(args[2]) == 0:
            self.cur.execute("UPDATE dashboard SET exercise_routine = (%s), body_weight = (%s) WHERE member_id = (%s) AND exercise = (%s)", (args[1], args[3], id, args[0]))
        else:
            self.cur.execute("UPDATE dashboard SET exercise_routine = (%s), personal_best = (%s), body_weight = (%s) WHERE member_id = (%s) AND exercise = (%s)", (args[1], args[2], args[3], id, args[0]))
        self.conn.commit()

    def get_all_exercises_by_id(self, id):
        self.cur.execute("SELECT * FROM dashboard WHERE member_id = (%s)", (id,))
        return self.cur.fetchall()

    def get_goal_by_goal(self, id, goal):
        self.cur.execute("SELECT goal FROM goals WHERE member_id = (%s) AND goal = (%s)", (id, goal))
        return self.cur.fetchone()
    
    def add_goal_by_goal(self, id, goal, target):
        self.cur.execute("INSERT INTO goals (member_id, goal, target) VALUES (%s, %s, %s)", (id, goal, target))
        self.conn.commit()
    
    def delete_goal_by_goal(self, id, goal):
        self.cur.execute("DELETE FROM goals WHERE member_id = (%s) AND goal = (%s)", (id, goal))
        self.conn.commit()

    def update_goal_by_goal(self, id, goal, target):
        self.cur.execute("UPDATE goals SET target = (%s) WHERE member_id = (%s) AND goal = (%s)", (target, id, goal))
        self.conn.commit()

    def get_all_goals_by_id(self, id):
        self.cur.execute("SELECT * FROM goals WHERE member_id = (%s)", (id,))
        return self.cur.fetchall()

    def add_trainer_by_username(self, username, password):
        try:
            self.cur.execute("INSERT INTO trainers (username, password) VALUES (%s, %s)", (username, password))
            self.conn.commit()
        except:
           print("Adding trainer didn't work for some reason")

    def get_trainer_username_by_username(self, username):
        self.cur.execute("SELECT * FROM trainers WHERE username = (%s)", (username,))
        return self.cur.fetchone()
    
    def get_trainer_username_by_id(self, id):
        self.cur.execute("SELECT username FROM trainers WHERE trainer_id = (%s)", (id,))
        return self.cur.fetchone()[0]
    
    def get_trainer_id_by_username(self, username):
        self.cur.execute("SELECT trainer_id FROM trainers WHERE username = (%s)", (username,))
        id = self.cur.fetchone()
        return None if id == None else id[0]
    
    def get_trainer_password_by_username(self, username):
        self.cur.execute("SELECT password FROM trainers WHERE username = (%s)", (username,))
        return self.cur.fetchone()[0]
    
    def get_availability_by_id(self, id):
        self.cur.execute("SELECT * FROM trainer_schedule WHERE trainer_id = (%s)", (id,))
        return self.cur.fetchall()
    
    def get_availability_by_interval(self, id, date, start, end):
        self.cur.execute("SELECT * FROM trainer_schedule WHERE trainer_id = (%s) AND available_day = (%s) AND (available_start_time = (%s) OR available_end_time = (%s))", (id, date, start, end))
        return self.cur.fetchone()
    
    def add_availability_by_id(self, id, date, start_time, end_time):
        self.cur.execute("INSERT INTO trainer_schedule (trainer_id, available_day, available_start_time, available_end_time) VALUES (%s, %s, %s, %s)", 
                            (id, date, start_time, end_time))
        self.conn.commit()

    def delete_availability_by_availability(self, id, date, start_time, end_time):
        self.cur.execute("DELETE FROM trainer_schedule WHERE trainer_id = (%s) AND available_day = (%s) AND available_start_time = (%s) AND available_end_time = (%s)", 
                            (id, date, start_time, end_time))
        self.conn.commit()

    def get_admin_username_by_username(self, username):
        self.cur.execute("SELECT username FROM administrators WHERE username = (%s)", (username,))
        return self.cur.fetchone()
    
    def add_admin_by_username(self, username, password):
        self.cur.execute("INSERT INTO administrators (username, password) VALUES (%s, %s)", 
                            (username, password))
        self.conn.commit()
    
    def get_admin_password_by_username(self, username):
        self.cur.execute("SELECT password FROM administrators WHERE username = (%s)", (username,))
        return self.cur.fetchone()[0]

    def get_admin_id_by_username(self, username):
        self.cur.execute("SELECT admin_id FROM administrators WHERE username = (%s)", (username,))
        return self.cur.fetchone()[0]

    def get_all_rooms(self):
        self.cur.execute("SELECT * FROM rooms")
        return self.cur.fetchall()
    
    def get_room_by_id(self, id):
        self.cur.execute("SELECT * FROM rooms WHERE room_id = (%s)", (id,))
        return self.cur.fetchone()
    
    def update_room_by_id(self, id, availability, usage):
        if usage == '' or 'ex.' in usage:
            self.cur.execute("UPDATE rooms SET status = (%s) WHERE room_id = (%s)", (availability, id))
        elif availability == '' or 'ex.' in availability:
            self.cur.execute("UPDATE rooms SET usage = (%s) WHERE room_id = (%s)", (usage, id))
        else:
            self.cur.execute("UPDATE rooms SET status = (%s), usage = (%s) WHERE room_id = (%s)", (availability, usage, id))
        self.conn.commit()

    def get_all_equipments(self):
        self.cur.execute("SELECT * FROM equipment")
        return self.cur.fetchall()
    
    def get_equipment_by_id(self, id):
        self.cur.execute("SELECT * FROM equipment WHERE equipment_id = (%s)", (id,))
        return self.cur.fetchone()
    
    def add_equipment_by_id(self, id, name, status):
        if status == '' or 'ex' in status:
            self.cur.execute("INSERT into equipment (equipment_id, equipment_name) VALUES (%s, %s)", (id, name))
        else:
            self.cur.execute("INSERT into equipment (equipment_id, equipment_name, equipment_status) VALUES (%s, %s, %s)", (id, name, status))
        self.conn.commit()

    def delete_equipment_by_id(self, id):
        self.cur.execute("DELETE FROM equipment WHERE equipment_id = (%s)", (id,))
        self.conn.commit()

    def update_equipment_by_id(self, id, name, status):
        if status == '' or 'ex.' in status:
            self.cur.execute("UPDATE equipment SET equipment_name = (%s) WHERE equipment_id = (%s)", (name, id))
        elif name == '' or 'ex.' in name:
            self.cur.execute("UPDATE equipment SET equipment_status = (%s) WHERE equipment_id = (%s)", (status, id))
        else:
            self.cur.execute("UPDATE equipment SET equipment_name = (%s), equipment_status = (%s) WHERE equipment_id = (%s)", (name, status, id))
        self.conn.commit()

    def get_bill_by_id(self, id):
        self.cur.execute("SELECT * FROM bills WHERE bill_id = (%s)", (id))
        return self.cur.fetchone()

    def add_bill_by_id(self, id, name, amount, item):
        self.cur.execute("INSERT INTO bills (bill_id, member_name, amount, item) VALUES (%s, %s, %s, %s)", (id, name, amount, item))
        self.conn.commit()

    def get_all_bills(self):
        self.cur.execute("SELECT * FROM bills")
        return self.cur.fetchall()
    
    def delete_bill_by_id(self, id):
        self.cur.execute("DELETE FROM bills WHERE bill_id = (%s)", (id,))
        self.conn.commit()

    def update_bill_by_id(self, id, name, amount, item):
        if (name == '' or 'ex.' in name) and (amount == '' or 'ex.' in amount):
            self.cur.execute("UPDATE bills SET item = (%s) WHERE bill_id = (%s)", (item, id))
        elif (name == '' or 'ex.' in name) and (item == '' or 'ex.' in item):
            self.cur.execute("UPDATE bills SET amount = (%s) WHERE bill_id = (%s)", (amount, id))
        elif (amount == '' or 'ex.' in amount) and (item == '' or 'ex.' in item):
            self.cur.execute("UPDATE bills SET member_name = (%s) WHERE bill_id = (%s)", (name, id))
        elif name == '' or 'ex.' in name:
            self.cur.execute("UPDATE bills SET amount = (%s), item = (%s) WHERE bill_id = (%s)", (amount, item, id))
        elif item == '' or 'ex.' in item:
            self.cur.execute("UPDATE bills SET member_name = (%s), amount = (%s) WHERE bill_id = (%s)", (name, amount, id))
        elif amount == '' or 'ex.' in amount:
            self.cur.execute("UPDATE bills SET member_name = (%s), item = (%s) WHERE bill_id = (%s)", (name, item, id))
        else:
            self.cur.execute("UPDATE bills SET member_name = (%s), amount = (%s), item = (%s) WHERE bill_id = (%s)", (name, amount, item, id))
        self.conn.commit()

    def get_all_classess(self):
        self.cur.execute("SELECT * FROM class_schedule")
        return self.cur.fetchall()
    
    def get_class_by_id(self, id):
        self.cur.execute("SELECT * FROM class_schedule WHERE class_id = (%s)", (id,))
        return self.cur.fetchone()
    
    def get_trainer_schedule_day_by_day(self, day, id):
        self.cur.execute("SELECT available_day FROM trainer_schedule WHERE available_day = (%s) AND trainer_id = (%s)", (day, id))
        return self.cur.fetchone()

    def get_trainer_schedule_start_by_start(self, start, id):
        self.cur.execute("SELECT available_start_time FROM trainer_schedule WHERE available_start_time = (%s) AND trainer_id = (%s)", (start, id))
        return self.cur.fetchone()

    def get_trainer_schedule_end_by_end(self, end, id):
        self.cur.execute("SELECT available_end_time FROM trainer_schedule WHERE available_end_time = (%s) AND trainer_id = (%s)", (end, id))
        return self.cur.fetchone()

    def add_class_by_id(self, class_id, trainer_id, name, day, start, end):
        self.cur.execute("INSERT INTO class_schedule (class_id, trainer_id, class_name, session_day, start_time, end_time) VALUES (%s, %s, %s, %s, %s, %s)", (class_id, trainer_id, name, day, start, end))
        self.conn.commit()

    def get_all_availabilites(self):
        self.cur.execute("SELECT * FROM trainer_schedule")
        return self.cur.fetchall()
    
    def delete_class_by_id(self, class_id):
        self.cur.execute("DELETE FROM class_schedule WHERE class_id = (%s)", (class_id,))
        self.conn.commit()

    def get_trainer_schedule_from_class_by_id(self, class_id):
        self.cur.execute("SELECT trainer_id, session_day, start_time, end_time FROM class_schedule WHERE class_id = (%s)", (class_id,))
        return self.cur.fetchone()
    
    def update_class_by_id(self, class_id, trainer_id, name, day, start, end):
        
        if name == '' or 'ex.' in name:
            self.cur.execute("UPDATE class_schedule SET trainer_id = (%s), session_day = (%s), start_time = (%s), end_time = (%s) WHERE class_id = (%s)", (trainer_id, day, start, end, class_id))
        elif trainer_id == ''  or day == '' or start == '' or end == '' or 'ex.' in day or'ex.' in start or 'ex.' in end:
            self.cur.execute("UPDATE class_schedule SET class_name = (%s) WHERE class_id = (%s)", (name, class_id))
        else:
            self.cur.execute("UPDATE class_schedule SET trainer_id = (%s), session_day = (%s), start_time = (%s), end_time = (%s), class_name = (%s) WHERE class_id = (%s)", (trainer_id, day, start, end, name, class_id))
        self.conn.commit()

    def get_member_schedule(self, id):
        self.cur.execute("SELECT session_day, session_id, to_char(start_time, 'HH24:MI') || ' - ' || to_char(end_time, 'HH24:MI') AS time FROM member_schedule WHERE member_id = (%s)", (id,))
        return self.cur.fetchall()
    
    def get_member_schedule_by_time(self, id, day, start, end):
        self.cur.execute("SELECT * FROM member_schedule WHERE member_id = (%s) AND session_day = (%s) AND (start_time = (%s) OR end_time = (%s))", (id, day, start, end))
        return self.cur.fetchone()
    
    def get_member_schedule_by_id(self, id, session):
        self.cur.execute("SELECT * FROM member_schedule WHERE member_id = (%s) AND session_id = (%s)", (id, session))
        return self.cur.fetchone()
    
    def add_member_schedule_by_time(self, id, trainer_id, day, start, end):
        self.cur.execute("INSERT INTO member_schedule (member_id, trainer_id, session_day, start_time, end_time) VALUES (%s, %s, %s, %s, %s)", (id, trainer_id, day, start, end))
        self.conn.commit()

    def get_trainer_schedule_from_member_by_time(self, id, session_id):
        self.cur.execute("SELECT trainer_id, session_day, start_time, end_time FROM member_schedule WHERE member_id = (%s) AND session_id = (%s)", (id, session_id))
        return self.cur.fetchone()
    
    def get_trainer_schedule_from_member_by_time_and_id(self, id, day, start, end):
        self.cur.execute("SELECT trainer_id, session_day, start_time, end_time FROM member_schedule WHERE trainer_id = (%s) AND session_day = (%s) AND start_time = (%s) AND end_time = (%s)", (id, day, start, end))
        return self.cur.fetchone()
    
    def get_trainer_schedule_from_member_by_id(self, id, session):
        self.cur.execute("SELECT trainer_id, session_day, start_time, end_time FROM member_schedule WHERE member_id = (%s) AND session_id = (%s)", (id, session))
        return self.cur.fetchone()

    def delete_session_by_time(self, id, session_id):
        self.cur.execute("DELETE FROM member_schedule WHERE member_id = (%s) AND session_id = (%s)", (id, session_id))
        self.conn.commit()
    
    def update_session_by_id(self, id, trainer_id, session, day, start, end):
        self.cur.execute("UPDATE member_schedule SET trainer_id = (%s), session_day = (%s), start_time = (%s), end_time = (%s) WHERE member_id = (%s) AND session_id = (%s) ", (trainer_id, day, start, end, id, session))
        self.conn.commit() 

    def get_member_class_by_id(self, id, class_id):
        self.cur.execute("SELECT * FROM class_registration WHERE class_id = (%s) AND member_id = (%s)", (class_id, id))
        return self.cur.fetchone()

    def add_member_to_class_by_id(self, member_id, class_id):
        self.cur.execute("INSERT INTO class_registration (class_id, member_id) VALUES (%s, %s)", (class_id, member_id))
        self.conn.commit()

    def get_member_class_schedule(self, id):
        self.cur.execute("SELECT class_id FROM class_registration WHERE member_id = (%s)", (id,))
        return self.cur.fetchall()
    
    def get_class_time_by_id(self, id):
        self.cur.execute("SELECT session_day, class_name, to_char(start_time, 'HH24:MI') || ' - ' || to_char(end_time, 'HH24:MI') AS time FROM class_schedule WHERE class_id = (%s)", (id,))
        return self.cur.fetchall()
    
    def get_class_regestry_by_id(self, class_id, id):
        self.cur.execute("SELECT * FROM class_registration WHERE member_id = (%s) AND class_id = (%s)", (id, class_id))
        return self.cur.fetchone()
    
    def delete_class_regestry_by_id(self, class_id, id):
        self.cur.execute("DELETE FROM class_registration WHERE class_id = (%s) AND member_id = (%s)", (class_id, id))
        self.conn.commit()

    # Closing any open connections and cursors
    def close_connection(self):
        self.conn.close()
        self.cur.close()