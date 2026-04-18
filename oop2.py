#---------------oops 2--------------------------last chapter

#del - delete keyword

#class cls:
#    def __init__(self, name, txt):
#       self.name = name
#        self.txt = txt
#c1 = cls("kali","oli")
#print(c1.name)
#print(c1.txt)

#del c1.name 
#print(c1.name)
#print(c1.txt)     #not working

#2)--------private---methode use __ front of the object-----------------------

#----------------------password fixing-------------------

#class cls:
#    def __init__(self, name ,password):
#        self.name = name 
#        self.__password = password #------not directly access in the print fn--------------
#    def showpassword(self):
#        return self.__password #------acces in the print fn and display the password----

#c1 = cls("kali","200626")
#print(c1.name)
#print(c1.showpassword())



#class cls:
#    __name = "kali" # direct print(c1.__name) -- error output

#    def __ini(self):
#        return "hello kali"
#    def welcome(self):
#        return self.__ini()
#    def o(self):             # if run this fn come error
#        return self.__name() # if run this fn come error
    
#c1 = cls()
#print(c1.welcome())
    
#3) -----------Inheritance-----------in the oops 3piller--------------------------

# ------------------*single inheritance-----------------
#-----------------parent---->child------------------

#-------------------*multi level inheritance-----------------
#------------parent-parent-child------------
#class car:
#    color = "black"
#    @staticmethod
#    def start():
#        print("car started...")
#    @staticmethod
#    def stop():
#        print("car stopped..")
#    
#class bmw(car):
#    def __init__(self, brand):
#        self.brand = brand    #----child is not give the input 

#class m4(bmw):
#    def __init__(self, name):
#        self.name = name


#c1 = m4("kali")
#print(c1.name)
#c1.start()
#c1.stop()

#-------------------------------

#-----------*multiple Inheritance--------------

#-------------many parent connected to the single child-----

#class A:
#    varA = "welcome class A"
#class B:
#    varB = "welcome class B"
#class C(A, B):
#    varC = "welcome class C"

#c1 = C()
#print(c1.varA)
#print(c1.varB)
#print(c1.varC)
    
#*************************************************************************#

#4)-----------------super method-------------#acces parent class

#class car:
#    def __init__(self, type):
#        self.type = type  # not access in another class to access mean use super method
    
#    @staticmethod  #not want to use the self(object name)
#    def start():
#        print("car is started")

#    @staticmethod
#    def stop():
#        print("car is stopped")

#class bmw(car):
#    def __init__(self, name, type):
#        self.name = name
#        super().__init__(type) #----accessing the first class car
#         super().start()        #---------car is started-----------------#

#c1 = bmw("M5", "petrol")
#print(c1.type)
#print(c1.name)


#5)--------------------------class method------------------#
    
#---------------------normally changing name ------------------#
#lass person:
#    name = "kali"         # how to change this name using def
#    def changename(self, name):
#        person.name = name        # using person.name is accesing the class name 

#p1 = person()
#p1.changename("oli")
#print(p1.name)
#print(person.name)  #output----- kali

#----------------------------------------- using another normal fn-----(__class__)

#class person:
#    name = 'kali'
#    def changename(self, name):
#        self.__class__.name = name
#p1 = person()
#p1.changename("esh")
#print(p1.name)
#print(person.name)

#----------------------------using class method
 
#class person:
#    name = "kali"

#    @classmethod         #------direct access theclass object
#    def changename(cls, name):
#        cls.name = name
#p1 = person()
#p1.changename("oli")
#print(p1.name)
#print(person.name)

#6)------------------property method---------------------------


#---------------------------------------normal code not change the value
#class person:
#    def __init__(self, phy, chem, math):
#        self.phy = phy
#        self.chem = chem
#        self.math = math
#        self.persentage = str((self.phy + self.chem + self.math)/3)+ "%"
    
#p1 = person(99, 98, 97)
#print(p1.persentage) #98.0%

#p1.phy = 95
#print(p1.persentage)     # not changed the previus persentage

#print(p1.phy)

#-------------------------------------another normal code to change the value


#class person:
#    def __init__(self, phy, chem, math):
#        self.phy = phy
#        self.chem = chem
#        self.math = math

#    def persentage(self):
#        return str((self.phy + self.chem + self.math)/3)+ "%"
    
#p1 = person(99, 98, 97)
#print(p1.persentage())
#p1.phy = 95
#print(p1.persentage) output is change


#--------------------------------------------using property method

#class person:
#    def __init__(self, phy, chem, math):
#        self.phy = phy
#        self.chem = chem
#        self.math = math

#    @property
#    def persentage(self):
#            return str((self.phy+self.chem+self.math)/3)+"%"
#p1 = person(90, 89,91)
#print(p1.persentage)

#p1.phy = 87
#print(p1.persentage)   # change output there not want to write brack ()

#7)---------------polymorphism:operator ovweloading---------------------

#-------------------notes of dunder fn


#8)----------------------------complex number----------------------#

class complex:
    def __init__(self, real, img):
        self.real = real
        self.img = img

    def val(self):
        print(self.real,"i +",self.img,"j")

    def __add__(self, num2):
        newreal = self.real + num2.real
        newimg = self.img + num2.img
        return complex(newreal, newimg)
    
#    def val(self):
#        print(self.real,"i +",self.img,"j")

num1 = complex(6,6)
print(num1.val())

num2 = complex(4, 6)
print(num2.val())

num3 = num1+num2
print(num3.val())
