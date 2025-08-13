# -*- coding: utf-8 -*-

import time
import re
from itertools import repeat
from _random import Random

Resource = ("Resource", "6eb6d990-007a-4f4d-b76c-b35685922b22")
Damage = ("Damage", "3abb22bb-b259-4857-ae8f-f2cdf93de5e0")
Clue = ("Clue", "33d9ed22-458b-4c7f-9901-5daf2fa43a23")
Horror = ("Horror", "9461c5e5-1aa8-4286-88f1-01661a8aaa02")
Doom = ("Doom", "a6605071-57d2-4e7f-b6b4-7809147a565a")
Lock = ("Lock", "62d688a4-46ef-45be-9414-2257a1221351")
Action = ("Action", "654ac64a-ff25-42dd-946f-cc15c03448cf")
Curse = ("Curse", "f59396af-8536-4a82-96d3-6cefdc849103")
Bless = ("Bless", "aad7ef0b-5806-4884-b420-c36a2d417bf7")
Flood1 = ("Floodl", "b5c9e09a-163f-4f60-9c0c-0579d1c5512e")
Flood2 = ("Floodh", "9a1ffb97-35bd-4f99-9646-f15732cb36a9")
Zero = ("Zero", "605c41ac-98f0-4475-a86d-d58847b1f19b")
CurseID = '81df3f18-e341-401d-a6bb-528940a9c39e'
BlessID = '360db0ee-c362-4bbe-9554-b1fbf101d9ab'

boost_lookup = {'Eye of Ghatanothoa': ('Willpower', [2]),'Four of Cups': ('Willpower', [1]),'Dr. Francis Morgan': (('Combat', [None])), "St. Hubert's Key": (('Willpower', [0]), ('Intellect', [0])), 'Peter Sylvestre': (('Willpower', [2]), ('Agility', [0, 2])), 'Holy Rosary': (('Willpower', [0, 2]),), 'Brother Xavier': (('Willpower', [1]),), 'Crystal Pendulum': (('Willpower', [0]),), 'Crystalline Elder Sign': (('Willpower', [3]), ('Agility', [3]), ('Combat', [3]), ('Intellect', [3])), 'The Codex of Ages': (('Willpower', None),), 'Granny Orne': (('Willpower', [0, 3]), ('Intellect', [3])), 'Plucky': (('Willpower', [3]), ('Intellect', [3])), 'Moxie': (('Willpower', [3]), ('Agility', [3])), "Alton O'Connell": (('Agility', [0]),), 'Cat Burglar': (('Agility', [1]),), 'Combat Training': (('Agility', [3]), ('Combat', [3])), 'Track Shoes': (('Agility', [0]),), 'The Moon · XVIII': (('Agility', [1]),), "Delilah O'Rourke": (('Agility', [3]), ('Combat', [3])), 'Robert Castaigne': (('Combat', [0, 4]),), 'Dr. Francis Morgan': (('Combat', [None]),), 'Lonnie Ritter': (('Combat', [0]),), 'Ace of Swords': (('Combat', [1]),), 'Beat Cop': (('Combat', [0, 2]),), 'Grete Wagner': (('Combat', [0, 3]), ('Intellect', [3])), 'Jessica Hyde': (('Combat', [1]),), 'Archibald MacVeigh': (('Intellect', [5]),), 'Lawrence Carlisle': (('Intellect', [0]),), 'Gabriel Carillo': (('Intellect', [1]),), 'Alice Luxley': (('Intellect', [0, 2]),), 'Alyssa Graham': (('Intellect', [0]),), 'Death XIII': (('Intellect', [1]),), 'Dr. Milan Christopher': (('Intellect', [0]),), 'Field Agent': (('Intellect', [2]),)}

BoardWidth = 1100
Spacing = 92
InvestigatorSpacing = 10
InvestigatorY = 175
StagingStart = -515
StagingWidth = 619
StagingY = -222
StagingSpace = 82
AgendaX = 221
AgendaY = -222
ActX = 309
ActY = -222
Act31X = 117
Act31Y = -128
Act32X = 221
Act32Y = -128
Act33X = 325
Act33Y = -128
Act41X = 88
Act41Y = -135
Act42X = 188
Act42Y = -123
Act43X = 288
Act43Y = -123
Act44X = 388
Act44Y = -135
EncounterX = 147
EncounterY = -234.75
Encounter2X = 147
Encounter2Y = -135
ScenarioX = 408.5
ScenarioY = -234.75
CampaignX = 500
CampaignY = -234.75
ChaosTokenX = 94
ChaosTokenY = -211
ChaosBagX = 0
ChaosBagY = -234.75

TarotWidth = 69

DoneColour = "#D8D8D8" # Grey
WaitingColour = "#FACC2E" # Orange
ActiveColour = "#82FA58" # Green
EliminatedColour = "#FF0000" # Red
BlueColour = "#0C0CAD"
OrangeColour = "#D68F00"
GreenColour = "#046C06"
PurpleColour = "#3B0A9D"
RedColour = "#B80404"
BlackColour = "#000000"
WhiteColour = "#FFFFFF"

TarotDeck = None

showDebug = False #Can be changed to turn on debug - we don't care about the value on game reconnect so it is safe to use a python global

def debug(str):
    if showDebug:
        whisper(str)

def toggleDebug(group, x=0, y=0):
    global showDebug
    showDebug = not showDebug
    if showDebug:
        notify("{} turns on debug".format(me))
    else:
        notify("{} turns off debug".format(me))


def phasePassed(args):
    mute()
    thisPhase = currentPhase()
    newPhase = thisPhase[1]
   
    if newPhase == 1:
        phase = "Myth"
        if turnNumber() != 1 and getGlobalVariable("allowMythosPhase") == "True":
            doMythosPhase(False)
            setGlobalVariable("allowMythosPhase", "False")
    elif newPhase == 2:
        # Investigation Phase
        phase = "Investigation"
        mute()
        doInvestigationPhase()
    elif newPhase == 3:
        # Enemy
        phase = "Enemy"
        mute()
        doEnemyPhase()
    elif newPhase == 4 and getGlobalVariable("allowUpkeepPhase") == "True":
        # Upkeep
        phase = "Upkeep"
        remoteCall(me, "doUpkeepPhase", [False])
        setGlobalVariable("allowUpkeepPhase", "False")
        
    saveTable(phase)

def turnPassed(args):

    setGlobalVariable("allowMythosPhase", "True")
    setGlobalVariable("allowUpkeepPhase", "True")
    
    
    if turnNumber() == 1:
        setPhase(2)
    else:
        setPhase(1)
    

def advancePhase(group = None, x = 0, y = 0):
    if turnNumber() == 0:
        me.setActive()
        for c in table:
            if InvestigatorName(c.owner) == "Norman Withers":
                if not c.owner.deck.top().isFaceUp:
                    flipcard(c.owner.deck.top())
                    if c.owner.deck.top().Name == "The Harbinger":
                        if not deckLocked(c.owner):
                            toggleLock(c.owner.deck)
                break
    else:
        thisPhase = currentPhase()
        nextPhase = thisPhase[1] + 1
        if nextPhase > 4:
            me.setActive()
        else:
            setPhase(nextPhase)

        
#Return the default x coordinate of the players investigator
def investigatorX(player):
    return (BoardWidth * player / len(getPlayers())) - (BoardWidth / 2)

def num(s):
   if not s: return 0
   try:
      return int(s)
   except ValueError:
      return 0

def moveCard(model, x, y):
    for c in table:
        if c.model == model:
            c.moveToTable(x, y)
            return c
    return table.create(model, x, y)

#Find and return this players left most hero card
def firstInvestigator(player):
    first = None
    for h in table:
        if h.owner == player and h.Type == "Investigator" and h.isFaceUp:
            if first is None:
                first = h
            else:
                x,y = h.position
                minx, miny = first.position
                if x < minx:
                    first = h
    return first

def getPlayer(id):
    for p in getPlayers():
        if playerID(p) == id:
            return p
    return None

def countInvestigators():
    investigators = 0
    for card in table:
        if card.Type == "Investigator":
            investigators += 1
    return investigators

#Work out if the player is still in the game (threat < 50 and has heroes on the table)
def inGame(p):
    for card in table:
        if card.Type == "Mini" and card.owner == p:
            return True

def cardDoubleClicked(args):
    # args = card, mouseButton, keysDown
    mute()
    card = args.card
    if hasattr(card, 'Type'):
        if card.Type == "Chaos Bag": # Draw Chaos Token
            drawChaosTokenForPlayer(me, [])
        elif card.Type == "Chaos Token": # Discard Chaos Token
            if card.controller == me:
                doDiscard(me, card, chaosBag())
            else:
                remoteCall(card.controller, "doDiscard", [me, card, chaosBag()])
        elif card.Type == "Encounter Draw": # Draw Encounter Card
            addEncounter(table)
        elif card.Type == "Encounter2 Draw":
            if card.Subtype == "Special":
                nextEncounter2(specialDeck(), False)
            elif card.Subtype == "Location":
                nextEncounter2(locationDeck(), False)
        elif card.Type == "nextAgenda":
            nextAgendaStage()
        elif card.Type == "nextAct":
            nextActStage()
        elif card.Type == "Path" or card.Type == "Tarot": # Rotate Path cards
            rotateRight(card)

def activePlayers():
    count=0
    for p in getPlayers():
        count+=1
#       if not eliminated(p):
#           count+=1
    return count

def agendaCount(group):
    count = 0
    for c in group:
        if c.Type == "Agenda":
            count += 1
    return (count)

def actCount(group):
    count = 0
    for c in group:
        if c.Type == "Act":
            count += 1
    return (count)

#Check see if a card at x1,y1 overlaps a card at x2,y2
def overlaps(x1, y1, x2, y2, w1, h1, w2 = 0, h2 = 0):
    # if no width/height specified for card 2, assumed card 2 has the same dimensions as card 1
    if w2 == 0:
        w2 = w1
    if h2 == 0:
        h2 = h1
    #Four checks, one for each corner
    if int(x1) >= int(x2) and int(x1) <= int(x2) + int(w2) and int(y1) >= int(y2) and int(y1) <= int(y2) + int(h2): return True
    if int(x1) + int(w1) >= int(x2) and int(x1) <= int(x2) and int(y1) >= int(y2) and int(y1) <= int(y2) + int(h2): return True
    if int(x1) >= int(x2) and int(x1) <= int(x2) + int(w2) and int(y1) + int(h1) >= int(y2) and int(y1) <= int(y2): return True
    if int(x1) + int(w1) >= int(x2) and int(x1) <= int(x2) and int(y1) + int(h1) >= int(y2) and int(y1) <= int(y2): return True
    return False

def cardoverlaps(card1,card2):
    x1,y1 = card1.position
    x2,y2 = card2.position
    w1 = card1.width
    h1 = card1.height
    if overlaps(x1,y1,x2,y2,w1,h1):
        if (x1,y1) == (x2,y2):
            return False
        else: return True
    return False

def overlapPartialCard(x, y):
    cw = 0
    ch = 0
    for c in table:
        cx, cy = c.position
        if overlaps(x, y, cx, cy, cw, ch):
            return c
    return None

# check if the card with specified dimension being inserted at
# position x, y overlaps with any existing card
def overlapCard(x, y, width, height, ignoreChaosToken = True):
    for existingCard in table:
        if overlaps(x, y, cardX(existingCard), cardY(existingCard), width, height, existingCard.width, existingCard.height):
            if not ignoreChaosToken:
                return existingCard
            elif existingCard.Type != 'Chaos Token':
                return existingCard

    return None

def cardX(card):
    x, y = card.position
    return x

def cardY(card):
    x, y = card.position
    return y

