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

def select(list: list):
    selectionList=[]
    while True:
        number=int(input(f"Please enter the number in brackets next to the institution you would like to select."))
        if number > len(list) or number < 0:
            print(f"Your selection, '{number}' was not found.")
        else:
            selection = list[number]
            print(f"You selected '{selection[0]} in {selection[1]},{selection[2]}.'")
            selectionList.append(selection)
            break
        
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
        navigation(2)
        return stateList
    elif mode == 2:
        for uni in rows:
            if uni[2]==str(state).upper():
                stateList.append(uni)
        return stateList

def citySearch(): #ISSUE RESOLVED issue where, when generating city colleges to choose from, all options are duplicated. is likely due to the fact that the program proceeds throught the normal state search and then something else. 
    state=enterState()
    stateList=stateSearch(state,2)
    cityResults=[]
    count = 0
    city = input(f"\n\n\nCity:")
    for uni in stateList:
        if city.upper() in uni[1]:
            print(f"[{count}] : {uni[0]} in {uni[1]},{uni[2]}")
            count+=1
            cityResults.append(uni)

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
                print(f"goHome")
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

stateSearch(enterState,1)