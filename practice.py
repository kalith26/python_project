#practice 1
#with open("p.txt","w") as f:
#    f.write("hi everyone\nwe are learning file i/o\n")
#    f.write("using java\ni like programming in java")

#practice 2
#with open("p.txt","r") as f:
#    d =f.read()
#new_d = d.replace("java", "python")
#print(new_d)
#with open("p.txt","w") as f: # not be truncate
#    f.write(new_d)

#p 3
#def check():

#    with open("p.txt","r") as f:
#        d = f.read()
#        if (d.find("learning")!=-1): # -1 is valide index 
#            print("found")
#        else:
#            print("not found")
#check()

#p 4
#def line():
#    word = "java"
#    d = True
#    l_no = 1 
#    with open("p.txt","r") as f:
#        while d:
#            d = f.readline()
#            if(word in d):
#                print(l_no)
#            l_no+=1
#    return-1
#line()

#p 5
c =0
with open("p.txt","r") as f:
    d = f.read()
    print(d)

#    num = ""
#    for i in range(len(d)):
#        if(d[i]==","):
#            print(num)
#            num = ""
#        else:
#            num+=d[i]
#or
#    num = d.split(",")
#    for i in num:
#        if(int(i)%2==0):
#            c+=1
#        print("no")
#print(c)







