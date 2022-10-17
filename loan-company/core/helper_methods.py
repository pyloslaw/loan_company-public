import datetime
from decimal import Decimal
from dateutil.relativedelta import relativedelta

class ProductMethods:
    '''
    methods to be inherited for Product model
    '''

    @property
    def days_since_create(self):
        today = datetime.date.today()
        try:
            days_passed = today - self.created_date
            days_passed_split = str(days_passed).split(' ')
            return int(days_passed_split[0])
        except:
            return 0

    @property
    def total_amount_dec(self):
        return round(self.installments_dec*Decimal(str(self.loan_period)),2)

    @property
    def installments_dec(self):
        p = (self.global_interest_rate_dec / Decimal('100') * Decimal('2')) / Decimal('12')
        nu = p * ((Decimal('1') + p) ** Decimal(str(self.loan_period)))
        de = ((Decimal('1') + p) ** Decimal(str(self.loan_period))) - Decimal('1')
        total = Decimal(str(self.amount_requested)) * nu/de
        if self.product_name == 'L1':
            result = total + (Decimal('0.15') * total)
            return round(result, 2)
        else:

            return round(total, 2)


    def __str__(self):
        return f'ID: {self.id}, amount: {self.amount_requested}, period: {self.loan_period}'

    @property
    def installement_schedule(self):
        try:
            z = []
            for x in range(1, self.loan_period+1):                
                z.append(f'{x} - amount: -- {self.installments_dec} ---- Required by: -- {self.created_date + relativedelta(months=x)}')
            return '\n'.join(z)
            # return z
        except:
            return 'You must create a loan first ! '
        

    @property
    def installment_dict(self):
        try:
            installments = {}
            for x in range(1, self.loan_period+1):
                installments[x] = {
                    'amount' : self.installments_dec,
                    'required by' : str(self.created_date + relativedelta(months=x))
                }
            return installments
        except:
            return 'NO Loans'

    @property
    def inst_sch(self):
        try:
            schedule = []
            for x in range(self.loan_period):
                schedule.append((x, self.created_date + relativedelta(months=x), self.installments_dec))
            return schedule
        except TypeError:
            return 'No active Loans'


    @property
    def get_payments(self):
        payments = self.payments_query
        payment_list = []
        for payment in payments:
            payment_list.append((payment.created_date, payment.amount))
        # return sorted(payment_list)
        return payment_list

    @property
    def paid_total(self):
        paid_total = 0
        for (a,b) in self.get_payments:
            paid_total = paid_total + b
        return paid_total


    @property
    def paid_by_day(self):
        daily_payements = {}
        for a,b in self.get_payments:
            if a in daily_payements:
                daily_payements[a] += b
            else:
                daily_payements[a] = b
        return daily_payements

    def paid_by_day_human(self):
        x = [f'{a} -- {b}' for (a,b) in self.paid_by_day.items()]
        return '\n'.join(x)

    def payments_human(self):
        x = [f'{a} -- {b}' for (a,b) in self.get_payments]
        return '\n'.join(x)
    
    
    def count_payment(self, payment_no, payment_date, payment):
        '''
        function to count payment against installment,
        every payment should have this function called        
        '''
        # (installment_no, installment, due_date, payment_no, payment, payment_date, installment_remainder, payment_remainder)
        new = []

        if not self.complete:
            installment_no = 0
        elif self.complete[-1][6] == 0 and self.complete[-1][7] == 0:
            # installment_no = len(self.complete)
            installment_no = self.complete[-1][0] + 1
        else:
            installment_no = self.complete[-1][0]
       
        iter = 0        
        remainder = payment * Decimal('-1')

        if self.complete and self.complete[-1][6] > 0:
            installment = self.complete[-1][6]
        else:
            try:
                installment = self.inst_sch[installment_no][2]
            except IndexError:
                installment = self.inst_sch[-1][2]


        try:    
            while installment + remainder < Decimal('0'):
                remainder = installment + remainder
                delay = payment_date - self.inst_sch[installment_no][1]
                new.append((installment_no, self.inst_sch[installment_no][2], 
                self.inst_sch[installment_no][1], payment_no, payment, 
                payment_date, 0, remainder, delay.days))

                iter += 1
                installment_no += 1
                installment = self.inst_sch[installment_no][2]

            else:
                if installment + remainder > Decimal('0'):
                    installment_remainder = installment + remainder
                    delay = datetime.date.today() - self.inst_sch[installment_no][1]
                    new.append((installment_no, self.inst_sch[installment_no][2], 
                    self.inst_sch[installment_no][1], payment_no, payment, 
                    payment_date, installment_remainder, 0, delay.days))

                    iter = 0
                else:
                    delay = payment_date - self.inst_sch[installment_no][1]
                    new.append((installment_no, self.inst_sch[installment_no][2], 
                    self.inst_sch[installment_no][1], payment_no, payment, 
                    payment_date, 0, 0, delay.days))

        except IndexError:
            if iter == 0:
                delay = payment_date - self.inst_sch[-1][1]
                new.append((9999, '', '', payment_no, payment, payment_date, 0, payment*Decimal('-1'), delay.days))
            else:
                delay = payment_date - self.inst_sch[-1][1]
                new.append((9999, '', '', payment_no, payment, payment_date, 0, 0, delay.days))
        ### zrobić warunek inny niż try/except do index errrora ###
        
        return new

    def calc_delay(self, inst_due_date):
        '''
        generating delay in days if installment is behind schedule
        '''
        today = datetime.date.today()
        delay = today - inst_due_date
        return delay.days if delay.days > 0 else ''

    
    def create_schedule(self):
        '''
        generating full schedule - with installments delays and all payments
        '''
        self.complete = []
        if not self.get_payments:
            [self.complete.append((a,c,b,'','','','','','')) for (a,b,c) in self.inst_sch]
            return self.complete
        [self.complete.extend(self.count_payment(n, self.get_payments[n][0], self.get_payments[n][1])) for n in range(len(self.get_payments))]
        if self.complete[-1][0] < len(self.inst_sch):
            last_inst_no = self.complete[-1][0]
            [self.complete.append((a,c,b,'','','','','', self.calc_delay(b))) for (a,b,c) in self.inst_sch[last_inst_no+1:]]
        return self.complete


    def schedule_human(self):
        x = [f'rata: {a} - {b} - {c} // wplata: {d} - {e} - {f} // zost raty: {g} // zost wpl: {h} // zwloka: {i}' for (a,b,c,d,e,f,g,h,i) in self.complete]
        return '\n'.join(x)

    '''

        ### Old part-using floats instead of decimals ###

 
    @property
    def total_amount(self):
        return round(self.installments*self.loan_period,2)

    @property
    def installments(self):
              
        p = (self.global_interest_rate/100*2)/12
        nu = p*((1+p)**self.loan_period)
        de = ((1+p)**self.loan_period)-1
        total = self.amount_requested * (nu/de)
        if self.product_name == 'L1':
            return round(total + (0.15*total), 2)
        else:
            return round(total, 2)
    
    @property
    def installement_schedule(self):
        try:
            z = []
            for x in range(1, self.loan_period+1):
                
                z.append(f'{x} - amount: -- {self.installments} ---- Required by: -- {self.created_date + relativedelta(months=x)}')
            return '\n'.join(z)
            # return z
        except:
            return 'You must create a loan first ! '

    @property
    def installment_dict(self):
        try:
            installments = {}
            for x in range(1, self.loan_period+1):
                installments[x] = {
                    'amount' : self.installments,
                    'required by' : str(self.created_date + relativedelta(months=x))
                }
                # installments['amount'] = self.installments
                # installments['required by'] = self.created_date + relativedelta(months=x)
            return installments
        except:
            return 'NO Loans'

    '''