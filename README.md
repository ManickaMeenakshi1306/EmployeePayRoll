EmployeePay – Payroll Management Prototype
What is this?

EmployeePay is a simple payroll management system built in Python. It demonstrates how HR and Finance teams handle salary processing, from creating payroll requests to approving them and generating salary slips.

This project is intended as a learning prototype and not a production-ready system.

Features
Add and manage employee records
Calculate salary components such as basic pay, HRA, allowances, deductions, and bonus
Create payroll requests from the HR side
Approve or reject payroll requests from the Finance side
Generate salary slips as text files
Support basic user roles: HR, Finance, and Employee
Includes unit tests for core payroll logic
Project Structure

main.py

db.py                    n# In-memory database
model.py                 # Data models

 service/
   hr_service.py        # HR operations
   finance_service.py   # Finance approvals
   user_service.py      # User management



test_hr_service.py        # Unit tests
slip_*.txt               # Generated salary slips
How it Works

The application follows a layered design:

model.py defines the core data structures such as employees, users, and payroll requests
db.py acts as a simple in-memory storage shared across the application
service/ contains the business logic for HR, Finance, and user management
main.py provides a command-line interface to interact with the system
Salary Calculation Logic

The payroll is calculated using a simplified structure:

Basic salary is 50% of CTC
HRA is 40% of the basic salary
Special allowance is the remaining portion
Deductions include PF, ESI, simplified TDS, and loss of pay
Bonus is calculated at 1.5 times the hourly rate for extra work
Salary is adjusted for mid-month joining and leave days

The system also prevents duplicate payroll requests.

Running the Project
Open a terminal in the project folder
Run the application:
python main.py

Follow the on-screen options for HR and Finance operations
Running Tests
python -m unittest test_hr_service.py


Example Workflow
HR adds employees
HR creates payroll requests
Finance reviews and approves or rejects requests
Salary slips are generated after approval
Limitations
Uses in-memory storage, so data is not saved between runs
Passwords are stored in plain text
No secure authentication mechanism
Payroll calculations are simplified
Future Improvements
Add persistent storage using a database
Improve authentication and password handling
Build a web interface or API
Implement more realistic payroll and tax rules
Add an employee-facing portal
Final Note

EmployeePay is a basic prototype that demonstrates the flow of payroll management in a clear and structured way. It can be extended further into a more complete system depending on requirements.
