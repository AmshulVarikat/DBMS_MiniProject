
"""
populate_db.py — Populate vehicle_workshop_management with sample data.

- Connects to MySQL database.
- Truncates tables (deletes data only).
- Inserts at least 6 valid rows into each table.
- Runs quietly unless an error occurs.
"""

import mysql.connector as mysql
import sys
import getpass

HOST = "localhost"
USER = "root"
DATABASE = "vehicle_workshop_management"

def connect_db():
    """Connect to database with password prompt"""
    try:
        password = getpass.getpass("Enter MySQL password for root: ")
        return mysql.connect(
            host=HOST, 
            user=USER, 
            password=password, 
            database=DATABASE, 
            autocommit=True
        )
    except mysql.Error as e:
        print(f"Connection error: {e}")
        sys.exit(1)

def exec(cursor, query, params=None):
    """Execute query with error handling"""
    try:
        cursor.execute(query, params or ())
    except mysql.Error as e:
        print(f"Error executing: {query[:100]}...")
        print(f"Error: {e}")
        raise

def truncate_tables(cursor):
    """Clear all tables in correct order"""
    print("Clearing existing data...")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    tables = [
        "assigns", "Done_By", "needs", "parts", "complaints",
        "Service_Job", "vehicle", "customers", "customer_reps", "service_technician"
    ]
    for t in tables:
        try:
            exec(cursor, f"TRUNCATE TABLE {t};")
            print(f"  Cleared {t}")
        except mysql.Error as e:
            print(f"  Warning: Could not truncate {t}: {e}")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

