"""
Project 331
CSE
Ms. Koelm
Ryan Grund, CLI crook & Wiliam Orban, vetted json wizard
1st Hour
"""
import json, bcrypt
accountList=None
activeAccounts=[]
uname=None
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
                    open(f"/Volumes/WMO32/CSE/Project 331/privAssets/userLists/{fileName}.json", "x") #MAC FILE PATH
                    #open(f"E:\CSE\Project 331\privAssets\userLists{fileName}.json", "x") #WINDOWS PATH
                    with open(f"/Volumes/WMO32/CSE/Project 331/privAssets/userLists/{fileName}.json", "w") as outfile:# mac
                    #with open(f"E:\CSE\Project 331\privAssets\userLists{fileName}.json", "w") as outfile: #WINDOWS VERSION

                        outfile.write("[\n\n]")
                    hashedPassword=hash(password, globalSalt)
                    print(f"Password set!") #confirmation message
                    jsonExport(fname, lname, removeByteMark(str(hashedPassword))) #exports account data to accountData.json, byte data removed from hash.
                    print(f"\n\nAcount created! Redirecting to login...") #account creation confirmation message
                    break
                else: 
                    print(f"The password entered did not match. Please try again.")
        break

    


def login(): #user logs in.
    login = False
    while login == False:
        print(f"Please enter your name and password to login successfully.")
        fname=input(f"First name: ").lower()
        lname=input(f"Last name: ").lower()
        loginUser=f"{fname}{lname}"
        global uname 
        uname = f"{fname.lower()}{lname.lower()}"
        if loginUser in activeAccounts: #if user exists from pullAccount()
            while True: 
                jsonData=json.load(open(jsonPath))
                for user in jsonData:
                    if user["uname"] == loginUser:
                        userFileHash=user["password"] #pulls hash from loginUser's json data
                loginPassword = input(f"Password: ")
                if hash(loginPassword, globalSalt) == bytes(userFileHash, "utf-8)"): #conditional checks to see if hashed passwords match, if they do, login is sucessful and login funciton breaks
                    print(f"Login successful!\n\nWelcome, {fname}.")
                    login = True
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

import csv

csvFile="/Volumes/WMO32/CSE/Project 331/privAssets/unis.csv" #mac
#csvFile=r"E:\CSE\Project 331\privAssets\unis.csv" #windows
stateList=[ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
cityList=[]
rows=[]
with open(csvFile, "r") as csvFile:
    csvReader=csv.reader(csvFile)
    for row in csvReader:
        rows.append(row)

results=[]

def exportSelection(selection):
    uniExport = []
    with open(f"/Volumes/WMO32/CSE/Project 331/privAssets/userLists/{uname}.json", "r") as outfile: #MAC VERSION
    #with open(f"E:\CSE\Project 331\privAssets\userLists{uname}.json", "r") as outfile: #WINDOWS VERSION
        uniExport = json.load(outfile)
    uniNames=[]
    for uniName in uniExport:
        uniNames.append(uniName["uniName"])
    if selection[0] not in uniNames: #if selection is not already exported
        uniExport.append(
            {
                "uniName":selection[0],
                "uniCity":selection[1],
                "uniState":selection[2]
            }
        )
    else:
        print(f"It looks like you have already saved this university to your list.")
        #ADD WHILE LOOP/BREAK THING ONCE YOU GET YOUR NAVIGATION STRAIGHT

    with open(f"/Volumes/WMO32/CSE/Project 331/privAssets/userLists/{uname}.json", 'w') as json_file: #MAC VERSION
    #with open(f"E:\CSE\Project 331\privAssets\userLists{fileName}.json{uname}.json", 'w') as json_file: #WINDOWS VERSION
        json.dump(uniExport, json_file, indent=4)
    while True:
        again=int(input(f"Would you like to select another university to add to your list? Enter the number in brackets next to your response:\n[0] : No\n[1] : Yes\n Selection:    "))
        if again == 0:
            print(f"Ending selection...")
            select = False
            break
        elif again == 1:
            print(f"Repeating selction process...")
            select = True
            numCheck=False
            break
        else:
            print(f"It looks like your response of '{again.upper()}' was not recognized. Please try again.")
        

def select(list: list):
    selectionList=[]
    select=True
    numCheck=False
    while select == True:
        while numCheck==False:
            number=input(f"Please enter the number in brackets next to the institution you would like to select. If you would not like to select any institution mentioned, enter, 'x'.").lower()
            if number == "x":
                print(f"Exiting...")
                select=False
                numCheck=True
                break
            elif int(number) > len(list) or int(number) < 0:
                print(f"Your selection, '{number}' was not found.")
                numCheck=False #number not found, will ask again
            else:
                selection = list[int(number)]
                uniFormatted=f"{selection[0]} in {selection[1]}, {selection[2]}"
                print(f"You selected '{uniFormatted}.'")
                selectionList.append(selection)
                exportSelection(selection)
    return selectionList

def enterState(): #procedure for user entering state
    while True:
        state=input(f"\n\n\nState: ")
        if len(state) > 2: #conditional that checks state entry
            print(f"It looks like you're selection of '{state.upper()}' was invalid as it was {len(state)} characters long. Please only enter in 2-character US state identification codes. ")
            state=None
        elif state.upper() not in stateList:
            print(f"It looks like your slection of '{state.upper()}' was invalid. Please only enter in 2-character US state identification codes.")
            state=None
        else:
            return state
        
def stateSearch(state, mode: int):
    stateList=[]
    count=0
    if mode == 1:
        for uni in rows:
            if uni[2]==str(state).upper():
                print(f"[{count}] : {uni[0]} in {uni[1]},{uni[2]}")
                count+=1
                stateList.append(uni)
        select(stateList)
        navigation(2)
        return stateList
    elif mode == 2:
        for uni in rows:
            if uni[2]==str(state).upper():
                stateList.append(uni)
        return stateList

def citySearch(): #ISSUE RESOLVED issue where, when generating city colleges to choose from, all options are duplicated. is likely due to the fact that the program proceeds throught the normal state search and then something else. 
    state=enterState()
    citySearching=True
    while citySearching==True:
        stateList=stateSearch(state,2)
        cityResults=[]
        count = 0
        city = input(f"\n\n\nCity:")
        for uni in stateList:
            if city.upper() in uni[1]:
                print(f"[{count}] : {uni[0]} in {uni[1]},{uni[2]}")
                count+=1
                cityResults.append(uni)
                citySearching=False
                break
            elif city.upper() not in uni[1] and stateList.index(uni)==len(stateList)-1:
                print(f"\n\nIt looks like your city selection of '{city.upper()}' did not warrant any results. Please try again. ")
                citySearching=True

    select(cityResults)
    navigation(2)
    return cityResults

def navigation(stage):
    print(f"\n\nEnter the corresponding number to go the the respective part of the program:")
    if stage==1:
        print(f"[0] : Home\n")
        navSelection=input(f"Selection: ")
        match int(navSelection):
            case 0:
                goHome()
                #ADD LOGOUT FUNCTIONALITY
    elif stage==2:
        print(f"[0] : Home\n[1] : Search by state.\n[2] : Search by city")
        navSelection=input(f"Selection: ")
        match int(navSelection):
            case 0:
                #goHome()
                print(f"GoHome()")
            case 1:
                stateSearch(enterState(),1)
            case 2:
                citySearch()

navigation(2)