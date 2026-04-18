import random
target = random.randint(1, 100)

while True:
    userchoice = input("guess the target or Quick(Q): ")
    if(userchoice == "Q"):
        break;
    userchoice = int(userchoice)
    if (userchoice == target):
        print("Success: correct guess!")
        break;
    elif(userchoice < target):
        print("user number was smaller. take the bigger guess..")
    else:
        print("user number was big . take the smaller guess")
print("----------Game Over----------")
