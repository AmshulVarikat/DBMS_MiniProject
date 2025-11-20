import customtkinter as ctk
from ManagerView import (
    add_new_technician,
    add_new_customer_rep,
    get_all_technicians,
    get_all_customer_reps,
    delete_technician,
    delete_customer_rep,
    get_techs_by_part  # Imported new function
)

class ManagerViewGUI(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        # Title
        title = ctk.CTkLabel(self, text="Manager Dashboard", font=("", 18, "bold"))
        title.pack(pady=10)

        # Button Section
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)

        # Row 1
        ctk.CTkButton(btn_frame, text="Add Technician", command=self.add_technician).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="Add Customer Rep", command=self.add_customer_rep).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="View Technicians", command=self.show_technicians).grid(row=0, column=2, padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="View Customer Reps", command=self.show_customer_reps).grid(row=0, column=3, padx=5, pady=5)
        
        # Row 2
        ctk.CTkButton(btn_frame, text="Delete Technician", command=self.delete_tech_popup).grid(row=1, column=0, padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="Delete Customer Rep", command=self.delete_rep_popup).grid(row=1, column=1, padx=5, pady=5)
        
        # Row 2 - New Button for Nested Query Feature
        ctk.CTkButton(btn_frame, text="Find Techs by Part Used", command=self.find_techs_by_part_popup, fg_color="#E67E22", hover_color="#D35400").grid(row=1, column=2, padx=5, pady=5)

        # Output Section
        self.output = ctk.CTkTextbox(self, width=900, height=450)
        self.output.pack(pady=20)

    def show_technicians(self):
        """Display all service technicians"""
        try:
            data = get_all_technicians()
        except Exception as e:
            self.output.delete("1.0", "end")
            self.output.insert("end", f"Error fetching technicians: {e}\n")
            return

        self.output.delete("1.0", "end")
        
        if not data:
            self.output.insert("end", "No technicians found.\n")
            return

        self.output.insert("end", "=== ALL SERVICE TECHNICIANS ===\n\n")
        
        for d in data:
            # Handle both dict and other formats
            if isinstance(d, dict):
                tid = d.get('technician_ID', '')
                fname = d.get('Fname', '')
                lname = d.get('Name', '')
                trained = d.get('Trained_For', '')
                spec = d.get('Specialization', '')
                yoe = d.get('YOE', '')
                
                self.output.insert("end", f"ID: {tid} | {fname} {lname}\n")
                self.output.insert("end", f"  Trained For: {trained}\n")
                self.output.insert("end", f"  Specialization: {spec}\n")
                self.output.insert("end", f"  Experience: {yoe} years\n\n")
            else:
                self.output.insert("end", f"{d}\n")

    def show_customer_reps(self):
        """Display all customer representatives"""
        try:
            data = get_all_customer_reps()
        except Exception as e:
            self.output.delete("1.0", "end")
            self.output.insert("end", f"Error fetching customer reps: {e}\n")
            return

        self.output.delete("1.0", "end")
        
        if not data:
            self.output.insert("end", "No customer representatives found.\n")
            return

        self.output.insert("end", "=== ALL CUSTOMER REPRESENTATIVES ===\n\n")
        
        for c in data:
            # Handle both dict and other formats
            if isinstance(c, dict):
                emp_id = c.get('Employee_ID', '')
                name = c.get('Name', '')
                phone = c.get('Phone_Number', '')
                yoe = c.get('YOE', '')
                
                self.output.insert("end", f"Employee ID: {emp_id}\n")
                self.output.insert("end", f"  Name: {name}\n")
                self.output.insert("end", f"  Phone: {phone}\n")
                self.output.insert("end", f"  Experience: {yoe} years\n\n")
            else:
                self.output.insert("end", f"{c}\n")

    def add_technician(self):
        """Popup to add a new technician"""
        popup = ctk.CTkToplevel(self)
        popup.title("Add New Technician")
        popup.geometry("450x550")

        labels = ["Technician ID", "First Name", "Last Name", "Trained For", "Specialization", "Years of Experience"]
        entries = {}

        for label in labels:
            ctk.CTkLabel(popup, text=label).pack(pady=5)
            entries[label] = ctk.CTkEntry(popup, width=350)
            entries[label].pack(pady=5)

        def submit():
            try:
                tech_id = entries["Technician ID"].get().strip()
                fname = entries["First Name"].get().strip()
                lname = entries["Last Name"].get().strip()
                trained = entries["Trained For"].get().strip()
                spec = entries["Specialization"].get().strip()
                yoe = entries["Years of Experience"].get().strip()

                success, msg = add_new_technician(tech_id, fname, lname, trained, spec, yoe)
                
                popup.destroy()
                self.output.delete("1.0", "end")
                
                if success:
                    self.output.insert("end", f"✓ {msg}\n")
                else:
                    self.output.insert("end", f"✗ {msg}\n")

            except Exception as e:
                self.output.delete("1.0", "end")
                self.output.insert("end", f"Error: {str(e)}\n")
                popup.destroy()

        ctk.CTkButton(popup, text="Add Technician", command=submit).pack(pady=20)

    def add_customer_rep(self):
        """Popup to add a new customer representative"""
        popup = ctk.CTkToplevel(self)
        popup.title("Add Customer Representative")
        popup.geometry("450x400")

        labels = ["Employee ID", "Name", "Phone Number", "Years of Experience"]
        entries = {}

        for label in labels:
            ctk.CTkLabel(popup, text=label).pack(pady=5)
            entries[label] = ctk.CTkEntry(popup, width=350)
            entries[label].pack(pady=5)

        def submit():
            try:
                emp_id = entries["Employee ID"].get().strip()
                name = entries["Name"].get().strip()
                phone = entries["Phone Number"].get().strip()
                yoe = entries["Years of Experience"].get().strip()

                success, msg = add_new_customer_rep(emp_id, name, phone, yoe)
                
                popup.destroy()
                self.output.delete("1.0", "end")
                
                if success:
                    self.output.insert("end", f"✓ {msg}\n")
                else:
                    self.output.insert("end", f"✗ {msg}\n")

            except Exception as e:
                self.output.delete("1.0", "end")
                self.output.insert("end", f"Error: {str(e)}\n")
                popup.destroy()

        ctk.CTkButton(popup, text="Add Representative", command=submit).pack(pady=20)

    def delete_tech_popup(self):
        """Popup to delete a technician"""
        popup = ctk.CTkToplevel(self)
        popup.title("Delete Technician")
        popup.geometry("450x200")

        ctk.CTkLabel(popup, text="⚠️ Warning: This will permanently delete the technician", 
                     text_color="orange").pack(pady=10)
        
        ctk.CTkLabel(popup, text="Technician ID:").pack(pady=5)
        tech_entry = ctk.CTkEntry(popup, width=350)
        tech_entry.pack(pady=5)

        def submit():
            tech_id = tech_entry.get().strip()
            
            if not tech_id:
                self.output.delete("1.0", "end")
                self.output.insert("end", "Error: Technician ID is required!\n")
                return

            try:
                success, msg = delete_technician(tech_id)
                
                popup.destroy()
                self.output.delete("1.0", "end")
                
                if success:
                    self.output.insert("end", f"✓ {msg}\n")
                else:
                    self.output.insert("end", f"✗ {msg}\n")

            except Exception as e:
                self.output.delete("1.0", "end")
                self.output.insert("end", f"Error: {str(e)}\n")
                popup.destroy()

        ctk.CTkButton(popup, text="Delete", command=submit, fg_color="red", hover_color="darkred").pack(pady=15)

    def delete_rep_popup(self):
        """Popup to delete a customer representative"""
        popup = ctk.CTkToplevel(self)
        popup.title("Delete Customer Representative")
        popup.geometry("450x200")

        ctk.CTkLabel(popup, text="⚠️ Warning: This will permanently delete the representative", 
                     text_color="orange").pack(pady=10)
        
        ctk.CTkLabel(popup, text="Employee ID:").pack(pady=5)
        emp_entry = ctk.CTkEntry(popup, width=350)
        emp_entry.pack(pady=5)

        def submit():
            emp_id = emp_entry.get().strip()
            
            if not emp_id:
                self.output.delete("1.0", "end")
                self.output.insert("end", "Error: Employee ID is required!\n")
                return

            try:
                success, msg = delete_customer_rep(emp_id)
                
                popup.destroy()
                self.output.delete("1.0", "end")
                
                if success:
                    self.output.insert("end", f"✓ {msg}\n")
                else:
                    self.output.insert("end", f"✗ {msg}\n")

            except Exception as e:
                self.output.delete("1.0", "end")
                self.output.insert("end", f"Error: {str(e)}\n")
                popup.destroy()

        ctk.CTkButton(popup, text="Delete", command=submit, fg_color="red", hover_color="darkred").pack(pady=15)

    def find_techs_by_part_popup(self):
        """Popup to find technicians by part number (Nested Query Feature)"""
        popup = ctk.CTkToplevel(self)
        popup.title("Find Technicians by Part")
        popup.geometry("450x200")

        ctk.CTkLabel(popup, text="Enter Part Number:", font=("", 14)).pack(pady=10)
        ctk.CTkLabel(popup, text="(e.g. P001, P002)", text_color="gray").pack()
        
        part_entry = ctk.CTkEntry(popup, width=300)
        part_entry.pack(pady=5)

        def submit():
            part_no = part_entry.get().strip()
            
            if not part_no:
                self.output.delete("1.0", "end")
                self.output.insert("end", "Error: Part Number is required!\n")
                return

            try:
                results = get_techs_by_part(part_no)
                
                popup.destroy()
                self.output.delete("1.0", "end")
                
                if results:
                    self.output.insert("end", f"=== TECHNICIANS WHO USED PART: {part_no} ===\n\n")
                    for r in results:
                        self.output.insert("end", f"ID: {r['technician_ID']} | Name: {r['Fname']} {r['Name']}\n")
                else:
                    self.output.insert("end", f"No technicians found who used part {part_no}.\n")

            except Exception as e:
                self.output.delete("1.0", "end")
                self.output.insert("end", f"Error: {str(e)}\n")
                popup.destroy()

        ctk.CTkButton(popup, text="Search", command=submit).pack(pady=15)