#Move the given card in the staging area to the first available space on the left of the Staging Area
#If there is no room then we compress all the cards in the staging area to make room
def layoutStage(card):
    x = StagingStart
    y = StagingY
    s = StagingSpace
    while x < StagingStart + StagingWidth - s:
        if overlapCard(x, y, cardX(card), cardY(card)) is None:
            card.moveToTable(x, y)
            return
        x += s
    card.moveToTable(x - s, y)
    #There was no room - we neeed to move all the cards to make space
    staged = []
    for c in table:
        if c.Type != 'Chaos Token' and overlaps(cardX(c), cardY(c), StagingStart, StagingY, StagingWidth, 100):
            staged.append(c)

    for c in staged:
        cx, cy = c.position
        shift = (cx - StagingStart) // len(staged)
        c.moveToTable(cx - shift, cy)

def clearTargets(group=table, x=0, y=0):
    for c in group:
        if c.controller == me or (c.targetedBy is not None and c.targetedBy == me):
            c.target(False)
    #notify("x={} y={}".format(str(x), str(y)))

def findCard(group, model):
    for c in group:
        if c.model == model:
            return c
    return None

def encounterDeck():
    return shared.piles['Encounter']

def encounterDiscard():
    return shared.piles['Encounter Discard Pile']

def specialDeck():
    return shared.piles['Special']

def specialDiscard():
    return shared.piles['Special Discard Pile']

def secondspecialDeck():
    return shared.piles['2nd Special']

def secondspecialDiscard():
    return shared.piles['2nd Special Discard Pile']

def agendaDeck():
    return shared.piles['Agenda']

def agendaDiscard():
    return shared.piles['Agenda Discard Pile']

def actDeck():
    return shared.piles['Act']

def actDiscard():
    return shared.piles['Act Discard Pile']

def locationDeck():
    return shared.piles['Location']

def locationDiscard():
    return shared.piles['Location Discard Pile']

def chaosBag():
    return shared.piles['Chaos Bag']

def setupDeck():
    return shared.piles['Setup']

def isPlayerCard(card):
    return ((card.Subtype in ["Weakness", "Basic Weakness"]) or (card.Type in ["Asset","Event","Skill","Mini","Investigator"])) and card.Class != "Mythos"

def isLocationCard(card):
    return card.Type == 'Location' and card.Traits != "Otherworld. Extradimensional."

def isChaosToken(card):
    return card.Type == 'Chaos Token'

def isEncounterCard(card):
	return ((card.Type == 'Enemy' or card.Type == 'Treachery') and card.Subtype not in ["Weakness", "Basic Weakness"])

def isPath(card):
    return card.Type == 'Path'

def isConcealed(card):
    return card.Type == "Mini" and card.alternateProperty("", "Name") == "Concealed Card"
    
#------------------------------------------------------------
# Global variable manipulations function
#------------------------------------------------------------

def getLock():
    lock = getGlobalVariable("lock")
    if lock == str(me._id):
        return True

    if len(lock) > 0: #Someone else has the lock
        return False

    setGlobalVariable("lock", str(me._id))
    if len(getPlayers()) > 1:
        update()
    return getGlobalVariable("lock") == str(me._id)

def clearLock():
    lock = getGlobalVariable("lock")
    if lock == str(me._id):
        setGlobalVariable("lock", "")
        update()
        return True
    debug("{} id {} failed to clear lock id {}".format(me, me._id, lock))
    return False


#Store this player's starting position (his ID for this game)
#The first player is 0, the second 1 ....
#These routines set global variables so should be called within getLock() and clearLock()
#After a reset, the game count will be updated by the first player to setup again which invalidates all current IDs
def myID():
    if me.getGlobalVariable("game") == getGlobalVariable("game") and len(me.getGlobalVariable("playerID")) > 0:
        return playerID(me) # We already have a valid ID for this game
        
    g = getGlobalVariable("playersSetup")
    if len(g) == 0:
        id = 0
    else:
        id = num(g)
    me.setGlobalVariable("playerID", str(id))
    game = getGlobalVariable("game")
    me.setGlobalVariable("game", game)
    setGlobalVariable("playersSetup", str(id+1))
    update()
    debug("Player {} sits in position {} for game {}".format(me, id, game))
    return id

def playerID(p):    
    return num(p.getGlobalVariable("playerID"))

#In phase management this represents the player highlighted in green
def setActivePlayer(p):
   if p is None:
       setGlobalVariable("activePlayer", "-1")
   else:
       setGlobalVariable("activePlayer", str(playerID(p)))
   update()

def setPlayerDone():
    done = getGlobalVariable("done")
    if done:
        playersDone = eval(done)
    else:
        playersDone = set()
    playersDone.add(me._id)
    setGlobalVariable("done", str(playersDone))
    #notify("done {}".format(str(playersDone)))
    update()

def deckLocked(player):
    return player.getGlobalVariable("deckLocked") == "1"

def lockDeck():
    me.setGlobalVariable("deckLocked", "1")
    
def unlockDeck():
    me.setGlobalVariable("deckLocked", "0")
        
#---------------------------------------------------------------------------
# Workflow routines
#---------------------------------------------------------------------------

#Triggered event OnGameStart
def startOfGame():
    global HunchCard, AmandaCard 
    HunchCard = None
    AmandaCard = None
    unlockDeck()
    setActivePlayer(None)   
    if me._id == 1:
        setGlobalVariable("playersSetup", "")       
        setGlobalVariable("game", str(num(getGlobalVariable("game"))+1))
        notify("Starting Game {}".format(getGlobalVariable("game")))

    #---------------------------------------------------------------------------
    # NEW
    #---------------------------------------------------------------------------
    setGlobalVariable("currentPlayers",str([]))

def release(args):
    global attached
    mute()
    if isinstance(args.fromGroups[0],Table) and isinstance(args.toGroups[0],Pile):
        if len(args.cards) == 1:
            card = args.cards[0]
            marker = eval(args.markers[0])
            if card.owner == me:
                if Bless in marker:
                    for _ in range(marker[Bless]):
                        addBless()
                elif Curse in marker:
                    for _ in range(marker[Curse]):
                        addCurse()
                elif Zero in marker:
                    for _ in range(marker[Zero]):
                        chaosBag().create('35137ccc-db2b-4fdd-b0a8-a5d91f453a43', quantity = 1)
                    notify("{} releases {} 0 tokens.".format(card.owner, marker[Zero]))
                if card._id in attached: # if card is a host card, deletes all dict entries
                    del(attached[card._id])
                elif isAttached(card._id): # if it is attached
                    detachCard(card)

def setUpgrades(card, x=0, y=0):
    mute()
    bondedUpgrade = [c for c in card.owner.piles['Sideboard'] if c.Name == card.Name and c.Type == "Upgrades"]
    if bondedUpgrade:
        upgrade = bondedUpgrade[0]
        match = re.findall(r'□+\s(.*?)\.\s(.*?)\.(?:&#10;)?', upgrade.Text)
        choice_list = []
        color_list = []
        for m in match:
            choice_list.append(str(m[0]))
            color_list.append(InvestigatorColor(card.owner))
        choice_list.append("Done")
        color_list.append("#999999")
        while True:
            choice = askChoice("Choose upgrades", choice_list, color_list)
            if choice != 0 and choice != len(choice_list):
                choice_list.pop(choice -1)
                color_list.pop(choice -1)
                card.properties["Name"] = card.properties["Name"] + "&#10;" + match[choice - 1][1]
                notify("{} {}".format(match[choice - 1][1], card.properties["Name"]))
            else:
                break


def normanDeck(args):
    mute()
    card = args.cards[0] # card being moved
    if InvestigatorName(me) == "Norman Withers" and turnNumber() > 0 and card.owner == me: # if card being moved belongs to Norman's player
        if card.Name == "The Harbinger":
            if args.fromGroups[0] == card.owner.deck and card.owner.getGlobalVariable("deckLocked") == "1": # Unlocks the deck if HB leaves it for any reason
                toggleLock(card.owner.deck)
        if args.fromGroups[0] == card.owner.deck or args.toGroups[0] == card.owner.deck:
            if not(len(card.owner.deck)):
                return
            if len(card.owner.deck) >= 2:
                if card.owner.deck[1].isFaceUp: # checks if second top is face up and turns it down if so
                   card.owner.deck[1].isFaceup = False
            if not card.owner.deck.top().isFaceUp: # Flips first card of the deck faceup
                card.owner.deck.top().isFaceUp = True
            if card.owner.deck.top().Name == "The Harbinger": # Locks deck if it is the Harbinger
                if card.owner.getGlobalVariable("deckLocked") == "0":
                    toggleLock(card.owner.deck)

def autoClues(args):
    mute()
    #Only for move card from Pile to Table
    if isinstance(args.fromGroups[0],Pile) and isinstance(args.toGroups[0],Table):
        if len(args.cards) == 1:
            card = args.cards[0]
            if card.controller == me and card.properties["Type"] == "Location":
                loadClues(card) 

def autoCharges(args):
    mute()
    #Only for move card from Pile to Table
    if isinstance(args.fromGroups[0],Pile) and isinstance(args.toGroups[0],Table):
        if len(args.cards) == 1:
            card = args.cards[0]
            if card.owner == me and card.isFaceUp and card.Type in ["Asset","Event"]:
                autocharges = re.search(r'[Uu]ses\s\((\d+|X)\s(\w+)\)',card.Text)
                if autocharges:
                    if autocharges.group(1).isnumeric():
                        charges = int(autocharges.group(1))
                        text = autocharges.group(2)
                        if text == "charges" and InvestigatorName(card.owner) == "Akachi Onyele":
                            charges += 1
                        if charges > 1 and text[-1] != "s":
                            text += "s"
                        notify("{} adds {} {} to {}".format(card.owner, charges, text, card))
                        card.markers[Resource] = charges
                    else: print("Sorry, no automation for X")

#Triggered event OnLoadDeck
# args: player, cards, fromGroups, toGroups, indexs, xs, ys, highlights, markers, faceups, filters, alternates
def moveCards(args):
    mute()
    autoCharges(args)
    autoClues(args)
    normanDeck(args)
    release(args)
    moveCardsSound(args) 
#Triggered event OnLoadDeck
# args: player, groups
def deckLoaded(args):
    mute()
    if args.player != me:
        return
    
    isShared = False
    isPlayer = False
    for g in args.groups:
        if (g.name == 'Hand') or (g.name in me.piles):
            isPlayer = True
        elif g.name in shared.piles:
            isShared = True
    
    #If we are loading into the shared piles we need to become the controller of all the shared piles   
    if isShared:
        notify("{} Takes control of the encounter deck".format(me))
        for p in shared.piles:
            if shared.piles[p].controller != me:
                shared.piles[p].controller = me
        update()
    #Cards for the encounter deck and player deck are loaded into the discard pile because this has visibility="all"    
    #Check for cards with a Setup effects and move other cards back into the correct pile
    for pile in args.groups:
        for card in pile:
            if card.Setup == 't' and card.Type not in [ 'Agenda' , 'Act', 'Scenario' ]:
                addToTable(card)
            elif card.Setup == 's' and card.Type not in [ 'Agenda' , 'Act', 'Scenario' ]:
                addToStagingArea(card)
            elif pile == shared.piles['Encounter Discard Pile']:
                card.moveTo(shared.piles['Encounter'])
            elif pile == me.piles['Discard Pile']:
                card.moveTo(me.deck)
        if pile.name == "Chaos Bag":
            createChaosBag(table)
        elif pile.name == "Encounter Discard Pile":
            createEncounterCardClicky(table)

    if isShared:
        deckSetup()
    update()
    playerSetup(table, 0, 0, isPlayer, isShared)
    if not isPlayer:
        for cardT in table:
            loadClues(cardT)
    #if automate():         <-----Turning off Automation by default for ScriptVersion updates, but still want playerSetup to run
    #   playerSetup(table, 0, 0, isPlayer, isShared)

