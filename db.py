from model import Emp, PayReq, HRUser, FinUser, EmpUser

class Database:
    _instance = None

    def __init__(self):
        self.users = []
        self.employees = []
        self.payroll_requests = []
        self.uid = 1
        self.eid = 1
        self.pid = 1
    #singleton design initialization
    @staticmethod
    def get_instance():
        if Database._instance is None:
            Database._instance = Database()
        return Database._instance

    def connect(self):
        pass

    def create_tables(self):
        pass

    # ---------- USERS ----------
    def add_user(self, uname, pwd, role, eid=None):
        uname = uname.lower()

        if role == 'HR':
            user = HRUser(self.uid, uname, pwd)
        elif role == 'Fin':
            user = FinUser(self.uid, uname, pwd)
        else:
            user = EmpUser(self.uid, uname, pwd, eid)

        self.users.append(user)
        self.uid += 1
        return user

    def get_users(self):
        return self.users

    def get_user_by_username(self, uname):
        uname = uname.lower()
        for u in self.users:
            if u.uname == uname:
                return u
        return None

    # ---------- EMPLOYEES ----------
    def add_employee(self, name, pos, ctc, dept, jdate=None, ldays=0, miss=False):
        emp = Emp(self.eid, name, pos, ctc, dept, jdate, ldays, miss)
        self.employees.append(emp)
        self.eid += 1
        return emp.id

    def get_employees(self):
        return self.employees

    def get_employee_by_id(self, eid):
        for e in self.employees:
            if e.id == eid:
                return e
        return None

    # ---------- PAYROLL ----------
    def add_payroll_request(self, eid, mon, yr, basic, hra, spl, gross,
                            pf, esi, tds, lop, bonus, net, hold, block):

        req = PayReq(self.pid, eid, mon, yr, basic, hra, spl, gross,
                     pf, esi, tds, lop, bonus, net,
                     'pending', hold, block)

        self.payroll_requests.append(req)
        self.pid += 1
        return req

    def get_payroll_requests(self, status=None):
        if status:
            return [r for r in self.payroll_requests if r.stat == status]
        return self.payroll_requests

    def update_payroll_request_status(self, rid, status):
        for r in self.payroll_requests:
            if r.id == rid:
                r.stat = status
                return True
        return False