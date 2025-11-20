import customtkinter as ctk
from DB_connecrtors import run_query

class CustomerView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.current_customer_id = None
        self.build_ui()

    def build_ui(self):
        # Title
        title = ctk.CTkLabel(self, text="Customer Dashboard", font=("", 18, "bold"))
        title.pack(pady=10)

        # Customer ID Section
        id_frame = ctk.CTkFrame(self)
        id_frame.pack(pady=10)
        
        ctk.CTkLabel(id_frame, text="Customer ID:").grid(row=0, column=0, padx=5)
        self.cust_entry = ctk.CTkEntry(id_frame, width=200)
        self.cust_entry.grid(row=0, column=1, padx=5)
        
        ctk.CTkButton(id_frame, text="Login", command=self.login_customer).grid(row=0, column=2, padx=5)

        # Button Section
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Show My Vehicles", command=self.show_vehicles).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Register My Details", command=self.register_self).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Register My Vehicle", command=self.register_vehicle).grid(row=0, column=2, padx=5)
        ctk.CTkButton(btn_frame, text="View Service Status", command=self.view_service_status).grid(row=0, column=3, padx=5)

        # Output Section
        self.output = ctk.CTkTextbox(self, width=800, height=400)
        self.output.pack(pady=20)

    def login_customer(self):
        """Verify customer exists and store ID"""
        cust_id = self.cust_entry.get().strip()
        
        if not cust_id:
            self.output.delete("1.0", "end")
            self.output.insert("end", "Error: Please enter a Customer ID!\n")
            return

        query = "SELECT Customer_ID, Name, email_ID FROM customers WHERE Customer_ID = %s"
        try:
            result = run_query(query, (cust_id,), fetch=True)
            
            if result and len(result) > 0:
                self.current_customer_id = cust_id
                self.output.delete("1.0", "end")
                self.output.insert("end", f"✓ Welcome, {result[0]['Name']}!\n")
                self.output.insert("end", f"Customer ID: {result[0]['Customer_ID']}\n")
                self.output.insert("end", f"Email: {result[0]['email_ID']}\n\n")
                self.output.insert("end", "You can now use the dashboard features.\n")
            else:
                self.current_customer_id = None
                self.output.delete("1.0", "end")
                self.output.insert("end", "Customer ID not found. Please register first.\n")
        except Exception as e:
            self.output.delete("1.0", "end")
            self.output.insert("end", f"Error: {str(e)}\n")

    def show_vehicles(self):
        """Display all vehicles registered to this customer"""
        cust_id = self.cust_entry.get().strip()
        
        if not cust_id:
            self.output.delete("1.0", "end")
            self.output.insert("end", "Error: Please enter your Customer ID!\n")
            return

        query = "SELECT Reg_No, Make, Model, Year, Body_type, Chassis_No FROM vehicle WHERE CustomerID=%s"
        try:
            results = run_query(query, (cust_id,), fetch=True)
            self.output.delete("1.0", "end")

            if not results:
                self.output.insert("end", "No vehicles registered under this Customer ID.\n")
                return

            self.output.insert("end", f"=== YOUR REGISTERED VEHICLES ===\n\n")
            for v in results:
                self.output.insert("end", f"Registration: {v['Reg_No']}\n")
                self.output.insert("end", f"  Make/Model: {v['Make']} {v['Model']} ({v['Year']})\n")
                self.output.insert("end", f"  Body Type: {v['Body_type']}\n")
                self.output.insert("end", f"  Chassis No: {v['Chassis_No']}\n\n")
        except Exception as e:
            self.output.delete("1.0", "end")
            self.output.insert("end", f"Error: {str(e)}\n")

    def register_self(self):
        """Allow customer to register their own details"""
        popup = ctk.CTkToplevel(self)
        popup.title("Register Your Details")
        popup.geometry("400x500")

        labels = ["Customer ID", "Full Name", "Email", "Phone Number", "License Number", "Age"]
        entries = {}

        for label in labels:
            ctk.CTkLabel(popup, text=label).pack(pady=5)
            entries[label] = ctk.CTkEntry(popup, width=300)
            entries[label].pack(pady=5)

        # Pre-fill Customer ID if available
        if self.cust_entry.get():
            entries["Customer ID"].insert(0, self.cust_entry.get())

        def submit_registration():
            try:
                data = (
                    entries["Customer ID"].get().strip(),
                    entries["Full Name"].get().strip(),
                    entries["Email"].get().strip(),
                    entries["Phone Number"].get().strip(),
                    entries["License Number"].get().strip(),
                    int(entries["Age"].get()),
                )

                if not all([data[0], data[1], data[2], data[3], data[4]]):
                    self.output.delete("1.0", "end")
                    self.output.insert("end", "Error: All fields are required!\n")
                    return

                # Note: empID is set to NULL since customer is self-registering
                query = """
                INSERT INTO customers (Customer_ID, Name, email_ID, Phone_no, license_No, Age, First_Joined, empID)
                VALUES (%s, %s, %s, %s, %s, %s, CURDATE(), NULL)
                """

                result = run_query(query, data)

                if result is True:
                    popup.destroy()
                    self.cust_entry.delete(0, "end")
                    self.cust_entry.insert(0, data[0])
                    self.current_customer_id = data[0]
                    self.output.delete("1.0", "end")
                    self.output.insert("end", f"✓ Successfully registered, {data[1]}!\n")
                    self.output.insert("end", f"Your Customer ID is: {data[0]}\n")
                    self.output.insert("end", "You can now register vehicles and view services.\n")
                elif isinstance(result, str):
                    self.output.delete("1.0", "end")
                    self.output.insert("end", f"Registration Error:\n{result}\n")
                else:
                    self.output.delete("1.0", "end")
                    self.output.insert("end", "Error: Failed to register. Please try again.\n")

            except ValueError:
                self.output.delete("1.0", "end")
                self.output.insert("end", "Error: Age must be a valid number!\n")
            except Exception as e:
                self.output.delete("1.0", "end")
                self.output.insert("end", f"Error: {str(e)}\n")

        ctk.CTkButton(popup, text="Register", command=submit_registration).pack(pady=20)

    def register_vehicle(self):
        """Allow customer to register their own vehicle"""
        cust_id = self.cust_entry.get().strip()
        
        if not cust_id:
            self.output.delete("1.0", "end")
            self.output.insert("end", "Error: Please enter your Customer ID first!\n")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Register Your Vehicle")
        popup.geometry("400x550")

        labels = ["Registration Number", "Make", "Model", "Year", "Chassis Number", "Body Type"]
        entries = {}

        for label in labels:
            ctk.CTkLabel(popup, text=label).pack(pady=5)
            entries[label] = ctk.CTkEntry(popup, width=300)
            entries[label].pack(pady=5)

        def submit_vehicle():
            try:
                data = (
                    entries["Registration Number"].get().strip(),
                    entries["Make"].get().strip(),
                    entries["Model"].get().strip(),
                    int(entries["Year"].get()),
                    entries["Chassis Number"].get().strip(),
                    entries["Body Type"].get().strip(),
                    cust_id,
                    None,  # empID is NULL for self-registration
                )

                if not all([data[0], data[1], data[2], data[4], data[5]]):
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
                    self.output.insert("end", f"✓ Vehicle registered successfully!\n")
                    self.output.insert("end", f"Registration Number: {data[0]}\n")
                    self.output.insert("end", f"Vehicle: {data[1]} {data[2]} ({data[3]})\n")
                elif isinstance(result, str):
                    self.output.delete("1.0", "end")
                    self.output.insert("end", f"Registration Error:\n{result}\n")
                else:
                    self.output.delete("1.0", "end")
                    self.output.insert("end", "Error: Failed to register vehicle.\n")

            except ValueError:
                self.output.delete("1.0", "end")
                self.output.insert("end", "Error: Year must be a valid number!\n")
            except Exception as e:
                self.output.delete("1.0", "end")
                self.output.insert("end", f"Error: {str(e)}\n")

        ctk.CTkButton(popup, text="Register Vehicle", command=submit_vehicle).pack(pady=20)

    def view_service_status(self):
        """View service details for customer's vehicles"""
        cust_id = self.cust_entry.get().strip()
        
        if not cust_id:
            self.output.delete("1.0", "end")
            self.output.insert("end", "Error: Please enter your Customer ID!\n")
            return

        query = """
        SELECT 
            sj.Service_ID,
            sj.Reg_No,
            v.Make,
            v.Model,
            sj.Description,
            sj.Start_date,
            sj.Predicted_End_Date,
            sj.Predicted_cost
        FROM Service_Job sj
        JOIN vehicle v ON sj.Reg_No = v.Reg_No
        WHERE v.CustomerID = %s
        ORDER BY sj.Start_date DESC
        """

        try:
            results = run_query(query, (cust_id,), fetch=True)
            self.output.delete("1.0", "end")

            if not results:
                self.output.insert("end", "No service records found for your vehicles.\n")
                return

            self.output.insert("end", f"=== YOUR SERVICE RECORDS ===\n\n")

            for service in results:
                self.output.insert("end", f"Job ID: {service['Service_ID']}\n")
                self.output.insert("end", f"Vehicle: {service['Make']} {service['Model']} ({service['Reg_No']})\n")
                self.output.insert("end", f"Description: {service['Description']}\n")
                self.output.insert("end", f"Start Date: {service['Start_date']}\n")
                self.output.insert("end", f"Predicted End Date: {service['Predicted_End_Date']}\n")
                self.output.insert("end", f"Predicted Cost: ₹{service['Predicted_cost']}\n")

              
        except Exception as e:
            self.output.delete("1.0", "end")
            self.output.insert("end", f"Error: {str(e)}\n")