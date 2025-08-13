#!/usr/bin/env python
# -*- coding: utf-8 -*-

HunchCard = None
AmandaCard = None
endoftherounddiscard = ["Antarctic Wind","Dissonant Voices","Dreamlands Eclipse",
                        "Intrepid","Nebulous Miasma","Ooze and Filth","Polar Vortex",
                        "Snakescourge","Tough Crowd","Whiteout","Whispers in the Dark", "Famine"]
eotrhighlight = ["Ancient Hall", "Between Worlds","Bringer of Paradise",
                 "City of the Moon-Beasts","Cosmic Ingress","Freigh Car","Glowing Eyes",
                 "Lure","Mists from Beyond","Poisonous Spores","Radical Treatment",
                 "Relentless Dark Young","Sordid and Silent","Tear Through Space",
                 "Terror of the Stars","The Pit Below","To Fight the Black Wind",
                 "Unstable Energies","Web-Spinner","Zealot of Paradise","Disciple of the Swarm",
                 "Nihilistic Stargazer","Poisonblossom"]
eotrdiscard1 = ["Aquatic Ambush","Children of Valusia","Deep Dark","Fog over Innsmouth",
                "Furtive Locals","Secrets in the Attic","Tenebrous Eclipse","Desiccation"]
hunters = {}
eotr = {}



def doMythosPhase(setPhaseVar = True):
    mute()
    debug("doMythosPhase()")
    
    if setPhaseVar:
        setGlobalVariable("phase", "Mythos")
    notify("Beginnig of the round effects")
    for card in table:
        if card.Name == "Sister Mary" and card.Type == "Investigator" and card.controller == me and countBless() < 10:
            if 1 == askChoice('Add a Bless Token in the Chaos Bag ?', ['Yes', 'No'], ['#dd3737', '#d0d0d0']):
                addBless()
        if card._id in eotr:
            card.highlight = eotr[card._id]
    # Auto-replenish
        replenish = re.search(r'[Uu]ses\s\((\d|X+)\s\w+\)\.\sReplenish\s(?:(\d)\sof\s)*(?:this|these)\s\w+ at the start of each round', card.Text)
        if replenish:
            if card.controller == me:
                if replenish.group(2):
                    if replenish.group(2).isnumeric() and (card.markers[Resource] < int(replenish.group(1))):
                        notify("Start of the round: {} is replenished.".format(card))
                        card.markers[Resource] += int(replenish.group(2))
                else: 
                    if replenish.group(1).isnumeric():
                        charges = int(replenish.group(1))
                        if card.markers[Resource] < charges:
                            notify("Start of the round: {} is replenished.".format(card))
                            card.markers[Resource] = charges
        # Agenda Doom
        if card.Type == "Agenda" and card.controller == me and not isLocked(card) and card.isFaceUp:
            addDoom(card)

    eotr.clear()

    shared.counters['Round'].value += 1

def doInvestigationPhase():
    if me._id == 1:
        notify("End of the Mythos Phase")
    for c in table:
        if (c.Name == "Wizard of the Order" or c.Name == "Corpse-Taker" or c.Name == "Stolen Mind" or c.Name == "Keeper of Secrets") and c.controller == me and c.Type != "Mini":
            addDoom(c)
        if c.Name == "Infestation Test" or c.Name == "Seeker of Carcosa" or c.Name == "Predation Test":
            c.highlight = RedColour
    global AmandaCard
    global HunchCard
    isJoe = filter(lambda card: (card.Name == "Joe Diamond" and card.Type == "Investigator" and card.owner == me and not isLocked(card) and inGame(card.owner)) , table)
    familyInheritance = filter(lambda card: card.Name == "Family Inheritance" and card.owner == me, table)
    if familyInheritance:
        familyInheritance[0].markers[Resource] += 4
    if next((c for c in table if c.Name == "Amanda Sharpe" and c.Type == "Investigator"), None):
        amanda = c
        notify("Amanda found")
        x, y = c.position
        if inGame(amanda.owner):
            notify("Amanda In Game")
            draw(amanda.owner.deck)
            if AmandaCard: # Discard card under Amanda
                discard(AmandaCard)
            if not next((c for c in amanda.owner.hand if c.Name == "Whispers from the Deep"), None):
                dlg = cardDlg(amanda.owner.hand)
                dlg.title = "Amanda Sharpe"
                dlg.text = "Select 1 card to put beneath Amanda:"
                dlg.min = 1
                dlg.max = 1
                cardsSelected = dlg.show()
                cardSelected = cardsSelected[0]
            else:
                cardSelected = c # Whispers from the Deep
            notify("Card Selected: {}".format(cardSelected))
            if cardSelected is not None:
                cardSelected.moveToTable(x + 15, y - 50)
                cardSelected.sendToBack()
                AmandaCard = cardSelected
                notify("{} places {} under {}".format(c.owner,AmandaCard,amanda))
    if isJoe:
        if len(me.piles['Secondary Deck']) > 0:
            HunchCard = me.piles['Secondary Deck'].top()
            HunchCard.isFaceUp = True # Show the first Hunch Card
        else: HunchCard = None

