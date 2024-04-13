INSERT INTO administrators (username, password) 
VALUES 
('Elon Musk', 'tesla'),
('Jeff Bezos', 'amazon');

INSERT INTO trainers (username, password)
VALUES
('Lebron James', 'sunshine'),
('Rocky', 'boxer'),
('Usain Bolt', 'fastest');

INSERT INTO members (username, password)
VALUES
('Ronaldo', 'CR7'),
('Faker', 'olympian');

INSERT INTO class_schedule (trainer_id, class_name, session_day, start_time, end_time)
VALUES
(1, 'Dunks', '2024-04-15', '14:00', '15:00'),
(1, 'Layups', '2024-04-15', '15:00', '16:00'),
(2, 'Conditioning', '2024-04-17', '18:00', '20:00'),
(2, 'Sparring', '2024-04-20', '18:00', '20:00');

INSERT INTO schedules (class_id, admin_id)
VALUES
(DEFAULT, DEFAULT),
(DEFAULT, 1),
(DEFAULT, 1),
(DEFAULT, 1);


INSERT INTO dashboard (member_id, exercise, exercise_routine, personal_best, body_weight) 
VALUES 
(1, 'Weighted Running', '5 km', '15:00 min', 83),
(1, 'Penalties', '100', NULL, 83),
(1, 'Football', '90 min', NULL, 83);

INSERT INTO goals (member_id, goal, target)
VALUES
(1, 'Football', 'World Cup Trophy'),
(2, 'Scrims', 'Dominate'),
(2, 'Worlds', 'Win'),
(2, 'Olympics', 'Gold Medal'),
(2, 'Bicep Curls', '100 lbs');

INSERT INTO member_schedule (trainer_id, member_id, session_day, start_time, end_time)
VALUES
(1, 2, '2024-04-16', '13:00', '18:00'),
(1, 2, '2024-04-17', '22:00', '24:00');

INSERT INTO class_registration (class_id, member_id)
VALUES
(1,2),
(2,2);

INSERT INTO trainer_schedule (trainer_id, available_day, available_start_time, available_end_time)
VALUES
(1, '2024-04-18', '17:00', '18:00'),
(1, '2024-04-19', '18:00', '19:00'),
(3, '2024-04-18', '17:00', '19:00'),
(3, '2024-04-19', '18:00', '20:00');

INSERT INTO rooms (status, usage)
VALUES 
('Available', NULL),
('Occupied', 'Zumba'),
('Available', NULL);

INSERT INTO update_room (room_id, admin_id) 
VALUES 
(DEFAULT, DEFAULT),
(DEFAULT, 1),
(DEFAULT, 1);

INSERT INTO equipment (equipment_name, equipment_status)
VALUES
('Basketball', 'Good'),
('Basketball', 'Deflated'),
('Squat Rack', 'Good'),
('Leg Press', 'Repair');

INSERT INTO monitors (equipment_id, admin_id) 
VALUES 
(DEFAULT, DEFAULT),
(DEFAULT, 1),
(DEFAULT, 1),
(DEFAULT, 1);

INSERT INTO bills (member_name, amount, item)
VALUES
('Faker', '100', 'League Skin');


INSERT INTO issues (bill_id, admin_id) 
VALUES 
(DEFAULT, DEFAULT);