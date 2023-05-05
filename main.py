"""
Project 331
CSE
Ms. Koelm
Ryan Grund & Wiliam Orban
1st Hour
"""
import json, bcrypt
activeAccounts=[]
uname=None
unameFP=None


#jsonPath=r'/Volumes/WMO32/CSE/Project 331/privAssets/accountData.json' #mac
#jsonPath=r'E:\CSE\Project 331\privAssets\accountData.json' #windows
#csvFile="/Volumes/WMO32/CSE/Project 331/privAssets/unis.csv" #mac
#csvFile=r"E:\CSE\Project 331\privAssets\unis.csv" #windows


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
    global unameFP, uname
    print(f"Please enter the following information as it is presented to create your account.")
    while True:

        fname=input(f"First name: ").lower()
        lname=input(f"Last name: ").lower()
        uname=f"{fname.lower()}{lname.lower()}"
        unameFP=f"/Volumes/WMO32/CSE/Project 331/privAssets/userLists/{uname}.json" #mac
        #unameFP=f"E:\CSE\Project 331\privAssets\userLists\{uname}.json" #windows
        if uname in activeAccounts: #if user already exists, redirects to login.
            print(f"\nIt looks like the username you have entered is already associated with another account. Proceeding to login... ")
            break
        else: #otherwise, account setup proceeds
            while True:

                password=input(f"Set password: ")
                checkPassword=input(f"Please reenter your password: ")

                if checkPassword==password: #if password matches and is confirmed, then backend assets are created.
                    uname=f"{fname.lower()}{lname.lower()}"
                    open(unameFP, "x") #WINDOWS PATH
                    with open(unameFP, "w") as outfile: #WINDOWS VERSION

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
    global unameFP, uname
    login = False
    while login == False:
        print(f"Please enter your name and password to login successfully.")
        fname=input(f"First name: ").lower()
        lname=input(f"Last name: ").lower()
        uname = f"{fname.lower()}{lname.lower()}"
        unameFP=f"/Volumes/WMO32/CSE/Project 331/privAssets/userLists/{uname}.json" #mac
        #unameFP=f"E:\CSE\Project 331\privAssets\userLists\{uname}.json" #windows
        if uname in activeAccounts: #if user exists from pullAccount()
            while True: 
                jsonData=json.load(open(jsonPath))
                for user in jsonData:
                    if user["uname"] == uname:
                        userFileHash=user["password"] #pulls hash from uname's json data
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
            print(f"Account not found. Loginuser: {uname}")

    
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
    global uname
    uniExport = []
    with open(unameFP, "r") as outfile: #WINDOWS VERSION
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

    with open(unameFP, 'w') as json_file: 
        json.dump(uniExport, json_file, indent=4)
        

def select(list: list):
    selectionList=[]
    select=True
    numCheck=False
    while select == True:
        while numCheck==False:
            number=input(f"\nPlease enter the number in brackets next to the institution you would like to select to add to your list. If you would not like to select any institution mentioned, enter, 'x' : ").lower()
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
                print(f"\n\nYou selected '{uniFormatted}.'\n\n")
                selectionList.append(selection)
                exportSelection(selection)
                while True:
                    again=int(input(f"Would you like to select another university to add to your list? Enter the number in brackets next to your response:\n[0] : No\n[1] : Yes\nSelection:    "))
                    if again == 0:
                        print(f"Ending selection...")
                        select = False
                        numCheck= True
                        break
                    elif again == 1:
                        print(f"Repeating selction process...")
                        select = True
                        numCheck=False
                        break
                    else:
                        print(f"It looks like your response of '{again.upper()}' was not recognized. Please try again.")
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
        navigation()
        return stateList
    elif mode == 2:
        for uni in rows:
            if uni[2]==str(state).upper():
                stateList.append(uni)
        return stateList

def citySearch(): 
    citySearching=True
    while citySearching==True:
        cityResults=[]
        count = 0
        stateList=stateSearch(enterState(),2)
        city = input(f"\n\n\nCity:")
        for uni in stateList:
            if city.upper() in uni[1]:
                print(f"[{count}] : {uni[0]} in {uni[1]},{uni[2]}")
                count+=1
                cityResults.append(uni)
                #citySearching=False
                #break
            elif stateList.index(uni)==len(stateList)-1:
                citySearching=False
                break
        if cityResults==[]:
            print(f"\n\nIt looks like your city selection of '{city.upper()}' did not warrant any results. Please try again. ")
            citySearching=True    
    select(cityResults)
    navigation()
    return cityResults

def viewSaved(mode:int):
    global unameFP, uname
    count = 0
    match mode:
        case 1:
            userSaved=[]
            userData=json.load(open(unameFP, "r"))
            for institution in userData:
                count +=1
                print(f"[{count}] : {institution['uniName']} in {institution['uniCity']}, {institution['uniState']}")
                userSaved.append(institution)
            print(f"\nYou have {count} institutions saved. ")
            navigation()
            return userSaved
        case 2:
            userSaved=[]
            userData=json.load(open(unameFP, "r"))
            for institution in userData:
                print(f"[{count}] : {institution['uniName']} in {institution['uniCity']}, {institution['uniState']}")
                count +=1
                userSaved.append(institution)
            return userSaved


            

def remove():
    select=True
    numCheck=False
    userSaved=viewSaved(2)
    while select == True:
        while numCheck==False:
            choice=input(f"\nPlease enter the number in brackets next to the institution you would like to select to delete. If you would not like to select any institution mentioned, enter, 'x' : ").lower()
            if choice == "x":
                print(f"Exiting...")
                navigation()
                select=False
                numCheck=True
                break
            elif int(choice) > len(userSaved) or int(choice) < 0:
                print(f"Your selection, '{choice}' was not found.")
                numCheck=False #number not found, will ask again
            else:
                selection = userSaved[int(choice)]
                uniFormatted=f"{selection['uniName']} in {selection['uniCity']}, {selection['uniState']}"
                print(f"\n\nYou selected '{uniFormatted}.'\n\n")
                removeSelection(selection)
                while True:
                    again=int(input(f"Would you like to select another university to remove from your list? Enter the number in brackets next to your response:\n[0] : No\n[1] : Yes\nSelection:    "))
                    if again == 0:
                        print(f"Ending selection...")
                        select = False
                        numCheck= True
                        break
                    elif again == 1:
                        print(f"\nRepeating deletion process...\n")
                        userSaved=viewSaved(2)
                        select = True
                        numCheck=False
                        break
                    else:
                        print(f"It looks like your response of '{again.upper()}' was not recognized. Please try again.")


def removeSelection(selection):
    with open(unameFP, "r") as jsonFile:
        data=json.load(jsonFile)
    data.remove(selection)
    with open(unameFP, "w") as jsonFile2:
        json.dump(data, jsonFile2, indent=4)

def navigation():
    print(f"\n\nEnter the corresponding number to go the the respective part of the program:\n\n")
    print(f"[0] : Home\n[1] : Search by state\n[2] : Search by city\n[3] : View saved institutions\n[4] : Delete an institution from your list")
    navSelection=input(f"\n\nSelection: ")
    match int(navSelection):
        case 0:
            goHome()
        case 1:
            stateSearch(enterState(),1)
        case 2:
            citySearch()
        case 3:
            viewSaved(1)
        case 4:
            remove()

navigation()