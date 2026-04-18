#-----practice bank account statements---------------#

class account:
    def __init__(self, acc, bal):
        self.account_no = acc
        self.balance = bal
    def debit(self, amount):
        self.balance -=amount

        print("Rs.",amount," was debited")
        print("Total balance =",self.get_balance())

    def credit(self, amount):
        self.balance+=amount

        print("Rs.",amount," was credited")
        print("Total balance =",self.get_balance())
    
    def get_balance(self):
        return self.balance

acc = account(1234, 1000)
acc.credit(int(input("Enter a credit amount:  ")))
acc.debit(int(input("Enter debit amount:  ")))
