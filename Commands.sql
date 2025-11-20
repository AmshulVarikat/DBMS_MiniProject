-- Drop tables in correct dependency order
DROP TABLE IF EXISTS assigns;
DROP TABLE IF EXISTS Done_By;
DROP TABLE IF EXISTS needs;
DROP TABLE IF EXISTS parts;
DROP TABLE IF EXISTS complaints;
DROP TABLE IF EXISTS service_job;
DROP TABLE IF EXISTS vehicle;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS customer_reps;
DROP TABLE IF EXISTS service_technician;


-----------------------------------------
-- 1. service_technician
-----------------------------------------
CREATE TABLE service_technician (
    technician_ID  VARCHAR(10) NOT NULL,
    Fname VARCHAR(20) NOT NULL,
    Name VARCHAR(20) NOT NULL,
    Trained_For VARCHAR(20),
    Specialization VARCHAR(30),
    YOE INT NOT NULL,
    CONSTRAINT st_pk_techID PRIMARY KEY (technician_ID)
);


-----------------------------------------
-- 2. customer_reps
-----------------------------------------
CREATE TABLE customer_reps (
    Employee_ID CHAR(10) NOT NULL,
    Name VARCHAR(40) NOT NULL,
    Phone_Number INT,
    YOE INT,
    CONSTRAINT cr_pk_empID PRIMARY KEY (Employee_ID)
);


-----------------------------------------
-- 3. customers
-----------------------------------------
CREATE TABLE customers (
    Customer_ID CHAR(10) NOT NULL,
    Name VARCHAR(40) NOT NULL,
    email_ID VARCHAR(50),
    Phone_no CHAR(10),
    license_No CHAR(16) NOT NULL,
    Age INT NOT NULL,
    First_Joined DATE NOT NULL,
    empID CHAR(10),

    CONSTRAINT C_pk_CustID PRIMARY KEY (Customer_ID),
    CONSTRAINT fk_emp FOREIGN KEY (empID)
        REFERENCES customer_reps(Employee_ID),
    CONSTRAINT chk_ageRange CHECK (Age >= 18 AND Age <= 100),
    CONSTRAINT chk_phoneNo CHECK (CHAR_LENGTH(Phone_no) = 10)
);


-----------------------------------------
-- 4. vehicle
-----------------------------------------
CREATE TABLE vehicle (
    Reg_No VARCHAR(10) NOT NULL,
    Make VARCHAR(15) NOT NULL,
    Model VARCHAR(15) NOT NULL,
    Year INT NOT NULL,
    Chassis_No VARCHAR(17) NOT NULL,
    Body_type VARCHAR(15),
    CustomerID CHAR(10),
    EmpID CHAR(10),

    CONSTRAINT vh_pk_regNo PRIMARY KEY (Reg_No),
    CONSTRAINT fk_vehicle_customer FOREIGN KEY (CustomerID)
        REFERENCES customers(Customer_ID) ON DELETE CASCADE,
    CONSTRAINT fk_vehicle_emp FOREIGN KEY (EmpID)
        REFERENCES customer_reps(Employee_ID),

    CONSTRAINT chk_BodyType CHECK (
        Body_type IN (
           'Sedan','SUV','Hatchback','Coupe','Convertible',
           'Pickup','Van','Minivan','Wagon'
        )
    ),

    CONSTRAINT chk_licenseNo CHECK(
        REGEXP_LIKE(
            Reg_No,
            '^((AN|AP|AR|AS|BR|CG|CH|DD|DL|GA|GJ|HP|HR|JH|JK|KA|KL|LA|LD|MH|ML|MN|MP|MZ|NL|OD|PB|PY|RJ|SK|TN|TR|TS|UK|UP|WB)[0-9]{2}[A-Z]{1,3}[0-9]{4}|[0-9]{2}BH[0-9]{4}[A-Z]{2})$'
        )
    )
);


-----------------------------------------
-- 5. service_job
-----------------------------------------
CREATE TABLE service_job (
    Job_ID INT NOT NULL PRIMARY KEY,
    Reg_no VARCHAR(10) NOT NULL,
    Description VARCHAR(1024),
    Start_date DATE NOT NULL,
    Predicted_End_Date DATE,
    Predicted_cost INT,
    EmpID CHAR(10),

    CONSTRAINT fk_service_emp FOREIGN KEY (EmpID)
        REFERENCES customer_reps(Employee_ID),

    CONSTRAINT fk_service_vehicle FOREIGN KEY (Reg_no)
        REFERENCES vehicle(Reg_No)
);


