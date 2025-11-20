import customtkinter as ctk
from customer_rep_view import CustomerRepView
from customer_view import CustomerView
from ServiceTechViewGUI import ServiceTechViewGUI
from ManagerViewGUI import ManagerViewGUI
from DB_connecrtors import initialize_connection_pool, test_connection, close_pool
import sys

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("🚗 Vehicle Workshop Management System")
        self.geometry("1200x750")
        self.minsize(1000, 650)
        
        # Center window on screen
        self.center_window()
        
        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initialize database connection
        if not self.initialize_database():
            self.show_connection_error()
            return
        
        self.build_ui()
    
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def initialize_database(self):
        """Initialize database connection pool"""
        print("\n" + "="*60)
        print("🚗 Vehicle Workshop Management System")
        print("="*60)
        return initialize_connection_pool()
    
    def show_connection_error(self):
        """Show error if database connection fails"""
        error_frame = ctk.CTkFrame(self)
        error_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            error_frame,
            text="Database Connection Failed",
            font=("", 24, "bold"),
            text_color="red"
        ).pack(pady=30)
        
        ctk.CTkLabel(
            error_frame,
            text="Could not connect to the MySQL database.\nPlease check your credentials and try again.",
            font=("", 14)
        ).pack(pady=10)
        
        ctk.CTkButton(
            error_frame,
            text="Retry Connection",
            command=self.retry_connection,
            width=200,
            height=40
        ).pack(pady=20)
        
        ctk.CTkButton(
            error_frame,
            text="Exit",
            command=self.quit,
            width=200,
            height=40,
            fg_color="gray"
        ).pack(pady=5)
    
    def retry_connection(self):
        """Retry database connection"""
        # Clear window
        for widget in self.winfo_children():
            widget.destroy()
        
        # Try to reconnect
        if self.initialize_database():
            self.build_ui()
        else:
            self.show_connection_error()
    
    def build_ui(self):
        """Build the main user interface"""
        # Header frame
        header = ctk.CTkFrame(self, height=90, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        # Title with icon
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(expand=True)
        
        ctk.CTkLabel(
            title_frame,
            text="🚗 Vehicle Workshop Management System",
            font=("", 28, "bold")
        ).pack(pady=5)
        
        ctk.CTkLabel(
            title_frame,
            text="Professional Service Management Solution",
            font=("", 13),
            text_color="gray"
        ).pack()
        
        # Status bar
        status_frame = ctk.CTkFrame(self, height=35, corner_radius=0)
        status_frame.pack(fill="x", side="bottom")
        status_frame.pack_propagate(False)
        
        # Connection status indicator
        status, message = test_connection()
        status_color = "#2ecc71" if status else "#e74c3c"
        status_text = "● Connected" if status else "● Disconnected"
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text=status_text,
            font=("", 11),
            text_color=status_color
        )
        self.status_label.pack(side="left", padx=15)
        
        ctk.CTkLabel(
            status_frame,
            text="Database: vehicle_workshop_management",
            font=("", 11),
            text_color="gray"
        ).pack(side="left", padx=10)
        
        # Add theme toggle
        self.theme_switch = ctk.CTkSwitch(
            status_frame,
            text="Dark Mode",
            command=self.toggle_theme,
            onvalue="dark",
            offvalue="light"
        )
        self.theme_switch.pack(side="right", padx=15)
        self.theme_switch.select()  # Start in dark mode
        
        # Main content frame
        content_frame = ctk.CTkFrame(self, corner_radius=0)
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Create tabview with custom styling
        self.tabs = ctk.CTkTabview(
            content_frame,
            corner_radius=10,
            border_width=2,
            segmented_button_fg_color="#1f538d",
            segmented_button_selected_color="#14375e",
            segmented_button_selected_hover_color="#1a4a7a"
        )
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs with icons
        customer_tab = self.tabs.add("👤 Customer")
        rep_tab = self.tabs.add("👨‍💼 Customer Rep")
        tech_tab = self.tabs.add("🔧 Technician")
        manager_tab = self.tabs.add("👔 Manager")
        
        # Initialize views
        self.customer_view = CustomerView(customer_tab)
        self.rep_view = CustomerRepView(rep_tab)
        self.tech_view = ServiceTechViewGUI(tech_tab)
        self.manager_view = ManagerViewGUI(manager_tab)
        
        print("\n✓ All modules loaded successfully!")
        print("="*60 + "\n")
    
    def toggle_theme(self):
        """Toggle between dark and light mode"""
        if self.theme_switch.get() == "dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
    
    def on_closing(self):
        """Handle application closing"""
        print("\n" + "="*60)
        print("Closing application...")
        print("="*60)
        
        # Close database connections
        close_pool()
        
        # Destroy window and exit
        self.destroy()
        sys.exit(0)

def main():
    """Main entry point"""
    try:
        app = MainApp()
        app.mainloop()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()