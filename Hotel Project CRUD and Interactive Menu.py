# Import db_base as db
import db_base as db
from datetime import datetime
from datetime import timedelta

# Create user class for user table to create CRUD functions for later use
class User(db.DBbase):

    # Initialize class into the HotelReservation DB
    def __init__(self):
        super().__init__("HotelReservation.sqlite")

    # Create SQL Method to Create New Table
    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS User;

                CREATE TABLE User (
                    user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    first_name TEXT,
                    last_name TEXT,
                    username TEXT UNIQUE
                );
            """
            super().execute_script(sql)
        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    # Create method that adds a new user
    def create_user(self, first_name, last_name, username):
        try:
            super().get_cursor.execute("""
                INSERT INTO User (first_name, last_name, username)
                VALUES (?,?,?)
            """, (first_name, last_name, username))
            super().get_connection.commit()
            print("User created successfully.")
        except Exception as e:
            print(e)

    # Create method that retrieves a new user by user_id
    def retrieve_all_user(self):
        try:
            return super().get_cursor.execute("SELECT * FROM User").fetchall()
        except Exception as e:
            print("An error occurred.", e)

    # Create method that retrieves a new user by user_id
    def retrieve_user(self, user_id):
        try:
            super().get_cursor.execute("""
                SELECT * FROM User WHERE user_id=?
            """, (user_id,))
            user_data = super().get_cursor.fetchall()
            if user_data:
                return user_data
            else:
                print("User not found.")
                return None
        except Exception as e:
            print(e)

    # Create a method that allows user to update their information
    def update_user(self, user_id, first_name=None, last_name=None, username=None):
        try:
            update_query = "UPDATE User SET "
            params = []
            if first_name:
                update_query += "first_name=?, "
                params.append(first_name)
            if last_name:
                update_query += "last_name=?, "
                params.append(last_name)
            if username:
                update_query += "username=?, "
                params.append(username)
            update_query = update_query.rstrip(", ") + " WHERE user_id=?"
            params.append(user_id)

            super().get_cursor.execute(update_query, tuple(params))
            super().get_connection.commit()
            print("User updated successfully.")
        except Exception as e:
            print(e)

    def delete_user(self, user_id):
        try:
            super().get_cursor.execute("""
                DELETE FROM User WHERE user_id=?
            """, (user_id,))
            super().get_connection.commit()
            print("User deleted successfully.")
        except Exception as e:
            print(e)

# Create user class for room table to create CRUD functions for later use
class Room(db.DBbase):
    # Initialize class into the HotelReservation DB
    def __init__(self):
        super().__init__("HotelReservation.sqlite")

    # Create SQL Method to Create New Table
    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS Room;

                CREATE TABLE Room (
                    room_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    room_number INTEGER UNIQUE,
                    room_name TEXT,
                    floor INTEGER,
                    beds INTEGER,
                    room_type TEXT
                );
            """
            super().execute_script(sql)
        except Exception as e:
            print("An error occured.", e)
        finally:
            super().close_db()

    # Create SQL Method to add new room to hotel
    def add_room(self, room_number, room_name, floor, beds, room_type):
        try:
            super().get_cursor.execute("""INSERT OR IGNORE into Room 
            (room_number, room_name, floor, beds, room_type) 
            values(?, ?, ?, ?, ?);""",
                                       (room_number, room_name, floor, beds, room_type))
            super().get_connection.commit()
            print(f"Added {room_number} successfully")
        except Exception as e:
            print("An error occurred.", e)

    # Create Method to fetch the room information for a room_id
    def fetch_room_by_id(self, room_id = None):
        # if room_id is null (or None), then get everything, else get by room_id
        try:
            if room_id is not None:
                return super().get_cursor.execute("SELECT * FROM Room WHERE room_id = ?", (room_id,)).fetchone()
            else:
                return super().get_cursor.execute("SELECT * FROM room").fetchall()
        except Exception as e:
            print("An error occurred.", e)

    # Create method that allows user to update room information
    def update_room(self, room_id, room_number=None, room_name=None, floor=None, beds=None, room_type=None):
        try:
            update_query = "UPDATE Room SET "
            params = []
            if room_number:
                update_query += "room_number=?, "
                params.append(room_number)
            if room_name:
                update_query += "room_name=?, "
                params.append(room_name)
            if floor:
                update_query += "floor=?, "
                params.append(floor)
            if beds:
                update_query += "beds=?, "
                params.append(beds)
            if room_type:
                update_query += "room_type=?, "
                params.append(room_type)
            update_query = update_query.rstrip(", ") + " WHERE room_id=?"
            params.append(room_id)

            super().get_cursor.execute(update_query, tuple(params))
            super().get_connection.commit()
            print("Room updated successfully.")
        except Exception as e:
            print(e)

    # Create method that allows user delete room information
    def delete_room(self, room_id):
        try:
            super().get_cursor.execute("""
                DELETE FROM Room WHERE room_id=?
            """, (room_id,))
            super().get_connection.commit()
            print("Room deleted successfully.")
        except Exception as e:
            print(e)

