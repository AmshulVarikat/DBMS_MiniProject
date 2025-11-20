import customtkinter as ctk
from DB_connecrtors import run_query

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class CustomerView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Customer Portal - Vehicle Workshop")
        self.geometry("700x500")

        self.label = ctk.CTkLabel(self, text="Enter Customer ID:")
        self.label.pack(pady=10)

        self.customer_id_entry = ctk.CTkEntry(self, width=200)
        self.customer_id_entry.pack(pady=5)

        self.submit_btn = ctk.CTkButton(self, text="View My Vehicles", command=self.show_vehicles)
        self.submit_btn.pack(pady=10)

        self.output_box = ctk.CTkTextbox(self, width=600, height=300)
        self.output_box.pack(pady=10)

    def show_vehicles(self):
        customer_id = self.customer_id_entry.get().strip()
        if not customer_id:
            self.output_box.insert("end", "⚠️ Please enter a valid Customer ID\n")
            return
        
        query = "SELECT Reg_No, Make, Model, Year, Body_type FROM vehicle WHERE CustomerID = %s"
        vehicles = run_query(query, (customer_id,), fetch=True)

        self.output_box.delete("1.0", "end")
        if vehicles:
            for v in vehicles:
                self.output_box.insert("end", f"🚗 {v['Reg_No']} | {v['Make']} {v['Model']} ({v['Year']}) - {v['Body_type']}\n")
        else:
            self.output_box.insert("end", "No vehicles found for this customer.\n")


if __name__ == "__main__":
    app = CustomerView()
    app.mainloop()
