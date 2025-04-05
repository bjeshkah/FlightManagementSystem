




db_creation_file ='/workspaces/FlightManagementSystem/create_database.sql'

import sqlite3
from system_functions import *
conn = sqlite3.connect('airline.db')
cursor=conn.cursor()

tables = ["PilotAssignment","Flight","Aircraft","Location","Pilot"]
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table};")
conn.commit()

with open(db_creation_file,'r') as file:
    sql_script=file.read()
cursor.executescript(sql_script)
conn.commit()

def main():
    while True:
        print("\n Welcome to the Flight Management System. What would you like to do?")
        print("1.Add a new Flight")
        print("2.View Flights by criteria")
        print("3.Update Flight Information")
        print("4.Assign Pilot to Flight")
        print("5.View Pilot Schedule")
        print("6.View Destination Information")
        print("7.Update Destination Information")

        user_input=input("Please select one (1-7):")

        if user_input == "1":
            add_new_flight(conn)
        elif user_input == "2":
            view_flights_by_criteria(conn)
        elif user_input == "3":
            update_flight_information(conn)
        elif user_input == "4":
            assign_pilot_flight(conn)
        elif user_input == "5":
            view_pilot_schedule(conn)
        elif user_input == "6":
            view_destination(conn)
        elif user_input == "7":
            update_destination(conn)
        elif user_input == "8":
            print("Leaving Application")
            conn.close()
            break
        else:
            print("Invalid choice. Please try again")

if __name__== "__main__":
    main()











