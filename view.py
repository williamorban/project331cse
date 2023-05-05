def remove():
    select=True
    numCheck=False
    userSaved=viewSaved()
    while select == True:
        while numCheck==False:
            choice=input(f"Please enter the number in brackets next to the institution you would like to select to delete. If you would not like to select any institution mentioned, enter, 'x'.").lower()
            if choice == "x":
                print(f"Exiting...")
                select=False
                numCheck=True
                break
            elif int(choice) > len(userSaved) or int(choice) < 0:
                print(f"Your selection, '{choice}' was not found.")
                numCheck=False #number not found, will ask again
            else:
                selection = userSaved[int(choice)]
                uniFormatted=f"{selection[0]} in {selection[1]}, {selection[2]}"
                print(f"You selected '{uniFormatted}.'")
                removeSelection(selection)
                while True:
                    again=int(input(f"Would you like to select another university to remove from your list? Enter the number in brackets next to your response:\n[0] : No\n[1] : Yes\n Selection:    "))
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


def removeSelection(selection):
    with open(unameFP, "r") as jsonFile:
        data=json.load(jsonFile)
    data.remove(selection)
    with open(unameFP, "w") as jsonFile:
        json.dummp(data, jsonFile, indent=4)
    

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
