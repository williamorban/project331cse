import csv

csvFile="/Volumes/WMO32/CSE/Project 331/privAssets/unis.csv" #mac
#csvFile=r"E:\CSE\Project 331\privAssets\saltFile.txt" #windows
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

"""while True:
    stateSelect=input(f"\n\n\nState: ")
    if len(stateSelect) > 2: #conditional that checks state entry
        print(f"It looks like you're selection of '{stateSelect.upper()}' was invalid as it was {len(stateSelect)} characters long. Please only enter in 2-character US state identification codes. ")
    elif stateSelect.upper() not in stateList:
        print(f"It looks like your slection of '{stateSelect.upper()}' was invalid. Please only enter in 2-character US state identification codes.")
    else:
        break"""

results=[]



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
    count = 1
    stateList=[]
    if mode == 1:
        for uni in rows:
            if uni[2]==str(state).upper():
                results.append(uni[0])
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

def citySearch():
    state=enterState()
    stateList=stateSearch(state,2)
    cityResults=[]
    count = 1
    city = input(f"\n\n\nCity:")
    for uni in stateList:
        if city.upper() in uni[1]:
            print(f"[{count}] : {uni[0]} in {uni[1]},{uni[2]}")
            count+=1
            cityResults.append(uni)
    for cityUni in cityResults:
        if city.upper() in cityUni[1]:
            print(f"[{count}] : {cityUni[0]} in {cityUni[1]},{cityUni[2]}")
        elif city.upper() not in cityUni[1]:
            print(f"It looks like your selection of '{city.upper()}' was not in the state you searched for, '{state.upper()}'.")
    navigation(2)
    return cityResults

"""print(f"Enter the corresponding number to go the the respective part of the program:")
print(f"[0] : Home\n[1] : Search by state.\n[2] : Search by city")"""


def navigation(stage):
    print(f"Enter the corresponding number to go the the respective part of the program:")
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