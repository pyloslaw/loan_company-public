class Liczenie2:
    def __init__(self, raty, wplaty):
        self.raty = raty
        self.wplaty = wplaty
        
        # (nr_raty, rata, nr_wpl, wplata, pozostala_kwota_raty, pozostala_kwota_wplaty)
        self.complete = []
        
    def wplac(self, kwota):
        self.wplaty.append(kwota)
        return self.wplaty
    
    def licz(self, nr_wplaty, wplata):
        # (nr_raty, rata, nr_wpl, wplata, pozostala_kwota_raty, pozostala_kwota_wplaty)
        new = []
        
        
        
        # nr_raty = 0 if self.complete == [] else self.complete[-1][0]

        if not self.complete:
            nr_raty = 0
        elif self.complete[-1][4] == 0 and self.complete[-1][5] == 0:
            # nr_raty = len(self.complete)
            nr_raty = self.complete[-1][0] + 1
        else:
            nr_raty = self.complete[-1][0]

        iter = 0
        if iter == 0:
            reszta = wplata * (-1)


        # try:
        #     rata = self.complete[-1][4] if self.complete[-1][4] > 0 and iter == 0 else self.raty[nr_raty]
        # except IndexError:
        #     rata = self.raty[nr_raty]


        if self.complete and self.complete[-1][4] > 0:
            rata = self.complete[-1][4]
        else:
            try:
                rata = self.raty[nr_raty]
            except IndexError:
                rata = self.raty[-1]


        


        try:    
            while rata + reszta < 0:
                reszta = rata + reszta
                new.append((nr_raty, self.raty[nr_raty], nr_wplaty, wplata, 0, reszta))
                iter += 1
                nr_raty += 1
                rata = self.raty[nr_raty]

            else:
                if rata + reszta > 0:
                    pozost_kw_raty = rata + reszta
                    new.append((nr_raty, self.raty[nr_raty], nr_wplaty, wplata, pozost_kw_raty, 0))
                    iter = 0

                else:
                    new.append((nr_raty, self.raty[nr_raty], nr_wplaty, wplata, 0, 0))
        except IndexError:
            new.append((9999, 0, nr_wplaty, wplata, 0, reszta))
        ### zrobić warunek inny niż try/except do index errrora ###
        
        return new
        
    def count_all(self):
        [self.complete.extend(self.licz(n, self.wplaty[n])) for n in range(len(self.wplaty))]
        return self.complete
        



kal_raty = [200, 200, 200, 200, 200]
kal_wplaty = [200, 190, 10, 191] 

ac = Liczenie2(kal_raty, kal_wplaty)

ac.count_all()

print(ac.complete)