def loadBasicWeaknesses(group, x = 0, y = 0):
    basic_weakness_pile = me.piles[BasicWeakness.PILE_NAME]
    if len(basic_weakness_pile) == 0:
        choice_list = ['all', 'core']
        color_list = ['#0000FF', '#00FF00']
        sets = askChoice("Which sets to load?", choice_list, color_list)
        # load all sets if window is closed
        if sets == 0:
            sets = 1
        bw = BasicWeakness(me, choice_list[sets - 1])
        bw.create_deck()
        basic_weakness_pile.shuffle()
        notify("{} loaded Basic Weakness Deck".format(me))
    else:
        notify("{}'s Basic Weakness Deck already loaded.".format(me))

# #Triggered event OnPlayerGlobalVariableChanged
# #We use this to manage turn and phase management by tracking changes to the player "done" variable            
def globalChanged(args):
    debug("globalChanged(Variable {}, from {}, to {})".format(args.name, args.oldValue, args.value))
    if args.name == "done":
        checkPlayersDone()
    elif args.name == "phase":
        notify("Phase: {}".format(args.value))
        
# calculate the number of plays that are Done
def numDone():
    done = getGlobalVariable("done")
    if done:
        return len(eval(done))
    else:
        return 0
    
def highlightPlayer(p, state):
    if len(getPlayers()) <= 1:
        return
    debug("highlightPlayer {} = {}".format(p, state))
    for card in table:
        if card.Type == "Investigator" and card.controller == p and card.isFaceUp:
            card.highlight = state

#Called when the "done" global variable is changed by one of the players
#We use this check to see if all players are ready to advance to the next phase 
#Note - all players get called whenever any player changes state. To ensure we don't all do the same thing multiple times
#       only the Encounter player is allowed to change the phase or step and only the player triggering the event is allowed to change the highlights   
def checkPlayersDone():
    mute()
    if not turnManagement():
        return

    #notify("done updated: {} {}".format(numDone(), len(getPlayers())))
    if numDone() == len(getPlayers()):
        doUpkeepPhase()
        doMythosPhase()
        setGlobalVariable("phase", "Investigator")
        setGlobalVariable("done", str(set()))

#---------------------------------------------------------------------------
# Table menu options
#---------------------------------------------------------------------------
def isLocation(cards):
    for c in cards:
        if c.Type != 'Location':
            return False
    return True
    
def isEnemy(cards):
    for c in cards:
        if c.isFaceUp and (c.type != "Enemy" or c.orientation == Rot90):
            return False
    return True
    
#---------------------------------------------------------------------------
# Table group actions
#---------------------------------------------------------------------------

def turnManagementOn(group, x=0, y=0):
    mute()
    setGlobalVariable("Automation", "Turn") 
    
def automationOff(group, x = 0, y = 0):
    mute()
    setGlobalVariable("Automation", "Off")
    notify("{} disables all turn management".format(me))
    
def turnManagement():
    mute()
    auto = getGlobalVariable("Automation")
    return auto == "Turn" or len(auto) == 0

def createChaosBag(group, x=0, y=0):
    for c in group:
        if c.owner == me and c.model == "faa82643-1dda-4af7-96ad-298bc2d5b2dd":
            c.moveToTable(x, y)
            return
    group.create("faa82643-1dda-4af7-96ad-298bc2d5b2dd", ChaosBagX, ChaosBagY, 1, False)
    for c in table:
        if c.name == "Sister Mary" and c.Type == "Investigator":
            for _ in range(2):
                addBless()
            break

def createEncounterCardClicky(group, x=0, y=0):
    group.create("f4633a2e-0102-452d-8387-678b5aa17878", EncounterX, EncounterY, 1, False)

def createEncounter2CardClicky(pile, alt):
    card = table.create("f4633a2e-0102-452d-8387-678b5aa17878", Encounter2X, Encounter2Y, 1, False)
    card.alternate = alt
    card.Subtype = pile

def createActCardClicky(x, y):
    table.create("94f90b4e-5dd7-47cd-9d9b-afba493c6a81", x, y, 1, False)

def createAgendaCardClicky(x, y):
    card = table.create("d16e42c3-06a0-4721-b13b-d1fa6bf02a4e", x, y, 1, False)
    return card

def flipCoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
        notify("{} flips heads.".format(me))
    else:
        notify("{} flips tails.".format(me))

def randomPlayer(group, x=0, y=0):
    mute()
    players = getPlayers()
    if len(players) <= 1:
        notify("{} randomly selects {}".format(me, me))
    else:
        n = rnd(0, len(players)-1)
        notify("{} randomly selects {}".format(me, players[n]))

def randomAsset(group, x=0, y=0):
    mute()
    randomCard(table, "Asset")

def randomHero(group, x=0, y=0):
    mute()
    randomCard(table, "Investigator")
    
def randomCard(group, type):
    n = 0
    for card in group:
        if card.controller == me and card.Type == type:
            n = n + 1
    if n == 0:
        whisper("You have no cards of that type")
    else:
        c = rnd(1, n)
        n = 0
        for card in group:
            if card.controller == me and card.Type == type:
                n = n + 1
                if n == c:
                    notify("{} randomly selects {}".format(me, card))
                    card.select()

def randomNumber(group, x=0, y=0):
    mute()
    max = askInteger("Random number range (1 to ....)", 6)
    if max == None: return
    notify("{} randomly selects {} (1 to {})".format(me, rnd(1,max), max))

def readyForRefresh(group, x = 0, y = 0):
    mute()
    if turnManagement():
        highlightPlayer(me, WaitingColour)
    doRestoreAll()
    
def doRestoreAll(group=table): 
    mute()
        
    debug("doRestoreAll({})".format(group)) 
    myCards = (card for card in group
                if card.controller == me)
    for card in myCards:
        if not isLocked(card) and not card.anchor and not (card.markers[Action] and card.Type == "Enemy"):
            card.orientation &= ~Rot90
        if card.markers[Action] and card.Type == "Enemy": # Place a marker on an enemy to enable "does not ready during the next upkeep phase"
            card.markers[Action] = 0
            notify("{} does not ready this upkeep phase".format(card))
    notify("{} readies all their cards.".format(me))

def resetEncounterDeck(group):
    if group == specialDeck():
        discard = specialDiscard()
    else:
        discard = encounterDiscard()
    if len(discard) == 0: return
    for c in discard:
        c.moveTo(group)
    notify("{} moves all cards from {} to {}".format(me, discard.name, group.name))
    shuffle(group)

def addHidden(group=None, x=0, y=0):
    nextEncounter(encounterDeck(), x, y, True)

def addHiddenSpecial(group, x=0, y=0):
    nextEncounter(specialDeck(), x, y, True)
    
def addEncounter(group=None, x=0, y=0):
    nextEncounter(encounterDeck(), x, y, False)
    
def addEncounterSpecial(group=None, x=0, y=0):
    nextEncounter(specialDeck(), x, y, False)

def addLocation(group=None, x=0, y=0):
    nextLocation(locationDeck(), x, y)

def addToStagingArea(card, facedown=False, who=me):
    #Check to see if there is already an encounter card here.
    #If so shuffle it left to make room
    ex = StagingStart + StagingWidth - card.width
    ey = StagingY
    move = overlapCard(ex, ey, card.width, card.height)
    while move is not None:
        layoutStage(move)
        move = overlapCard(ex, ey, card.width, card.height)
    card.moveToTable(ex, ey, facedown)          
    layoutStage(card)
    notify("{} adds '{}' to the staging area.".format(who, card))
    
def nextEncounter(group, x, y, facedown, who=me):
    mute()
    if group.controller != me:
        remoteCall(group.controller, "nextEncounter", [group, x, y, facedown, me])
        return

    if len(group) == 0:
        if 1 == askChoice("Reshuffle the encounter discard pile into the encounter deck ?", ["Yes","No"],["#000000","#000000"]):
            resetEncounterDeck(group)
    if len(group) == 0: # No cards
        return

    clearTargets()
    card = group.top()
    if " Hidden." in card.Text: # Checks if card drawn has the Hidden keyword
        Hidden = True
    else: Hidden = False
    if x == 0 and y == 0:  #Move to default position in the staging area 
        if not Hidden:
            card.moveToTable(EncounterX, EncounterY, facedown)
            notify("{} places '{}' on the table.".format(who, card))  
        else: # move the card facedown on the table
            card.moveToTable(EncounterX, EncounterY, True)
            notify("{} places a Hidden card on the table.".format(who))  
    else:
        if not Hidden:
            card.moveToTable(x, y, facedown)
            notify("{} places '{}' on the table.".format(who, card))
        else:
            card.moveToTable(x, y, True)
            notify("{} places a Hidden card on the table.".format(who))
    card.controller = who

    if len(group) == 0:
        if campaignName() == "Return to the Circle Undone" or campaignName() == "The Circle Undone" or campaignName() == "For the Greater Good" or campaignName() == "The Secret Name" or campaignName() == "The Wages of Sin" or campaignName() == "Union and Disillusion" or campaignName() == "In the Clutches of Chaos" or campaignName() == "Before the Black Throne":
            for i in range(0, len(getPlayers())):
                remoteCall(getPlayers()[i], "notifyBar", ["#dd3737", "{} is empty !".format(group.name)]) # Warns players if the encounter deck is empty

    revealEncounterSound(card)

def nextEncounter2(group, facedown, who=me):
    mute()

    if group.controller != me:
        remoteCall(group.controller, "nextEncounter2", [group, facedown, who])
        return

    if len(group) == 0:
        for i in range(0, len(getPlayers())):
            remoteCall(getPlayers()[i], "notifyBar", ["#dd3737", "{} is empty and is reshuffled !".format(group.name)])
        resetEncounterDeck(group)
    if len(group) == 0: # No cards
        return

    clearTargets()
    card = group.top()

    card.moveToTable(Encounter2X, Encounter2Y, facedown)
    notify("{} places '{}' on the table.".format(who, card))

    card.controller = who

def nextLocation(group, x, y, who=me):
    mute()

    if group.controller != me:
        remoteCall(group.controller, "nextLocation", [group, x, y, me])
        return

    if len(group) == 0:
        notify("No more location cards")
        return

    card = group.top()
    if x == 0 and y == 0:  #Move to default position in the staging area
        addToStagingArea(card, False, who)
    else:
        card.moveToTable(x-card.width()/2, y-card.height()/2, facedown)
        notify("{} places '{}' on the table.".format(who, card))
    card.controller = who
    
def nextAgendaStage(group=None, x=0, y=0):
    mute()
    
    #We need a new Agenda card
    if group is None or group == table:
        group = agendaDeck()
    if len(group) == 0: return
    
    if group.controller != me:
        remoteCall(group.controller, "nextAgendaStage", [group, x, y])
        return
        
    if x == 0 and y == 0: #The keyboard shortcut was used
        x = AgendaX
        y = AgendaY
            
    card = group.top()
    card.moveToTable(x, y)
    
    #agendaSetup(card)
    notify("{} advances agenda to '{}'".format(me, card))
	
def addToTable(card):
    x = AgendaX - 45.5
    y = -40
    blocked = overlapPartialCard(x, y)
    while blocked is not None:
        x += 16
        blocked = overlapPartialCard(x, y)
    card.moveToTable(x, y)  
    
def deckSetup():
    if len(setupDeck()) > 0:
        setupHelper()
        for c in setupDeck():
            if c.Type == "Scenario":
                c.moveToTable(ScenarioX, ScenarioY)
                changeGameBoard(c.model)
            elif c.Type == "Campaign":
                c.moveToTable(CampaignX, CampaignY)
            else:
                addToTable(c)