# Create user class for booking table to create CRUD functions for later use
class Booking(Room):

    # Create SQL Method to Create New Table
    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS Booking;

                CREATE TABLE Booking (
                    booking_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    room_id INTEGER NOT NULL,
                    start_date DATE,
                    end_date DATE,
                    FOREIGN KEY (room_id) REFERENCES room (room_id)
                );
            """
            super().execute_script(sql)
        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    # Create Method to fetch the booking dates of a room based off of id
    def fetch_booking_date(self, room_id = None):
        # if room_id is null (or None), then don't return anything, else get by room_id
        try:
            if room_id is not None:
                return super().get_cursor.execute("SELECT start_date, end_date FROM Booking WHERE room_id = ?", (room_id,)).fetchall()
            else:
                pass
        except Exception as e:
            print("An error occurred.", e)

    # Create Method to fetch the end date of a room based off of id
    def find_booked_dates_from_room_id(self, room_id = None):
        # if room_id is null (or None), then don't return anything, else get by room_id
        try:
            date_list = self.fetch_booking_date(room_id)
            new_date_list = []
            for date_set in date_list:
                new_date_set = []
                for date in date_set:
                    new_date_set.append(datetime.strptime(date, '%m/%d/%y'))
                new_date_list.append(new_date_set)
            booked_dates = []
            for date_set in new_date_list:
                date_append = date_set[0]
                while date_append < date_set[1]:
                    booked_dates.append(date_append)
                    date_append = date_append + timedelta(days=1)
            return booked_dates
        except Exception as e:
            print("An error occurred.", e)

    def find_booking_dates(self, start_date, end_date):
        try:
            requested_dates = []
            date_append = datetime.strptime(start_date, '%m/%d/%y')
            while date_append < datetime.strptime(end_date, '%m/%d/%y'):
                    requested_dates.append(date_append)
                    date_append = date_append + timedelta(days=1)
            return requested_dates
        except Exception as e:
            print("An error occurred.", e)

    def check_available(self, room_id, start_date, end_date):
        try:
            booked_dates = self.find_booked_dates_from_room_id(room_id = room_id)
            requested_dates = self.find_booking_dates(start_date, end_date)
            available = True
            for reqdate in requested_dates:
                if reqdate in booked_dates:
                    available = False
            return available
        except Exception as e:
            print("An error occurred.", e)


    # Create Method that adds a new booking
    def add_booking(self, room_id, start_date, end_date):
    # First check to see if room_id exists in table
        if super().fetch_room_by_id(room_id = room_id) is not None:
            if self.check_available(room_id, start_date, end_date):
                try:
                    super().get_cursor.execute("""INSERT OR IGNORE into Booking 
                    (room_id, start_date, end_date) 
                    values(?, ?, ?);""",
                                           (room_id, start_date, end_date))
                    super().get_connection.commit()
                    print(f"Added booking for {room_id} successfully")
                except Exception as e:
                    print("An error occurred.", e)
            else:
                print("The room is not available to book. Try booking another room or at different dates")
        else:
            print("The room you are trying to book does not exist, please book a different room or contact an admin to add the room information")

    # Create method that queries all reservations
    def fetch_all_bookings(self):
        try:
            return super().get_cursor.execute("SELECT * FROM Bookings").fetchall()
        except Exception as e:
            print("An error occurred.", e)

    # Create method that retrieves booking by booking id
    def retrieve_booking(self, booking_id):
        try:
            super().get_cursor.execute("""
                SELECT * FROM Booking WHERE booking_id=?
            """, (booking_id,))
            booking_data = super().get_cursor.fetchall()
            if booking_data:
                return booking_data
            else:
                print("Booking not found.")
                return None
        except Exception as e:
            print(e)

    # Create method that updates booking by booking_id and information
    def update_booking(self, booking_id, room_id=None, start_date=None, end_date=None):
        try:
            if self.check_available(room_id, start_date, end_date):
                update_query = "UPDATE Booking SET "
                params = []
                if room_id:
                    update_query += "room_id=?, "
                    params.append(room_id)
                if start_date:
                    update_query += "start_date=?, "
                    params.append(start_date)
                if end_date:
                    update_query += "end_date=?, "
                    params.append(end_date)
                update_query = update_query.rstrip(", ") + " WHERE booking_id=?"
                params.append(booking_id)

                super().get_cursor.execute(update_query, tuple(params))
                super().get_connection.commit()
                print("Booking updated successfully.")
            else:
                print("The update you are trying to make is not available. Please try a new room or new set of dates")
        except Exception as e:
            print(e)

    def delete_booking(self, booking_id):
        try:
            super().get_cursor.execute("""
                DELETE FROM Booking WHERE booking_id=?
            """, (booking_id,))
            super().get_connection.commit()
            print("Booking deleted successfully.")
        except Exception as e:
            print(e)

class InteractiveMenu:
    def run(self):
        hotel_option = {"create user": "create a new user",
                      "retrieve user": "Get user by id",
                      "update user": "update user by id",
                      "delete user": "delete user by id",
                      "create room": "create new room",
                      "fetch room": "Get room by id",
                      "update room": "update room by id",
                      "delete room": "delete room by id",
                      "create booking": "create new booking",
                      "fetch booking": "Get booking by id",
                      "update booking": "update booking by id",
                      "delete booking": "delete booking by id",
                      "reset": "Reset database",
                      "exit": "Exit Program"
                      }
        print("Welcome to my hotel program, please choose a selection")
        user_selection = ""
        while user_selection != "exit":
            print("*** Option List ***")
            for option in hotel_option.items():
                print(option)

            user_selection = input("Select an option: ").lower()

            user = User()
            room = Room()
            booking = Booking()

            if user_selection == "create user":
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                username = input("Enter username: ")
                user.create_user(first_name,last_name,username)
                print("Done\n")
                input("Press return to continue")

            elif user_selection == "create room":
                room_number= int(input("Enter room number: "))
                room_name = input("Enter room name ")
                floor = int(input("Enter floor: "))
                beds = int(input("Enter beds: "))
                room_type = input("Enter room_type: ")
                room.add_room(room_number, room_name, floor, beds, room_type)
                print("Done\n")
                input("Press return to continue")

            elif user_selection == "create booking":
                room_id = int(input("Enter room_id: "))
                start_date = input("Enter start_date (mm/dd/yy): ")
                end_date = input("Enter end_date (mm/dd/yy): ")
                booking.add_booking(room_id,start_date,end_date)
                print("Done\n")
                input("Press return to continue")

            elif user_selection == "retrieve user":
                user_id = input("Enter user id:")
                results = user.retrieve_user(user_id)
                for item in results:
                    print(item)
                input("Press return to continue")

            elif user_selection == "retrieve room":
                room_id = input("Enter room id:")
                results = room.fetch_room_by_id(room_id)
                for item in results:
                    print(item)
                input("Press return to continue")

            elif user_selection == "retrieve booking":
                booking_id = input("Enter booking id:")
                results = booking.retrieve_booking(booking_id)
                for item in results:
                    print(item)
                input("Press return to continue")

            elif user_selection == "update user":
                user_id = int(input("Enter user id: "))
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                username = input("Enter username: ")
                user.update_user(user_id, first_name,last_name,username)
                print("Done\n")
                input("Press return to continue")

            elif user_selection == "update room":
                room_id = int(input("Enter room id: "))
                room_number= int(input("Enter room number: "))
                room_name = input("Enter room name ")
                floor = int(input("Enter floor: "))
                beds = int(input("Enter beds: "))
                room_type = input("Enter room_type: ")
                room.update_room(room_id, room_number, room_name, floor, beds, room_type)
                print("Done\n")
                input("Press return to continue")

            elif user_selection == "update booking":
                booking_id = int(input("Enter booking id: "))
                room_id = int(input("Enter room_id: "))
                start_date = input("Enter start_date (mm/dd/yy): ")
                end_date = input("Enter end_date (mm/dd/yy): ")
                booking.update_booking(booking_id, room_id,start_date,end_date)
                print("Done\n")
                input("Press return to continue")

            elif user_selection == "delete user":
                id = int(input("Enter user id: "))
                user.delete_user(id)
                print("Done\n")
                input("Press return to continue")

            elif user_selection == "delete room":
                id = int(input("Enter room id: "))
                room.delete_room(id)
                print("Done\n")
                input("Press return to continue")

            elif user_selection == "delete booking":
                id = int(input("Enter booking id: "))
                booking.delete_booking(id)
                print("Done\n")
                input("Press return to continue")

            elif user_selection == "reset":
                confirm = input("This will delete all records, continue? (y/n) ").lower()
                if confirm == "y":
                    user.reset_database()
                    room.reset_database()
                    booking.reset_database()
                    print("Reset complete")
                    input("Press return to continue")
                else:
                    print("Reset aborted")
                    input("Press return to continue")

            else:
                if user_selection != "exit":
                    print("Invalid selection, please try again\n")

project = InteractiveMenu()
project.run()