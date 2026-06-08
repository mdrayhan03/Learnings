'''
A cursor based pagination is like a bookmark where we don't search page by page rather than last row or word
'''

data = [
    (f"Name {i}", f"Description {i}") for i in range(1, 101)
]

last_row = 0
offset = 10

def load(data, last_row, direction, offset) :
    if direction == "prev" :
        if last_row - offset > 0 :
            last_row = last_row - offset
        else :
            last_row = 0
        show(data[last_row: last_row + offset])
    elif direction == "next" :
        if last_row + offset < len(data) :
            last_row = last_row + offset
        else :
            last_row = 0
        show(data[last_row - offset: last_row])
    
    return last_row

def show(data) :
    for ele in data :
        print(ele)

def prev(data, last_row, offset) :
    return load(data, last_row, "prev", offset)


def next(data, last_row, offset) :
    return load(data, last_row, "next", offset)

last_row = next(data, last_row, offset)
while True :
    print("Give your input from options: 1.prev, 2.next, 3.quit (give number)")
    inp = int(input("Enter your option no: "))

    if inp == 1 :
        last_row = prev(data, last_row, offset)
    elif inp == 2 :
        last_row = next(data, last_row, offset)
    elif inp == 3 :
        print("Thank you")
        break