def select(list):
    selectionList=[]
    while True:
        number=int(input(f"Please enter the number in brackets next to the institution you would like to select."))
        if number > len(list) or number < 0:
            print(f"Your selection, '{number}' was not found.")
        else:
            selection = list[number]
            print(f"You selected '{selection.upper()}.'")
            selectionList.append(selection)
            break
    return selectionList

select(citySearch)