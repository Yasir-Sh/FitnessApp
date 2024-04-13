CREATE TABLE members (
    member_id SERIAL PRIMARY KEY, 
    username VARCHAR(256) UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL
);

CREATE TABLE trainers (
    trainer_id SERIAL PRIMARY KEY,
    username VARCHAR(256) NOT NULL UNIQUE,
    password VARCHAR(256) NOT NULL
);

CREATE TABLE administrators (
    admin_id SERIAL PRIMARY KEY,
    username VARCHAR(256) NOT NULL UNIQUE,
    password VARCHAR(256) NOT NULL
);

CREATE TABLE member_schedule(
    session_id SERIAL PRIMARY KEY, 
    trainer_id SERIAL,
    member_id SERIAL,
    session_day DATE NOT NULL,
    start_time TIME NOT NULL, 
    end_time TIME NOT NULL,
    UNIQUE(member_id, session_day, start_time, end_time),
    Foreign Key (member_id) REFERENCES members(member_id) ON DELETE CASCADE ,
    Foreign Key (trainer_id) REFERENCES trainers(trainer_id) ON DELETE CASCADE 
);

CREATE TABLE trainer_schedule (
    trainer_id SERIAL,
    available_day DATE NOT NULL,
    available_start_time TIME NOT NULL,
    available_end_time TIME NOT NULL, 
    UNIQUE (trainer_id, available_day, available_start_time, available_end_time),
    Foreign Key (trainer_id) REFERENCES trainers(trainer_id) ON DELETE CASCADE
);

CREATE TABLE class_schedule(
    class_id SERIAL PRIMARY KEY,
    trainer_id SERIAL,
    class_name VARCHAR(256) NOT NULL,
    session_day DATE NOT NULL,
    start_time TIME NOT NULL, 
    end_time TIME NOT NULL,
    Foreign Key (trainer_id) REFERENCES trainers(trainer_id) ON DELETE CASCADE
);

CREATE TABLE schedules(
    class_id SERIAL,
    admin_id SERIAL,
    Foreign Key (class_id) REFERENCES class_schedule(class_id) ON DELETE CASCADE, 
    Foreign Key (admin_id) REFERENCES administrators(admin_id) ON DELETE CASCADE,
    PRIMARY KEY (class_id, admin_id) 
);


CREATE TABLE class_registration(
    class_id SERIAL,
    member_id SERIAL,
    Foreign Key (class_id) REFERENCES class_schedule(class_id) ON DELETE CASCADE, 
    Foreign Key (member_id) REFERENCES members(member_id) ON DELETE CASCADE 
);

CREATE TABLE dashboard (
    member_id SERIAL,
    exercise VARCHAR(256) NOT NULL UNIQUE,
    exercise_routine VARCHAR(256) NOT NULL,
    personal_best VARCHAR(256),
    body_weight INT,
    Foreign Key (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

CREATE TABLE goals (
    member_id SERIAL,
    goal VARCHAR(256) NOT NULL UNIQUE,
    target VARCHAR(256) NOT NULL,
    Foreign Key (member_id) REFERENCES members ON DELETE CASCADE 
);

CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    status VARCHAR(256) NOT NULL,
    usage VARCHAR(256)
);

CREATE TABLE equipment (
    equipment_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(256) NOT NULL,
    equipment_status VARCHAR(256)
);

CREATE TABLE bills(
    bill_id SERIAL PRIMARY KEY,
    member_id SERIAL, 
    amount FLOAT NOT NULL,
    item VARCHAR(256) NOT NULL,
    Foreign Key (member_id) REFERENCES members(member_id) ON DELETE CASCADE 
);

CREATE TABLE issues(
    bill_id SERIAL,
    admin_id SERIAL, 
    Foreign Key (bill_id) REFERENCES bills(bill_id) ON DELETE CASCADE,
    Foreign Key (admin_id) REFERENCES administrators(admin_id) ON DELETE CASCADE, 
    PRIMARY KEY (bill_id, admin_id)
);

CREATE TABLE monitors(
    equipment_id SERIAL,
    admin_id SERIAL, 
    Foreign Key (equipment_id) REFERENCES equipment(equipment_id) ON DELETE CASCADE,
    Foreign Key (admin_id) REFERENCES administrators(admin_id) ON DELETE CASCADE, 
    PRIMARY KEY (equipment_id, admin_id) 
);

CREATE TABLE update_room(
    room_id SERIAL,
    admin_id SERIAL, 
    Foreign Key (room_id) REFERENCES rooms(room_id) ON DELETE CASCADE,
    Foreign Key (admin_id) REFERENCES administrators(admin_id) ON DELETE CASCADE, 
    PRIMARY KEY (room_id, admin_id) 
);