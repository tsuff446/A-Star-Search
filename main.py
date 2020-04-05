from tkinter import *
import heapq

windowWidth = 50
rowNum = 10
colNum = 10

endpoints = []

root = Tk()
root.title("A* Algorithm")

buttonArray = []
Label(root, text="Testing")
window = Frame(root, width=windowWidth)
window.grid(row=0, column=0, columnspan=colNum)

# handles left clicks
def left(event):
    xCoord = event.x_root - window.winfo_rootx()
    yCoord = event.y_root - window.winfo_rooty()
    newX, newY = window.grid_location(xCoord, yCoord)
    if buttonArray[newX][newY].cget('bg') != "green":
        buttonArray[newX][newY].configure(bg="green")
        consoleText['text'] = "Added endpoint at (" + str(newX) + ", " + str(newY) + ")"
        global endpoints
        endpoints.append((newX, newY))
    else:
        buttonArray[newX][newY].configure(bg="white")
        consoleText['text'] = "Removed endpoint at (" + str(newX) + ", " + str(newY) + ")"
        endpoints.remove((newX, newY))


# handles right clicks
def right(event):
    xCoord = event.x_root - window.winfo_rootx()
    yCoord = event.y_root - window.winfo_rooty()
    newX, newY = window.grid_location(xCoord, yCoord)
    if buttonArray[newX][newY].cget('bg') == "black":
        buttonArray[newX][newY].configure(bg="white")
        consoleText['text'] = "Removed wall at (" + str(newX) + ", " + str(newY) + ")"
    elif buttonArray[newX][newY].cget('bg') == "green":
        buttonArray[newX][newY].configure(bg="black")
        consoleText['text'] = "Added wall at (" + str(newX) + ", " + str(newY) + ")"
        global endpoints
        endpoints.remove((newX, newY))
    else:
        buttonArray[newX][newY].configure(bg="black")
        consoleText['text'] = "Added wall at (" + str(newX) + ", " + str(newY) + ")"


# draws buttons to screen and stores them in array
for x in range(colNum):
    buttonArray.append([])
    for y in range(rowNum):
        buttonArray[x].append(
            Button(window, padx=5, pady=5))
        buttonArray[x][y].grid(row=y, column=x)
        buttonArray[x][y].bind('<Button-1>', left)  # bind left mouse click
        buttonArray[x][y].bind('<Button-3>', right)  # bind right mouse click
        buttonArray[x][y].configure(width=int(windowWidth/colNum), height=int(windowWidth/(2*colNum)), bg="white")


# "Manhattan" distance
def h(curr, goal):
    return abs(curr[0] - goal[0]) + abs(curr[1] - goal[1])

# highlights path red
def highlightPath(end, previous):
    curr = previous[end]
    distance = 1
    while previous[curr] is not None:
        buttonArray[curr[0]][curr[1]].configure(bg="red")
        curr = previous[curr]
        distance += 1
    consoleText['text'] = "Final Distance: " + str(distance)

# clears all red squares
def clearRed():
    for x in range(colNum):
        for y in range(rowNum):
            if buttonArray[x][y].cget('bg') == "red":
                buttonArray[x][y].configure(bg="white")

# clears entire board
def clearAll():
    for x in range(colNum):
        for y in range(rowNum):
                buttonArray[x][y].configure(bg="white")
    global endpoints
    endpoints = []

# implements A* algorithm to find shortest path
def startSearch():
    clearRed()
    if len(endpoints) != 2:
        consoleText['text'] = "Error: Incorrect number of endpoints"
        return False
    binheap = []
    start = endpoints[0]
    end = endpoints[1]
    fDist = {}
    gDist = {}
    previous = {}
    seen = {}
    for x in range(colNum):
        for y in range(rowNum):
            fDist[(x,y)] = float('+inf')
            gDist[(x,y)] = float('+inf')
            previous[(x,y)] = None
            seen[(x,y)] = False

    gDist[start] = 0
    fDist[start] = h(start, end)
    heapq.heappush(binheap, (h(start, end), start))
    while binheap != []:
        currNode = heapq.heappop(binheap)
        currCoord = currNode[1]
        if currCoord == end:
            highlightPath(end, previous)
            return True
        if seen[currCoord] == False:
            seen[currCoord] = True
            if currCoord[0] + 1 < colNum:
                new = (currCoord[0]+1, currCoord[1])
                if gDist[currCoord] + 1 < gDist[new] and buttonArray[new[0]][new[1]].cget('bg') != "black":
                    previous[new] = currCoord
                    fDist[new] = gDist[currCoord] + h(new, end)
                    gDist[new] = gDist[currCoord] + 1
                    heapq.heappush(binheap, (fDist[new], new))
            if currCoord[0] - 1 >= 0:
                new = (currCoord[0]-1, currCoord[1])
                if gDist[currCoord] + 1 < gDist[new] and buttonArray[new[0]][new[1]].cget('bg') != "black":
                    previous[new] = currCoord
                    fDist[new] = gDist[currCoord] + h(new, end)
                    gDist[new] = gDist[currCoord] + 1
                    heapq.heappush(binheap, (fDist[new], new))
            if currCoord[1] + 1 < rowNum:
                new = (currCoord[0], currCoord[1] + 1)
                if gDist[currCoord] + 1 < gDist[new] and buttonArray[new[0]][new[1]].cget('bg') != "black":
                    previous[new] = currCoord
                    fDist[new] = gDist[currCoord] + h(new, end)
                    gDist[new] = gDist[currCoord] + 1
                    heapq.heappush(binheap, (fDist[new], new))
            if currCoord[1] - 1 >= 0:
                new = (currCoord[0], currCoord[1]-1)
                if gDist[currCoord] + 1 < gDist[new] and buttonArray[new[0]][new[1]].cget('bg') != "black":
                    previous[new] = currCoord
                    fDist[new] = gDist[currCoord] + h(new, end)
                    gDist[new] = gDist[currCoord] + 1
                    heapq.heappush(binheap, (fDist[new], new))
    consoleText['text'] = "Error: Path impossible"
    return False


consoleText = Label(window, text="Left Click to place an endpoint, Right Click to place a wall", padx=windowWidth, pady=10)
consoleText.grid(row=rowNum, columnspan=colNum)

startButton = Button(window, text="Start", padx = 20, command=startSearch)
startButton.grid(row=rowNum+1, column=int(colNum/2), columnspan=7)
startButton.configure(bg="blue")

clearButton = Button(window, text="Clear", padx= 20, command=clearAll)
clearButton.grid(row=rowNum+1, column=0,columnspan=3)
clearButton.configure(bg="red")


root.mainloop()