def nextAgenda(group = None, x = 0, y = 0):
    nextAgendaStage(group, x, y)

def nextActStage(group=None, x=0, y=0):
    mute()
    
    #If the current Act card has side A showing it is simply flipped and we are done
    if getGlobalVariable("multiActAgenda") == "Default":
        for c in table:
            if c.Type in ("Act") and c.alternates is not None and "B" in c.alternates and c.alternate != "B":
                flipcard(c)
                return
    
    #We need a new Act card
    if group is None or group == table:
        group = actDeck()
    if len(group) == 0: return
    
    if group.controller != me:
        remoteCall(group.controller, "nextActStage", [group, x, y])
        return
        
    if x == 0 and y == 0: #The keyboard shortcut was used
        x = ActX
        y = ActY

    gV = getGlobalVariable("multiActAgenda")
    if gV == "3Act":
        card = nextAct3()
    elif gV == "4Act":
        card = nextAct4()
    else:
        card = group.top()
        card.moveToTable(x, y)
    
#   actSetup(card)
    notify("{} advances act to '{}'".format(me, card))

def nextAct(group = None, x = 0, y = 0):
    nextActStage(group, x, y)

def setAbilityCounters(investigatorCard):
    me.counters['Willpower'].value = num(investigatorCard.Willpower)
    me.counters['Intellect'].value = num(investigatorCard.Intellect)
    me.counters['Combat'].value = num(investigatorCard.Combat)
    me.counters['Agility'].value = num(investigatorCard.Agility)
    me.counters['Maximum Hand Size'].value = num("8")
    
    
def readyForNextRound(group=table, x=0, y=0):
    mute()
    #notify("readyForNextRound {}".format(turnManagement()))
    if turnManagement():
        highlightPlayer(me, DoneColour)
        setPlayerDone()

def playerSetup(group=table, x=0, y=0, doPlayer=True, doEncounter=False):
    Hank = False
    mute()
    if not getLock():
        whisper("Others players are setting up, please try manual setup again")
        return
        
    unlockDeck()
    if doPlayer:
        id = myID() # This ensures we have a unique ID based on our position in the setup order
        investigatorCount = countInvestigators()
        
        # Find any Permanent cards
        permanents = filter(lambda card: "Permanent" in card.Keywords or "Permanent." in card.Text or "Key" in card.Subtype, me.deck)
        # Check if Stick to the Plan or Ancestral Knowledge is in the deck
        sttp = next((c for c in me.deck if c.Name == "Stick to the Plan"), None)
        bewitching = next((c for c in me.deck if c.Name == "Bewitching"), None)
        shortSupply = next((c for c in me.deck if c.Name == "Short Supply"), None)
        ancestralKnowledge = next((c for c in me.deck if c.Name == "Ancestral Knowledge"), None)
        underworldMarket = next((c for c in me.deck if c.Name == "Underworld Market"), None)
        haveForcedLearning = next((c for c in me.deck if c.Name == "Forced Learning"), None)
        if haveForcedLearning:
            me.counters['Card Draw'].value = 2
        isJenny = next((c for c in me.hand if c.Name == "Jenny Barnes"), None)
        if isJenny:
            me.counters['Ressource per upkeep'].value = 2
        isMary = next((c for c in me.hand if c.Name == "Sister Mary"), None)
        if isMary:
            if len(chaosBag()):
                for _ in range(2):
                    addBless()
        # Find any Start cards
        startCard = filter(lambda card: "Sophie" == card.Name or "Gate Box" == card.Name or "Duke" == card.Name or "Dark Insight" == card.Name or "Darrell's Kodak" == card.Name or "Flux Stabilizer" == card.Name, me.deck)
        # Create Bonded Card
        listB = makeListBonded(me.deck)
        if not listB:
            me.piles['Sideboard'].collapsed = True
        else:
            for card in listB:
                me.piles['Sideboard'].create(card)
	
        # Move Investigators to the table
        newInvestigator = False
        investigator = filter(lambda card: card.Type == "Investigator", me.hand)
        if len(investigator) == 2: # Hank
            Hank = True
        mini = filter(lambda card: card.Type == "Mini", me.hand)
        miniX = 0
        miniWidth = 0
        if investigator and (mini or Hank):
            if Hank: # Hank
                hank2 = filter(lambda card: card.Type == "Investigator" and card.Name == "Hank Samson" and "Resolute." in card.Traits, me.hand)
                hank2[0].delete()
            investigatorCount += 1
            newInvestigator = True
            investigatorCard = investigator[0]
            setAbilityCounters(investigatorCard)
            if not Hank:
                miniCard = mini[0]
            elif Hank:
                miniCard = me.hand.create("4f2a5f9b-8888-43df-ba0f-380d531e7cba")
            investigatorCard.moveToTable(investigatorX(id), InvestigatorY)
            if Hank:
                me.piles['Sideboard'].create("0b47ec14-d252-4692-9d78-90efd034ff8c")
            miniX = cardX(investigatorCard) + investigatorCard.width + InvestigatorSpacing
            miniCard.moveToTable(miniX, cardY(investigatorCard))
            miniWidth = miniCard.width
            notify("{} places his Investigator on the table".format(me))
        
        # Move any Permanents found to the table
        permX = miniX + miniWidth + InvestigatorSpacing
        for card in permanents:
            card.moveToTable(permX, cardY(investigatorCard))
            permX = permX + card.width + InvestigatorSpacing
            notify("{} places the Permanent card {} on the table".format(me, card))
	# Move startCard found to the table
        for card in startCard:
            if card.Name == "Dark Insight":
                card.moveTo(me.hand)
                DarkInsight = True
            else:
                card.moveToTable(permX, cardY(investigatorCard))
                permX = permX + card.width + InvestigatorSpacing
                notify("{} places the start card {} on the table".format(me, card))
        
        if newInvestigator:
            if len(me.hand) == 0 or DarkInsight: 
                if sttp: 
                    whisper("Stick to the Plan available")
                    sttp.highlight = WhiteColour
                if ancestralKnowledge:
                    whisper("Ancestral Knowledge available")
                    ancestralKnowledge.highlight = WhiteColour
                if bewitching:
                    whisper("Bewitching available")
                    betwitching.highlight = WhiteColour
                if shortSupply:
                    shortSupply.highlight = WhiteColour
                if not (sttp or ancestralKnowledge or underworldMarket or bewitching): #Only draws opening hand if no Stick to the Plan or Ancestral Knowledge available
                    drawOpeningHand(me)
                    
            # Check for starting resources modifiers
            startingResource = 5
            for card in permanents:
                if card.Name == "Another Day, Another Dollar":
                    startingResource += 2
                    whisper("You start the game with 2 additional resources")
                if card.Name == "Indebted":
                    startingResource -= 2
                    whisper("You start the game with 2 less resources")
                if card.Name == "Arcane Research":
                    addHorror(Investigator(card.owner))
            for i in repeat(None, startingResource):
                addResource(investigatorCard)
        
        
    # If we loaded the encounter deck - add the first Agenda & Act card to the table
    if doEncounter or encounterDeck().controller == me:
        count = agendaCount(table)
        if count == 0:
            nextAgendaStage()
            nextActStage()
            shuffle(locationDeck())
            shuffle(encounterDeck())
            shuffle(specialDeck())  
        
    if not clearLock():
        notify("Players performed setup at the same time causing problems, please reset and try again")

def concealCard(card, x=0, y=0):
    conceal = re.search('.*Concealed\s(\d)(π)?.*', card.Text, re.IGNORECASE)
    if conceal:        
        decoy = int(conceal.group(1))
        if conceal.group(2):
            decoy = decoy * countInvestigators()
    elif "Cultist" in card.Traits:
        decoy = 1
    else:
        whisper("No conceal for this card")
        return
    x, y = card.position
    concealed = []
    cardList = [c for c in secondspecialDeck()
    if c.Type == "Mini" and card.Name in c.alternateProperty("B", "Name")]
    if cardList:
        for c in secondspecialDeck():
            if c in cardList and c.alternate == "":
                c.alternate = 'B'

        if len(cardList) > 1 and len(set(c.model for c in cardList)) != 1:
            dlg = cardDlg(cardList)
            dlg.title = "Multiple possible concealed cards"
            dlg.text = "Select 1 card:"
            dlg.min = 1
            dlg.max = 1
            cardreturned = dlg.show()
            if cardreturned:
                c = cardreturned[0].model
        else:
            c = cardList[0].model
        if c:
            concealed.append(c)
            for _ in range(decoy):
                concealed.append("7afe70d3-b76c-4d2f-9d2f-b06b6cfa2c5e")
            for _ in range(decoy+1):
                c = table.create(str(concealed.pop(rnd(0,len(concealed)-1))), x, y, quantity = 1, persist = True)

    

def tskCampaign(card, x=0, y=0):
    for c in table:
        if c.Type == "Scenario":
            if c.set == "The Scarlet Keys Campaign Expansion":
                return True
            else: return False

def campaignName():
    mute()
    for c in table:
        if c.Type == "Scenario":
            return c.set
        

def addDecoy(card, x=0, y=0):
    x, y = card.position
    c = table.create("7afe70d3-b76c-4d2f-9d2f-b06b6cfa2c5e", x, y, quantity = 1, persist = True)

def drawOpeningHand(player):
    studious = 0
    player.deck.shuffle()
    for c in table:
        if c.name == "Studious" and c.owner == player:
            studious += 1
            if studious == 2:
                break
    isSefina = filter(lambda card: card.Name == "Sefina Rousseau" and card.Type == "Investigator" and card.owner == player, table)
    isJoe = filter(lambda card: card.Name == "Joe Diamond" and card.Type == "Investigator" and card.owner == player, table)
    if isSefina and 1 == askChoice("Automate Sefina Drawing Hand ?", ["Yes","No"],["#000000","#000000"]):
        SefinaOpening(player)
    elif isJoe and 1 == askChoice("Automate Joe Hunch Deck ?", ["Yes","No"],["#000000","#000000"]):
        JoeOpening(player)
        drawMany(player.deck, shared.OpeningHandSize + studious)
        if studious > 0:
            whisper("You start the game with {} additional card in hand.".format(studious))
        removeWeaknessCards()
    else:
        drawMany(player.deck, shared.OpeningHandSize + studious)
        if studious > 0:
            whisper("You start the game with {} additional card in hand.".format(studious))
        removeWeaknessCards()
    player.deck.shuffle()

def removeWeaknessCards():
    weaknesses = []
    for card in filter(lambda card: (card.subType == "Weakness"  or card.subType == "Basic Weakness") and (card.Name != "The Tower · XVI" or card.Name == "The Devil XV"), me.hand):
        weaknesses.append(card)
        notify("{} replacing weakness '{}'".format(me, card))

    if not weaknesses: return None

    drawMany(me.deck, len(weaknesses))
    for card in weaknesses:
        card.moveTo(me.deck)

    return removeWeaknessCards()
    
def toggleLock(group, x=0, y=0):
    if deckLocked(group.player):
        unlockDeck()
        if len(group.player.deck) > 0:
            if isLocked(group.player.deck.top()):
                lockCard(group.player.deck.top())
        notify("{} Unlocks his deck".format(group.player))
    else:
        lockDeck()
        if len(group.player.deck) > 0:
            lockCard(group.player.deck.top())
        notify("{} Locks his deck".format(group.player))
           
