"""
Project 331
CSE
Ms. Koelm
Ryan Grund & Wiliam Orban
1st Hour
"""
import json, bcrypt
accountList=None
activeAccounts=[]
#jsonPath=r'E:\CSE\Project 331\privAssets\accountData.json' #windows
jsonPath=r'/Volumes/WMO32/CSE/Project 331/privAssets/accountData.json' #mac
#saltFile=open('E:\CSE\Project 331\privAssets\saltFile.txt', "r") #windows
saltFile=open('/Volumes/WMO32/CSE/Project 331/privAssets/saltFile.txt', "r") #mac
globalSalt=bytes(saltFile.readline(), "utf-8")

def hash(plainText, salt): #password hashing function
    bytePass=bytes(plainText, "utf-8")
    return bcrypt.hashpw(bytePass, salt)


def pullAccountList(): #pulls all accounts from accountData.json file into program list activeAccounts.
    jsonData=json.load(open(jsonPath))
    for user in jsonData:
        activeAccounts.append(user["uname"])

def removeByteMark(byte): #removes the b'' added when a byte is stored to get the raw byte in string form that can then be converted to string for storage 
    targetIndex=[0,1]
    byteList=[]
    for letter in byte:
        byteList.append(letter)
    byteList.pop(0)
    byteList.pop(0)
    byteList.pop()
    return "".join(byteList)       


def jsonExport(fname, lname, hashedPassword): #creates user dictionary to be saved into json file
        listObj = []
        
        with open(jsonPath) as outfile:
            listObj = json.load(outfile)
        listObj.append(
        {
        "uname":f"{fname}{lname}",
        "password":hashedPassword
        })

        with open(jsonPath, 'w') as json_file:
            json.dump(listObj, json_file, indent=4)

def createAccount(): #creates a user account
    print(f"Please enter the following information as it is presented to create your account.")
    while True:

        fname=input(f"First name: ").lower()
        lname=input(f"Last name: ").lower()
        if f"{fname}{lname}" in activeAccounts: #if user already exists, redirects to login.
            print(f"\nIt looks like the username you have entered is already associated with another account. Proceeding to login... ")
            break
        else: #otherwise, account setup proceeds
            while True:

                password=input(f"Set password: ")
                checkPassword=input(f"Please reenter your password: ")

                if checkPassword==password: #if password matches and is confirmed, then backend assets are created.
                    fileName=f"{fname.lower()}{lname.lower()}"
                    open(f"{fileName}.txt", "x")
                    hashedPassword=hash(password, globalSalt)
                    print(f"Password set!") #confirmation message
                    jsonExport(fname, lname, removeByteMark(str(hashedPassword))) #exports account data to accountData.json, byte data removed from hash.
                    print(f"\n\nAcount created! Redirecting to login...") #account creation confirmation message
                    break
                else: 
                    print(f"The password entered did not match. Please try again.")
        break

    


def login(): #user logs in.
    print(f"Please enter your name and password to login successfully.")
    fname=input(f"First name: ").lower()
    lname=input(f"Last name: ").lower()
    loginUser=f"{fname}{lname}"
    if loginUser in activeAccounts: #if user exists from pullAccount()
        while True: 
            jsonData=json.load(open(jsonPath))
            for user in jsonData:
                if user["uname"] == loginUser:
                    userFileHash=user["password"] #pulls hash from loginUser's json data
            loginPassword = input(f"Password: ")
            if hash(loginPassword, globalSalt) == bytes(userFileHash, "utf-8)"): #conditional checks to see if hashed passwords match, if they do, login is sucessful and login funciton breaks
                print(f"Login successful!\n\nWelcome, {fname}.")
                break
            elif hash(loginPassword, globalSalt) != bytes(userFileHash, "utf-8)"):
                print(f"Login failed. ")
            else:
                print(f"Unexpected error")
                break
    else:
        print(f"Account not found. Loginuser: {loginUser}")

    
def goHome():
    while True:
        pullAccountList()
        print("\n\nWelcome to Super Spiffy Ultra-Cool College Wishlist!\n\nPlease create an account or login by entering the corresponding number associated with an action.")
        accountAction=input(f"\nCreate Account: 1\nLogin: 2\n\nSelection: ")


        if accountAction == "1":
            createAccount()
            print(f"\n\nPlease login: \n")
            pullAccountList()
            login()
            break
        elif accountAction == "2":
            login()
            break
        else:
            print(f"\nInvalid Selection, please Try again:")
goHome()

#END OF LOGIN
