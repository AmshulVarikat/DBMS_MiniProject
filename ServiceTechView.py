from DB_connecrtors import run_query

def get_jobs_for_technician(technician_id):
    """
    Get all jobs assigned to a specific technician
    Returns list of job dictionaries
    """
    query = """
    SELECT 
        sj.Service_ID, 
        sj.Reg_No,
        v.Make,
        v.Model,
        sj.Service_type,
        sj.Start_Date,
        sj.Predicted_End_date,
        sj.Predicted_Cost
    FROM Service_Job sj
    JOIN Done_By db ON sj.Service_ID = db.JobID
    JOIN vehicle v ON sj.Reg_No = v.Reg_No
    WHERE db.TechID = %s
    ORDER BY sj.Start_Date DESC
    """
    
    try:
        results = run_query(query, (technician_id,), fetch=True)
        return results if results else []
    except Exception as e:
        print(f"Error fetching jobs for technician: {e}")
        return []

def get_job_details(job_id):
    """
    Get detailed information about a specific job
    Returns dictionary with job details
    """
    query = """
    SELECT 
        sj.Service_ID,
        sj.Reg_No,
        v.Make,
        v.Model,
        v.Year,
        v.Chassis_No,
        v.Body_type,
        sj.Service_type,
        sj.Description,
        sj.Start_Date,
        sj.Predicted_End_date,
        sj.Predicted_Cost,
        c.Customer_ID,
        c.Name as Customer_Name,
        c.Phone_no,
        c.email_ID,
        (
            SELECT COALESCE(SUM(p.Quantity * p.Price), 0)
            FROM parts p
            WHERE p.JobID = sj.Service_ID
        ) AS Total_Parts_Cost
    FROM Service_Job sj
    JOIN vehicle v ON sj.Reg_No = v.Reg_No
    JOIN customers c ON v.CustomerID = c.Customer_ID
    WHERE sj.Service_ID = %s
    """
    
    try:
        results = run_query(query, (job_id,), fetch=True)
        return results[0] if results else None
    except Exception as e:
        print(f"Error fetching job details: {e}")
        return None

def add_complaint_for_job(job_id, complaint_text):
    """
    Add a complaint/issue for a specific job
    Returns True if successful, error string otherwise
    """
    query = """
    INSERT INTO complaints (JobID, Complaints, Fixed)
    VALUES (%s, %s, NULL)
    """
    
    try:
        result = run_query(query, (job_id, complaint_text))
        return result
    except Exception as e:
        print(f"Error adding complaint: {e}")
        return str(e)

def get_complaints_for_job(job_id):
    """
    Get all complaints for a specific job
    Returns list of complaint dictionaries
    """
    query = """
    SELECT Complaints, Fixed
    FROM complaints
    WHERE JobID = %s
    """
    
    try:
        results = run_query(query, (job_id,), fetch=True)
        return results if results else []
    except Exception as e:
        print(f"Error fetching complaints: {e}")
        return []

def add_parts_for_job(job_id, parts_list):
    """
    Add parts required for a job
    parts_list: list of tuples (part_no, quantity, price)
    Returns True if successful, error string otherwise
    """
    if not parts_list:
        return "No parts provided"
    
    query = """
    INSERT INTO parts (JobID, Part_No, Quantity, Price)
    VALUES (%s, %s, %s, %s)
    """
    
    try:
        for part_no, quantity, price in parts_list:
            result = run_query(query, (job_id, part_no, quantity, price))
            if result is not True:
                return result
        
        return True
    except Exception as e:
        print(f"Error adding parts: {e}")
        return str(e)

def get_parts_for_job(job_id):
    """
    Get all parts for a specific job
    Returns list of part dictionaries
    """
    query = """
    SELECT Part_No, Quantity, Price, (Quantity * Price) as Total
    FROM parts
    WHERE JobID = %s
    """
    
    try:
        results = run_query(query, (job_id,), fetch=True)
        return results if results else []
    except Exception as e:
        print(f"Error fetching parts: {e}")
        return []

def get_total_parts_cost(job_id):
    """
    Calculate total cost of all parts for a job
    Returns total cost as integer
    """
    query = """
    SELECT SUM(Quantity * Price) as Total_Cost
    FROM parts
    WHERE JobID = %s
    """
    
    try:
        results = run_query(query, (job_id,), fetch=True)
        if results and results[0]['Total_Cost']:
            return results[0]['Total_Cost']
        return 0
    except Exception as e:
        print(f"Error calculating total parts cost: {e}")
        return 0
