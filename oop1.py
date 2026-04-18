#python oop concept

#  1) class and object

#class student:          #-------class---------
#    name = "kali"
#s = student()           #-------object---------
#print(s.name)

#s1 = student()    #--------same output is display---------
#print(s1.name)

#own
#class car:
#    color = "black"
#    brand = "kali"
#c = car()
#print(c.color)
#print(c.brand)

#***********************************************************************************#

#  2) ------------constructor or __init__ fn (initialization fn)--------------

#complasary write a __init__ in init fn

#class S:
#    def __init__(self, fullname): #constructor or init fn..self and fullname is parameter
#        self.name = fullname
#        print("adding a new student")
#s1 = S("kalith")
#print(s1.name)
#
#s2 = S("olith")
#print(s2.name)

#class student:
#    def __init__(s, name, mark):   #---- s is defining the object---------
#        s.name = name        #-------no problem to same word in object and parameter------ 
#        s.mark = mark
#        print("Adding new student")
#s1 = student("kalith", 9)
#print(s1.name, s1.mark)

#example 
#class s:
    #default constructor
#    def __init__(self):
#        pass
    #parameterized constructor
#    def __init__(m, n):
#        m.n = n
#        print("new name")
#s1 = s("kali")
#print(s1.n)

#*************************************************************************************#

# 3)  ---------class & instance attributes 1.(class.attr) 2. (obj.attr)------------

#class student:
#    clg_name = "apna clg" #----------single time store in memory like clg----------

#    name = "kali" #class attr

#    def __init__(self, name, mark):
#        self.name = name #obj.attr ,   ---------object.attr >  class.attr---------
#        self.mark = mark              # ------1st preference is obj----------
#        print("adding new student")

#s1 = student("kali", 95)
#print(s1.name, s1.mark)
#print(s1.clg_name)

#s2 = student("oli",95)
#print(s2.name, s2.mark)
#print(s2.clg_name)

#print(student.clg_name) it also work

#***********************************************************************#

# 4) ----------Methods------------ 

#class student:
#    def __init__(self, name):
#        self.name = name
#    def hello(self):
#        print("hello ",self.name)
#s1= student("kali")
#print(s1.name)
#print(s1.hello())  # hole fn is run

#example

#class student:
#    def __init__(self, name, mark):
#        self.name = name
#        self.mark = mark
#    def welcome(self):
#        print("welcome ",self.name)
#    def get_mark(self):
#        return self.mark
#s1 = student("kali",6)
#print(s1.welcome())
#print(s1.get_mark())


#practice  name and average of 3subject

#class student:
#    def __init__(self, name, mark):
#        self.name = name
#        self.mark = mark
#    def avg(self):
#        sum = 0
#        for i in self.mark:
#            sum+=i
#        print("average ",sum/3)

#s1 = student("kali",[90,89,91])
#print(s1.avg()) 
#print(s1.name)

#s1.name = "oli"       # ----directly change the value------
#print(s1.name)
#print(s1.avg())

#**************************************************************#

# 5)----------static Methods-----------

#class student:
    
#    def __init__(self, name):
#        self.name = name
#    @staticmethod   #---decorator---  here not want to use the self parameter  
#    def hello(): # if not use self parametr come error but using the static methode not use self
#        print("hello")

#s1 = student("kali")
#print(s1.name)

#print(s1.hello())   #or s1.hello()

#************************************************************************************#

#-------important------4piller of oops

#--------Abstraction-----encapsulation-----inheritance-------polymerphism--------#

#  1) abstraction

#class car():
#    def __init__(self):
#        self.acc = False  # Unnessasary thing is hide not to display
#        self.brk = False
#        self.clutch = False
#    def start(self):
#        self.clutch = True
#        self.acc = True
#        print("car started")

#s1 = car()
#s1.start()

# 2) -----------encapsulation--------

class account:
    def __init__(self, bal, acc):
        self.account_no = acc
        self.balance = bal
acc = account(12345,1000)
print(acc.balance)
print(acc.account_no)








