#circle - radius, area, perimeter  

#class circle:
#    def __init__(self, radius):
#        self.radius = radius
#    def area(self):
#        return 2*22/7*self.radius**2
#    def perimeter(self):
#        return 2*22/7*self.radius
#c1 = circle(21)
#print(c1.area())
#print(c1.perimeter())

#p 2

#employees table

#class employee:
#    def __init__(self, role, dept, salary):
#        self.role = role
#        self.dept = dept
#        self.salary = salary
#    def showdetail(self):
#        print("role =",self.role)
#        print("dept =",self.dept)
#        print("salary =",self.salary)

#        print("name =",self.name)
#        print("age =",self.age)

#class engineer(employee):
#    def __init__(self, name, age):
#        self.name = name
#        self.age = age
#        super().__init__("engineer","IT","88000")

#c = engineer("kaith", 20)
#print(c.showdetail())


class order:
    def __init__(self, item, price):
        self.item = item
        self.price = price
    def __gt__(self, ord2):
        return self.price > ord2.price

a = int(input()) 
b = int(input())   
ord1 = order("boxe",a)
ord2 = order("tea",b)
print(ord1>ord2)

    