-----------------------------------------
-- 6. complaints
-----------------------------------------
CREATE TABLE complaints (
    JobID INT NOT NULL,
    Complaints VARCHAR(200) NOT NULL,
    Fixed VARCHAR(200),
    FOREIGN KEY (JobID) REFERENCES service_job(Job_ID)
);


-----------------------------------------
-- 7. parts
-----------------------------------------
CREATE TABLE parts (
    JobID INT NOT NULL,
    Part_No VARCHAR(15) NOT NULL,
    Quantity INT,
    Price INT NOT NULL,
    FOREIGN KEY (JobID) REFERENCES service_job(Job_ID)
);


-----------------------------------------
-- 8. needs
-----------------------------------------
CREATE TABLE needs (
    RegNum VARCHAR(10) NOT NULL,
    JobID INT,
    FOREIGN KEY (JobID) REFERENCES service_job(Job_ID),
    FOREIGN KEY (RegNum) REFERENCES vehicle(Reg_No)
);


-----------------------------------------
-- 9. Done_By
-----------------------------------------
CREATE TABLE Done_By (
    JobID INT,
    TechID VARCHAR(10),
    FOREIGN KEY (JobID) REFERENCES service_job(Job_ID),
    FOREIGN KEY (TechID) REFERENCES service_technician(technician_ID)
);


-----------------------------------------
-- 10. assigns
-----------------------------------------
CREATE TABLE assigns (
    JobID INT,
    EmpID CHAR(10),
    TechID VARCHAR(10),
    FOREIGN KEY (EmpID) REFERENCES customer_reps(Employee_ID),
    FOREIGN KEY (JobID) REFERENCES service_job(Job_ID),
    FOREIGN KEY (TechID) REFERENCES service_technician(technician_ID)
);



-----------------------------------------------------
-- TRIGGERS
-----------------------------------------------------

DELIMITER $$

CREATE TRIGGER before_customer_insert
BEFORE INSERT ON customers
FOR EACH ROW
BEGIN
    IF NEW.email_ID IS NULL AND NEW.Phone_no IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot add customer: an email ID or a phone number is required.';
    END IF;
END$$

DELIMITER ;


DELIMITER $$

CREATE TRIGGER check_dates_before_insert
BEFORE INSERT ON service_job
FOR EACH ROW
BEGIN
    IF NEW.Predicted_End_date IS NOT NULL AND NEW.Predicted_End_date < NEW.Start_Date THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Predicted_End_date cannot be before Start_Date';
    END IF;
END$$

DELIMITER ;


DELIMITER $$

CREATE TRIGGER check_dates_before_update
BEFORE UPDATE ON service_job
FOR EACH ROW
BEGIN
    IF NEW.Predicted_End_date IS NOT NULL AND NEW.Predicted_End_date < NEW.Start_Date THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Predicted_End_date cannot be before Start_Date';
    END IF;
END$$

DELIMITER ;



-----------------------------------------------------
-- PROCEDURE
-----------------------------------------------------

DELIMITER $$

CREATE PROCEDURE UpdateTotalJobCost(IN p_JobID INT)
BEGIN
    DECLARE v_total_parts_cost INT;

    SELECT COALESCE(SUM(Quantity * Price), 0)
    INTO v_total_parts_cost
    FROM parts
    WHERE JobID = p_JobID;

    UPDATE service_job
    SET Predicted_cost = COALESCE(Predicted_cost,0) + v_total_parts_cost
    WHERE Job_ID = p_JobID;
END$$

DELIMITER ;



-----------------------------------------------------
-- FUNCTIONS
-----------------------------------------------------

DELIMITER $$

CREATE FUNCTION GetCustomerIDByRegNo(p_RegNo VARCHAR(10))
RETURNS CHAR(10)
READS SQL DATA
BEGIN
    DECLARE v_CustomerID CHAR(10);
    SELECT CustomerID INTO v_CustomerID
    FROM vehicle
    WHERE Reg_No = p_RegNo;
    RETURN v_CustomerID;
END$$

DELIMITER ;


DELIMITER $$

CREATE FUNCTION GetRepIDByRegNo(p_RegNo VARCHAR(10))
RETURNS CHAR(10)
READS SQL DATA
BEGIN
    DECLARE v_EmpID CHAR(10);
    SELECT EmpID INTO v_EmpID
    FROM vehicle
    WHERE Reg_No = p_RegNo;
    RETURN v_EmpID;
