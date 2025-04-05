CREATE TABLE Pilot (
    pilot_id INTEGER PRIMARY KEY,
    first_name text not null,
    last_name text not null,
    licence_number text not null unique,
    role text not null,
    mobile_number integer not null

);

CREATE TABLE Location (
    location_id INTEGER PRIMARY KEY,
    airport_code text not null,
    city text not null,
    country text not null

);

CREATE TABLE Aircraft (
    aircraft_id INTEGER PRIMARY KEY,
    model text not null,
    licence_plate text not null unique,
    functional_status text not null

);

CREATE TABLE Flight (
    flight_id INTEGER PRIMARY KEY,
    departure_location_id INTEGER,
    arrival_location_id INTEGER,
    aircraft_id INTEGER not null,
    flight_number INTEGER not null,
    departure_time DATETIME not null,
    arrival_time DATETIME not null,
    status text not null,
    FOREIGN KEY (departure_location_id) REFERENCES Location(location_id),
    FOREIGN KEY (arrival_location_id) REFERENCES Location(location_id),
    FOREIGN KEY (aircraft_id) REFERENCES Aircraft(aircraft_id)


);

CREATE TABLE PilotAssignment (
    flight_id integer ,
    pilot_id text not null,
    role text not null,
    PRIMARY KEY (flight_Id,pilot_Id),
    FOREIGN KEY (flight_id) REFERENCES Flight(flight_id),
    FOREIGN KEY (pilot_id) REFERENCES Pilot(pilot_id)

);


--Insert into section

INSERT INTO Pilot (pilot_id, first_name, last_name, licence_number, role, mobile_number) VALUES
(1, 'James', 'Wilson', 'PIL789456', 'Captain', 15551234567),
(2, 'Sarah', 'Johnson', 'PIL123789', 'Co Pilot', 15552345678),
(3, 'Robert', 'Chen', 'PIL456123', 'Captain', 15553456789),
(4, 'Emily', 'Davis', 'PIL987654', 'Co Pilot', 15554567890),
(5, 'Michael', 'Brown', 'PIL654321', 'Captain', 15555678901),
(6, 'Jessica', 'Lee', 'PIL321987', 'Co Pilot', 15556789012),
(7, 'David', 'Kim', 'PIL147258', 'Captain', 15557890123),
(8, 'Olivia', 'Martin', 'PIL258369', 'Co Pilot', 15558901234),
(9, 'Daniel', 'Garcia', 'PIL369147', 'Captain', 15559012345),
(10, 'Sophia', 'Rodriguez', 'PIL741852', 'Co Pilot', 15550123456),
(11, 'Matthew', 'Martinez', 'PIL852963', 'Captain', 15551234560),
(12, 'Emma', 'Thompson', 'PIL963741', 'Co Pilot', 15552345670),
(13, 'Christopher', 'Lewis', 'PIL159357', 'Captain', 15553456780),
(14, 'Ava', 'Walker', 'PIL357951', 'Co Pilot', 15554567890),
(15, 'Andrew', 'Hall', 'PIL951753', 'Captain', 15555678900);

INSERT INTO Location (location_id, airport_code, city, country) VALUES
(1, 'JFK', 'New York', 'United States'),
(2, 'LAX', 'Los Angeles', 'United States'),
(3, 'ORD', 'Chicago', 'United States'),
(4, 'LHR', 'London', 'United Kingdom'),
(5, 'CDG', 'Paris', 'France'),
(6, 'FRA', 'Frankfurt', 'Germany'),
(7, 'DXB', 'Dubai', 'UAE'),
(8, 'HND', 'Tokyo', 'Japan'),
(9, 'SYD', 'Sydney', 'Australia'),
(10, 'PEK', 'Beijing', 'China'),
(11, 'DEL', 'Delhi', 'India'),
(12, 'SIN', 'Singapore', 'Singapore'),
(13, 'ICN', 'Seoul', 'South Korea'),
(14, 'YYZ', 'Toronto', 'Canada'),
(15, 'GRU', 'São Paulo', 'Brazil');

