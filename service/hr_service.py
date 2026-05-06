from db import Database
from model import Emp, PayReq, HRUser, FinUser, EmpUser
import datetime

class HRService:
    def __init__(self):
        self.db = Database.get_instance()
        self.db.connect()
        self.db.create_tables()

    def add_employee(self, name, pos, ctc, dept, jdate=None, ldays=0, miss=False):
        return self.db.add_employee(name, pos, ctc, dept, jdate, ldays, miss)

    def get_employees(self):
        return self.db.get_employees()

    def calculate_salary_components(self, employee, month_str, year, extra_time_hours=0):
        month = datetime.datetime.strptime(month_str, '%B').month  # Convert month name to int
        if employee.miss:
            raise ValueError(f'Employee details missing for {employee.name}, flag to HR')

        ctc = employee.ctc
        basic = 0.5 * ctc  # 50% of CTC
        hra = 0.4 * basic  # 40% of basic
        gross = ctc  # assuming gross = CTC
        spl_allowance = gross - basic - hra

        # Deductions
        pf = 0.12 * basic  # 12% of basic
        esi = 0.0075 * gross  # 0.75% of gross

        # TDS - simplified slab, assume 10% for now
        annual_gross = gross * 12
        if annual_gross <= 250000:
            tds = 0
        elif annual_gross <= 500000:
            tds = 0.05 * (annual_gross - 250000)
        else:
            tds = 0.2 * (annual_gross - 500000) + 0.05 * 250000
        tds_monthly = tds / 12

        # Alternate flows
        lop = 0
        bonus = 0
        if employee.ldays > 0:
            daily_rate = basic / 30  # assuming 30 days month
            lop = employee.ldays * daily_rate

        # Mid join deduction - assume jdate is datetime.date
        if employee.jdate:
            join_month = employee.jdate.month
            join_year = employee.jdate.year
            if join_month == month and join_year == year:
                days_in_month = (datetime.date(year, month+1, 1) - datetime.date(year, month, 1)).days if month < 12 else 31
                worked_days = days_in_month - employee.jdate.day + 1
                deduction = (days_in_month - worked_days) / days_in_month * basic
                lop += deduction  # add to lop

        # Bonus for extra time - assume 1.5x for extra hours
        if extra_time_hours > 0:
            hourly_rate = basic / (30 * 8)  # assuming 8 hours/day
            bonus = extra_time_hours * hourly_rate * 1.5

        # Net
        deductions = pf + esi + tds_monthly + lop
        net = gross - deductions + bonus

        # Exception: over deduction hold
        over_deduction_hold = deductions > gross

        # Duplicate block - check if already exists
        duplicate_block = self._check_duplicate_payroll(employee.id, month_str, year)

        return {
            'basic': basic,
            'hra': hra,
            'spl_allowance': spl_allowance,
            'gross': gross,
            'pf': pf,
            'esi': esi,
            'tds': tds_monthly,
            'lop': lop,
            'bonus': bonus,
            'net': net,
            'over_deduction_hold': over_deduction_hold,
            'duplicate_block': duplicate_block
        }

    def _check_duplicate_payroll(self, employee_id, month_str, year):
        requests = self.db.get_payroll_requests()
        for req in requests:
            if req.employee_id == employee_id and req.month == month_str and req.year == year:
                return True
        return False

    def create_payroll_request(self, eid, mon, yr, extra_time_hours=0):
        emp = self.db.get_employee_by_id(eid)
        if emp is None:
            raise ValueError(f'Employee with id {eid} not found')

        components = self.calculate_salary_components(emp, mon, yr, extra_time_hours)

        return self.db.add_payroll_request(
            eid, mon, yr,
            components['basic'], components['hra'], components['spl_allowance'], components['gross'],
            components['pf'], components['esi'], components['tds'], components['lop'], components['bonus'], components['net'],
            components['over_deduction_hold'], components['duplicate_block']
        )

    def get_payroll_requests(self):
        return self.db.get_payroll_requests()