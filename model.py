class Emp:
    def __init__(self, id=None, name='', pos='', ctc=0.0, dept='', jdate=None, ldays=0, miss=False):
        self.id = id
        self.name = name
        self.pos = pos
        self.ctc = ctc
        self.dept = dept
        self.jdate = jdate
        self.ldays = ldays
        self.miss = miss


class User:
    def __init__(self, id=None, uname='', pwd=''):
        self.id = id
        self.uname = uname.lower()  
        self.pwd = pwd

    def role(self):
        return 'User'


class HRUser(User):
    def role(self):
        return 'HR'


class FinUser(User):
    def role(self):
        return 'Fin'


class EmpUser(User):
    def __init__(self, id=None, uname='', pwd='', eid=None):
        super().__init__(id, uname, pwd)
        self.eid = eid

    def role(self):
        return 'Emp'


class PayReq:
    def __init__(self, id=None, eid=None, mon=0, yr=0,
                 basic=0.0, hra=0.0, spl=0.0, gross=0.0,
                 pf=0.0, esi=0.0, tds=0.0, lop=0.0,
                 bonus=0.0, net=0.0,
                 stat='pending', hold=False, block=False):

        self.id = id
        self.eid = eid
        self.mon = mon
        self.yr = yr
        self.basic = basic
        self.hra = hra
        self.spl = spl
        self.gross = gross
        self.pf = pf
        self.esi = esi
        self.tds = tds
        self.lop = lop
        self.bonus = bonus
        self.net = net
        self.stat = stat
        self.hold = hold
        self.block = block