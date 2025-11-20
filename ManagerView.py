from DB_connecrtors import run_query

def add_new_technician(tech_id, fname, lname, trained_for, specialization, yoe):
    """
    Add a new service technician
    Returns (success: bool, message: str)
    """
    query = """
    INSERT INTO service_technician (technician_ID, Fname, Name, Trained_For, Specialization, YOE)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    try:
        # Validate inputs
        if not all([tech_id, fname, lname, trained_for, specialization, yoe]):
            return False, "All fields are required"
        
        yoe_int = int(yoe)
        if yoe_int < 0:
            return False, "Years of Experience must be non-negative"
        
        result = run_query(query, (tech_id, fname, lname, trained_for, specialization, yoe_int))
        
        if result is True:
            return True, f"Technician {fname} {lname} added successfully!"
        else:
            return False, f"Error: {result}"
            
    except ValueError:
        return False, "Years of Experience must be a valid number"
    except Exception as e:
        return False, f"Error: {str(e)}"

def add_new_customer_rep(emp_id, name, phone, yoe):
    """
    Add a new customer representative
    Returns (success: bool, message: str)
    """
    query = """
    INSERT INTO customer_reps (Employee_ID, Name, Phone_Number, YOE)
    VALUES (%s, %s, %s, %s)
    """
    
    try:
        # Validate inputs
        if not all([emp_id, name, phone, yoe]):
            return False, "All fields are required"
        
        phone_int = int(phone)
        yoe_int = int(yoe)
        
        if yoe_int < 0:
            return False, "Years of Experience must be non-negative"
        
        result = run_query(query, (emp_id, name, phone_int, yoe_int))
        
        if result is True:
            return True, f"Customer Representative {name} added successfully!"
        else:
            return False, f"Error: {result}"
            
    except ValueError:
        return False, "Phone and YOE must be valid numbers"
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_all_technicians():
    """
    Get all service technicians
    Returns list of technician dictionaries
    """
    query = """
    SELECT technician_ID, Fname, Name, Trained_For, Specialization, YOE
    FROM service_technician
    ORDER BY Fname, Name
    """
    
    try:
        results = run_query(query, fetch=True)
        return results if results else []
    except Exception as e:
        print(f"Error fetching technicians: {e}")
        return []

def get_all_customer_reps():
    """
    Get all customer representatives
    Returns list of customer rep dictionaries
    """
    query = """
    SELECT Employee_ID, Name, Phone_Number, YOE
    FROM customer_reps
    ORDER BY Name
    """
    
    try:
        results = run_query(query, fetch=True)
        return results if results else []
    except Exception as e:
        print(f"Error fetching customer reps: {e}")
        return []

def delete_technician(tech_id):
    """
    Delete a technician
    Returns (success: bool, message: str)
    """
    try:
        delete_query = "DELETE FROM service_technician WHERE technician_ID = %s"
        result = run_query(delete_query, (tech_id,))
        
        if result is True:
            return True, "Technician deleted successfully"
        else:
            return False, f"Error: {result}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def delete_customer_rep(emp_id):
    """
    Delete a customer representative
    Returns (success: bool, message: str)
    """
    try:
        delete_query = "DELETE FROM customer_reps WHERE Employee_ID = %s"
        result = run_query(delete_query, (emp_id,))
        
        if result is True:
            return True, "Customer representative deleted successfully"
        else:
            return False, f"Error: {result}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_techs_by_part(part_no):
    """
    Get technicians who worked on jobs using a specific part (Nested Query)
    """
    query = """
    SELECT 
        st.technician_ID, 
        st.Fname, 
        st.Name
    FROM service_technician st
    WHERE st.technician_ID IN (
        SELECT db.TechID
        FROM Done_By db
        WHERE db.JobID IN (
            SELECT p.JobID
            FROM parts p
            WHERE p.Part_No = %s
        )
    )
    """
    
    try:
        results = run_query(query, (part_no,), fetch=True)
        return results if results else []
    except Exception as e:
        print(f"Error fetching techs by part: {e}")
        return []
