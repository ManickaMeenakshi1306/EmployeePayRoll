from db import Database

class FinanceService:
    def __init__(self):
        self.db = Database.get_instance()
    #approve code
    def approve_payroll_request(self, request_id):
        if not self.db.update_payroll_request_status(request_id, 'approved'):
            raise ValueError("Request not found")
        
    #reject payload
    def reject_payroll_request(self, request_id):
        if not self.db.update_payroll_request_status(request_id, 'rejected'):
            raise ValueError("Request not found")

    def get_pending_requests(self):
        return self.db.get_payroll_requests(status='pending')

    def get_approved_requests(self):
        return self.db.get_payroll_requests(status='approved')