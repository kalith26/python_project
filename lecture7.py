#f = open("deno.txt","r")
 # read and readline 
#d1 = f.readline()
#print(d1)
#d2 = f.readline()
#print(d2)
#print(f.readline()) 
#f.close()

# write  turncate the file
#f = open("deno.txt","w")
#d = f.write("kalith learning python")
#f.close()

#apend store in end
#f = open("deno.txt","a")
#f.write(" by apnaclg ")
#f.write("\n now studing 4sem") #next line
#f.close()

#  r+ read and write
#f = open("deno.txt","r+")
#f.write("oli") #overwrite kalith is change to oliith
#print(f.read())# print with pointer
#f.close()

# w+ write annd read  truncate the file
#f = open("deno.txt","w+")
#print(f.read()) # truncate the file
#f.close()
#f.write("abc")
#f.close()

#a+ 
#f = open("deno.txt","a+")
#print(f.read())
#f.write("acb")
#f.close()

#with syntax
# using with not want to use a close fn compulsary

#with open("deno.txt","r") as f:
#    d = f.read()
#    print(d)

#with open("deno.txt","w") as f:
#    f.write(" new data stored")

#with open("deno.txt","r") as f:
#    print(f.read())


#deleting a file

#import os
#os.remove("sim.txt") # delete a file