END$$

DELIMITER ;



-----------------------------------------------------
-- INSERT DATA
-----------------------------------------------------

INSERT INTO service_technician VALUES
('T001', 'Raj', 'Kumar', 'Engine', 'Petrol Engines', 5),
('T002', 'Priya', 'Sharma', 'Electrical', 'EV Systems', 3),
('T003', 'Amit', 'Singh', 'General', 'All Models', 8);


INSERT INTO customer_reps VALUES
('E01', 'Anjali Mehta', 987654321, 4);


INSERT INTO customers VALUES
('CUST001', 'Anika Reddy', 'anika.r@email.com', NULL, 'DL01234567890123',
 34, '2022-05-10', 'E01'),
('CUST002', 'Rohan Desai', NULL, '9888777666', 'DL01234567890456',
 45, '2021-11-20', 'E01'),
('CUST003', 'Sanya Gupta', 'sanya.g@email.com', '9555444333',
 'DL01234567890789', 28, '2023-01-15', 'E01'),
('CUST004', 'Randy Orton', NULL, '9887788666',
 'DL01234567892089', 28, '2023-01-15', 'E01');


INSERT INTO vehicle VALUES
('KA01AB1111', 'Honda', 'City', 2020, 'CHASSISNO11111111', 'Sedan', 'CUST001', 'E01'),
('KA01AB2222', 'Toyota', 'Fortuner', 2022, 'CHASSISNO22222222', 'SUV', 'CUST001', 'E01'),
('KA05CD3333', 'Maruti', 'Swift', 2019, 'CHASSISNO33333333', 'Hatchback', 'CUST002', 'E01'),
('KA05CD4444', 'Hyundai', 'Verna', 2021, 'CHASSISNO44444444', 'Sedan', 'CUST002', 'E01'),
('KA03EF5555', 'Kia', 'Seltos', 2023, 'CHASSISNO55555555', 'SUV', 'CUST003', 'E01'),
('KA02ZZ2355', 'Ford', 'Mustang Mach 1', 1969, '9R02M1234567890', 'Coupe', 'CUST004', 'E01');


INSERT INTO service_job VALUES
(101, 'KA01AB1111', 'Engine work', '2025-09-01', NULL, 2000, 'E01'),
(102, 'KA05CD3333', 'Brake service', '2025-09-10', NULL, 1500, 'E01'),
(103, 'KA01AB2222', 'AC repair', '2025-09-15', NULL, 5000, 'E01'),
(104, 'KA03EF5555', 'General service', '2025-10-01', NULL, 800, 'E01'),
(105, 'KA05CD4444', 'Diagnostics', '2025-10-08', NULL, 3000, 'E01'),
(106, 'KA01AB1111', 'Headlight fix', '2025-10-09', NULL, 2500, 'E01'),
(201, 'KA02ZZ2355', 'Special check', '2025-10-10', NULL, 5000, 'E01');


INSERT INTO needs VALUES
('KA01AB1111', 101),
('KA05CD3333', 102),
('KA01AB2222', 103),
('KA03EF5555', 104),
('KA05CD4444', 105),
('KA01AB1111', 106),
('KA02ZZ2355', 201);


INSERT INTO Done_By VALUES
(101, 'T001'),
(102, 'T003'),
(103, 'T002'),
(104, 'T003'),
(105, 'T001'),
(106, 'T002'),
(201, 'T003');


INSERT INTO complaints VALUES
(101, 'Engine knocking sound.', 'Replaced ignition coil.'),
(102, 'Squealing brakes.', 'Replaced brake pads.'),
(103, 'AC not cooling.', 'Gas refilled.'),
(104, 'General service.', 'Oil changed.'),
(105, 'Check engine light.', NULL),
(106, 'Headlight not working.', NULL),
(201, 'Special consignment restock.', NULL);


INSERT INTO parts VALUES
(101, 'IGNCOIL-1A', 1, 1800),
(102, 'BRKPAD-S2B', 2, 600),
(104, 'OILFLTR-K1', 1, 450),
(104, 'ENGN-OIL-5L', 1, 1200),
(105, 'O2SENSOR-H3', 1, 2500),
(201, 'STAEDTLER-HB2', 3, 100),
(201, 'COMBAT-KNIFE-SET', 1, 8000),
(201, 'H&K-P30L-9MM', 1, 55000);