INSERT INTO Aircraft (aircraft_id, model, licence_plate, functional_status) VALUES
(1, 'Boeing 737-800', 'N123AA', 'Operational'),
(2, 'Airbus A320-200', 'N456BB', 'Operational'),
(3, 'Boeing 787-9', 'N789CC', 'Operational'),
(4, 'Airbus A350-900', 'N012DD', 'Maintenance'),
(5, 'Boeing 777-300ER', 'N345EE', 'Operational'),
(6, 'Airbus A380-800', 'N678FF', 'Operational'),
(7, 'Boeing 737 MAX 8', 'N901GG', 'Operational'),
(8, 'Airbus A321neo', 'N234HH', 'Operational'),
(9, 'Boeing 747-8', 'N567II', 'Maintenance'),
(10, 'Embraer E190', 'N890JJ', 'Operational'),
(11, 'Bombardier CRJ900', 'N123KK', 'Operational'),
(12, 'Airbus A330-300', 'N456LL', 'Operational'),
(13, 'Boeing 767-400ER', 'N789MM', 'Operational'),
(14, 'Airbus A220-300', 'N012NN', 'Operational'),
(15, 'Boeing 757-200', 'N345OO', 'Maintenance');

INSERT INTO Flight (flight_Id, flight_number, departure_time, arrival_time, status, departure_location_id,arrival_location_id, aircraft_id) VALUES
(101, 1001, '2023-12-01 08:00:00', '2023-12-01 11:00:00', 'Scheduled', 1, 2, 1),
(102, 1002, '2023-12-01 09:30:00', '2023-12-01 17:15:00', 'Scheduled', 4, 1, 3),
(103, 1003, '2023-12-01 22:00:00', '2023-12-02 07:30:00', 'Scheduled', 1, 7, 5),
(104, 1004, '2023-12-02 14:00:00', '2023-12-03 06:00:00', 'Delayed', 2, 9, 6),
(105, 1005, '2023-12-03 10:00:00', '2023-12-04 08:30:00', 'On Time', 8, 4, 12),
(106, 1006, '2023-12-02 13:45:00', '2023-12-02 16:30:00', 'Scheduled', 6, 5, 2),
(107, 1007, '2023-12-03 07:15:00', '2023-12-03 10:45:00', 'Scheduled', 3, 1, 7),
(108, 1008, '2023-12-04 11:20:00', '2023-12-04 14:10:00', 'Scheduled', 5, 6, 8),
(109, 1009, '2023-12-05 09:00:00', '2023-12-06 06:45:00', 'Scheduled', 12, 10, 3),
(110, 1010, '2023-12-03 15:30:00', '2023-12-04 12:15:00', 'On Time', 10, 13, 5),
(111, 1011, '2023-12-04 18:00:00', '2023-12-05 04:30:00', 'Scheduled', 11, 7, 12),
(112, 1012, '2023-12-05 12:45:00', '2023-12-06 09:15:00', 'Scheduled', 13, 8, 13),
(113, 1013, '2023-12-06 10:30:00', '2023-12-06 13:15:00', 'Scheduled', 14, 3, 11),
(114, 1014, '2023-12-07 16:20:00', '2023-12-08 02:45:00', 'Scheduled', 15, 2, 3),
(115, 1015, '2023-12-08 06:00:00', '2023-12-08 09:30:00', 'Scheduled', 1, 3, 1);

INSERT INTO PilotAssignment (flight_id, pilot_id, role) VALUES
(101, 1, 'Captain'),
(101, 2, 'Co Pilot'),
(102, 3, 'Captain'),
(102, 4, 'Co Pilot'),
(103, 5, 'Captain'),
(103, 6, 'Co Pilot'),
(104, 7, 'Captain'),
(104, 8, 'Co Pilot'),
(105, 9, 'Captain'),
(105, 10, 'Co Pilot'),
(106, 11, 'Captain'),
(106, 12, 'Co Pilot'),
(107, 13, 'Captain'),
(107, 14, 'Co Pilot'),
(108, 15, 'Captain');
