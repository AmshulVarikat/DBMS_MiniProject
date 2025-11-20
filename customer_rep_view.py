import customtkinter as ctk
from DB_connecrtors import run_query
from datetime import datetime

class CustomerRepView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        self.title = ctk.CTkLabel(self, text="Customer Representative Dashboard", font=("", 18))
        self.title.pack(pady=10)

        # First row of buttons
        btns1 = ctk.CTkFrame(self)
        btns1.pack(pady=5)
        
        ctk.CTkButton(btns1, text="Register New Customer", command=self.add_customer).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btns1, text="Register Vehicle", command=self.add_vehicle).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btns1, text="View Technicians", command=self.show_techs).grid(row=0, column=2, padx=5)
        ctk.CTkButton(btns1, text="View Customers", command=self.show_customers).grid(row=0, column=3, padx=5)

        # Second row of buttons
        btns2 = ctk.CTkFrame(self)
        btns2.pack(pady=5)
        
        ctk.CTkButton(btns2, text="Create Service Job", command=self.create_service_job).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btns2, text="Assign Technician", command=self.assign_technician).grid(row=0, column=1, padx=5)

        self.output = ctk.CTkTextbox(self, width=800, height=350)
        self.output.pack(pady=20)

    def show_techs(self):
        query = "SELECT technician_ID, Fname, Name, Trained_For, Specialization, YOE FROM service_technician"
        data = run_query(query, fetch=True)
        self.output.delete("1.0", "end")
        
        if not data:
            self.output.insert("end", "No technicians found.\n")
            return
            
        self.output.insert("end", "=== SERVICE TECHNICIANS ===\n\n")
        for d in data:
            self.output.insert("end", f"ID: {d['technician_ID']} | {d['Fname']} {d['Name']}\n")
            self.output.insert("end", f"  Trained For: {d['Trained_For']} | Specialization: {d['Specialization']} | Experience: {d['YOE']} years\n\n")

    def show_customers(self):
        query = "SELECT Customer_ID, Name, email_ID, Phone_no FROM customers"
        data = run_query(query, fetch=True)
        self.output.delete("1.0", "end")
        
        if not data:
            self.output.insert("end", "No customers found.\n")
            return
            
        self.output.insert("end", "=== REGISTERED CUSTOMERS ===\n\n")
        for c in data:
            self.output.insert("end", f"ID: {c['Customer_ID']} | {c['Name']} | {c['email_ID']} | {c['Phone_no']}\n")

    def add_customer(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Register New Customer")
        popup.geometry("400x450")

        labels = ["Customer ID", "Name", "Email", "Phone", "License No", "Age", "EmpID"]
        entries = {}

        for label in labels:
            ctk.CTkLabel(popup, text=label).pack(pady=3)
            entries[label] = ctk.CTkEntry(popup, width=300)
            entries[label].pack(pady=3)

        def submit_customer():
            try:
                data = (
                    entries["Customer ID"].get().strip(),
                    entries["Name"].get().strip(),
                    entries["Email"].get().strip(),
                    entries["Phone"].get().strip(),
                    entries["License No"].get().strip(),
                    int(entries["Age"].get()),
                    entries["EmpID"].get().strip(),
                )

                if not all([data[0], data[1], data[2], data[3], data[4], data[6]]):
                    self.output.delete("1.0", "end")
                    self.output.insert("end", "Error: All fields are required!\n")
                    return

                query = """
                INSERT INTO customers (Customer_ID, Name, email_ID, Phone_no, license_No, Age, First_Joined, empID)
                VALUES (%s, %s, %s, %s, %s, %s, CURDATE(), %s)
                """

                result = run_query(query, data)

                if result is True:
                    popup.destroy()
                    self.output.delete("1.0", "end")
                    self.output.insert("end", f"✓ Successfully added customer: {data[1]} (ID: {data[0]})\n")
                elif isinstance(result, str):
                    self.output.delete("1.0", "end")
                    self.output.insert("end", f"MySQL Error:\n{result}\n")
                else:
                    self.output.delete("1.0", "end")
                    self.output.insert("end", "Error: Failed to add customer.\n")

            except ValueError:
                self.output.delete("1.0", "end")
                self.output.insert("end", "Error: Age must be a valid number!\n")
            except Exception as e:
                self.output.delete("1.0", "end")
                self.output.insert("end", f"Error: {str(e)}\n")

        ctk.CTkButton(popup, text="Submit", command=submit_customer).pack(pady=15)
            
    def add_vehicle(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Register New Vehicle")
        popup.geometry("400x550")

        labels = ["Reg_No", "Make", "Model", "Year", "Chassis_No", "Body_type", "CustomerID", "EmpID"]
        entries = {}

        for label in labels:
            ctk.CTkLabel(popup, text=label).pack(pady=3)
            entries[label] = ctk.CTkEntry(popup, width=300)
            entries[label].pack(pady=3)

        def submit_vehicle():
            try:
                data = (
                    entries["Reg_No"].get().strip(),
                    entries["Make"].get().strip(),
                    entries["Model"].get().strip(),
                    int(entries["Year"].get()),
                    entries["Chassis_No"].get().strip(),
                    entries["Body_type"].get().strip(),
                    entries["CustomerID"].get().strip(),
                    entries["EmpID"].get().strip(),
                )

                if not all([data[0], data[1], data[2], data[4], data[5], data[6], data[7]]):
                    self.output.delete("1.0", "end")
                    self.output.insert("end", "Error: All fields are required!\n")
                    return

                query = """
                INSERT INTO vehicle (Reg_No, Make, Model, Year, Chassis_No, Body_type, CustomerID, EmpID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """

                result = run_query(query, data)

                if result is True:
                    popup.destroy()
                    self.output.delete("1.0", "end")
                    self.output.insert("end", f"✓ Vehicle {data[0]} successfully registered for Customer {data[6]}!\n")
                elif isinstance(result, str):
                    self.output.delete("1.0", "end")
                    self.output.insert("end", f"MySQL Error:\n{result}\n")
                else:
                    self.output.delete("1.0", "end")
                    self.output.insert("end", "Error: Failed to register vehicle.\n")

            except ValueError:
                self.output.delete("1.0", "end")
                self.output.insert("end", "Error: Year must be a valid number!\n")
            except Exception as e:
                self.output.delete("1.0", "end")
                self.output.insert("end", f"Error: {str(e)}\n")

        ctk.CTkButton(popup, text="Submit", command=submit_vehicle).pack(pady=15)

    def create_service_job(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Create Service Job")
        popup.geometry("450x600")

        labels = ["Service ID", "Vehicle Reg_No", "Service Type", "Description", 
                  "Start Date (YYYY-MM-DD)", "Predicted End Date (YYYY-MM-DD)", 
                  "Predicted Cost", "EmpID"]
        entries = {}

        for label in labels:
            ctk.CTkLabel(popup, text=label).pack(pady=3)
            entries[label] = ctk.CTkEntry(popup, width=350)
            entries[label].pack(pady=3)

        def submit_job():
            try:
                data = (
                    int(entries["Service ID"].get().strip()),
                    entries["Start Date (YYYY-MM-DD)"].get().strip(),
                    entries["Vehicle Reg_No"].get().strip(),
                    entries["Service Type"].get().strip(),
                    entries["Description"].get().strip(),
                    entries["Predicted End Date (YYYY-MM-DD)"].get().strip(),
                    int(entries["Predicted Cost"].get()),
                    entries["EmpID"].get().strip(),
                )

                if not all([data[1], data[2], data[4], data[5], data[7]]):
                    self.output.delete("1.0", "end")
                    self.output.insert("end", "Error: All fields are required!\n")
                    return

                query = """
                INSERT INTO Service_Job (Service_ID, Start_Date, Reg_No, Service_type, 
                                    Description, Predicted_End_date, Predicted_Cost, EmpID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """

                result = run_query(query, data)

                if result is True:
                    popup.destroy()
                    self.output.delete("1.0", "end")
                    self.output.insert("end", f"✓ Service job {data[0]} created successfully for vehicle {data[2]}!\n")
                    self.output.insert("end", f"  Type: {data[3]} | Predicted Cost: ${data[6]}\n")
                elif isinstance(result, str):
                    self.output.delete("1.0", "end")
                    self.output.insert("end", f"MySQL Error:\n{result}\n")
                else:
                    self.output.delete("1.0", "end")
                    self.output.insert("end", "Error: Failed to create service job.\n")

            except ValueError:
                self.output.delete("1.0", "end")
                self.output.insert("end", "Error: Service ID and Predicted Cost must be valid numbers!\n")
            except Exception as e:
                self.output.delete("1.0", "end")
                self.output.insert("end", f"Error: {str(e)}\n")

        ctk.CTkButton(popup, text="Create Job", command=submit_job).pack(pady=15)

    def assign_technician(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Assign Technician to Service Job")
        popup.geometry("450x400")

        ctk.CTkLabel(popup, text="Service ID:").pack(pady=5)
        service_entry = ctk.CTkEntry(popup, width=300)
        service_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="Available Technicians:", font=("", 14, "bold")).pack(pady=10)

        # Show available technicians
        tech_list = ctk.CTkTextbox(popup, width=400, height=150)
        tech_list.pack(pady=5)

        query = "SELECT technician_ID, Fname, Name, Specialization, YOE FROM service_technician"
        techs = run_query(query, fetch=True)
        
        if techs:
            for t in techs:
                tech_list.insert("end", f"ID: {t['technician_ID']} | {t['Fname']} {t['Name']} - {t['Specialization']} ({t['YOE']} yrs)\n")
        else:
            tech_list.insert("end", "No technicians available.\n")

        ctk.CTkLabel(popup, text="Technician ID to Assign:").pack(pady=5)
        tech_entry = ctk.CTkEntry(popup, width=300)
        tech_entry.pack(pady=5)

        def submit_assignment():
            try:
                job_id = service_entry.get().strip()
                tech_id = tech_entry.get().strip()

                if not job_id or not tech_id:
                    self.output.delete("1.0", "end")
                    self.output.insert("end", "Error: Both Service ID and Technician ID are required!\n")
                    return

                query = """
                INSERT INTO Done_By (JobID, TechID)
                VALUES (%s, %s)
                """

                result = run_query(query, (int(job_id), tech_id))

                if result is True:
                    popup.destroy()
                    self.output.delete("1.0", "end")
                    self.output.insert("end", f"✓ Technician {tech_id} assigned to Service Job {job_id} successfully!\n")
                elif isinstance(result, str):
                    self.output.delete("1.0", "end")
                    self.output.insert("end", f"MySQL Error:\n{result}\n")
                else:
                    self.output.delete("1.0", "end")
                    self.output.insert("end", "Error: Failed to assign technician.\n")

            except ValueError:
                self.output.delete("1.0", "end")
                self.output.insert("end", "Error: Service ID must be a valid number!\n")
            except Exception as e:
                self.output.delete("1.0", "end")
                self.output.insert("end", f"Error: {str(e)}\n")

        ctk.CTkButton(popup, text="Assign", command=submit_assignment).pack(pady=15)