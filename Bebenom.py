################################################################################
##
##  Bebenom
##
##  This programs allows for the collaborative selection of baby names in a
##  systematic manner.
##
##
##  Author: Austin Chen
##  Email: austin@austinandemily.com
##  Last Revision: 01/13/16
##
##
## * Code for yourself first! *
##
##
## TO-DO
## -----
## X Save to settings file
## X Read from settings file
## X Rating
## X Get names (up to 1000)
## X '+/-' copy
## X Controls
##   X Quit session
##   X Save session
##   X Go back
##   X Skip
##   X Favorite
## X Back action
## X Back action wrap-around
##
## X Boy/girl session
## X Skip completed new names
## X Complete ratings scenario: all boys or all girls finished
## X Change 'Session complete!' copy
## N Change order of controls (not needed for eventual GUI)
##
## X Loop instead of exiting for invalid user/etc.
## X Add .upper/.lower support for robust user/session detection
## X Add '1' or '2' option for user select, etc.
## X '\n' entry error
##
## X UX: Plan out functionality and menu hierarchy
##   X Main menu: begin session, view results, reset
##   X View results (e.g. liked names)
##   X No settings found upon loading
##   X Selective names loading: only upon 1st run
##   X New users: only upon 1st run
##   X reset all (users, names, ratings)
##
## X Bug: girl names only for small numNames
## X Bug: false completion (numNames = 0)
## N Bug: blank user names
## X UX: save, stop/quit in session (save and quit)
##
## X UX: double spacing for readability (selectively)
## X UX: results formatting
##
## X BRUH, this needs a name... Coordiname/Bebenom
## X Rename project
## X Comment (top-level)
## X rename data file to [name].dat (or .log or .cfg)
## X Toggle surname
## N Stats to results (x out of x names complete, or %, etc.)
## N Double-wide results with users side-by-side (not needed for eventual GUI)
## X ? or h for help (bring up controls again)
##
## W Settings
##   N order: popularity/random
##   W autosave y/n
##   N skip completed names y/n
##   W toggle surname (always on or always off)
##


import sys                  #for basic I/O


################################################################################
##
##  Declarations/Initializations
##
##  User-customizable settings/variables are denoted by **
##

# User-customizable variables
dataFile = 'data.bbn'       #saved data **
numLoadNames = 600          #how many names to pull from 'yob' files (per gender) **

# Data-related
users = []                  #user data
names = []                  #name data
ratings = [[],[]]           #rating data

# Miscellaneous
userIndex = -1              #current user
numNames = 0                #actual number of names loaded (per gender)
lastName = ''               #last name
lastNameToggle = False      #whether or not to display the last name




#################################  FUNCTIONS  ##################################

  
#######################################
##
## Main Menu
## ---------
## Start Session
## View Results
## Switch User
## Reset
## Quit
##
        
def menu():

    global userIndex

    # Loop until completion or the user chooses to quit
    while True:   

        # Show user controls and accept input from the user
        print('\n\n  s: start  v: view results  u: switch user  r: reset  q: quit\n')
        inChar = sys.stdin.readline()[0]
        
        # Start a rating session
        if inChar.lower() == 's':            

            # Begin a new session
            session()

            # Save user data to file
            saveData()

        # View results
        elif inChar.lower() == 'v':                    
            viewResults()

        # Switch user
        elif inChar.lower() == 'u':
            userIndex = abs(userIndex-1)
            print('\nHi, ' + users[userIndex] + '!')
            pass
        
        # Reset data
        elif inChar.lower() == 'r':
            print('\nAre you sure you want to reset? All data will be lost.')
            resetChar = sys.stdin.readline()[0]

            if resetChar.lower() == 'y':            
                print('\n\n')
                newData()                    

        # Quit
        elif inChar.lower() == 'q':            
            return
        
        # Invalid input
        else:
            print('\nInvalid input.')


#######################################
##
##  User select
##

def selectUser():

    global users; global userIndex;

    userIndex = -1;
    while userIndex < 0:            
        print('\nPlease select a user: ' + users[0] + ' or ' + users[1] + '?')
        selectedUser = sys.stdin.readline().split('\n')[0]
        if selectedUser == users[0] or selectedUser == users[0].lower() or \
           selectedUser == users[0].upper() or selectedUser == '1':
            userIndex = 0
            print('\nHi, ' + users[userIndex] + '!')
            break
        elif selectedUser == users[1] or selectedUser == users[1].lower() or \
             selectedUser == users[1].upper() or selectedUser == '2':
            userIndex = 1        
            print('\nHi, ' + users[userIndex] + '!')
            break
        else:
            print('\nInvalid user.')                        


#######################################
##
## Rating session
##
        