def populate(cursor):
    """Insert sample data into all tables"""
    print("\nInserting sample data...")
    
    # 1. service_technician
    print("  Inserting technicians...")
    technicians = [
        ("T001", "Rahul", "Menon", "Engine", "Petrol Engines", 5),
        ("T002", "Amit", "Kumar", "Transmission", "Gearbox", 7),
        ("T003", "Sneha", "Rao", "Electrical", "Diagnostics", 4),
        ("T004", "Vijay", "Patel", "AC", "HVAC Systems", 6),
        ("T005", "Arun", "Nair", "Suspension", "Wheel Alignment", 8),
        ("T006", "Priya", "Shah", "Body", "Painting", 3)
    ]
    for t in technicians:
        exec(cursor, "INSERT INTO service_technician (technician_ID, Fname, Name, Trained_For, Specialization, YOE) VALUES (%s,%s,%s,%s,%s,%s)", t)

    # 2. customer_reps
    print("  Inserting customer representatives...")
    reps = [
        ("E001", "Anjali Gupta", 9876543210, 4),
        ("E002", "Karan Singh", 9123456789, 6),
        ("E003", "Neha Sharma", 9811122233, 3),
        ("E004", "Raj Patel", 9090909090, 5),
        ("E005", "Deepa Iyer", 9000011111, 2),
        ("E006", "Arvind Rao", 9888888888, 7)
    ]
    for r in reps:
        exec(cursor, "INSERT INTO customer_reps (Employee_ID, Name, Phone_Number, YOE) VALUES (%s,%s,%s,%s)", r)

    # 3. customers
    print("  Inserting customers...")
    customers = [
        ("C001", "Aditya Varma", "aditya@example.com", "9999990001", "KL01234567891234", 29, "2021-01-10", "E001"),
        ("C002", "Meera Thomas", None, "8888880002", "MH98765432109876", 34, "2022-03-15", "E002"),
        ("C003", "Rohit Das", "rohit@example.com", None, "DL11112222333344", 45, "2020-07-23", "E003"),
        ("C004", "Lakshmi Pillai", "lakshmi@example.com", "7777770003", "TN55556666777788", 25, "2023-05-02", "E004"),
        ("C005", "Vikram Chauhan", "vikram@example.com", "6666660004", "GJ33334444555566", 39, "2019-11-18", "E005"),
        ("C006", "Divya Reddy", None, "9555550005", "AP22223333444455", 27, "2021-09-27", "E006")
    ]
    for c in customers:
        exec(cursor, "INSERT INTO customers (Customer_ID, Name, email_ID, Phone_no, license_No, Age, First_Joined, empID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", c)

    # 4. vehicle
    print("  Inserting vehicles...")
    vehicles = [
        ("KL01AB1234", "Hyundai", "i20", 2020, "CHS12345678901234", "Hatchback", "C001", "E001"),
        ("MH02CD5678", "Maruti", "Baleno", 2019, "CHS98765432109876", "Hatchback", "C002", "E002"),
        ("DL03EF9101", "Honda", "City", 2021, "CHS55554444333322", "Sedan", "C003", "E003"),
        ("TN04GH1213", "Tata", "Nexon", 2022, "CHS11112222333344", "SUV", "C004", "E004"),
        ("GJ05IJ1415", "Toyota", "Fortuner", 2020, "CHS99998888777766", "SUV", "C005", "E005"),
        ("AP06KL1617", "Ford", "EcoSport", 2018, "CHS66667777888899", "SUV", "C006", "E006")
    ]
    for v in vehicles:
        exec(cursor, "INSERT INTO vehicle (Reg_No, Make, Model, Year, Chassis_No, Body_type, CustomerID, EmpID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", v)

    # 5. Service_Job
    print("  Inserting service jobs...")
    jobs = [
        (1, "2024-01-05", "KL01AB1234", "Oil Change", "Routine oil change service", "2024-01-06", 2000, "E001"),
        (2, "2024-02-10", "MH02CD5678", "Brake Service", "Brake pad replacement", "2024-02-12", 3500, "E002"),
        (3, "2024-03-08", "DL03EF9101", "AC Repair", "AC not cooling properly", "2024-03-10", 4000, "E003"),
        (4, "2024-04-01", "TN04GH1213", "Body Work", "Body painting and dent removal", "2024-04-05", 10000, "E004"),
        (5, "2024-05-15", "GJ05IJ1415", "Transmission", "Transmission check and repair", "2024-05-18", 8000, "E005"),
        (6, "2024-06-20", "AP06KL1617", "General Service", "Regular maintenance service", "2024-06-21", 1500, "E006")
    ]
    for j in jobs:
        exec(cursor, """
            INSERT INTO Service_Job 
            (Service_ID, Start_Date, Reg_No, Service_type, Description, 
             Predicted_End_date, Predicted_Cost, EmpID) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, j)

    # 6. complaints
    print("  Inserting complaints...")
    complaints = [
        (1, "Oil leakage noticed", "Fixed with new gasket"),
        (2, "Brakes squeaking loudly", "Replaced brake pads"),
        (3, "AC not cooling effectively", "Recharged refrigerant"),
        (4, "Paint chipped on door", "Repainted door panel"),
        (5, "Gear slip in 3rd gear", "Adjusted transmission"),
        (6, "Minor rattling noise from engine", "Tightened loose components")
    ]
    for comp in complaints:
        exec(cursor, "INSERT INTO complaints (JobID, Complaints, Fixed) VALUES (%s,%s,%s)", comp)

    # 7. parts - FIXED with shorter part numbers
    print("  Inserting parts...")
    parts = [
        (1, "P001", 1, 500),
        (2, "P002", 2, 700),
        (3, "P003", 1, 1200),
        (4, "P004", 3, 400),
        (5, "P005", 2, 3000),
        (6, "P006", 1, 800)
    ]
    for p in parts:
        exec(cursor, "INSERT INTO parts (JobID, Part_No, Quantity, Price) VALUES (%s,%s,%s,%s)", p)

    # 8. needs
    print("  Inserting vehicle-job relationships...")
    needs = [
        ("KL01AB1234", 1),
        ("MH02CD5678", 2),
        ("DL03EF9101", 3),
        ("TN04GH1213", 4),
        ("GJ05IJ1415", 5),
        ("AP06KL1617", 6)
    ]
    for n in needs:
        exec(cursor, "INSERT INTO needs (RegNum, JobID) VALUES (%s,%s)", n)

    # 9. Done_By
    print("  Inserting technician assignments...")
    doneby = [
        (1, "T001"),
        (2, "T002"),
        (3, "T003"),
        (4, "T004"),
        (5, "T005"),
        (6, "T006")
    ]
    for d in doneby:
        exec(cursor, "INSERT INTO Done_By (JobID, TechID) VALUES (%s,%s)", d)

    # 10. assigns
    print("  Inserting assignment records...")
    assigns = [
        (1, "E001", "T001"),
        (2, "E002", "T002"),
        (3, "E003", "T003"),
        (4, "E004", "T004"),
        (5, "E005", "T005"),
        (6, "E006", "T006")
    ]
    for a in assigns:
        exec(cursor, "INSERT INTO assigns (JobID, EmpID, TechID) VALUES (%s,%s,%s)", a)

def main():
    print("="*60)
    print("Vehicle Workshop Management - Database Population Script")
    print("="*60)
    
    conn = connect_db()
    cur = conn.cursor()
    
    try:
        truncate_tables(cur)
        populate(cur)
        print("\n" + "="*60)
        print("✓ Sample data inserted successfully!")
        print("="*60)
        print("\nData Summary:")
        print("  - 6 Service Technicians")
        print("  - 6 Customer Representatives")
        print("  - 6 Customers")
        print("  - 6 Vehicles")
        print("  - 6 Service Jobs")
        print("  - 6 Complaints")
        print("  - 6 Parts")
        print("\nYou can now run your GUI application.")
        print("="*60)
    except Exception as e:
        print(f"\n✗ Population failed: {e}")
        sys.exit(1)
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)