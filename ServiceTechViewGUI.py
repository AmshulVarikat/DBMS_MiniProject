import customtkinter as ctk
from ServiceTechView import (
    get_jobs_for_technician,
    get_job_details,
    add_complaint_for_job,
    add_parts_for_job,
    get_complaints_for_job,
    get_parts_for_job,
    get_total_parts_cost
)
from datetime import date

class ServiceTechViewGUI(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.current_tech_id = None
        self.selected_job_id = None
        self.build_ui()

    def build_ui(self):
        # Title
        title = ctk.CTkLabel(self, text="Service Technician Dashboard", font=("", 18, "bold"))
        title.pack(pady=10)

        # Technician Login Section
        login_frame = ctk.CTkFrame(self)
        login_frame.pack(pady=10)
        
        ctk.CTkLabel(login_frame, text="Technician ID:").grid(row=0, column=0, padx=5)
        self.tech_id_entry = ctk.CTkEntry(login_frame, width=200)
        self.tech_id_entry.grid(row=0, column=1, padx=5)
        
        ctk.CTkButton(login_frame, text="Login", command=self.login_technician).grid(row=0, column=2, padx=5)

        # Button Section
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=5)

        ctk.CTkButton(btn_frame, text="My Jobs", command=self.show_my_jobs).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Job Details", command=self.show_job_details).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Add Complaint", command=self.add_complaint_popup).grid(row=0, column=2, padx=5)
        ctk.CTkButton(btn_frame, text="Add Parts", command=self.add_parts_popup).grid(row=0, column=3, padx=5)

        # Output Section
        self.output = ctk.CTkTextbox(self, width=900, height=400)
        self.output.pack(pady=20)

    def login_technician(self):
        """Verify technician exists and store ID"""
        tech_id = self.tech_id_entry.get().strip()
        
        if not tech_id:
            self.output.delete("1.0", "end")
            self.output.insert("end", "Error: Please enter a Technician ID!\n")
            return

        try:
            # Try to fetch jobs to verify technician exists
            jobs = get_jobs_for_technician(tech_id)
            self.current_tech_id = tech_id
            self.output.delete("1.0", "end")
            self.output.insert("end", f"✓ Logged in as Technician {tech_id}\n")
            self.output.insert("end", f"You have {len(jobs)} assigned job(s).\n\n")
            self.output.insert("end", "Use the buttons above to view jobs and manage work.\n")
        except Exception as e:
            self.output.delete("1.0", "end")
            self.output.insert("end", f"Error: {str(e)}\n")

    def show_my_jobs(self):
        """Display all jobs assigned to the logged-in technician"""
        if not self.current_tech_id:
            self.output.delete("1.0", "end")
            self.output.insert("end", "Error: Please login with your Technician ID first!\n")
            return

        try:
            jobs = get_jobs_for_technician(self.current_tech_id)
            self.output.delete("1.0", "end")

            if not jobs:
                self.output.insert("end", f"No jobs assigned to Technician {self.current_tech_id}.\n")
                return

            self.output.insert("end", f"=== JOBS ASSIGNED TO TECHNICIAN {self.current_tech_id} ===\n\n")
            
            for job in jobs:
                self.output.insert("end", f"Service ID: {job['Service_ID']}\n")
                self.output.insert("end", f"  Vehicle: {job['Make']} {job['Model']} ({job['Reg_No']})\n")
                self.output.insert("end", f"  Service Type: {job['Service_type']}\n")
                self.output.insert("end", f"  Start Date: {job['Start_Date']}\n")
                self.output.insert("end", f"  Predicted End: {job['Predicted_End_date'] if job['Predicted_End_date'] else 'Not Set'}\n")
                self.output.insert("end", f"  Predicted Cost: ${job['Predicted_Cost'] if job['Predicted_Cost'] else 0}\n")
                self.output.insert("end", "\n" + "="*60 + "\n\n")

        except Exception as e:
            self.output.delete("1.0", "end")
            self.output.insert("end", f"Error fetching jobs: {str(e)}\n")

    def show_job_details(self):
        """Show detailed popup to select and view job details"""
        popup = ctk.CTkToplevel(self)
        popup.title("View Job Details")
        popup.geometry("450x200")

        ctk.CTkLabel(popup, text="Enter Service ID:").pack(pady=10)
        job_entry = ctk.CTkEntry(popup, width=300)
        job_entry.pack(pady=5)

        def submit():
            job_id = job_entry.get().strip()
            if not job_id:
                self.output.delete("1.0", "end")
                self.output.insert("end", "Error: Please enter a Service ID!\n")
                return

            try:
                details = get_job_details(job_id)
                
                if not details:
                    self.output.delete("1.0", "end")
                    self.output.insert("end", f"No details found for Service ID {job_id}.\n")
                    popup.destroy()
                    return

                # Get complaints and parts
                complaints = get_complaints_for_job(job_id)
                parts = get_parts_for_job(job_id)

                self.selected_job_id = job_id
                self.output.delete("1.0", "end")
                self.output.insert("end", f"=== JOB DETAILS: {job_id} ===\n\n")
                
                # Vehicle Information
                self.output.insert("end", "VEHICLE INFORMATION:\n")
                self.output.insert("end", f"  Registration: {details['Reg_No']}\n")
                self.output.insert("end", f"  Make/Model: {details['Make']} {details['Model']} ({details['Year']})\n")
                self.output.insert("end", f"  Chassis No: {details['Chassis_No']}\n")
                self.output.insert("end", f"  Body Type: {details['Body_type']}\n\n")
                
                # Customer Information
                self.output.insert("end", "CUSTOMER INFORMATION:\n")
                self.output.insert("end", f"  ID: {details['Customer_ID']}\n")
                self.output.insert("end", f"  Name: {details['Customer_Name']}\n")
                self.output.insert("end", f"  Phone: {details['Phone_no']}\n")
                self.output.insert("end", f"  Email: {details['email_ID']}\n\n")
                
                # Service Information
                self.output.insert("end", "SERVICE INFORMATION:\n")
                self.output.insert("end", f"  Service Type: {details['Service_type']}\n")
                self.output.insert("end", f"  Description: {details['Description'] if details['Description'] else 'N/A'}\n")
                self.output.insert("end", f"  Start Date: {details['Start_Date']}\n")
                self.output.insert("end", f"  Predicted End: {details['Predicted_End_date'] if details['Predicted_End_date'] else 'Not Set'}\n")
                self.output.insert("end", f"  Predicted Cost: ${details['Predicted_Cost'] if details['Predicted_Cost'] else 0}\n\n")
                
                # Complaints
                self.output.insert("end", "COMPLAINTS/ISSUES:\n")
                if complaints:
                    for i, comp in enumerate(complaints, 1):
                        self.output.insert("end", f"  {i}. {comp['Complaints']}\n")
                        if comp['Fixed']:
                            self.output.insert("end", f"     Fixed: {comp['Fixed']}\n")
                else:
                    self.output.insert("end", "  No complaints recorded.\n")
                self.output.insert("end", "\n")
                
                # Parts
                self.output.insert("end", "PARTS USED:\n")
                if parts:
                    total_parts_cost = 0
                    for part in parts:
                        self.output.insert("end", f"  Part No: {part['Part_No']} | Qty: {part['Quantity']} | Price: ${part['Price']} | Total: ${part['Total']}\n")
                        total_parts_cost += part['Total']
                    self.output.insert("end", f"\n  Total Parts Cost: ${total_parts_cost}\n")
                else:
                    self.output.insert("end", "  No parts recorded.\n")

                popup.destroy()

            except Exception as e:
                self.output.delete("1.0", "end")
                self.output.insert("end", f"Error fetching job details: {str(e)}\n")
                popup.destroy()

        ctk.CTkButton(popup, text="View Details", command=submit).pack(pady=15)

    def add_complaint_popup(self):
        """Popup to add complaints/issues for a job"""
        popup = ctk.CTkToplevel(self)
        popup.title("Add Complaint/Issue")
        popup.geometry("500x350")

        ctk.CTkLabel(popup, text="Service ID:").pack(pady=5)
        job_entry = ctk.CTkEntry(popup, width=350)
        job_entry.pack(pady=5)

        if self.selected_job_id:
            job_entry.insert(0, self.selected_job_id)

        ctk.CTkLabel(popup, text="Complaint/Issue Description:").pack(pady=5)
        complaint_text = ctk.CTkTextbox(popup, width=450, height=150)
        complaint_text.pack(pady=5)

        def submit():
            job_id = job_entry.get().strip()
            text = complaint_text.get("1.0", "end").strip()

            if not job_id or not text:
                self.output.delete("1.0", "end")
                self.output.insert("end", "Error: Both Service ID and complaint text are required!\n")
                return

            try:
                result = add_complaint_for_job(job_id, text)
                
                popup.destroy()
                self.output.delete("1.0", "end")
                
                if result is True:
                    self.output.insert("end", f"✓ Complaint added successfully for Service ID {job_id}!\n")
                elif isinstance(result, str):
                    self.output.insert("end", f"Error: {result}\n")
                else:
                    self.output.insert("end", "Error: Failed to add complaint.\n")

            except Exception as e:
                self.output.delete("1.0", "end")
                self.output.insert("end", f"Error: {str(e)}\n")
                popup.destroy()

        ctk.CTkButton(popup, text="Submit Complaint", command=submit).pack(pady=15)

    def add_parts_popup(self):
        """Popup to add parts for a job"""
        popup = ctk.CTkToplevel(self)
        popup.title("Add Parts for Job")
        popup.geometry("550x450")

        ctk.CTkLabel(popup, text="Service ID:").pack(pady=5)
        job_entry = ctk.CTkEntry(popup, width=400)
        job_entry.pack(pady=5)

        if self.selected_job_id:
            job_entry.insert(0, self.selected_job_id)

        ctk.CTkLabel(popup, text="Enter parts (one per line):").pack(pady=5)
        ctk.CTkLabel(popup, text="Format: PartNo:Quantity:Price", font=("", 10), text_color="gray").pack()
        ctk.CTkLabel(popup, text="Example: ABC123:2:150", font=("", 10), text_color="gray").pack()
        
        parts_text = ctk.CTkTextbox(popup, width=450, height=200)
        parts_text.pack(pady=10)

        def submit():
            job_id = job_entry.get().strip()
            raw = parts_text.get("1.0", "end").strip()

            if not job_id:
                self.output.delete("1.0", "end")
                self.output.insert("end", "Error: Service ID is required!\n")
                return

            if not raw:
                self.output.delete("1.0", "end")
                self.output.insert("end", "Error: Please enter at least one part!\n")
                return

            parts_list = []
            try:
                for line in raw.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                    part_no, qty, price = line.split(':')
                    parts_list.append((part_no.strip(), int(qty.strip()), int(float(price.strip()))))

            except Exception as e:
                self.output.delete("1.0", "end")
                self.output.insert("end", f"Error parsing parts input: {str(e)}\n")
                self.output.insert("end", "Please use format: PartNo:Quantity:Price (one per line)\n")
                return

            try:
                result = add_parts_for_job(job_id, parts_list)
                
                popup.destroy()
                self.output.delete("1.0", "end")
                
                if result is True:
                    self.output.insert("end", f"✓ {len(parts_list)} part(s) added successfully for Service ID {job_id}!\n")
                    
                    # Calculate and show total cost
                    total_cost = get_total_parts_cost(job_id)
                    self.output.insert("end", f"Total parts cost for this job: ${total_cost}\n")
                elif isinstance(result, str):
                    self.output.insert("end", f"Error: {result}\n")
                else:
                    self.output.insert("end", "Error: Failed to add parts.\n")

            except Exception as e:
                self.output.delete("1.0", "end")
                self.output.insert("end", f"Error: {str(e)}\n")
                popup.destroy()

        ctk.CTkButton(popup, text="Add Parts", command=submit).pack(pady=15)