def session():

    global names; global ratings; global userIndex; global numNames
    global lastName; global lastNameToggle

    # Initialize variables    
    newEntries = [[],[]]    #stores data for this session: nameIndex, rating
    entryIndex = 0;         #points to the current new entry being worked on
    nextName = 0;           #for picking upcoming names
    
    # Select a session type
    sessionType = -1;
    while sessionType < 0:            
        print('\nPlease select a session type: boys or girls?')
        inChar = sys.stdin.readline()[0]
        if inChar.lower() == 'b' or inChar == '1':
            sessionType = 1
            nextName = numNames
            break
        elif inChar.lower() == 'g' or inChar == '2':
            sessionType = 0
            nextName = 0
            break
        else:            
            print('\nInvalid type.')  

    # Show user controls
    print('\n\n  +: like  -: dislike  *: favorite  b: back  s: save and quit')

    # Loop until completion or the user chooses to quit
    while True:   
        
        # Add to the list of new entries if needed
        if entryIndex >=  len(newEntries[0]):    

            while True:
                
                # Check for completion
                if sessionType == 0 and nextName >= numNames or \
                   sessionType == 1 and nextName >= numNames*2:
                    if sessionType == 0:
                        print('\nAll girl names have been completed!')
                    else:
                        print('\nAll boy names have been completed!')
                    for index in range(len(newEntries[0])):
                        ratings[userIndex][newEntries[0][index]] = newEntries[1][index]
                    saveData()
                    return
                if ratings[userIndex][nextName] != '0':
                    nextName += 1
                else:
                    break
            
            # Add the nameIndex and rating
            newEntries[0].append(nextName)            
            newEntries[1].append(ratings[userIndex][entryIndex])
        
            # Select the next name
            nextName += 1

        # Display the name to rate and accept input from the user
        if lastNameToggle == False:
            print('\n'+names[newEntries[0][entryIndex]])
        else:
            print('\n'+names[newEntries[0][entryIndex]]+' '+lastName)
        inChar = sys.stdin.readline()[0]

        # Store valid user ratings and move on
        if inChar == '+' or inChar == '-' or inChar == '*' or inChar == '0':
            newEntries[1][entryIndex] = inChar    
            entryIndex += 1

        # Toggle whether or not to display the last name
        elif inChar.lower() == 't':
            lastNameToggle = not lastNameToggle

        # Quit (but save data first)
        elif inChar.lower() == 'q':
            for index in range(len(newEntries[0])-1):
                ratings[userIndex][newEntries[0][index]] = newEntries[1][index]
            saveData()
            break

        # Save data and quit
        elif inChar.lower() == 's':                    
            for index in range(len(newEntries[0])-1):
                ratings[userIndex][newEntries[0][index]] = newEntries[1][index]
            saveData()
            #print('\nData saved.')
            break

        # Back
        elif inChar.lower() == 'b':     
            entryIndex -= 1

            # Check for wrap-around
            if entryIndex < 0:
                entryIndex = 0

        # Help
        elif inChar.lower() == 'h' or inChar == '?':            
            print('\n\n  +: like  -: dislike  *: favorite  b: back  s: save and quit')

        # Invalid input
        else:
            print('\nInvalid input.')


#######################################
##
##  View results
##
    
def viewResults():

    global users; global names; global ratings;

    both_boys = []
    both_girls = []
    fav0_boys = []
    fav0_girls = []
    fav1_boys = []
    fav1_girls = []
    printString = ''
    tabLength = 16

    # Find favorites and overlaps (girls)
    for index in range(numNames):

        # Find favorites
        if ratings[0][index] == '*':
            fav0_girls.append(names[index])

        if ratings[1][index] == '*':
            fav1_girls.append(names[index])

        # Find overlaps
        if ratings[0][index] == '+' and ratings[1][index] == '+' or \
           ratings[0][index] == '*' and ratings[1][index] == '+' or \
           ratings[0][index] == '+' and ratings[1][index] == '*' or \
           ratings[0][index] == '*' and ratings[1][index] == '*':
            both_girls.append(names[index])

    # Find favorites and overlaps (boys)
    for index in range(numNames, numNames*2):

        # Find favorites
        if ratings[0][index] == '*':
            fav0_boys.append(names[index])

        if ratings[1][index] == '*':
            fav1_boys.append(names[index])

        # Find overlaps
        if ratings[0][index] == '+' and ratings[1][index] == '+' or \
           ratings[0][index] == '*' and ratings[1][index] == '+' or \
           ratings[0][index] == '+' and ratings[1][index] == '*' or \
           ratings[0][index] == '*' and ratings[1][index] == '*':
            both_boys.append(names[index])            

    # Pad the results for formatting
    if len(both_boys) > len(both_girls):
        for i in range(len(both_boys)-len(both_girls)):
            both_girls.append('')
    elif len(both_boys) < len(both_girls):
        for i in range(len(both_girls)-len(both_boys)):
            both_boys.append('')
    if len(fav0_boys) > len(fav0_girls):
        for i in range(len(fav0_boys)-len(fav0_girls)):
            fav0_girls.append('')
    elif len(fav0_boys) < len(fav0_girls):
        for i in range(len(fav0_girls)-len(fav0_boys)):
            fav0_boys.append('')
    if len(fav1_boys) > len(fav1_girls):
        for i in range(len(fav1_boys)-len(fav1_girls)):
            fav1_girls.append('')
    elif len(fav1_boys) < len(fav1_girls):
        for i in range(len(fav1_girls)-len(fav1_boys)):
            fav1_boys.append('')
                
    # Display findings
    if len(both_boys) > 0  or len(both_girls) > 0:
        printString = 'Names liked by both ' + users[0] + ' and ' + users[1]
        print('\n\n' + printString)        
        print('-' * len(printString))
        for index in range(max(len(both_boys), len(both_girls))):
            printString = both_boys[index]
            print(printString + ' ' * (tabLength - len(printString)) + both_girls[index])
    else:
        print('\nNo names liked by both users yet!')
    
    if len(fav0_boys) > 0 or len(fav0_girls) > 0:
        printString = 'Names favorited by ' + users[0]
        print('\n\n' + printString)
        print('-' * len(printString))           
        for index in range(max(len(fav0_boys), len(fav0_girls))):
            printString = fav0_boys[index]
            print(printString + ' ' * (tabLength - len(printString)) + fav0_girls[index])

    if len(fav1_boys) > 0 or len(fav1_girls) > 0:
        printString = 'Names favorited by ' + users[1]
        print('\n\n' + printString)
        print('-' * len(printString))       
        for index in range(max(len(fav1_boys), len(fav1_girls))):
            printString = fav1_boys[index]
            print(printString + ' ' * (tabLength - len(printString)) + fav1_girls[index])


