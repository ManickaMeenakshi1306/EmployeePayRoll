from service.hr_service import HRService
from service.finance_service import FinanceService
from service.user_service import UserService
from model import HRUser, FinUser, EmpUser
import datetime


# ---------- SLIP GENERATION ----------
def generate_payroll_slip(request, employee):
    filename = f"slip_{employee.id}_{request.mon}_{request.yr}.txt"

    content = f"""
Payroll Slip
----------------------------
Employee Name: {employee.name}
Employee ID: {employee.id}
Month: {request.mon}
Year: {request.yr}

Salary Details:
Basic: {request.basic}
HRA: {request.hra}
Special Allowance: {request.spl}
Gross Salary: {request.gross}

Deductions:
PF: {request.pf}
ESI: {request.esi}
TDS: {request.tds}
Loss of Pay: {request.lop}

Bonus: {request.bonus}
Net Salary: {request.net}

Status: {request.stat}
----------------------------
"""

    with open(filename, 'w') as f:
        f.write(content)

    print("Payroll slip generated:", filename)


# ---------- REGISTER USER ----------
def register_user(user_service):
    print("\nRegister New User")

    username = input("Username: ")
    password = input("Password: ")
    role_input = input("Role (HR / Financier / Employee): ").lower()

    role_map = {
        'hr': 'HR',
        'financier': 'Fin',
        'fin': 'Fin',
        'employee': 'Emp'
    }

    role = role_map.get(role_input)

    if not role:
        print("Invalid role. Please enter HR, Financier, or Employee.")
        return

    employee_id = None
    if role == 'Emp':
        employee_id = int(input("Enter Employee ID: "))

    user_service.add_user(username, password, role, employee_id)
    print("User registered successfully.")


# ---------- HR MENU ----------
def hr_menu(hr, user_service):
    while True:
        print("\nHR Menu")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Create Payroll Request")
        print("4. View Payroll Requests")
        print("5. Add User")
        print("6. View Users")
        print("7. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Employee Name: ")
            pos = input("Position: ")
            ctc = float(input("CTC: "))
            dept = input("Department: ")

            emp_id = hr.add_employee(name, pos, ctc, dept, None, 0, False)
            print("Employee added with ID:", emp_id)

        elif choice == '2':
            employees = hr.get_employees()
            if not employees:
                print("No employees found.")
            else:
                for e in employees:
                    print(f"ID: {e.id}, Name: {e.name}, Department: {e.dept}, CTC: {e.ctc}")

        elif choice == '3':
            eid = int(input("Employee ID: "))
            mon = int(input("Month (1-12): "))
            yr = int(input("Year (for example 2026): "))
            extra = float(input("Extra hours: "))

            try:
                hr.create_payroll_request(eid, mon, yr, extra)
                print("Payroll request created.")
            except Exception as e:
                print("Error:", e)

        elif choice == '4':
            requests = hr.get_payroll_requests()
            if not requests:
                print("No payroll requests found.")
            else:
                for r in requests:
                    print(f"ID: {r.id}, EmpID: {r.eid}, Month: {r.mon}, Year: {r.yr}, Net: {r.net}, Status: {r.stat}")

        elif choice == '5':
            register_user(user_service)

        elif choice == '6':
            users = user_service.get_users()
            if not users:
                print("No users found.")
            else:
                for u in users:
                    print(f"Username: {u.uname}, Role: {u.role()}")

        elif choice == '7':
            print("Logging out from HR account.")
            break

        else:
            print("Invalid choice. Try again.")


# ---------- FINANCE MENU ----------
def finance_menu(finance, hr):
    while True:
        print("\nFinance Menu")
        print("1. View Pending Requests")
        print("2. Approve Request")
        print("3. Reject Request")
        print("4. View Approved Requests")
        print("5. Generate Salary Slips")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            pending = finance.get_pending_requests()
            if not pending:
                print("No pending requests.")
            else:
                for r in pending:
                    print(f"ID: {r.id}, Employee ID: {r.eid}, Net Salary: {r.net}")

        elif choice == '2':
            rid = int(input("Enter request ID: "))
            try:
                finance.approve_payroll_request(rid)
                print("Request approved.")
            except Exception as e:
                print("Error:", e)

        elif choice == '3':
            rid = int(input("Enter request ID: "))
            try:
                finance.reject_payroll_request(rid)
                print("Request rejected.")
            except Exception as e:
                print("Error:", e)

        elif choice == '4':
            approved = finance.get_approved_requests()
            if not approved:
                print("No approved requests.")
            else:
                for r in approved:
                    print(f"ID: {r.id}, Employee ID: {r.eid}, Net Salary: {r.net}")

        elif choice == '5':
            approved = finance.get_approved_requests()
            employees = hr.get_employees()
            emp_map = {e.id: e for e in employees}

            for r in approved:
                emp = emp_map.get(r.eid)
                if emp:
                    generate_payroll_slip(r, emp)

        elif choice == '6':
            print("Logging out from Finance account.")
            break

        else:
            print("Invalid choice. Try again.")


# ---------- EMPLOYEE MENU ----------
def employee_menu(hr, emp_id):
    while True:
        print("\nEmployee Menu")
        print("1. View My Approved Slips")
        print("2. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            requests = hr.get_payroll_requests()
            found = False

            for r in requests:
                if r.eid == emp_id and r.stat == 'approved':
                    emp = hr.db.get_employee_by_id(emp_id)
                    generate_payroll_slip(r, emp)
                    found = True

            if not found:
                print("No approved payroll slips available.")

        elif choice == '2':
            print("Logging out from Employee account.")
            break


# ---------- MAIN ----------
def main():
    hr = HRService()
    finance = FinanceService()
    user_service = UserService()

    if not user_service.get_users():
        user_service.add_user('hr', 'hr123', 'HR')
        user_service.add_user('finance', 'fin123', 'Fin')

        emp1 = hr.add_employee('John', 'Developer', 60000, 'IT', datetime.date(2023, 1, 1))
        emp2 = hr.add_employee('Jane', 'Manager', 80000, 'HR', datetime.date(2023, 4, 1))

        user_service.add_user('emp1', 'emp123', 'Emp', emp1)
        user_service.add_user('emp2', 'emp123', 'Emp', emp2)

    while True:
        print("\nEmployee Payroll System")
        print("1. Login")
        print("2. Register New User")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            uname = input("Username: ")
            pwd = input("Password: ")

            user = user_service.authenticate(uname, pwd)

            if not user:
                print("Invalid username or password.")
                continue

            print("Logged in as:", user.role())

            if isinstance(user, HRUser):
                hr_menu(hr, user_service)

            elif isinstance(user, FinUser):
                finance_menu(finance, hr)

            elif isinstance(user, EmpUser):
                employee_menu(hr, user.eid)

        elif choice == '2':
            register_user(user_service)

        elif choice == '3':
            print("Exiting system.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()