def exhaust(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot90
    if card.orientation & Rot90 == Rot90:
        notify("{} exhausts '{}'".format(me, card))
        exhaustCardsSound(card)
    else:
        notify("{} readies '{}'".format(me, card))

def inspectCard(card, x = 0, y = 0):
    whisper("{} - model {}".format(card, card.model))
    for k in card.properties:
        if len(card.properties[k]) > 0:
            whisper("{}: {}".format(k, card.properties[k]))

def loadClues(card):
    if card.Type == "Location" and card.isFaceUp and card.markers[Clue] == 0:
        clue = re.search('(\d)(π)?', card.Clues, re.IGNORECASE)
        if clue:
          if clue.group(2):
            nbClue = int(clue.group(1)) * countInvestigators()
          else:
            nbClue = int(clue.group(1))
          if nbClue > 0:
            notify("{} adds {} clue(s) on '{}'".format(me, str(nbClue),card))            
            card.markers[Clue] = nbClue

def flipcard(card, x = 0, y = 0):
    mute()
    
    if card.controller != me:
        notify("{} gets {} to flip card".format(me, card.controller))
        remoteCall(card.controller, "flipcard", card)
        return

    cardx, cardy = card.position

    #Card Alternate Flip
    if card.alternates is not None and "B" in card.alternates:
        if card.alternate == "B":
            card.alternate = ''
        else:
            card.alternate = 'B'
        #if card.Type != "Location": questSetup(card) #Don't do setup for double-sided locations
        notify("{} turns '{}' face up.".format(me, card))
    elif card.isFaceUp:
        card.isFaceUp = False
        notify("{} turns '{}' face down.".format(me, card))        
    else:
        card.isFaceUp = True
        notify("{} turns '{}' face up.".format(me, card))
    loadClues(card)
    flipCardsSound(card)

    if card.Type == "Mini" and card.alternate == "B":
        for c in table:
            if c.owner == card.owner:
                if c.Name == "Peter Sylvestre" and c.markers[Horror]:
                    subHorror(c)
                if c.Name == "Jessica Hyde" and c.markers[Damage]:
                    subDamage(c)
        if InvestigatorName(me) == "Monterey Jack":
            choice_list = ["Gain 1 resource", "Draw 1 card", "Do both"]
            color_list = ['#000000','#000000',"#000000"]
            sets = askChoice("Monterey Jack", choice_list, color_list)
            if sets == 0: return
            elif sets == 1:
                addResource(Investigator(me))
            elif sets == 2:
                draw(me.deck)
            else:
                addResource(Investigator(me))
                draw(me.deck)

def rotateRight(card, x = 0, y = 0):
    # Rot90, Rot180, etc. are just aliases for the numbers 0-3
    mute()
    if card.controller == me:
        if card.Type == "Tarot":
            card.orientation ^= Rot180
        else:
            card.orientation = (card.orientation + 1) % 4
        if card.isFaceUp:
            notify("{} Rotates '{}'".format(me, card.Name))
        else:
            notify("{} Rotates a card".format(me))

def rotateLeft(card, x = 0, y = 0):
    # Rot90, Rot180, etc. are just aliases for the numbers 0-3
    mute()
    if card.controller == me:
        if card.Type == "Tarot":
            card.orientation ^= Rot180
        else:
            card.orientation = (card.orientation - 1) % 4
        if card.isFaceUp:
            notify("{} Rotates '{}'".format(me, card.Name))
        else:
            notify("{} Rotates a card".format(me))
        
def addResource(card, x = 0, y = 0):
    addToken(card, Resource)
    
def addClue(card, x = 0, y = 0):
    addToken(card, Clue)

def addDoom(card, x = 0, y = 0):
    addToken(card, Doom)  

def addDamage(card, x = 0, y = 0):
    addToken(card, Damage)

def addHorror(card, x = 0, y = 0):
    addToken(card, Horror)

def addAction(card, x = 0, y = 0):
    addToken(card, Action)

def addFlood(card, x = 0, y = 0):
    mute()
    num1 = card.markers[Flood1]
    num2 = card.markers[Flood2]
    if (num1+num2 == 0):
        #no flood tokens
        card.markers[Flood1] = 1
    elif (num1 > 0):
        #Flood level 1
        card.markers[Flood1] = 0
        card.markers[Flood2] = 2
    else:
        #Flood level 2
        notify("This card is already at maximum Flood Level.")

def addToken(card, tokenType):
    mute()
    card.markers[tokenType] += 1
    notify("{} adds a {} to '{}'".format(me, tokenType[0], card))
    

def subResource(card, x = 0, y = 0):
    subToken(card, Resource)
    
def subClue(card, x = 0, y = 0):
    subToken(card, Clue)

def subDoom(card, x = 0, y = 0):
    subToken(card, Doom)  

def subDamage(card, x = 0, y = 0):
    subToken(card, Damage)

def subHorror(card, x = 0, y = 0):
    subToken(card, Horror)  

def subAction(card, x = 0, y = 0):
    subToken(card, Action)  

def subFlood(card, x = 0, y = 0):
    mute()
    num1 = card.markers[Flood1]
    num2 = card.markers[Flood2]
    if (num1+num2 == 0):
        #no flood tokens
        notify("This card is already at minimum Flood Level.")
    elif (num1 > 0):
        #Flood level 1
        card.markers[Flood1] = 0
        card.markers[Flood2] = 0
    else:
        #Flood level 2
        card.markers[Flood1] = 1
        card.markers[Flood2] = 0

def subToken(card, tokenType):
    mute()
    card.markers[tokenType] -= 1
    notify("{} removes a {} from '{}'".format(me, tokenType[0], card))

def markerChanged(args):
    mute()
    card = args.card
    modifyMarkerSound(args)
    thisPhase = currentPhase()
    
    inMythosPhase = False
    if getGlobalVariable("phase") == "Mythos" or thisPhase[1] == 1:
        inMythosPhase = True

    if card.Type == "Agenda" and args.marker == Doom[0] and inMythosPhase == True and card.properties[Doom[0]].isnumeric() and card.controller == me:
        elleRubash = filter(lambda c: c.Name == "Elle Rubash" and not isLocked(c), table)
        brewingCatv1 = filter(lambda c: c.Name == "Brewing Catastrophe (v. I)" and not isLocked(c), table)
        if elleRubash:
            elle = elleRubash[0]
        maxDoom = int(card.properties[Doom[0]])
        if card.markers[Action] == 0:
            totalDoom = 0
            for cardT in table:
                if cardT.markers[Doom] is not None and cardT.markers[Doom] > 0 and cardT.Type != "Mini":
                    totalDoom = totalDoom + cardT.markers[Doom]
                    if brewingCatv1 and cardT.Type != "Agenda":
                        totalDoom = totalDoom - (cardT.markers[Doom] *2)
                    if elleRubash:
                        if cardoverlaps(elle,cardT):
                            maxDoom = maxDoom + 1 
        else: totalDoom = int(card.markers[Doom])
        if totalDoom >= maxDoom:
            card.highlight = EliminatedColour
        else:
            card.highlight = None

    elif card.Type == "Investigator" and card.Name == "Calvin Wright" and card.owner == me and (args.marker == Damage[0] or args.marker == Horror[0]) :
        if args.marker == Damage[0]:
            if args.value < Investigator(me).markers[Damage]:
                me.counters["Combat"].value += 1
                me.counters["Agility"].value += 1
            else:
                me.counters["Combat"].value -= 1
                me.counters["Agility"].value -= 1
        elif args.marker == Horror[0]:
            if args.value < Investigator(me).markers[Horror]:
                me.counters["Willpower"].value += 1
                me.counters["Intellect"].value += 1
            else:
                me.counters["Willpower"].value -= 1
                me.counters["Intellect"].value -= 1

def lockCard(card, x=0, y=0):
    mute()
    if isLocked(card):
        card.markers[Lock] = 0
    else:
        card.markers[Lock] = 1

def isLocked(card):
    return card.markers[Lock] > 0
    
def setControllerRemote (card, player):
		card.controller=player
    
def discard(card, x=0, y=0):
    mute()
    if card.controller != me:
        whisper("{} does not control '{}' - discard cancelled".format(me, card))
        remoteCall (card.controller, "setControllerRemote", [card, me])
        
        
    if card.Type == "Agenda": #If we remove the only Agenda card then we reveal the next one
        card.moveToBottom(agendaDiscard())
        notify("{} discards '{}'".format(me, card))
        nextAgendaStage()
        return
        
    if card.Type == "Act": #If we remove the only Act card then we reveal the next one
        card.moveToBottom(actDiscard())
        notify("{} discards '{}'".format(me, card))
        nextActStage()
        return

    if isPath(card) or isConcealed(card):
        card.delete()
        return

    if "RemoveFromGame." in card.Subtype:
        notify("{} is removed from the game".format(card))
        card.delete()
        return
    
    if "ShuffleBack." in card.Subtype:
        card.Subtype = card.Subtype.replace('ShuffleBack.', '')
        notify("{} is shuffled back into {}'s deck".format(card, card.owner))
        shuffleIntoDeck(card, x=0, y=0, player=me)
        return
    
    if "ToHandAfterDiscard." in card.Subtype:
        card.Subtype = card.Subtype.replace('ToHandAfterDiscard.', '')
        notify("{} is moved back to {}'s hand".format(card, card.owner))
        card.moveTo(card.owner.hand)
        return

    if "Amulet." in card.Subtype:
        card.Subtype = card.Subtype.replace('Amulet.', '')
        notify("{} is moved at the bottom of {}'s deck".format(card, card.owner))
        card.moveToBottom(card.owner.deck)
        return	

    if isEncounterCard(card):
        pile = encounterDiscard()   
    elif isLocationCard(card):
        pile = locationDiscard()
    elif isChaosToken(card):
        pile = chaosBag()
    #For specific case like Asset in encounter deck
    elif not isPlayerCard(card):
        pile = encounterDiscard()
    else:
	#Last choice is player discard
        pile = card.owner.piles['Discard Pile']

    
        
       
    who = pile.controller
    discardCardsSound(card)
    if who != me:
        card.controller = who     
        random = rnd(100, 10000)
        remoteCall(who, "doDiscard", [me, card, pile])
    else:
        doDiscard(who, card, pile)

def discardSpecial(card, x=0, y=0):
    mute()
    if card.controller != me:
        whisper("{} does not control '{}' - discard cancelled".format(me, card))
        return
        
    if card.Type == "Agenda": #If we remove the only quest card then we reveal the next one
        card.moveToBottom(agendaDiscard())
        notify("{} discards '{}'".format(me, card))
        n, c = agendaCount(table)
        if c == 0:
            nextAgendaStage()
        return

    if isPlayerCard(card):
        pile = specialDiscard()
    else:
        pile = specialDiscard()
        
    who = pile.controller
    if who != me:
        card.controller = who    
        random(100,10000)
        remoteCall(who, "doDiscard", [me, card, pile])
    else:
        doDiscard(who, card, pile)


def doDiscard(player, card, pile):
    mute()
    if pile == chaosBag():
        if ((card.Name == "Bless") or (card.Name == "Curse")) and card.Subtype != "Sealed":
            card.delete()
            updateBlessCurse()
            return
    if "Sealed." in card.Subtype: 
        card.Subtype = card.Subtype.replace('Sealed.', '')
    if "EotRDiscard." in card.Subtype: 
        card.Subtype = card.Subtype.replace('EotRDiscard.', '')
    if "Locked." in card.Subtype:
        card.Subtype = card.Subtype.replace('Locked.', '')
    if "Boost." in card.Subtype:
        boost_info = boost_lookup.get(card.Name)
        card.Subtype = card.Subtype.replace('Boost.', '')
        for stat_info in boost_info:  # Itérer sur le tuple interne
            stat, levels = stat_info
            if levels is not None:
                if card.Level:
                    if int(card.Level) in levels:
                        card.owner.counters[str(stat)].value -= 1
                else: # Pas de niveau de carte
                    card.owner.counters[str(stat)].value -= 1
    card.moveTo(pile)
    if card.Type != "Chaos Token":
        notify("{} discards '{}'".format(player, card))
        if card.Type == "Asset": # Bonded card discard
            bonded_info = next((info for info in Bonded if info["sourceCard"] == card.Name), None)
            if bonded_info:
                removeBondedCards(card, bonded_info)

def removeBondedCards(sourceCard, bonded_info):
    bonded_codes = bonded_info["bondedCode"]
    codes_to_find = {code: bonded_codes.count(code) for code in set(bonded_codes)}
    groups_to_search = [sourceCard.owner.deck, sourceCard.owner.hand, table]
    for code in codes_to_find:
        for _ in range(codes_to_find[code]):
            found_card = findFirstCardInGroups(groups_to_search, code)
            if found_card:
                found_card.moveTo(sourceCard.owner.piles['Sideboard'])
                notify('{} is set aside'.format(found_card))
            else:
                break

def findFirstCardInGroups(groups, model_code):
    for group in groups:
        card = next((c for c in group if c.model == model_code), None)
        if card:
            return card
    return None



def shuffleIntoDeck(card, x=0, y=0, player=me):
    mute()
    if card.controller != me:
        whisper("{} does not control '{}' - shuffle cancelled".format(me, card))
        return
        
    if card.Type == "Agenda":
        whisper("Invalid operation on a {} card".format(card.Type))
        return
    if card.Type == "Act":
        whisper("Invalid operation on a {} card".format(card.Type))
        return


    if isPlayerCard(card):
        pile = card.owner.deck
    elif isLocationCard(card):
        pile = locationDeck()
    else:
        pile = encounterDeck()

    who=pile.controller
    notify("{} moves '{}' to '{}'".format(me, card, pile.name))     
    if who != me:
        card.controller = who
        remoteCall(who, "doMoveShuffle", [me, card, pile])
    else:
        doMoveShuffle(me, card, pile)
        
def shuffleIntoTop(card, x=0, y=0, player=me, group=None, count=None):
    mute()
    if count is None:
        count = askInteger("Shuffle with top x cards ?", 3)
    if count == 0:
        return
    
    if group is None:
        if isLocationCard(card):
            group = locationDeck()
        elif isEncounterCard(card):
            group = encounterDeck()
        else:
            group = card.owner.deck

    cards_to_shuffle = list(group[:min(count, len(group))])
    cards_to_shuffle.append(card)
    notify("{} shuffles {} with {} top {} cards.".format(me, card, group.name, len(cards_to_shuffle) - 1))
    while cards_to_shuffle:
        index = rnd(0, len(cards_to_shuffle) - 1)
        cards_to_shuffle.pop(index).moveTo(group)
        
def shuffleIntoBottom(card, x=0, y=0, player=me, group = None, count = None):
    mute()
    if count is None:
        count = askInteger("Shuffle with bottom x cards ?", 3)
    if group is None:
        if isLocationCard(card):
            group = locationDeck()
        elif isEncounterCard(card):
            group = encounterDeck()
        else:
            group = card.owner.deck
    notify("{} shuffles {} with {} bottom {} cards.".format(me, card, group.name, count))
    cards = []
    for c in  group[-count:]:
        cards.append(c)
    cards.append(card)
    while cards:
        cards.pop(rnd(0,len(cards)-1)).moveToBottom(group)
        
def doMoveShuffle(player, card, pile):
    mute()
    card.moveTo(pile)
    shuffle(pile)

def twohandedsolo(group, x=0, y=0):
    mute()
    whisper("Taking controll of {}...".format(Player(2)))
    while Player(2).hand.controller != me:
        Player(2).hand.controller = me
        update()
    for card in table:
        if card.controller == Player(2):
            while card.controller != me:
                card.controller = me
                update()
    while Player(2).deck.controller != me:
        Player(2).deck.controller = me
        update()
    while Player(2).piles['Discard Pile'].controller != me:
        Player(2).piles['Discard Pile'].controller = me
        update()
    while Player(2).hand.visibility != "all":
        Player(2).hand.visibility = "all"
        update()
    if len(Player(2).piles['Sideboard']):
        while Player(2).piles['Sideboard'].controller != me:
            Player(2).piles['Sideboard'].controller = me
            update()
        while Player(2).piles['Sideboard'].visibility != "all":
            Player(2).piles['Sideboard'].visibility = "all"
            update()
        
    whisper("...Took control of P2")

def shuffleOnTable(cards, x=0, y=0):
    positions = []
    cardsToShuffle = []
    for c in cards:
        positions.append(c.position)
        cardsToShuffle.append(c)

    for c in cardsToShuffle:
        pos = positions.pop(rnd(0,len(positions)-1))
        c.moveToTable(pos[0],pos[1])

    notify("Shuffled {} cards together".format(len(cards)))
    clearSelection()

    
def playCard(card, x=0, y=0):
    global reduceCost
    if x == 0 and y == 0 and inGame(card.owner):
        x, y = firstInvestigator(card.owner).position
        x += Spacing
        y += Spacing
    investigator = Investigator(card.owner)
    if card.Cost and card.Cost.isnumeric() and InvestigatorName(card.owner) != "Preston Fairmont":
        if investigator.markers[Resource] + reduceCost >= int(card.Cost): # 0 + reduCost (2) >= 2
            if reduceCost:
                investigator.markers[Resource] -= int(card.Cost) - reduceCost
                reduceCost = 0 
        else:
            whisper("Not enough resources to play {}".format(card))
            return
    card.moveToTable(x, y)
    if card.Type == "Event" or card.Type == "Asset":
        if not "Fast." in card.Keywords and not "Fast." in card.Text and not "Dilemma." in card.Traits:
            addAction(InvestigatorMini(card.owner))
        if "Double." in card.Traits:
            addAction(InvestigatorMini(card.owner))
        amulet = filter(lambda c: "Wendy's Amulet" in c.Name and c.owner == card.owner and not isLocked(c), table)
        if amulet and card.Type == "Event":
            card.Subtype = card.Subtype + "Amulet."
    if card.Type == "Asset" and isPlayerCard(card) and card.Name in boost_lookup:
        boost_info = boost_lookup.get(card.Name)
        if boost_info:
            card.Subtype += "Boost."
            for stat_info in boost_info:  # Itérer sur le tuple interne
                stat, levels = stat_info
                if levels is not None:
                    if card.Level:
                        if int(card.Level) in levels:
                            card.owner.counters[str(stat)].value += 1
                    else: # Pas de niveau de carte
                        card.owner.counters[str(stat)].value += 1

def playFromDiscard(group):
    shuffleback = ["Winging It","Impromptu Barrier","Improvised Shield","Improvised Weapon"]
    discardlist = [c for c in group
    if "from your discard pile" in c.Text or c.Name in ["Moonstone", "A Glimmer of Hope"]]
    if discardlist:
        dlg = cardDlg(discardlist)
        dlg.title = "Play from Discard"
        dlg.text = "Select the card you wish to play from Discard:"
        dlg.min = 1
        dlg.max = 1
        cardsSelected = dlg.show()
        if cardsSelected is not None:
            card = cardsSelected[0]
            if card.Name != "A Glimmer of Hope":
                playCard(card, 0, 0)
                if card.name in shuffleback:
                    card.Subtype = card.Subtype + "ShuffleBack."
                if card.group == table:
                    notify("{} plays {} from his/her Discard Pile".format(card.owner,card))
            elif card.Name == "A Glimmer of Hope":
                for c in card.owner.piles["Discard Pile"]:
                    if c.Name == "A Glimmer of Hope":
                        c.moveTo(c.owner.hand)

def swapCard(card):
    mute()
    if deckLocked(card.owner):
        whisper("Your deck is locked and cannot be manipulated")
        return
    draw(card.owner.deck)
    card.moveTo(card.owner.deck)
    

def sumVictory():
    v = 0
    for c in shared.piles['Victory Display']:
        v += num(c.properties['Victory Points'])
    shared.VictoryPoints = v
    
def moveToVictory(card, x=0, y=0):
    mute()
    card.moveTo(shared.piles['Victory Display'])
    v = num(card.properties['Victory Points'])
    sumVictory()
    notify("{} adds '{}' (+{}) to the Global Victory Display (Total = {})".format(me, card, v, shared.VictoryPoints))

    
#---------------------------
#movement actions
#---------------------------

#------------------------------------------------------------------------------
# Hand Actions
#------------------------------------------------------------------------------

def randomDiscard(group):
    mute()
    hand = [c for c in group
    if not "Hidden." in c.Text or "Hidden" in c.Keywords] 
    if hand:
        card = hand[rnd(0,len(hand)-1)]
        notify("{} randomly discards '{}'.".format(group.player, card))
        card.moveTo(group.player.piles['Discard Pile'])
    else:
        notify("No eligible card for random discard")
 
def mulligan(group, x = 0, y = 0):
    mute()
    hand = [c for c in group
    if not ("Dark Insight" in c.Name or "The Tower · XVI" in c.Name or "The Devil XV" in c.Name)]
    dlg = cardDlg(hand)
    dlg.title = "Mulligan!"
    dlg.text = "Select the cards you wish to replace:"
    dlg.min = 1
    dlg.max = len(hand)
    cardsSelected = dlg.show()
    if cardsSelected is not None:
        notify("{} declares a Mulligan, and replaces {} card(s).".format(group.player, len(cardsSelected)))
        for card in cardsSelected:
            deckWithoutWeakness = filter(lambda card: (card.Subtype != "Weakness"  and card.Subtype != "Basic Weakness") or (card.Name == "The Tower · XVI" or card.Name == "The Devil XV"), card.owner.deck)
            notify("{} replaces {}.".format(group.player, card))
            card.moveToBottom(card.owner.deck)
            deckWithoutWeakness[0].moveTo(card.owner.hand)
        shuffle(card.owner.deck)


#------------------------------------------------------------------------------
# Pile Actions
#------------------------------------------------------------------------------

def draw(group, x = 0, y = 0):
    mute()
    if deckLocked(group.player):
        whisper("Your deck is locked, you cannot draw a card at this time")
        return
    if len(group) == 0:
        takeHorror = True
        for c in group.player.piles['Discard Pile']:
            c.moveTo(group.player.deck)
        notify("{}'s deck is empty.".format(group.player))
        shuffle(group)
    else:
        takeHorror = False
    card = group[0]
    card.moveTo(group.player.hand) # Not using me.hand for two-handed solo players
    notify("{} draws '{}'".format(group.player, card))
    if takeHorror:
        remoteCall(group.player, "notifyBar", ["#86aceb", "Your deck is empty ! Take 1 horror !"])
    serumDoubleCheck(card)

def serumDoubleCheck(card):
    if haveSerum(card.owner):
        inHands = []
        for c in card.owner.hand:
            inHands.append(c.name)
        if inHands.count(card.name) > 1:
            for _ in range(haveSerum(card.owner)):
                for c in table:
                    if c.name == "Dream-Enhancing Serum" and c.owner == card.owner and c.orientation & Rot90 != Rot90:
                        c.highlight = WhiteColour
                        if 1 == askChoice("Trigger Dream-Enhancing Serum ?", ["Yes","No"],["#000000","#000000"]):
                            notify("{} uses {} to draw an additional card".format(card.owner, c))
                            exhaust(c, x=0,y=0)
                            draw(card.owner.deck)
                        c.highlight = None

def haveSerum(player):
    serum = 0
    for c in table:
        if c.name == "Dream-Enhancing Serum" and c.owner == player and c.orientation & Rot90 != Rot90:
            serum += 1
    return serum

def shuffle(group):
    mute()
    if len(group) > 0:
        update()
        group.shuffle()
        notify("{} shuffles {}".format(me, group.name))
        if group != encounterDeck():
            if InvestigatorName(group.player) == "Norman Withers" and group == group.player.deck and not group.top().isFaceUp:
                flipcard(group.top())

def drawMany(group, count = None):
    mute()
    if len(group) == 0: return
    if deckLocked(group.player):
        whisper("Your deck is locked, you cannot draw cards at this time")
        return
    if count is None:
        count = askInteger("Draw how many cards?", 4)
    if count is None or count <= 0:
        whisper("drawMany: invalid card count")
        return
    for i in range(0, count):
        draw(group)     

def search(group, count = None):
    mute()
    if len(group) == 0: return
    if count is None:
        count = askInteger("Search how many cards?", 5)
    if count is None or count <= 0:
        whisper("search: invalid card count")
        return
        
    notify("{} searches top {} cards".format(me, count))    
    moved = 0
    for c in group.top(count):
        c.moveTo(me.piles['Discard Pile'])
        moved += 1
    me.piles['Discard Pile'].lookAt(moved)
    
def moveMany(group, count = None):
    if len(group) == 0: return
    mute()
    if count is None:
        count = askInteger("Move how many cards to another deck?", 1)
        if count is None or count <= 0: return
    
    moved = 0
    
    if group == me.deck:
        pile = me.piles['Secondary Deck']
    else:
        choice_list = ['Special', '2nd Special']
        color_list = ['#000000','#000000']
        sets = askChoice("what is the arrival deck ?", choice_list, color_list)
        # load all sets if window is closed
        if sets == 0:
            return
        if sets == 1:
            pile = specialDeck()
        if sets == 2:
            pile = secondspecialDeck()

    for c in group.top(count):
        c.moveTo(pile)
        moved += 1
    notify("{} moves {} cards to the secondary deck".format(me, moved))
    if pile.collapsed:
        pile.collapsed = False

def discardMany(group, count = None):
    if len(group) == 0: return
    mute()
    if count is None:
        count = askInteger("Discard how many cards?", 1)
        if count is None or count <= 0: return
        
    if group != encounterDeck():
        pile = group.player.piles['Discard Pile']
        fr = "his deck"
    else:
        pile = encounterDiscard()
        fr = "the Encounter Deck"

    for c in group.top(count):
        c.moveTo(pile)
        notify("{} discards '{}' from {}".format(me, c, fr))

def moveAllToEncounter(group):
    mute()
    if confirm("Shuffle all cards from {} to Encounter Deck?".format(group.name)):
        for c in group:
            c.moveTo(encounterDeck())
        notify("{} moves all cards from {} to the Encounter Deck".format(me, group.name))
        shuffle(encounterDeck())

def moveAllToEncounterTop(group):
    mute()
    if confirm("Move all cards from {} to the top of the Encounter Deck?".format(group.name)):
        for c in group:
            c.moveTo(encounterDeck())
            notify("{} moves all cards from {} to the top of the Encounter Deck".format(me, group.name))

def moveAllToEncounterBottom(group):
    mute()
    if confirm("Move all cards from {} to the bottom of the Encounter Deck?".format(group.name)):
        for c in group:
            c.moveToBottom(encounterDeck())
            notify("{} moves all cards from {} to the bottom of the Encounter Deck".format(me, group.name))
       
def moveAllToSpecial(group):
    mute()
    if confirm("Shuffle all cards from {} to Special Deck?".format(group.name)):
        for c in group:
            c.moveTo(specialDeck())
        notify("{} moves all cards from {} to the Special Deck".format(me, group.name))
        shuffle(specialDeck())

def moveAllToPlayer(group):
    mute()
    if len(group) == 1 and len(group.player.deck) == 0:
        whisper("You cannot shuffle back 1 card into an empty deck")
        return
    if confirm("Shuffle all cards from {} to Player Deck?".format(group.name)):
        for c in group:
            if len(c.Setup) == 0:
                c.moveTo(c.owner.piles['Deck'])
        notify("{} moves all cards from {} to the Player Deck".format(me, group.name))
        shuffle(me.piles['Deck'])

def shuffleCardsIntoDeck(group):
    mute()
    owners = set()
    for card in group:
        if len(card.Setup) == 0:
            card.moveTo(card.owner.deck)
            owners.add(card.owner)
    for owner in owners:
        owner.deck.shuffle()

def swapWithEncounter(group):
    mute()
    if confirm("Swap all cards from {} with those in Encounter Deck?".format(group.name)):
      deck = encounterDeck()
      size = len(deck)
      for c in group:
          c.moveToBottom(deck)
      for c in deck.top(size):
          c.moveToBottom(group)
      notify("{} swaps {} and Encounter Deck.".format(me, group.name))

def drawPileToTable(player, group, x, y):
    mute()
    if len(group) == 0:
        notify("{} is empty.".format(group.name))
        return

    card = group[0]
    card.moveToTable(x, y)
    #failsave for sealed attribute
    if card.Type == "Chaos Token" and card.Subtype == "Sealed":
        if (card.Name == "Bless") or (card.Name == "Curse"):
            card.Subtype = "Blurse"
        else:
            card.Subtype = ""
    notify("{} draws {} from the {}.".format(player, card.name, group.name))
    return card
    
def drawChaosToken(group, x = 0, y = 0):
    drawChaosTokenForPlayer(me, group, x, y)  


def drawChaosTokenForPlayer(player, group, x = 0, y = 0, replace = True, xMod = 0, yMod = 0):
    mute()
    if chaosBag().controller == me:
        if replace:
            # check for existing chaos token on table
            table_chaos_tokens = [card for card in table
                if (card.Type == 'Chaos Token') and (card.Subtype != 'Sealed') and (card.Subtype != 'Blurse')]
            for token in table_chaos_tokens:
                if token.controller == me:
                    token.moveTo(chaosBag())
                else:
                    remoteCall(token.controller, "moveToRemote", [token, chaosBag()])
            chaosBag().shuffle()
  
        drawPileToTable(player, chaosBag(), ChaosTokenX + xMod, ChaosTokenY + yMod)
        updateBlessCurse()
    else:
        remoteCall(chaosBag().controller, "drawChaosTokenForPlayer", [me, chaosBag(), x, y, replace])
    
def moveToRemote (token, pile): # for remote calls
   token.moveTo(pile)	

def drawXChaosTokens(group, count = None, x = 0, y = 0):
    mute()
    if not count:
        xChaosTokens = askInteger("Draw how many Chaos Tokens?", 3)
        if xChaosTokens == None: return
    else: xChaosTokens = count
    
    for xTokens in range(0, xChaosTokens):
        replace = False
        if xTokens == 0: replace = True
        if chaosBag().controller == me:
                drawChaosTokenForPlayer(me, chaosBag(), x, y, replace, (xTokens * 10), (xTokens * 10))  
        else:
            remoteCall(chaosBag().controller, "drawChaosTokenForPlayer", [me,  chaosBag(), x, y, replace, (xTokens * 10), (xTokens * 10)])

def drawAddChaosToken(group, x = 0, y = 0):
    mute()
    num = 0
    for card in table: #find out how many Tokens there already are
        if card.Type == "Chaos Token" and card.subType != "Sealed":
            num += 1

    if chaosBag().controller == me:
        drawChaosTokenForPlayer(me, chaosBag(), x, y, False, num*10, num*10)
    else:
        remoteCall(chaosBag().controller, "drawChaosTokenForPlayer", [me,  chaosBag(), x, y, False, num*10, num*10])

def sealTokenOnCard(chaosToken, card):
    if card.controller != me:
        remoteCall(card.controller, "sealTokenOnCard", [chaosToken, card])
        return
    
    x,y = card.position
    x = x + card.width / 4
    y = y + card.height / 4
    chaosToken.moveToTable(x,y)
    chaosToken.Subtype = 'Sealed'
    chaosToken.filter = "#99999999"
    chaosToken.controller = card.controller
    updateBlessCurse()

def sealTokenCard(card, x = 0, y = 0, player = None):
    if card.controller != me:
        remoteCall(card.controller, "sealTokenCard", [card, x, y, me])
        return

    if player == None:
        player = me

    #failsave
    if card == None:
        return

    card.Subtype = 'Sealed'
    card.filter = "#99999999"
    card.controller = player
    updateBlessCurse()
    notify("{} seals {}.".format(player, card.name))

def sealToken(group, x = 0, y = 0, player = None):
    mute()

    if chaosBag().controller != me:
        remoteCall(chaosBag().controller, "sealToken", [group, x, y, me])
        return

    if player == None:
        player = me

    list = [card for card in table
                if (card.Type == 'Chaos Token') and (card.Subtype != 'Sealed')]
    for card in chaosBag():
        list.append(card)
    dlg = cardDlg(list)
    dlg.title = "Seal Chaos Token"
    dlg.text = "Select a Chaos Token to seal"
    card = dlg.show()
    if card == None:
        return
    card = card[0]
    card.moveToTable(ChaosTokenX, ChaosTokenY)
    card.Subtype = 'Sealed'
    card.filter = "#99999999"
    card.controller = player
    updateBlessCurse()
    notify("{} seals {}.".format(player, card.name))

def removeChaosTokenFromBag(card):
    if chaosBag().controller == me:
        cT = next((c for c in chaosBag() if c.Name == card),None)
        if cT:
            cT.delete()
    else:
        remoteCall(chaosBag().controller, "removeChaosTokenFromBag", [card])

def deleteChaosToken(card):
    card.delete()

def createChaosTokenInBag(id):
    if chaosBag().controller == me:
        chaosBag().create(id, quantity = 1)
    else:
        remoteCall(chaosBag().controller, "createChaosTokenInBag", [id])

####### Tarot Deck #######
def drawTarot(group, x = 0, y = 0, random = False):
    global TarotDeck
    if (TarotDeck == None or len(TarotDeck) == 0):
        TarotDeck = queryCard({"Type":"Tarot"}, True)
    cr = rnd(0, len(TarotDeck)-1)
    co = rnd(0,1)
    c = TarotDeck.pop(cr)
    c = table.create(c, x, y)
    if random and co:
        flipcard(c)

    return c

def drawTarotChaos(group, x = 0, y = 0):
    drawTarot(group, x, y, True)

def drawTarotBalance(group, x = 0, y = 0):
    x1 = x - (TarotWidth/2 + InvestigatorSpacing/2)
    x2 = x + (TarotWidth/2 + InvestigatorSpacing/2)
    drawTarot(group, x1, y)
    c = drawTarot(group, x2, y)
    flipcard(c)

def drawTarotChoice(group, x = 0, y = 0):
    x1 = x - (TarotWidth + InvestigatorSpacing)
    x2 = x + (TarotWidth + InvestigatorSpacing)
    drawTarot(group, x1, y)
    drawTarot(group, x, y)
    drawTarot(group, x2, y)
    update()
    notify("Choose two cards to reverse")

def drawBasicWeakness(group, x = 0, y = 0):
    mute()

    loadBasicWeaknesses(group, x, y)

    bw_cards = me.piles[BasicWeakness.PILE_NAME]
    bw_cards_count = len(bw_cards)
    if (bw_cards_count == 0):
        notify("There are no Basic Weakness cards left!")
        return

    card = bw_cards.top()
    return card

def clearScenario(group, x = 0, y = 0):
    if 1 == askChoice("Clear the scenario without resetting the player cards ?", ["Yes","No"],["#000000","#000000"]):
        for c in table:
            if c.Type == "Agenda" or c.Type == "Act" or c.Type == "Scenario" or c.Type == "Location" or c.Type == "Path":
                c.delete()
            if isEncounterCard(c):
                c.delete()
        for c in actDeck():
            c.delete()
        for c in agendaDeck():
            c.delete()
        for c in agendaDiscard():
            c.delete()
        for c in actDiscard():
            c.delete()
        for c in specialDeck():
            c.delete()
        for c in secondspecialDeck():
            c.delete()
        for c in encounterDeck():
            c.delete()
        for c in encounterDiscard():
            c.delete()
        notify("{} cleared the scenario".format(me))

def drawBasicWeaknessToDeck(group, x = 0, y = 0):
    mute()

    card = drawBasicWeakness(group, x, y)
    card.moveTo(me.deck)
    # do we notify players of what the basic weakness card that was shuffled in?
    notify("{} shuffles a random Basic Weakness into deck".format(me))
    me.deck.shuffle()


def drawBasicWeaknessToHand(group, x = 0, y = 0):
    card = drawBasicWeakness(group, x, y)
    card.moveTo(group.player.hand)
    notify("{} draws the Basic Weakness '{}' into their hand.".format(group.player, card))
    

def createCard(group=None, x=0, y=0):
	cardID, quantity = askCard()
	cards = table.create(cardID, x, y, quantity, True)
	try:
		iterator = iter(cards)
	except TypeError:
		# not iterable
		notify("{} created {}.".format(me, cards))
	else:
		# iterable	
		for card in cards:
			notify("{} created {}.".format(me, card))


def drawUnrevealed(group=None, x=0, y=0):
    mute()
    if len(group) == 0:
        notify("{} is empty.".format(group.name))
        return

    card = group[0]
    card.moveToTable(EncounterX, EncounterY, True)
    notify("{} draws an unrevealed card from the {}.".format(me, card.name, group.name))
    return card
    

def placeLongPath(group, x=0, y=0):
    pathCard = group.create("7f4029c8-1cee-406a-9913-9fbc6e341bed", x, y, 1, False)
    pathCard.sendToBack()

def placeMediumPath(group, x=0, y=0):
    pathCard = group.create("cf3d8bd6-354a-4284-b716-109e7040c3e9", x, y, 1, False)
    pathCard.sendToBack()

def placeShortPath(group, x=0, y=0):
    pathCard = group.create("2e964666-fa5a-40e4-a7f5-bf66c625d783", x, y, 1, False)
    pathCard.sendToBack()

def placeElbowPath(group, x=0, y=0):
    pathCard = group.create("3d9c7266-d4d0-46e0-b8b3-560fbcf1b294", x, y, 1, False)
    pathCard.sendToBack()

def placeCrossPath(group, x=0, y=0):
    pathCard = group.create("8ea6845b-b9bb-4f11-a814-e94b16e50629", x, y, 1, False)
    pathCard.sendToBack()

def placeThreeWayPath(group, x=0, y=0):
    pathCard = group.create("1b1493eb-cf9f-4709-9b50-f8f343f7a607", x, y, 1, False)
    pathCard.sendToBack()

def placeDiagonalConnectionPath(group, x=0, y=0):
    pathCard = group.create("d2ddabd3-b7b1-427e-8ca2-b7dbe272fce5", x, y, 1, False)
    pathCard.sendToBack()

def placeDirectionalMarker(group, x=0, y=0):
    pathCard = group.create("10bd7039-10f4-44c9-8be4-61bf182e1d9d", x, y, 1, False)
    pathCard.sendToBack()

def lockAllPaths(group, x=0, y=0):
    for card in table:
        if card.Type == "Path":
            if not hasattr(card, 'Subtype'):
                card.sendToBack()
            card.anchor = True

def unlockAllPaths(group, x=0, y=0):
    for card in table:
        if card.Type == "Path":
            card.anchor = False 

def blueHighlight(card, x=0 , y=0):
    card.highlight = BlueColour

def orangeHighlight(card, x=0 , y=0):
    card.highlight = OrangeColour
       
def greenHighlight(card, x=0 , y=0):
    card.highlight = GreenColour

def purpleHighlight(card, x=0 , y=0):
    card.highlight = PurpleColour

def redHighlight(card, x=0 , y=0):
    card.highlight = RedColour   

def blackHighlight(card, x=0 , y=0):
    card.highlight = BlackColour   

def whiteHighlight(card, x=0 , y=0):
    card.highlight = WhiteColour   

def clearHighlight(card, x=0 , y=0):
    card.highlight = None

#############################################
#                                           #
#           Gameboard Management            #
#                                           #
#############################################

def changeGameBoard(s):
    cultDeck = ['29338631-d9fc-425d-95e1-5dc408ca5355', 'f9fead41-dc88-4ece-a316-890df8213fd4']#, 'f81bfa10-12e0-45ca-9f65-1f52090277f6']
    exhibitDeck = ['f35868ff-263e-4a06-91d4-49fb17e22700']#, 'ceff1f22-cc40-45e6-8290-bc342b8227c4']
    catacombsDeck = ['e748e010-c470-4757-913b-3cdbd22ead1d']#, '248211c0-ccc3-483b-be2b-f8ab7dbf4aab']
    explorationDeck = ['6ea63fe0-6d47-49f8-aded-c891b70b6c63', '879c1767-bb80-4859-876a-264845386d78',
                       '10d7ffc2-11ee-4e1a-9353-c64e9ad9a245', '1a76e271-589d-4e28-8d0e-015c4c81ebbc',
                       '6876db05-c1e2-4e46-b172-1739f700f716', '9595aa3f-07ec-4d79-8d74-b8a79256e49f',
                       '88c8a01f-7824-4ff3-9df4-4437ec24d12e',]# '789d3a7d-7ab0-47c6-8cdf-24bc20f04cc3',
                       #'1a8b03a4-bf0a-49bf-b096-adcf9fa9188a', 'ffabc5ca-54ed-4ad4-9dc2-811911039950',
                       #'e8cbbe0b-5760-469f-b355-6619ab96b183', 'e4dfe2cd-224c-4749-a966-132b8f084cce',
                       #'0a8e6b32-5d1c-4ddf-9abf-031d84133235', '901acd41-cec5-4092-822e-1ff35fbae014',
                       #'3a459f09-4010-40b3-92d1-94cbc200b70b']
    unknownDeck = ['33bfb887-f781-43f9-a8a5-4677f811ca24']
    spectralDeck = ['a263c7a7-7641-479b-bb07-926c93371e15']
    cosmosDeck = ['6febb6ad-ef14-4445-8bc7-717919cc26b8']

    if isMultiActAgendaScenario(s):
        return

    board = True
    if s in cultDeck:
        createEncounter2CardClicky("Special", "cultistDraw")
    elif s in exhibitDeck:
        createEncounter2CardClicky("Location", "exhibitDraw")
    elif s in catacombsDeck:
        createEncounter2CardClicky("Location", "catacombsDraw")
    elif s in explorationDeck:
        createEncounter2CardClicky("Location", "explorationDraw")
    elif s in unknownDeck:
        createEncounter2CardClicky("Location", "unknownDraw")
    elif s in spectralDeck:
        createEncounter2CardClicky("Special", "spectralDraw")
    elif s in cosmosDeck:
        createEncounter2CardClicky("Location", "cosmosDraw")
    else:
        board = False

    if board:
        table.board = '2Encounter'

def isMultiActAgendaScenario(s):
    threads = '3e01c1d4-8e5c-472b-b803-357c6474ca01' #Needs to be handled differently, because the Return To Scenario changes Setup
    Act3 = ['3e01c1d4-8e5c-472b-b803-357c6474ca01']
    Act4 = ['8878eefa-e958-4b1f-9801-5c4127411fcc']
    Agenda2NoAct = ['0d7300da-ddb1-4d9b-81b0-ceab0a459f54']

    multi = True

    if s == threads:
        for c in setupDeck(): #See if we have the Return To Card in here
            if c.model == '8878eefa-e958-4b1f-9801-5c4127411fcc':
                return #We wait for the Return Card to come up

    if s in Act3:
        setGlobalVariable("multiActAgenda", "3Act")
        createAgendaCardClicky(AgendaX, AgendaY)
        createActCardClicky(Act31X, Act31Y)
        createActCardClicky(Act32X, Act32Y)
        createActCardClicky(Act33X, Act33Y)
        table.board = '3Act'
    elif s in Act4:
        setGlobalVariable("multiActAgenda", "4Act")
        createAgendaCardClicky(AgendaX, AgendaY)
        createActCardClicky(Act41X, Act41Y)
        createActCardClicky(Act42X, Act42Y)
        createActCardClicky(Act43X, Act43Y)
        createActCardClicky(Act44X, Act44Y)
        table.board = '4Act'
    elif s in Agenda2NoAct:
        #setGlobalVariable("multiActAgenda", "2AgendaNoAct")
        createAgendaCardClicky(AgendaX, AgendaY)
        c = createAgendaCardClicky(ActX, ActY)
        c.Type = "nextAct"
    else:
        multi = False
        createActCardClicky(ActX, ActY)
        createAgendaCardClicky(AgendaX, AgendaY)

    return multi

def nextAct3(nextAct=None):
    if nextAct == None: #Non-Setup Call
        #act location flags
        a1 = 1
        a2 = 2
        a3 = 4

        aN = 0
        #Check if Acts are on the table
        for c in table:
            if c.Type == "Act":
                if c.Setup[1] == "a":
                    aN |= a1
                elif c.Setup[1] == "c":
                    aN |= a2
                elif c.Setup[1] == "e":
                    aN |= a3

        if not aN: #Act Setup required
            nextAct3("1a")
            nextAct3("1c")
            card = nextAct3("1e")
            return card

        if not aN&a1:
            nextAct = "a"
        elif not aN&a2:
            nextAct = "c"
        elif not aN&a3:
            nextAct = "e"

        low = 999
        card = None
        for c in actDeck():
            if c.Setup[1] == nextAct and int(c.Setup[0]) < low:
                low = int(c.Setup[0])
                card = c
        nextAct = card.Setup

    else: #Setup Call
        for c in actDeck():
            if c.Setup == nextAct:
                card = c
                break

    if nextAct[1] == "a":
        x = Act31X
        y = Act31Y
    elif nextAct[1] == "c":
        x = Act32X
        y = Act32Y
    elif nextAct[1] == "e":
        x = Act33X
        y = Act33Y

    card.moveToTable(x, y)
    return card

def nextAct4(nextAct=None):
    if nextAct == None: #Non-Setup Call
        #act location flags
        a1 = 1
        a2 = 2
        a3 = 4
        a4 = 8

        aN = 0
        #Check if Acts are on the table
        for c in table:
            if c.Type == "Act":
                if c.Setup[1] == "a":
                    aN |= a1
                elif c.Setup[1] == "c":
                    aN |= a2
                elif c.Setup[1] == "e":
                    aN |= a3
                elif c.Setup[1] == "g":
                    aN |= a4

        if not aN: #Act Setup required
            nextAct4("1a")
            nextAct4("1c")
            nextAct4("1e")
            card = nextAct4("1g")
            return card

        if not aN&a1:
            nextAct = "a"
        elif not aN&a2:
            nextAct = "c"
        elif not aN&a3:
            nextAct = "e"
        elif not aN&a4:
            nextAct = "g"

        low = 999
        card = None
        for c in actDeck():
            notify(c.name)
            if c.Setup[1] == nextAct and int(c.Setup[0]) < low:
                low = int(c.Setup[0])
                card = c
        nextAct = card.Setup

    else: #Setup Call
        for c in actDeck():
            if c.Setup == nextAct:
                card = c
                break

    if nextAct[1] == "a":
        x = Act41X
        y = Act41Y
    elif nextAct[1] == "c":
        x = Act42X
        y = Act42Y
    elif nextAct[1] == "e":
        x = Act43X
        y = Act43Y
    elif nextAct[1] == "g":
        x = Act44X
        y = Act44Y

    card.moveToTable(x, y)
    return card