#######################################
##
##  New data
##
    
def newData():

    global users; global names; global ratings; global userIndex; global lastName

    #Reset
    users = []
    names = []
    ratings = [[],[]]
    userIndex = 0
    numNames = 0
    lastName = ''
                    
    # User information
    print('\nWelcome! What is your name?')
    users.append(sys.stdin.readline().split('\n')[0])
    
    print('\nWhat is your partner\'s name?')
    users.append(sys.stdin.readline().split('\n')[0])

    print('\nWhat will be the baby\'s last name?')
    lastName = sys.stdin.readline().split('\n')[0]

    # Load names
    print('\nWhich file has the list of names you\'d like to use?')
    namesFile = sys.stdin.readline().split('\n')[0]
    
    valid = loadNames(namesFile)
    while valid == -1:
        print('\nWe couldn\'t open that. Try including the location with the filename:')
        namesFile = sys.stdin.readline().split('\n')[0]
        valid = loadNames(namesFile)

    # Save the new data
    saveData()

    # All done
    print('\nYou\'re all set!')


#######################################
##
##  Load names
##
    
def loadNames(namesFile):

    global names; global ratings; global numLoadNames; global numNames
       
    names = []
    ratings = [[],[]]

    # Parse the file to load the names
    try:
        file_ = open(namesFile, 'r')
    except:
        return -1
    else:
        for line in file_:
            if ',F,' in line: 
                names.append(line.split(',')[0])
                if len(names) >= numLoadNames: break
        numGirls = len(names)
        
        file_.seek(0)
        for line in file_:
            if ',M,' in line: 
                names.append(line.split(',')[0])
                if len(names) >= numLoadNames*2: break
        file_.close()
        numBoys = len(names)-numGirls

    # Trim names evenly if necessary
    if numBoys != numGirls:
        if numBoys > numGirls:
            for i in range(numBoys-numGirls):
                names.pop()
        else:
            for i in range(numGirls-numBoys):
                names.remove(names[numBoys+i])

    # Set the number of names per gender and blank their ratings
    numNames = len(names)/2
    for i in range(numNames*2):
        ratings[0].append('0')
        ratings[1].append('0')              


#######################################
##
##  Load data
##
    
def loadData():

    global users; global names; global ratings
    global dataFile; global numNames; global lastName

    users = []
    names = []
    ratings = [[],[]]
    userIndex = -1
    lastName = ''
    
    try:
        file_ = open(dataFile, 'r')
    except:
        return -1
    else:
        users.append(file_.readline().split('\n')[0])
        users.append(file_.readline().split('\n')[0])
        lastName = file_.readline().split('\n')[0]
        for line in file_:
            linesplit = line.split('\n')[0].split(',')
            names.append(linesplit[0])
            ratings[0].append(linesplit[1])
            ratings[1].append(linesplit[2])
        
        file_.close()
        numNames = len(ratings[0])/2

            
#######################################
##
## Save data
##
            
def saveData():

    global users; global names; global ratings; global dataFile; global lastName

    try:
        file_ = open(dataFile, 'w')
    except:
        return -1
    else:        
        file_.write(users[0]+'\n')
        file_.write(users[1]+'\n')
        file_.write(lastName+'\n')
        for index, name in enumerate(names):
            file_.write(name+','+ratings[0][index]+','+ratings[1][index]+'\n')
        file_.close()




####################################  MAIN  ####################################

# Load user data from file
valid = loadData()

# Create new data if none available
if valid == -1:
    newData()
else:
    selectUser()

# Main menu
menu()