def doEnemyPhase(): # Also End of the Investigation Phase
    global HunchCard
    global hunters
    familyInheritance = filter(lambda card: card.Name == "Family Inheritance" and card.owner == me, table)
    if familyInheritance:
        familyInheritance[0].markers[Resource] = 0
    if HunchCard:
        if HunchCard == me.piles['Secondary Deck'].top(): # Checks if Hunch Card is still on top of the Hunch Deck
            HunchCard.isFaceUp = False
            me.piles['Secondary Deck'].shuffle() # Shuffle Hunch Deck
    for c in table: # Targets Hunter Enemies
        if c.Type == "Enemy" and ("Hunter." in c.Keywords or "Hunter." in c.Text or "Patrol (" in c.Keywords or "Patrol (" in c.Text) and c.orientation & Rot90 != Rot90 and c.isFaceUp:
            hunters[c._id] = c.highlight
            c.highlight = RedColour


def doUpkeepPhase(setPhaseVar = True):
    global hunters
    mute()
    if me._id == 1:
        notify("End of the Enemy Phase")
    for card in table:
        if card.Name == "Accursed Follower" and card.Controller == me:
            if countCurse() < 10:
                addCurse()
        if card._id in hunters:
            card.highlight = hunters[card._id]
    hunters.clear()
    debug("doUpkeepPhase()")
    if setPhaseVar:
        setGlobalVariable("phase", "Upkeep")

    if activePlayers() == 0:
        whisper("All players have been eliminated: You have lost the game")
        return

    clearTargets()
    doRestoreAll()

    if not inGame(me):
        whisper("You have been eliminated from the game.")
        return

    for card in table:
        #If Patrice, Discard all cards but weaknesses and draw to 5
        if card.Name == "Patrice Hathaway" and card.owner == me and card.Type == "Investigator" and not isLocked(card):
            for card in filter(lambda card: not card.Subtype in ["Weakness", "Basic Weakness"] and not "Peril. Hidden." in card.Text, me.hand):
                card.moveTo(me.piles['Discard Pile'])
                notify("{} discards '{}'".format(me, card))
            cardToDraw = 5 - len(me.hand)
            for i in range(0, cardToDraw):
                draw(me.deck)
            break
        #Else draw cards equal to selected value
        elif card.owner == me and card.Type == "Investigator":
            for i in range(0, card.owner.counters['Card Draw'].value):
                draw(card.owner.deck)
            break
    
    # Check for hand size!
    sizeHand = me.counters['Maximum Hand Size'].value
    peltShipment = filter(lambda card: card.Name == "Pelt Shipment", me.hand)
    if peltShipment:
        sizeHand -= 3
    #Checks if player has Dream-enhancing Serum on the table or Forced Learning
    haveForcedLearning = filter(lambda card: card.Name == "Forced Learning" and card.owner == me and not isLocked(card), table)
    haveSerum = filter(lambda card: card.Name == "Dream-Enhancing Serum" and card.owner == me and not isLocked(card), table)
    if haveForcedLearning and len(me.hand) > 1:
        forcedCards = [me.hand[0],me.hand[1]] #Last two cards drawn
        dlg = cardDlg(forcedCards)
        dlg.title = "Forcead Learning"
        dlg.text = "Select 1 card to discard:"
        dlg.min = 1
        dlg.max = 1
        cardsSelected = dlg.show()
        if cardsSelected is not None:
            discard(cardsSelected[0])
    if haveSerum:
        inHands = []
        duplicates = 0
        for c in me.hand:
            if c.Name in inHands:
                duplicates += 1
            inHands.append(c.Name)
        cardsInHand = len(me.hand) - duplicates
    else: cardsInHand = len(me.hand)
    if cardsInHand > sizeHand:
        discardCount = cardsInHand - sizeHand
        cardsToShow = [c for c in me.hand if not "Hidden" in c.Text]
        dlg = cardDlg(cardsToShow)
        dlg.title = "You have more than the allowed "+ str(sizeHand) +" cards in hand."
        dlg.text = "Select " + str(discardCount) + " Card(s):"
        dlg.min = 0
        dlg.max = discardCount
        cardsSelected = dlg.show()
        if cardsSelected is not None:
            for card in cardsSelected:
                discard(card)
    
    darkHorse = filter(lambda card: card.Name == "Dark Horse" and card.owner == me and not isLocked(card), table)
    for card in table:
        if card.Type == "Investigator" and card.owner == me and card.isFaceUp:
            if (me.counters['Ressource per upkeep'].value > 0):
                if darkHorse:
                    if 1 == askChoice('Dark Horse', ['Gain a resource', 'No resource'], ['#dd3737', '#d0d0d0']):
                        for i in repeat(None, me.counters['Ressource per upkeep'].value):
                            addResource(card)
                else:
                    for i in repeat(None, me.counters['Ressource per upkeep'].value):
                        addResource(card)
        elif card.Type == "Mini" and card.owner == me and card.Subtype != "Concealed":
            card.markers[Action] = 0
            if card.alternates is not None and "" in card.alternates:
                card.alternate = ''
    if me._id == 1:
        notify("End of the Round Effects")
    discarded = []
    for card in table:
        if card.Name in endoftherounddiscard and card.controller == me and card.isFaceUp:
            discard(card)
        elif card.Name in eotrhighlight and card.controller == me and card.isFaceUp:
            eotr[card._id] = card.highlight
            card.highlight = RedColour
        elif card.Name in eotrdiscard1 and card.Name not in discarded and card.controller == me and card.isFaceUp:
            discarded.append(card.Name)
            discard(card)
        if "EotRDiscard." in card.Subtype:
            discard(card)
        
        