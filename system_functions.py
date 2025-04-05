import sqlite3
from tabulate import tabulate,Line,DataRow,TableFormat
from datetime import datetime


def add_new_flight (conn):
    conn = sqlite3.connect('airline.db')
    cursor=conn.cursor()

    departure_location_code = input("Enter 3-letter Departure Airport Code : ").upper()
    cursor.execute("SELECT location_id FROM Location where airport_code=?", (departure_location_code,))
    departure_location=cursor.fetchone()

    if departure_location_code is None:
        print("Invalid Aiport code.")
        return
    
    arrival_location_code = input("Enter 3-letter Arrival Airport Code : ").upper()
    cursor.execute("SELECT location_id FROM Location where airport_code=?", (arrival_location_code,))
    arrival_location=cursor.fetchone()

    if arrival_location_code is None:
        print("Invalid Aiport code.")
        return
    
    aircraft_licence_plate = input("Enter the Aircraft Licence plate for your new flight : ").upper()
    cursor.execute("SELECT aircraft_id FROM Aircraft where licence_plate=?", (aircraft_licence_plate,))
    aircraft =cursor.fetchone()

    if aircraft_licence_plate is None:
        print("Invalid Licence Plate.")
        return

    flight_number = input("Enter Flight Number: ")
    departure_time_input = input("Enter Departure Time in YYYYMMDD HH:MM:SS format: ")
    arrival_time_input = input("Enter Arrival Time in YYYYMMDD HH:MM:SS format: ")
    flight_status = "Scheduled"

    try:
        departure_time = datetime.strptime(departure_time_input,"%Y%m%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        arrival_time = datetime.strptime(arrival_time_input,"%Y%m%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    except:
        print("Formatting Error.Please Try Again.")
        exit()

    cursor.execute("""
    INSERT INTO Flight (flight_number,departure_location_id,arrival_location_id,aircraft_id,departure_time,arrival_time,status)
    VALUES (?,?,?,?,?,?,?)
    """,
    (flight_number,departure_location[0],arrival_location[0],aircraft[0],departure_time,arrival_time,flight_status))

    conn.commit()
    print(f"Flight {flight_number} added Successfully")

def view_flights_by_criteria (conn):
    conn = sqlite3.connect('airline.db')
    cursor=conn.cursor()
    print("\nWhat would you like to view?")
    print("1.View Flights by Departure Location")
    print("2.View Flights by Arrival Location")
    print("3.View Flights by Flight Number")
    print("4.View Flights by Status")
    print("5.View Flights by Airplane")
    print("6.Departure Date Range")
    print("7.View All Flights")

    user_input = input("Please select one (1-7):")
    headers = ["Flight ID", "From","To","Flight Number","Departure Time","Arrival Time","Status","Aircraft Licence Plate","Aircraft"]

    query="""
    SELECT 
    f.flight_id,
    l1.airport_code as Departure_Location_Code, 
    l2.airport_code as Arrival_Location_Code,
    f.flight_number,f.departure_time,
    f.arrival_time,
    f.status,
    a.licence_plate,
    a.model 
    FROM Flight f
    JOIN Location l1 on l1.location_id=f.departure_location_id
    JOIN Location l2 on l2.location_id=f.arrival_location_id
    JOIN Aircraft a on a.aircraft_id = f.aircraft_id
    """
    
    criteria = ()

    if user_input == "1":
        departure_code_location = input("Enter 3-digit airport code:").upper()
        query += " WHERE l1.airport_code = ?"
        criteria = (departure_code_location,)
    
    elif user_input == "2":
        arrival_code_location = input("Enter 3-digit airport code:").upper()
        query += " WHERE l2.airport_code = ?"
        criteria = (arrival_code_location,)

    elif user_input == "3":
        flight_number = input("Enter Flight Number:").strip()
        query += " WHERE f.flight_number = ?"
        criteria = (flight_number,)  
    
    elif user_input == "4":
        status = input("Enter Flight Status (Scheduled/Delayed/On Time):").capitalize()
        query += " WHERE f.status = ?"
        criteria = (status,)

    elif user_input == "5":
        licence_plate = input("Enter Aircraft Licence Plate:")
        query += " WHERE a.licence_plate = ?"
        criteria = (licence_plate,)
    
    elif user_input == "6":
        start_date = input("Enter Start Range (YYYY-MM-DD):")
        end_date = input("Enter End Range (YYYY-MM-DD):")
        query += " WHERE f.departure_time BETWEEN ? AND ? "
        criteria = (start_date,end_date)
    
    elif user_input == "7":
        pass
    else:
        print ("Invalid input.Please try again")
        return
    #https://github.com/astanin/python-tabulate/issues/116
    try:
        cursor=conn.cursor()
        cursor.execute (query,criteria)
        output = cursor.fetchall()
        
        if not output:
            print("No results match the criteria.")
        else:
            cust_outline = TableFormat(
                lineabove=Line("|","-","|","|"),
                linebelowheader=Line("|","-","|","|"),
                linebetweenrows= None,
                linebelow= None,
                headerrow=DataRow("|","|","|"),
                datarow=DataRow("|","|","|"),
                padding=0,
                with_header_hide=["lineabove"],

            )
            headers = ["Flight ID", "From","To","Flight Number","Departure Time","Arrival Time","Status","Aircraft Licence Plate","Aircraft"]
        print(tabulate(output,headers=headers,tablefmt="cust_outline"))
        conn.close()
        
    except sqlite3.Error as e: 
        print(f"Error:{e}")
   
def update_flight_information (conn):
    conn = sqlite3.connect('airline.db')
    cursor=conn.cursor()
    flight_id = input("Enter the Flight Id you would like to update:")
    print("\nWhat would you like to update")
    print("1.Update Flight Departure Time")
    print("2.Update Flight Arrival Time")
    print("3.Update Flight Status")
    print("4.Update Aircraft")
    print("5.Update Departure Location")
    print("6.Update Arrival Location")

    user_input = input("Please select one (1-6)")
    flight_update = ()

    if user_input == "1":        
        departure_time = input("Enter the new Departure Time (YYYY-MM-DD HH:MM:SS)")
        cursor.execute("UPDATE Flight SET departure_time = ? WHERE flight_id = ?",(departure_time,flight_id))

    elif user_input == "2":        
        arrival_time = input("Enter the new Arrival Time (YYYY-MM-DD HH:MM:SS)")
        cursor.execute("UPDATE Flight SET arrival_time = ? WHERE flight_id = ?",(arrival_time,flight_id))
    
    elif user_input == "3":        
        flight_status = input("Enter the new Flight Status (Scheduled/Delayed/On Time)")
        cursor.execute("UPDATE Flight SET status = ? WHERE flight_id = ?",(flight_status,flight_id))

    elif user_input == "4":        
        aircraft_plate = input("Enter the Licence Plate of the new Aircraft you would like to use").upper()
        cursor.execute("Select aircraft_id from Aircraft WHERE licence_plate = ?",(aircraft_plate,))
        aircraft_id = cursor.fetchone()

        if aircraft_id is None:
            print ("Licence Plate not found")
        else:
            new_aircraft_id = aircraft_id[0]
            cursor.execute("UPDATE Flight SET aircraft_id = ? Where flight_id = ?",(new_aircraft_id,flight_id))

    elif user_input == "5":        
        departure_location = input("Enter the new 3-Letter Departure Location")
        cursor.execute("Select location_id from Location WHERE airport_code = ?",(departure_location,))
        dlocation_id = cursor.fetchone()

        if dlocation_id is None:
            print ("Departure Location not found")
        else:
            new_dlocation_id = dlocation_id[0]
            cursor.execute("UPDATE Flight SET departure_location_id = ? Where flight_id = ?",(new_dlocation_id,flight_id))
    
    elif user_input == "6":        
        arrival_location = input("Enter the new 3-Letter Arrival Location")
        cursor.execute("Select location_id from Location WHERE airport_code = ?",(arrival_location,))
        alocation_id = cursor.fetchone()

        if alocation_id is None:
            print ("Arrival Location not found")
        else:
            new_alocation_id = alocation_id[0]
            cursor.execute("UPDATE Flight SET arrival_location_id = ? Where flight_id = ?",(new_alocation_id,flight_id))

    conn.commit()
    print("Flight Updated Successfully!")
    
def assign_pilot_flight (conn):
    conn = sqlite3.connect('airline.db')
    cursor=conn.cursor()
    
    flight_id = input("Please enter Flight ID of the flight you would like to assign to a Pilot:")
    pilot_id = input ("Please enter Pilot ID of the pilot you wish to schedule")
    role = input ("Enter the role of the Pilot (Captain/Co-Pilot)") 

    cursor.execute("INSERT INTO PilotAssignment (flight_id,pilot_id,role) VALUES (?,?,?)",(flight_id,pilot_id,role))
    conn.commit()
    print("Pilot assigned successfully!")
    conn.close()

def view_pilot_schedule (conn):
    conn = sqlite3.connect('airline.db')
    cursor=conn.cursor()

    pilot_id = input("Enter Pilot ID")
    cursor.execute("""SELECT p.first_name,p.last_name,f.flight_id,f.flight_number,f.departure_time,f.arrival_time,f.status,l1.airport_code as Departure_Airport,l2.airport_code as Arrival_Airport
                   FROM Pilot p JOIN PilotAssignment pa ON p.pilot_id=pa.pilot_id JOIN Flight f on pa.flight_id=f.flight_id JOIN Location l1 on f.departure_location_id=l1.location_id JOIN Location l2 on f.arrival_location_id=l2.location_id WHERE p.pilot_id = ?""",(pilot_id,))
    
    schedule = cursor.fetchall()

    if schedule is None:
        print("No flights found for this Pilot.")
    else:
        headers = ["Pilot First Name","Pilot Last Name","Flight Id","Flight Number", "Departure Time","Arrival Time","Flight Status","From","To"]
        print(tabulate(schedule,headers=headers,tablefmt="grid"))
    
def view_destination (conn): 
    conn = sqlite3.connect('airline.db')
    cursor=conn.cursor()
    airport_code = input("Please enter Airport Code of the Airport you would like to view:").upper()
    cursor.execute("SELECT * from Location WHERE airport_code =?",(airport_code,))
    destination=cursor.fetchall()

    if not destination:
        print("No Airport Code found.")
    else:
        headers=["Location_Id","Airport_Code","City","Country"]
        print(tabulate(destination,headers=headers,tablefmt="grid"))

def update_destination (conn): 
    conn = sqlite3.connect('airline.db')
    cursor=conn.cursor()
    
    view_destination(cursor)
    
    location_id=input("Please enter Location Id of the Airport you wish to update")
    cursor.execute("""SELECT * from Location WHERE airport_code =?""",(location_id),)
    
    destination=cursor.fetchall()

    if destination is None:
        print("No Airport found.")
        return
    print("\nWhat would you like to update?")
    print("1.Update Airport Code")
    print("2.Update City")
    print("3.Update Country")
    update_info=input("Please select one (1-3)")
   

    if update_info == "1":
        airport_code_new=input("Enter new Airport Code").upper()
        cursor.execute("UPDATE Location Set airport_code =? WHERE location_id =?",(airport_code_new,location_id))
        conn.commit()
        print("Airport Code updated successfully")

    if update_info == "2":
        city_new=input("Enter new City Name")
        cursor.execute("UPDATE Location Set city =? WHERE location_id =?",(city_new,location_id))
        conn.commit()
        print("City Name updated successfully") 

    if update_info == "3":
        country_new=input("Enter new Country Name")
        cursor.execute("UPDATE Location Set country =? WHERE location_id =?",(country_new,location_id))
        conn.commit()
        print("Country Name updated successfully")

def summary_reports (conn):
    conn = sqlite3.connect('airline.db')
    cursor=conn.cursor()
    print("\nWhat would you like to view?")
    print("1.Number of flights to each destination")
    print("2.Number of flights assigned to a pilot")
    print("3.Number of flights per aircraft")
    print("4.Availabe Pilots on a given day")
    print("5.Availabe Planes on a given day")
    
    user_input = input("Please select one (1-7):")
    
    if user_input == "1":
        query="""
        SELECT l.airport_code as DESTINATION, COUNT(f.flight_id) as NumberOfFlights
        FROM Location l JOIN Flight f on f.arrival_location_id = l.location_id
        GROUP BY l.location_id
        ORDER BY NumberOfFlights DESC;
        """
        cursor.execute(query)
        output = cursor.fetchall()
        headers=["Destination","Number of Flights"]
        print(tabulate(output,headers=headers,tablefmt="grid"))

    elif user_input == "2":
        query="""
        SELECT p.licence_number,p.first_name || ' ' || p.last_name as Pilot_Name, COUNT(pa.flight_id) as NumberOfAssignments
        FROM Pilot p JOIN PilotAssignment pa on p.pilot_id=pa.pilot_id
        GROUP BY p.pilot_id
        ORDER BY NumberOfAssignments DESC;
        """
        cursor.execute(query)
        output = cursor.fetchall()
        headers=["Pilot Licence Number","Pilot Name","Number of Flights"]
        print(tabulate(output,headers=headers,tablefmt="grid"))

    elif user_input == "3":
        query="""
        SELECT a.licence_plate,a.model, COUNT(f.flight_id) as NumberOfFlights
        FROM Aircraft a JOIN Flight f on a.aircraft_id=f.aircraft_id
        GROUP BY a.aircraft_id
        ORDER BY NumberOfFlights DESC;
        """
        cursor.execute(query)
        output = cursor.fetchall()
        headers=["Aircraft Licence Plate","Aircraft Model","Number of Flights"]
        print(tabulate(output,headers=headers,tablefmt="grid"))

    elif user_input == "4":
        user_input=input("Please input a date YYYYMMDD:")
        query_date= datetime.strptime(user_input,"%Y%m%d").strftime("%Y-%m-%d")
        cursor.execute("""
        WITH available AS (
        SELECT pa.pilot_id from PilotAssignment pa JOIN Flight f on pa.flight_id=f.flight_id
        WHERE DATE(f.departure_time) = ?
                       )
        SELECT pilot_id,first_name,last_name from Pilot WHERE pilot_id NOT IN (SELECT pilot_id FROM available);
                       """,(query_date,))
        output = cursor.fetchall()
        headers=["Pilot ID","Pilot First Name","Pilot Last Name"]
        print(tabulate(output,headers=headers,tablefmt="grid"))

    elif user_input == "5":
        user_input=input("Please input a date YYYYMMDD:")
        query_date= datetime.strptime(user_input,"%Y%m%d").strftime("%Y-%m-%d")
        cursor.execute("""
        WITH available AS (
        SELECT aircraft_id from Flight
        WHERE DATE(departure_time) = ?
                       )
        SELECT a.licence_plate,a.model from Aircraft a WHERE a.aircraft_id NOT IN (SELECT aircraft_id FROM available);
                       """,(query_date,))
        output = cursor.fetchall()
        headers=["Aircraft Licence Plate","Aircraft Model"]
        print(tabulate(output,headers=headers,tablefmt="grid"))

    else:
        print("Invalid option. Please try again.")
        return


