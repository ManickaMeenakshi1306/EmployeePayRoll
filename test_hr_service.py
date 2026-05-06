import unittest
from service.hr_service import HRService
from model import Emp
import datetime


class TestHRService(unittest.TestCase):

    def setUp(self):
        self.hr = HRService()
        # reset DB
        self.hr.db.employees = []
        self.hr.db.payroll_requests = []

    # ---------- NORMAL ----------
    def test_normal_salary(self):
        emp = Emp(id=1, name='John', pos='Dev', ctc=60000.0,
                  dept='IT', jdate=datetime.date(2023, 1, 1),
                  ldays=0, miss=False)

        comp = self.hr.calculate_salary_components(emp, 4, 2026, 0)

        self.assertEqual(comp['basic'], 30000.0)
        self.assertEqual(comp['hra'], 12000.0)
        self.assertTrue(comp['net'] > 0)
        self.assertFalse(comp['over_deduction_hold'])

    # ---------- LOP ----------
    def test_lop_deduction(self):
        emp = Emp(id=2, name='Ravi', pos='Dev', ctc=60000.0,
                  dept='IT', jdate=datetime.date(2023, 1, 1),
                  ldays=5, miss=False)

        comp = self.hr.calculate_salary_components(emp, 4, 2026, 0)

        self.assertTrue(comp['lop'] > 0)
        self.assertTrue(comp['net'] < comp['gross'])

    # ---------- BONUS ----------
    def test_bonus_addition(self):
        emp = Emp(id=3, name='Asha', pos='Dev', ctc=60000.0,
                  dept='IT', jdate=datetime.date(2023, 1, 1),
                  ldays=0, miss=False)

        comp = self.hr.calculate_salary_components(emp, 4, 2026, 10)

        # FIXED TEST (correct validation)
        self.assertTrue(comp['bonus'] > 0)

    # ---------- MID JOIN ----------
    def test_mid_month_join(self):
        emp = Emp(id=4, name='Kiran', pos='Dev', ctc=60000.0,
                  dept='IT', jdate=datetime.date(2026, 4, 15),
                  ldays=0, miss=False)

        comp = self.hr.calculate_salary_components(emp, 4, 2026, 0)

        self.assertTrue(comp['lop'] > 0)

    # ---------- MISSING DATA ----------
    def test_missing_data_exception(self):
        emp = Emp(id=5, name='ErrorEmp', pos='Dev', ctc=60000.0,
                  dept='IT', jdate=datetime.date(2023, 1, 1),
                  ldays=0, miss=True)

        with self.assertRaises(ValueError):
            self.hr.calculate_salary_components(emp, 4, 2026, 0)

    # ---------- DUPLICATE ----------
    def test_duplicate_detection(self):
        eid = self.hr.add_employee('Test', 'Dev', 60000, 'IT',
                                   datetime.date(2023, 1, 1), 0, False)

        # First payroll
        self.hr.create_payroll_request(eid, 4, 2026, 0)

        # Second call should flag duplicate
        emp = self.hr.db.get_employee_by_id(eid)
        comp = self.hr.calculate_salary_components(emp, 4, 2026, 0)

        self.assertTrue(comp['duplicate_block'])

    # ---------- INVALID EMPLOYEE ----------
    def test_invalid_employee(self):
        with self.assertRaises(ValueError):
            self.hr.create_payroll_request(999, 4, 2026, 0)

    # ---------- OVER DEDUCTION (INTENTIONAL FAILURE FOR DEMO) ----------
    def test_over_deduction(self):
        emp = Emp(id=6, name='LowSalary', pos='Dev', ctc=1000.0,
                  dept='IT', jdate=datetime.date(2023, 1, 1),
                  ldays=30, miss=False)

        comp = self.hr.calculate_salary_components(emp, 4, 2026, 0)

        # This may fail depending on logic → used for explanation
        self.assertTrue(comp['over_deduction_hold'])


if __name__ == '__main__':
    unittest.main()