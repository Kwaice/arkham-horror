#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

cardToAttachTo =  None
cardsFound = []
Premonition = []
attached = {}

cardScripts={
	'Eureka!': {'onDoubleClick': [lambda card: eureka(card)]},
    'Mr. “Rook”' : {'onDoubleClick': [lambda card: mrRook(card)]},
    'Ancestral Knowledge' : {'onDoubleClick': [lambda card: ancestralKnowledge(card)]},
    'Occult Lexicon' : {'onDoubleClick': [lambda card: occultLexicon(card)]},
    'Old Book of Lore' : {'onDoubleClick': [lambda card: oldBookOfLore(card)]},
    'Cryptic Research' : {'onDoubleClick': [lambda card: crypticResearch(card)]},
    'No Stone Unturned' : {'onDoubleClick': [lambda card: noStoneUnturned(card)]},
    'Research Librarian' : {'onDoubleClick': [lambda card: researchLibrarian(card)]},
    "Guided by the Unseen" : {'onDoubleClick': [lambda card: guidedByTheUnseen(card)]},
    'Dr. Elli Horowitz' : {'onDoubleClick': [lambda card: drElliHorowitz(card)]},
    'Whitton Greene' : {'onDoubleClick': [lambda card: whittonGreene(card)]},
    'Otherworld Codex' : {'onDoubleClick': [lambda card: otherworldCodex(card)]},
    'Practice Makes Perfect' : {'onDoubleClick': [lambda card: practiceMakesPerfect(card)]},
    'Captivating Discovery': {'onDoubleClick': [lambda card: captivatingDiscovery(card)]},
    'Obscure Studies' : {'onDoubleClick': [lambda card: obscureStudies(card)]},
    'Professor William Webb': {'onDoubleClick': [lambda card: prWilliamWebb(card)]},
    'Mandy Thompson': {'onDoubleClick': [lambda card: mandyThompson(card)]},
    'Joe Diamond' : {'onDoubleClick': [lambda card: joeDiamond(card)]},
    "Livre d'Eibon" : {'onDoubleClick': [lambda card: livredEibon(card)]}
}

def search(group, target, count = None, TypeFilter="ALL", TraitsFilter="ALL", filterFunction='True', addWeakness='False'):
    mute()
    global cardsFound
    global cardToAttachTo
    global AmandaCard
    allowed_globals = {
    '__builtins__': None,
    'True': True,
    'False': False,
    'None': None}
    if len(group) == 0: return
    cardsFound = []
    if group != encounterDeck():
        if deckLocked(group.player):
            notify("{}'s deck is locked and cannot be searched".format(group.player))
            return
    if count == None:
        count = len(group)
    else:
      if not count == len(group):
            if next((c for c in table if c.Name == "Mandy Thompson" and c.Type == "Investigator"), None):
                option1 = count
                option2 = count + 3
                choice_list = [str(option1), str(option2)]
                color_list = ['#000000','#F4BB2F']
                sets = askChoice("Search how many cards ?", choice_list, color_list)
                if sets == 0:
                    return
                if sets == 1:
                    count = count
                if sets == 2:
                    count = option2
    shockingDiscoveryCard = next((c for c in group.top(count) if c.Name == "Shocking Discovery"), None)
    if shockingDiscoveryCard:
        shockingDiscoveryCard.moveToTable(table)
        shockingDiscoveryCard.highlight = RedColour
        notify("{} found ! Search cancelled !".format(shockingDiscoveryCard))
        cardToAttachTo = None
        shuffle(group)
        return
    if TypeFilter!="ALL":
        cardsInGroup_Type_Filtered=[card for card in group.top(count) if re.search(TypeFilter, card.Type)]
    else:
        cardsInGroup_Type_Filtered=[card for card in group.top(count)]
    if TraitsFilter!="ALL":
        cardsInGroup_TraitsandType_Filtered=[card for card in cardsInGroup_Type_Filtered if re.search(TraitsFilter, card.Traits)]
    else:
        cardsInGroup_TraitsandType_Filtered=cardsInGroup_Type_Filtered
    if filterFunction!='True':
        filteredCardsInGroup=[c for c in cardsInGroup_TraitsandType_Filtered if eval(filterFunction, allowed_globals, {'c':c})]
    else:
        filteredCardsInGroup=cardsInGroup_TraitsandType_Filtered
    special_cards_to_include = [
            "Astounding Revelation",
            "Occult Evidence",
            "Surprising Find",
        ]
    specialCount = 0
    for card_name in special_cards_to_include:
        found_special_card = next((c for c in group.top(count) if c.Name == card_name and group.name!="Discard Pile"), None)
        if found_special_card and found_special_card not in filteredCardsInGroup:
            filteredCardsInGroup.append(found_special_card)
            specialCount += 1
    if addWeakness != 'False': #Mr. Rook
        specialCount += 1
    if filteredCardsInGroup:
        dlg = cardDlg(filteredCardsInGroup)
        if count < len(group):
            dlg.title = "Search the top "+ str(count) +" cards."
        else:
            dlg.title = "Searching {}".format(group.name)
        dlg.text = "Select the card(s):"
        dlg.min = 1
        if specialCount == 0:
            dlg.max = 1
        else:
            dlg.max = 1 + specialCount
        cardsSelected = dlg.show()
        if cardsSelected != None:
            inc = 0
            for card in cardsSelected:
                cardsFound.append(card)
                if not cardToAttachTo:
                    if target == table:
                        card.moveToTable(-200,-100)
                        card.select()
                    else:
                        card.moveTo(target)
                        if target == card.owner.hand:
                            serumDoubleCheck(card)
                else:
                    card.moveToTable(cardToAttachTo[0], cardToAttachTo[1])
                    card.sendToBack()
                    if len(cardsSelected) == 1:
                        cardToAttachTo = None
                    else:
                        attachTo(card)
                        inc += 1
                        if inc == len(cardsSelected):
                            cardToAttachTo = None
    else:
        notify("No Cards Found")    
    if group.name != "Discard Pile":
        shuffle(group)

#############################################
#                                           #
#           Seeker Cards                    #
#                                           #
#############################################

def livredEibon(card):
    if card.owner.hand:
        sets = askChoice("Livre d'Eibon", ["Swap cards","Commit a card(manual)"],["#000000","#000000"])
        if sets == 0: return
        exhaust(card)
        if sets == 1:
            dlg = cardDlg(card.owner.hand)
            dlg.title = "Livre d'Eibon"
            dlg.text = "Select a card to swap with the top card of your deck"
            dlg.min = 1
            dlg.max = 1
            c = dlg.show()
            if c:
                notify("{} uses {} to swap {} with the top card of his/her deck".format(card.owner, card, c[0]))
                swapCard(c[0])
    else: whisper("No cards in hand")

def joeDiamond(card):
    if card.Type == "Investigator":
      if 1 == askChoice("Trigger Elder Sign ?", ["Yes","No"],["#000000","#000000"]):
          Insights = [card for card in card.owner.piles['Discard Pile']
          if "Insight." in card.Traits and card.Type == "Event"]
          dlg = cardDlg(Insights)
          dlg.title = "Joe Diamond"
          dlg.text = "Select 1 card to move back to the Hunch Deck:"
          dlg.min = 1
          dlg.max = 1
          cardsSelected = dlg.show()
          if cardsSelected:
              cardsSelected[0].moveToBottom(card.owner.piles['Secondary Deck'])

def mandyThompson(card):
    if card.Type == "Investigator":
        if 1 == askChoice("Trigger Elder Sign ?", ["Yes","No"],["#000000","#000000"]):
            whisper("Commit or draw is manual")
            search(card.owner.deck, table, 3)

def prWilliamWebb(card):
    if card.Level == "0":
        sets = askChoice("William Webb", ["Return an Item","Discover a connecting clue (manual)"],["#000000","#000000"])
        if sets == 1:
                if len(card.owner.piles['Discard Pile']):
                    search(card.owner.piles['Discard Pile'], card.owner.hand, TraitsFilter="Item")
                    if cardsFound:
                        exhaust(card)
                        card.markers[Resource] -= 1
                        notify("{} uses {} to return {} from the discard pile to his/her hand.".format(card.owner, card, cardsFound[0]))
                else: whisper("Your discard Pile is Empty")
        elif sets == 2:
                exhaust(card)
                card.markers[Resource] -= 1
                notify("{} uses {} to discover a clue at a connecting location.".format(card.owner, card))

    else:
        if len(card.owner.piles['Discard Pile']):
            exhaust(card)
            card.markers[Resource] -= 1
            notify("{} uses {} to return an Item from the discard pile and discover a clue at a connecting location.".format(card.owner, card))
            search(card.owner.piles['Discard Pile'], card.owner.hand, TraitsFilter="Item")
            if cardsFound:
                notify("{} uses {} to return {} from the discard pile to his/her hand.".format(card.owner, card, cardsFound[0]))


def obscureStudies(card):
    global AmandaCard
    if AmandaCard:
        x, y = AmandaCard.position
        AmandaCard.moveTo(card.owner.hand)
        card.moveToTable(x, y)
        card.sendToBack()
        notify('{} uses {} to swap {} with {}'.format(card.owner, card, AmandaCard, card))
        AmandaCard = card

def captivatingDiscovery(card):
    notify("{} uses {} to search the top 6 cards of their deck.".format(card.owner, card))
    search(card.owner.deck, card.owner.hand, 6)
    if cardsFound:
        card_names = [c.name for c in cardsFound]
        cards_list_str = ", ".join(card_names)
        notify("{} adds {} to his/her hand".format(card.owner, cards_list_str))

def practiceMakesPerfect(card):
    notify("{} uses {} to search their deck for a Practiced card to commit to the test.".format(card.owner, card))
    search(card.owner.deck, table, 9, TraitsFilter="Practiced")
    if cardsFound:
        notify("{}".format(cardsFound[0]))
        cardsFound[0].Subtype += "ToHandAfterDiscard."

def otherworldCodex(card):
    exhaust(card)
    subResource(card)
    search(encounterDeck(), encounterDiscard(), 9)
    notify("{} uses {} to look at the top 9 cards of the encounter deck and discards {}.".format(card.owner, card, cardsFound[0]))

def whittonGreene(card):
    exhaust (card)
    if card.Level == "0":
        notify("{} uses {} to search the top 6 cards of their deck for a Tome or Relic to draw.".format(card.owner, card))
        search(card.owner.deck, card.owner.hand, 6, filterFunction = "'Tome' in c.Traits or 'Relic' in c.Traits")
    else:
        notify("{} uses {} to search the top 9 cards of their deck for a Tome or Relic to draw.".format(card.owner, card))
        search(card.owner.deck, card.owner.hand, 9, filterFunction = "'Tome' in c.Traits or 'Relic' in c.Traits")

def drElliHorowitz(card):
    attachTo(card)
    notify("{} uses {} to search the top 9 cards of his/her deck for a Relic to attach to {}.".format(card.owner, card, card))
    search(card.owner.deck, table, 9, TraitsFilter="Relic")

def noStoneUnturned(card):
    if len(getPlayers()) == 1: # Solo
        if card.Level == "0":
            search(card.owner.deck, card.owner.hand, count==6)
        else:
            search(card.owner.deck, card.owner.hand)
    else:
        choice_list = []
        color_list = []
        for i in range(0, len(getPlayers())): 
            # Add player names to the list
            choice_list.append(str(InvestigatorName(getPlayers()[i])))
            # Add players investigator color to the list
            color_list.append(InvestigatorColor(getPlayers()[i]))
        sets = askChoice("Choose an investigator at your location:", choice_list, color_list)
        if sets == 0:
            return
        else:
            chosenPlayer = getPlayers()[sets - 1]
            if card.Level == "0":
                notify("{} uses {} to make {} search the top 6 cards of their deck.".format(card.owner, card, chosenPlayer))
                remoteCall(chosenPlayer,"search",[chosenPlayer.deck, chosenPlayer.hand, 6])
            else:
                notify("{} uses {} to make {} search their deck for a card to draw.".format(card.controller, card, chosenPlayer))
                remoteCall(chosenPlayer,"search",[chosenPlayer.deck, chosenPlayer.hand])

def crypticResearch(card):
    if len(getPlayers()) == 1: # Solo
        drawMany(me.deck, 3)
    else:
        choice_list = []
        color_list = []
        for i in range(0, len(getPlayers())): 
            # Add player names to the list
            choice_list.append(str(InvestigatorName(getPlayers()[i])))
            # Add players investigator color to the list
            color_list.append(InvestigatorColor(getPlayers()[i]))
        sets = askChoice("Choose an investigator at your location to draw 3 cards:", choice_list, color_list)
        if sets == 0:
            return
        else:
            chosenPlayer = getPlayers()[sets - 1]
            if deckLocked(chosenPlayer):
                whisper("{}'s deck is locked.".format(chosenPlayer))
                return
            notify("{} uses {} to make {} draw 3 cards.".format(card.owner, card, chosenPlayer))
            remoteCall(chosenPlayer,"drawMany",[chosenPlayer.deck,3])

def oldBookOfLore(card):
    exhaust (card)
    if len(getPlayers()) == 1: # Solo
        search(me.deck, me.hand, 3)
    else:
        choice_list = []
        color_list = []
        for i in range(0, len(getPlayers())): 
            # Add player names to the list
            choice_list.append(str(InvestigatorName(getPlayers()[i])))
            # Add players investigator color to the list
            color_list.append(InvestigatorColor(getPlayers()[i]))
        sets = askChoice("Choose a player at your location:", choice_list, color_list)
        if sets == 0:
            return
        else:
            chosenPlayer = getPlayers()[sets - 1]
            notify("{} uses {} to let {} search their deck for a card to draw.".format(card.owner, card, chosenPlayer))
            # Two handed solo option
            if chosenPlayer.deck.controller == me:
                search(chosenPlayer.deck,chosenPlayer.hand,3)
            else:
                remoteCall(chosenPlayer,"search",[chosenPlayer.deck,chosenPlayer.hand,3])

def occultLexicon(card):
    if not isLocked(card):
        stop = False
        for c in card.owner.piles['Sideboard']:
            if stop is not True and c.Name == "Blood-Rite":
                c.moveTo(c.owner.hand)
                stop = True
            else:
                if c.Name == "Blood-Rite":
                    c.moveTo(c.owner.deck)
        notify("{} uses {} to draw {} and shuffle 2 other copies in their deck.".format(card.owner, card, c))
        shuffle(card.owner.deck)

def eureka(card):
# Solo
    if len(getPlayers()) == 1:
        search(me.deck, me.hand, 3)
    else:
        choice_list = []
        color_list = []
        for i in range(0, len(getPlayers())): 
            # Add player names to the list
            choice_list.append(str(InvestigatorName(getPlayers()[i])))
            # Add player investigator colors to the list
            color_list.append(InvestigatorColor(getPlayers()[i]))
        sets = askChoice("Choose a player:", choice_list, color_list)
        if sets == 0:
            return
        else:
            chosenPlayer = getPlayers()[sets - 1]
            # Two handed solo option
            if chosenPlayer.deck.controller == me:
                notify("{} uses {} to search their deck for a card to draw.".format(card.controller, card))
                search(chosenPlayer.deck,chosenPlayer.hand,3)
            else:
                notify("{} uses {} to let {} search their deck for a card to draw.".format(card.controller, card, chosenPlayer))
                remoteCall(chosenPlayer,"search",[chosenPlayer.deck,chosenPlayer.hand,3])

def mrRook(card):
    exhaust(card)
    subResource(card)
    choice_list = ['3', '6', '9']
    color_list = ['#000000','#000000','#000000']
    sets = askChoice("Search how many cards ?", choice_list, color_list)
    if sets == 0:
        return
    else:
        count = sets * 3
        search(card.owner.deck, card.owner.hand, count, addWeakness='True')

def ancestralKnowledge(card):
    global cardToAttachTo
    if not card.Subtype == "Locked": # Using Locked to prevent an additional trigger
        shuffle(card.owner.deck)
        AncestralCards = []
        skills = [c for c in card.owner.deck
                if c.Type == "Skill" and not "Weakness" in c.Subtype]
        if len(skills) >= 5:
            notify("{} uses {} to attach 5 random skills to it.".format(card.owner, card))
            attachTo(card)
            for i in range(0, 5):  
                AncestralCards.append(skills[i])
            for c in AncestralCards:
                c.moveToTable(cardToAttachTo[0], cardToAttachTo[1], True)
                c.sendToBack()
                c.peek()
                attachTo(c)
            card.Subtype = 'Locked'
            cardToAttachTo = None
            shuffle(card.owner.deck)
            if 1 == askChoice('Draw opening hand ?'
            , ['Yes', 'Not now'], ['#dd3737', '#d0d0d0']):
                drawOpeningHand(card.owner)
        else:
            whisper("You don't have enough skills in your deck!")
    else:
        exhaust(card)

def researchLibrarian(card):
    notify("{} uses {} to search their deck for a Tome to draw.".format(card.owner, card))
    search(card.owner.deck, card.owner.hand, TraitsFilter="Tome.")

def guidedByTheUnseen(card):
    # Solo
    if len(getPlayers()) == 1:
        search(me.deck, table, 3)
    else:
        choice_list = []
        color_list = []
        for i in range(0, len(getPlayers())): 
            # Add player names to the list
            choice_list.append(str(InvestigatorName(getPlayers()[i])))
            # Add players investigator color to the list
            color_list.append(InvestigatorColor(getPlayers()[i]))
        sets = askChoice("Choose an investigator at your location:", choice_list, color_list)
        if sets == 0:
            return
        else:
            chosenPlayer = getPlayers()[sets - 1]
            notify("{} uses {} to make {} search their deck for a card commit to the test.".format(card.owner, card, chosenPlayer))
            remoteCall(chosenPlayer,"search",[chosenPlayer.deck, table, 3])


def attachCard(host, card):
    mute()
    global attached
    if not host._id in attached:
        attached[host._id] = []
    attached[host._id].append(card._id)
    
def detachCard(card):
    mute()
    global attached
    for value in attached.values():
        if card._id in value:
            value.remove(card._id)
            break
            
def isAttached(card):
    mute()
    for value in attached.values():
        if card in value:
            return True
    return False

def InvestigatorColor(player):
    mute()
    for card in table:
        if card.Type == "Investigator" and card.owner == player:
            if card.Class == "Guardian":
                return "#2F99F4"
            elif card.Class == "Seeker":
                return "#F4CB2F"
            elif card.Class == "Mystic":
                return "#AF2FF4"
            elif card.Class == "Rogue":
                return "#22A827"
            elif card.Class == "Survivor":
                return "#D43A2E"
            else:
                return "#999999"

def InvestigatorName(player):
    for card in table:
        if card.Type == "Investigator" and card.owner == player:
            return card.Name

def Investigator(player):
    for card in table:
        if card.Type == "Investigator" and card.owner == player:
            return card

def InvestigatorMini(player):
    for card in table:
        if card.Type == "Mini" and card.owner == player:
            return card

def InvestigatorList():
    choice_list = []
    color_list = []
    for i in range(0, len(getPlayers())):
        # Add player names to the list
        if InvestigatorName(getPlayers()[i]):
            choice_list.append(str(InvestigatorName(getPlayers()[i])))
        # Add players investigator color to the list
        if InvestigatorColor(getPlayers()[i]):
            color_list.append(InvestigatorColor(getPlayers()[i]))
    return choice_list, color_list

def lookToBottom(group, count = None): # Alyssa Graham automation
    global cardsFound
    mute()
    if len(group) == 0: return
    if deckLocked(group.player):
        whisper("{}'s deck is locked and cannot be looked at".format(group.player))
        return
    if count is None:
        count = askInteger("Look at how many cards?", 5)
    if count is None or count <= 0:
        whisper("search: invalid card count")
        return
    dlg = cardDlg(group.top(count))
    dlg.title = "Looking at cards"
    dlg.text = "Select a card:"
    cardsSelected = dlg.show()
    if cardsSelected != None:
        for c in cardsSelected:
            c.moveToBottom(group)
            cardsFound.append(c)
        notify("{} is moved at the bottom of {}".format(c, group.name))

def toBottomMove(card, group):
    if card.controller != me:
        card.controller = me
        update()
    card.moveToBottom(group)

def attachTo(card):
    global cardToAttachTo
    cardToAttachTo = card.offset(card.position[0], card.position[1])

    
def defaultAction(card, x = 0, y = 0):
    mute()
    global cardToAttachTo
    global AmandaCard
    global Premonition
    # Default for Done button is playerDone
    if not card.isFaceUp: #Face down card - flip
        flipcard(card, x, y)
    elif card.Type == "Path" or card.Type == "Tarot": # Action handled in OnCardDoubleClicked
        # Do nothing
        mute()
    elif isConcealed(card):
        flipcard(card, x, y)
    elif card.orientation & Rot90 == Rot90: #Rotated card - refresh
        exhaust(card, x, y)
    elif card.Type == "Location": #Add a progress token
        flipcard(card, x, y)
    elif card.Type == "Tarot": #Rotate 180
        card.orientation = (card.orientation + 2) % 4
    elif card.Type == "Enemy": #Add damage
        addDamage(card, x, y)
    elif card.Type == "Chaos Bag": # Action handled in OnCardDoubleClicked
        # Do nothing
        mute()
    elif card.Type == "Chaos Token": # Action handled in OnCardDoubleClicked
        # Do nothing
        mute()
    elif card.Type == "Encounter Draw" or card.Type == "Encounter2 Draw": # Action handled in OnCardDoubleClicked
        # Do nothing
        mute()
    elif card.Type == "nextAct" or card.Type == "nextAgenda": # Action handled in OnCardDoubleClicked
        # Do nothing
        mute()
    elif card.Type == "Mini": #Add action token
        addToken(card, Action)
    elif card.Type == "Campaign": #Add a progress token
        flipcard(card, x, y)
    elif card.Name == "Flood Token": #Flip flood token
        flipcard(card, x, y)
    elif card.Name in cardScripts:
        card_actions = cardScripts[card.Name]
        if 'onDoubleClick' in card_actions:
            # Récupérer la liste des fonctions
            functions_list = card_actions['onDoubleClick']

            # Vérifier si la liste n'est pas vide et que le premier élément est bien appelable
            if functions_list and callable(functions_list[0]): # <--- MODIFICATION ICI
                # Appeler le PREMIER élément de la liste, qui est la fonction lambda
                functions_list[0](card) # <--- MODIFICATION ICI
#############################################
#                                           #
#           Mystic Cards                    #
#                                           #
#############################################
    elif card.Name == "De Vermis Mysteriis":
        discardCards = [c for c in card.owner.piles['Discard Pile'] if "Insight" in c.Traits or "Spell" in c.Traits]
        if discardCards:
            exhaust(card, x, y)
            dlg = cardDlg(discardCards)
            dlg.title = "De Vermis Mysteriis"
            dlg.text = "Select 1 card"
            dlg.min = 1
            dlg.max = 1
            cardsSelected = dlg.show()
            if cardsSelected != None:
                c = cardsSelected[0]
                playCard(c)
                if c.group == table:
                    addDoom(card)
                    c.Subtype += "RemoveFromGame"
                    notify("{} uses {} to play {} from their discard pile".format(card.owner, card, c))               
        else:
            whisper("No Insight or Spell cards to play from discard")
    elif card.Name == "Arcane Initiate":
        exhaust(card, x, y)
        notify("{} uses {} to search their deck for a Spell card to draw.".format(card.owner, card))
        searchTopDeck(card.owner.deck, card.owner.hand, 3, traits="Spell")
    elif card.Name == "Stargazing":
        if len(encounterDeck()) > 9:
            stop = False
            for c in card.owner.piles['Sideboard']:
                if c.Name == "The Stars Are Right" and stop is not True:
                    shuffleIntoTop(c, 0, 0, me, encounterDeck(),10)
                    stop = True
            notify("{} uses {} to shuffle {} in the encounter deck top 10 cards.".format(card.owner, card, c))
        else: 
            whisper("There are not enough cards in the encounter Deck")
    elif card.Name == "Word of Command":
        notify("{} uses {} to search their deck for a Spell card to draw.".format(card.owner, card))
        searchTopDeck(card.owner.deck, card.owner.hand, traits="Spell")
    elif card.Name == "Prescient":
        notify("{} uses {} to move back a Spell from the discard pile to their hand.".format(card.owner, card))
        searchTopDeck(card.owner.piles['Discard Pile'], card.owner.hand, traits="Spell")
    elif card.Name == "Olive McBride":
        exhaust (card, x, y)
        drawXChaosTokens(chaosBag(), x = 0, y = 0)
        notify("{} uses {} to reveal 3 chaos tokens and choose 2 of them to resolve.".format(card.owner, card))
    elif card.Name == "Alyssa Graham":
        exhaust (card, x, y)
        choice_list = ['Encounter Deck']
        color_list = ['#46453E']
        for i in range(0, len(getPlayers())):
            # Add player names to the list
            choice_list.append(str(InvestigatorName(getPlayers()[i])))
            # Add players investigator color to the list
            color_list.append(InvestigatorColor(getPlayers()[i]))
        sets = askChoice("Choose a deck to look at:", choice_list, color_list)
        if sets == 0:
            return
        #Encounter Deck
        elif sets == 1:
            notify("{} uses {} to look at the top card of the encounter deck".format(card.owner, card))
            lookToBottom(encounterDeck(), 1)
        else:
            chosenPlayer = getPlayers()[sets - 2]
            if deckLocked(chosenPlayer):
                notify("{}'s deck is locked and cannot be looked at".format(chosenPlayer))
                return
            notify("{} uses {} to look at the top card of {}'s deck".format(card.owner, card, chosenPlayer))
            #Two-Handed solo option
            if chosenPlayer.deck.controller == me:
                    lookToBottom(chosenPlayer.deck, 1)
            else:
                chosenPlayer.deck.controller = card.owner
                lookToBottom(chosenPlayer.deck, 1)
                chosenPlayer.deck.controller = chosenPlayer
        if len(cardsFound) == 2: #if a card was moved to the bottom, add a Doom to Alyssa
            addDoom(card)
    elif card.Name == "Scroll of Secrets" and card.Level == "0":
        exhaust (card, x, y)
        subResource(card)
        choice_list = ['Encounter Deck']
        color_list = ['#46453E']
        for i in range(0, len(getPlayers())):
            # Add player names to the list
            choice_list.append(str(InvestigatorName(getPlayers()[i])))
            # Add players investigator color to the list
            color_list.append(InvestigatorColor(getPlayers()[i]))
        sets = askChoice("Choose a deck to look at:", choice_list, color_list)
        if sets == 0:
            return
        #Encounter Deck
        elif sets == 1:
            notify("{} uses {} to look at the bottom card of the encounter deck".format(card.owner, card))
            deckToCheck = encounterDeck()
        else:
            chosenPlayer = getPlayers()[sets - 2]
            deckToCheck = chosenPlayer.deck
            if deckLocked(chosenPlayer):
                notify("{}'s deck is locked and cannot be looked at".format(chosenPlayer))
                return
            notify("{} uses {} to look at the bottom card of {}'s deck".format(card.owner, card, chosenPlayer))
            if deckToCheck.controller != me and deckToCheck != encounterDeck():
                for p in chosenPlayer.piles:
                    chosenPlayer.piles[p].controller = me
        dlg = cardDlg(deckToCheck.bottom(1))
        dlg.title = "Scroll of Secrets"
        dlg.text = "Choose a card"
        dlg.min = 1
        dlg.max = 1
        cardsSelected = dlg.show()
        choice_list = ['Discard the card',"Leave it at the bottom","Place it on top of its owner's deck"]
        color_list = ['#46453E','#46453E','#46453E',]
        if deckToCheck != encounterDeck():
            choice_list.append("Add the card to its owner's hand")
            color_list.append('#46453E')
        sets = askChoice("Choose an option:", choice_list, color_list)
        if sets == 0:
            return
        elif sets == 1:
            if deckToCheck == encounterDeck():
                cardsSelected[0].moveTo(encounterDiscard())
            else:
                cardsSelected[0].moveTo(chosenPlayer.piles['Discard Pile'])
            notify("{} discards {}.".format(card.owner, cardsSelected[0]))
        elif sets == 2:
            notify("{} leaves the card at the bottom of the deck.".format(card.owner))
            return
        elif sets == 3:
            cardsSelected[0].moveTo(deckToCheck)
            notify("{} moves the card at the top of the deck.".format(card.owner))
        elif sets == 4:
            cardsSelected[0].moveTo(deckToCheck.player.hand)
            notify("{} adds the card to {}'s hand".format(card.owner,chosenPlayer))
        if deckToCheck.player != me and deckToCheck != encounterDeck():
            for p in chosenPlayer.piles:
                chosenPlayer.piles[p].controller = chosenPlayer
    elif card.Name == "Crystalline Elder Sign":
        attachTo(card)
        card.sendToBack()
        if chaosBag().controller != card.owner:
            chaosBag().controller == card.owner
        list = [card for card in table
                    if (card.Type == 'Chaos Token') and (card.Subtype != 'Sealed')]
        for card in chaosBag():
            if card.name == "+1" or card.name == "Elder Sign":
                list.append(card)
        dlg = cardDlg(list)
        dlg.title = "Seal Chaos Token"
        dlg.text = "Select a chaos token to seal"
        dlg.min = 1
        dlg.max = 1
        tokensSelected = dlg.show()
        if tokensSelected == None:
            return
        else:
            cT = tokensSelected[0]
            cT.moveToTable(cardToAttachTo[0], cardToAttachTo[1])
            cT.Subtype = 'Sealed'
            cT.filter = "#99999999"
            notify("{} seals {}.".format(card.owner, cT))
        cardToAttachTo = None
    elif card.Name == "Astronomical Atlas":
            if card.owner.deck:
                if 1 == askChoice("Look at the top card and attach a non-weakness ?", ["Yes","No"],["#000000","#000000"]):
                    if card._id in attached and len(attached[card._id]) == 5:
                        whisper("5 cards already attached to {}".format(card))
                        return
                    if deckLocked(card.owner):
                        whisper("Your deck is locked and cannot be looked at")
                        return
                    exhaust(card, x, y)
                    topCard = card.owner.deck.top()
                    if topCard.Subtype != "Weakness" and topCard.subType != "Basic Weakness":
                        attachCard(card, topCard) # attaches to Atlas
                        notify("{} uses {} to attach the top card of their deck".format(card.owner, card))
                        inc = 1
                        topCard.moveToTable(card.position[0], card.position[1], True)
                        for c in table:
                            if c._id in attached[card._id]: # if card is attached to Atlas
                                c.moveToTable(card.position[0] + (inc * 5), card.position[1] + (inc * 5), True)
                                c.sendToBack()
                                c.peek()
                                inc += 1
                                if inc - 1 == len(attached[card._id]):
                                    break
                    else:
                        topCard.peek()
                        notify("{} sees a forecoming weakness!".format(card.owner))
            else: whisper("Your deck is empty.")
    elif card.Name == "Rod of Carnamagos":
        rots = filter(lambda c: (" Rot" in c.Name), card.owner.piles['Sideboard'])
        if rots:
            exhaust(card, x=0,y=0)
            drawXChaosTokens(chaosBag(), x = 0, y = 0)
            if 1 == askChoice("Curse revealed ?", ["Yes","No"],["#000000","#000000"]):
                if card.Level == "0":
                    rot = rots[rnd(0,len(rots)-1)]
                    rot.moveToTable(x, y)
                else:
                    dlg = cardDlg(rots)
                    dlg.title = "Rod of Carnamagos"
                    dlg.text = "Select a card"
                    dlg.min = 1
                    dlg.max = 1
                    rot = dlg.show()
                    rot = rot[0]
                    rot.moveToTable(x, y)
            notify("{} uses {} to attach {} to an enemy".format(card.owner, card, rot))
    elif card.Name == "Shards of the Void":
        if card.Subtype != "Locked":
            if len(chaosBag()):
                for cT in chaosBag():
                    if cT.Name != "0":
                        continue
                    zero = cT
                    break
                if zero:
                    card.markers[Zero] = 1
                    removeChaosTokenFromBag("Zero")
                    notify("{} uses {} to seal a 0 token".format(card.owner, card))
                    card.Subtype = "Locked"
                else:
                    whisper("No 0 tokens in the Chaos Bag")
                    return
        else:
            sets = askChoice("Shards of the Void", ["Release a 0 token","Seal revealed 0 tokens here"],["#000000","#000000"])
            if sets == 0: return
            elif sets == 1:
                if card.markers[Zero]:
                    card.markers[Zero] -= 1
                    createChaosTokenInBag('35137ccc-db2b-4fdd-b0a8-a5d91f453a43')
                    notify("{} uses {} to release a 0 token".format(card.owner, card))
                else: whisper("No Zero tokens sealed on {}".format(card))
            elif sets == 2:
                inc = 0
                for cT in table:
                    if cT.name == "0" and cT.Subtype != "Sealed":
                        cT.delete()
                        if cT.controller == me:
                            cT.delete()
                        else:
                            remoteCall(cT.controller, "deleteChaosToken", [cT])
                        card.markers[Zero] += 1
                        inc += 1
                if inc:
                    notify("{} uses {} to seal {} revealed 0 tokens".format(card.owner, card, inc))
                else: whisper("No revealed 0 to seal")

    elif card.Name == "Premonition":
        if card.Subtype != "Locked":
            if chaosBag().controller != card.controller:
                chaosBag().controller = card.controller
            update()
            attachTo(card)
            chaosBag().shuffle()
            for cT in chaosBag():
                cT.moveToTable(cardToAttachTo[0], cardToAttachTo[1])
                cT.Subtype = 'Sealed'
                cT.filter = "#99999999"
                notify("{} randomly seals {} on {}.".format(card.owner, cT, card))
                Premonition.append(cT)
                break
            card.Subtype = "Locked"
            updateBlessCurse()
            cardToAttachTo = None
        elif 1 == askChoice("Trigger Premonition ?", ["Yes","No"],["#000000","#000000"]):
            Premonition[0].SubType = ""
            Premonition[0].filter = None
            Premonition[0].moveToTable(ChaosTokenX, ChaosTokenY)
            Premonition = []
            discard(card)
    elif card.Name == "Flute of the Outer Gods":
        if card.Subtype != "Locked":
            sealXCurse(card)
        elif 1 == askChoice("Trigger Flute of the Outer Gods ?", ["Yes","No"],["#000000","#000000"]) and card.markers[Curse] > 0:
            exhaust(card, x=0,y=0)
            card.markers[Curse] -= 1
            addCurse()
    elif card.Name == "Protective Incantation":
        if chaosBag().controller != card.controller:
            chaosBag().controller = card.controller
        if card.Subtype != "Locked":
            attachTo(card)
            list = [cT for cT in chaosBag()
        if not ("Auto Fail" in cT.Name)]
            dlg = cardDlg(list)
            dlg.title = "Protective Incantation"
            dlg.text = "Select a Chaos Token to seal:"
            dlg.min = 1
            dlg.max = 1
            cT = dlg.show()
            if cT is not None:
                cT[0].moveToTable(cardToAttachTo[0], cardToAttachTo[1])
                cT[0].Subtype = 'Sealed'
                cT[0].filter = "#99999999"
                notify("{} seals {} on {}.".format(card.owner, cT[0], card))
            card.Subtype = "Locked"
            cardToAttachTo = None

    elif card.Name == "Seal of the Seventh Sign":
        if chaosBag().controller != card.controller:
            chaosBag().controller = card.controller
        if card.Subtype != "Locked":
            attachTo(card)
            autoFail = [cT for cT in chaosBag()
        if "Auto Fail" in cT.Name]
            token = autoFail[0]
            token.moveToTable(cardToAttachTo[0], cardToAttachTo[1])
            token.Subtype = 'Sealed'
            token.filter = "#99999999"
            notify("{} seals {} on {}.".format(card.owner, token, card))
            card.Subtype = "Locked"
            cardToAttachTo = None

    elif card.Name == "The Chthonian Stone":
        if chaosBag().controller != card.controller:
            chaosBag().controller = card.controller
        if card.Subtype != "Locked":
            attachTo(card)
            list = [cT for cT in chaosBag()
        if "Elder One" in cT.Name or "Skull" in cT.Name or "Cultist" in cT.Name or "Tablet" in cT.Name]
            if list:
                dlg = cardDlg(list)
                dlg.title = "The Chthonian Stone"
                dlg.text = "Select a Chaos Token to seal:"
                dlg.min = 1
                dlg.max = 1
                cT = dlg.show()
                if cT is not None:
                    cT[0].moveToTable(cardToAttachTo[0], cardToAttachTo[1])
                    cT[0].Subtype = 'Sealed'
                    cT[0].filter = "#99999999"
                    notify("{} seals {} on {}.".format(card.owner, cT[0], card))
                card.Subtype = "Locked"
                cardToAttachTo = None

    elif card.Name == "The Codex of Ages":
        if chaosBag().controller != card.controller:
            chaosBag().controller = card.controller
        if card.Subtype != "Locked":
            attachTo(card)
            elderSign = [cT for cT in chaosBag()
        if "Elder Sign" in cT.Name]
            if elderSign:
                eS = elderSign[0]
                eS.moveToTable(cardToAttachTo[0], cardToAttachTo[1])
                eS.Subtype = 'Sealed'
                eS.filter = "#99999999"
                notify("{} seals {} on {}.".format(card.owner, eS, card))
                card.Subtype = "Locked"
                cardToAttachTo = None
    elif card.Name == "Word of Woe":
        weal = None
        for c in card.owner.piles['Discard Pile']:
            if c.Name == "Word of Weal":
                weal = c
                break
        if weal:
            if confirm("Shuffle Word of Weal into your deck?"):
                shuffleIntoDeck(c)

    elif card.Name == "Word of Weal":
        woe = None
        for c in card.owner.piles['Discard Pile']:
            if c.Name == "Word of Woe":
                woe = c
                break
        if woe:
            if confirm("Shuffle Word of Woe into your deck?"):
                shuffleIntoDeck(c)
    elif card.Name == "Kōhaku Narukami" and card.Type == "Investigator":
        choice_list = ["Remove 2 Bless and 2 Curse for an action","Add 1 Bless or 1 Curse to the Chaos Bag"]
        color_list = ["#000000","#000000"]
        sets = askChoice("Kôhaku Narukami", choice_list, color_list)
        if sets == 0:
            return
        elif sets == 1: # Remove 2 Bless and 2 Curse
            if blessInCB() >= 2 and curseInCB() >= 2:
                for _ in range(2):
                    removeChaosTokenFromBag("Bless")
                    removeChaosTokenFromBag("Curse")
                updateBlessCurse()
                notify("{} uses {} to remove 2 bless and 2 curse tokens from the chaos bag to take an additional action".format(card.owner, card))
            else:
                whisper("Not enough bless and curse tokens in the chaos bag.")
        elif sets == 2:
            if curseInCB() > blessInCB():
                addBless()
            elif curseInCB() < blessInCB():
                addCurse()
            elif curseInCB() == blessInCB():
                choice_list = ["Add Bless","Add Curse"]
                color_list = ["#000000","#000000"]
                sets = askChoice("Kôhaku Narukami", choice_list, color_list)
                if sets == 0:
                    return
                elif sets == 1: 
                    addBless()
                elif sets == 2:
                    addCurse()
    elif card.Name == "Book of Living Myths":
        if blessInCB() or curseInCB():
            exhaust (card, x, y)
            if blessInCB() > curseInCB():
                removeChaosTokenFromBag("Bless")
                table.create('360db0ee-c362-4bbe-9554-b1fbf101d9ab', ChaosTokenX, ChaosTokenY, quantity = 1, persist = False)
                notify("{} uses {} to reveal a Bless token".format(card.owner, card))
            elif blessInCB() < curseInCB():
                removeChaosTokenFromBag("Curse")
                table.create('81df3f18-e341-401d-a6bb-528940a9c39e', ChaosTokenX, ChaosTokenY, quantity = 1, persist = True)
                notify("{} uses {} to reveal a Curse token".format(card.owner, card))
            elif blessInCB() == curseInCB():
                choice_list = ["Resolve A Bless Token","Resolve a Curse Token"]
                color_list = ["#000000","#000000"]
                sets = askChoice("Book of Living Myths", choice_list, color_list)
                if sets == 0:
                    return
                elif sets == 1: 
                    removeChaosTokenFromBag("Bless")
                    table.create('360db0ee-c362-4bbe-9554-b1fbf101d9ab', ChaosTokenX, ChaosTokenY, quantity = 1, persist = False)
                    notify("{} uses {} to reveal a Bless token".format(card.owner, card))
                elif sets == 2:
                    removeChaosTokenFromBag("Curse")
                    table.create('81df3f18-e341-401d-a6bb-528940a9c39e', ChaosTokenX, ChaosTokenY, quantity = 1, persist = True)
                    notify("{} uses {} to reveal a Curse token".format(card.owner, card))
            updateBlessCurse()
        else:
            whisper("Not enough Bless/Curse tokens in the Chaos Bag")


#############################################
#                                           #
#           Guardian Cards                  #
#                                           #
#############################################        
    elif card.Name == "Crisis of Faith":
        if blessInCB():
            if 1 == askChoice('Replace X Bless with X Curse ?', ['Yes', 'No'], ['#dd3737', '#d0d0d0']):
                count = askInteger("Replace how many tokens ?", 1)
                if count > blessInCB():
                    whisper("Must be inferior to the number of bless tokens in the CB")
                    return
                else:
                    notify("{} uses {} to replace {} Bless tokens with {} Curse tokens".format(card.owner,card, count, count))
                    for _ in range(count):
                        removeChaosTokenFromBag("Bless")
                        addCurse()
                    updateBlessCurse()
    elif card.Name == "Prepared for the Worst":
        notify("{} uses {} to search their deck for a Weapon card to draw.".format(card.owner, card))
        searchTopDeck(card.owner.deck, card.owner.hand, 9, traits="Weapon")
    elif card.Name == "Rite of Sanctification":
        if card.Subtype != "Locked":
            sealXBless(card, 5)
        elif card.markers[Bless]:
            if 1 == askChoice('Release a sealed bless token ?', ['Yes', 'Not now'], ['#dd3737', '#d0d0d0']):
                exhaust (card, x, y)
                card.markers[Bless] -= 1
                addBless()
                if not card.markers[Bless]:
                    notify("{} has no sealed Bless tokens left and is discarded".format(card))
                    discard(card)
    elif card.Name == "Tetsuo Mori":
        choice_list = []
        color_list = []
        for i in range(0, len(getPlayers())): 
            # Add player names to the list
            choice_list.append(str(InvestigatorName(getPlayers()[i])))
            # Add players investigator color to the list
            color_list.append(InvestigatorColor(getPlayers()[i]))
        sets = askChoice("Choose a player at your location:", choice_list, color_list)
        if sets == 0:
            return
        else:
            chosenPlayer = getPlayers()[sets - 1]
            choice_list = ['Search the discard pile','Search the top 9 cards of the deck']
            color_list = ['#46453E','#46453E']
            sets = askChoice("Tetsuo Mori", choice_list, color_list)
            if sets == 0:
                return
            if sets == 1: # Discard Pile
                remoteCall(chosenPlayer,"searchTopDeck",[chosenPlayer.piles['Discard Pile'],chosenPlayer.hand])
            if sets == 2: # Top 9
                remoteCall(chosenPlayer,"searchTopDeck",[chosenPlayer.deck,chosenPlayer.hand,9])
    elif card.Name == "Nephthys":
        choice_list = ['Seal a Bless token on Nephthys']
        color_list = ['#000000']
        if card.markers[Bless] >= 3:
            choice_list.append('Release 3 Bless Tokens')
            choice_list.append('Return 3 Bless Tokens to deal 2 damage')
            color_list.append('#000000')
            color_list.append('#000000')
        if len(choice_list) == 1:
            if blessOnTable() > 0:
                card.markers[Bless] += 1
                for t in table:
                    if t.name != "Bless":
                        continue
                    if t.SubType != "Sealed":
                        if t.controller == me:
                            doDiscard(me, t, chaosBag())
                        else:
                            remoteCall(t.controller, "doDiscard", [me, t, chaosBag()])
                        break
                notify("{} uses {} to seal a Bless token".format(card.owner, card))
        else:
            sets = askChoice("Nephthys", choice_list, color_list)
            if sets == 0:
                return
            if sets == 1: 
                if blessOnTable() > 0:
                    card.markers[Bless] += 1
                    for t in table:
                        if t.name != "Bless":
                            continue
                        if t.SubType != "Sealed":
                            if t.controller == me:
                                doDiscard(me, t, chaosBag())
                            else:
                                remoteCall(t.controller, "doDiscard", [me, t, chaosBag()])
                        break
                    notify("{} uses {} to seal a Bless token".format(card.owner, card))
            if sets == 2:
                exhaust (card, x, y)
                card.markers[Bless] -= 3
                notify("{} uses {} to release 3 Bless Tokens".format(card.owner, card))
                for i in range(0, 3):
                    addBless()
            if sets == 3:
                exhaust (card, x, y)
                card.markers[Bless] -= 3
                notify("{} uses {} to return 3 Bless tokens to the token pool and deal 2 damage to an enemy".format(card.owner, card))
    elif card.Name == "Holy Spear":
        choice_list = ["Release a token sealed here"]
        color_list = ['#000000']
        if blessInCB() >= 2:
            choice_list.append("Seal 2 Bless tokens here")
            color_list.append('#000000')
        sets = askChoice("Holy Spear", choice_list, color_list)
        if sets == 0:
            return
        if sets == 1: 
            if card.markers[Bless] == 0:
                return
            else:
                card.markers[Bless] -= 1
                notify("{} uses {} to release 1 Bless token".format(card.owner, card))
                addBless()
        if sets == 2: # Seal 2 Bless Tokens from CB
            BlessTokensRemoved = 0
            for t in shared.piles["Chaos Bag"]:
                if t.name == "Bless":
                    if t.controller == me:
                        doDiscard(me, t, chaosBag())
                    else:
                        remoteCall(t.controller, "doDiscard", [me, t, chaosBag()])
                    BlessTokensRemoved += 1
                    if BlessTokensRemoved == 2:
                        break
            card.markers[Bless] += 2
            notify("{} uses {} to seal 2 Bless tokens".format(card.owner, card))
            updateBlessCurse()
    elif card.Name == "Hallowed Mirror" and not isLocked(card):
        stop = False
        for c in card.owner.piles['Sideboard']:
            if stop is not True and c.Name == "Soothing Melody":
                c.moveTo(c.owner.hand)
                stop = True
            else:
                if c.Name == "Soothing Melody":
                    c.moveTo(c.owner.deck)
        notify("{} uses {} to draw {} and shuffle 2 other copies in their deck.".format(card.owner, card, c))
        shuffle(card.owner.deck)
    elif card.Name == "Boxing Gloves" and card.Level == "0":
        exhaust (card, x, y)
        notify("{} uses {} to search their deck for a Spirit card to draw.".format(card.owner, card))
        searchTopDeck(card.owner.deck, card.owner.hand, 6, traits="Spirit")
    elif card.Name == "Boxing Gloves" and card.Level == "3":
        exhaust (card, x, y)
        notify("{} uses {} to search their deck for a Spirit card to draw.".format(card.owner, card))
        searchTopDeck(card.owner.deck, card.owner.hand, 9, traits="Spirit")
    elif card.Name == "Stick to the Plan" and not isLocked(card) and not card.Subtype == "Locked": # Locking to prevent an additional trigger
        attachTo(card)
        unfilteredEvents = [c for c in card.owner.deck
                if c.Type == "Event" and ("Tactic" in c.Traits or "Supply" in c.Traits)]
        filteredEvents = []
        duplicate = []
        for c in unfilteredEvents:
            if c.name not in duplicate:
                duplicate.append(c.name)
                filteredEvents.append(c)
        dlg = cardDlg(filteredEvents)
        dlg.title = "Stick to the Plan"
        dlg.text = "Select up to 3 Tactic/Supply:"
        dlg.min = 0
        dlg.max = 3
        cardsSelected = dlg.show()
        if cardsSelected != None:
            inc = 0
            for c in cardsSelected:
                c.moveToTable(cardToAttachTo[0], cardToAttachTo[1])
                c.sendToBack()
                if len(cardsSelected) == 1:
                    cardToAttachTo = None
                else:
                    attachTo(c)
                    inc += 1
                    if inc == len(cardsSelected): # Resets cardToAttachTo
                        cardToAttachTo = None
            card.Subtype = 'Locked'
            cardToAttachTo = None
            notify("{} uses {} to attach {} Supply or Tactic events to it.".format(card.owner, card, len(cardsSelected)))
        shuffle(card.owner.deck)
        if 1 == askChoice('Draw opening hand ?'
			, ['Yes', 'Not now'], ['#dd3737', '#d0d0d0']):
            drawOpeningHand(card.owner)
    elif card.Name == "On the Hunt" and card.Level == "0":
        notify("{} uses {} to search the encounter deck for an Enemy to draw.".format(card.owner, card))
        searchTopDeck(encounterDeck(), table, 9, traits="Enemy")
    elif card.Name == "On the Hunt" and card.Level == "3":
        notify("{} uses {} to search the encounter deck for an Enemy to draw.".format(card.owner, card))
        searchTopDeck(encounterDeck(), table, traits="Enemy")
    elif card.Name == "Radiant Smite":
        if card.Subtype != "Locked":
            sealXBless(card, 3)
        elif card.Subtype == "Locked":
            if 1 == askChoice("Radiant Smite Bless Tokens", ["Return to Token Pool","Release in Chaos Bag"],["#000000","#000000"]):
                card.markers[Bless] = 0
            else: 
                b = card.markers[Bless]
                card.markers[Bless] = 0
                for _ in range(b):
                    addBless()
    elif card.Name == "Shield of Faith":
        if card.Subtype != "Locked":
            sealXBless(card, 5)
        else:
            if 1 == askChoice("Release a Bless token ?", ["Yes","No"],["#000000","#000000"]):
                if card.markers[Bless]:
                    exhaust(card, x=0,y=0)
                    card.markers[Bless] -= 1
                    addBless()
                    if not card.markers[Bless]:
                        notify("{} has no Bless tokens left and is discarded.".format(card))
                        discard(card)
                else: whisper("No Bless Tokens sealed")
    elif card.Name == "Nathaniel Cho" and card.Type == "Investigator":
        if 1 == askChoice("Trigger Elder Sign ?", ["Yes","No"],["#000000","#000000"]):
            Events = [c for c in card.owner.piles['Discard Pile']
                if c.Type == "Event"]
            dlg = cardDlg(Events)
            dlg.title = "Nathaniel Cho"
            dlg.text = "Select 1 card:"
            dlg.min = 1
            dlg.max = 1
            cardsSelected = dlg.show()
            if cardsSelected != None:
                cardsSelected[0].moveTo(card.owner.hand)
    elif card.Name == "Leo Anderson" and card.Type == "Investigator":
        if 1 == askChoice("Trigger Elder Sign ?", ["Yes","No"],["#000000","#000000"]):
            searchTopDeck(card.owner.deck, card.owner.hand, 3, traits="Ally")
  


#############################################
#                                           #
#           Rogue Cards                     #
#                                           #
############################################# 
    elif card.Name == "Lucky Cigarette Case" and card.Level == "0":
        exhaust (card, x, y)
        draw(card.owner.deck)
    elif card.Name == "Pickpocketing" and card.Level == "0":
        exhaust (card, x, y)
        draw(card.owner.deck)
    elif card.Name == "Pickpocketing" and card.Level == "2":
        exhaust (card, x, y)
        sets = askChoice("Pickpocketing", ["Draw 1 card","Gain 1 resource","Do both"],["#000000","#000000","#000000"])
        if sets == 0: return
        elif sets == 1:
            draw(card.owner.deck)
        elif sets == 2:
            Investigator(card.owner).markers[Resource] += 1
        elif sets == 3:
            draw(card.owner.deck)
            Investigator(card.owner).markers[Resource] += 1
    elif card.Name == "Lucky Cigarette Case" and card.Level == "3":
        exhaust (card, x, y)
        count = askInteger("Succeeded by how much ?", 2)
        if count is None or count <= 0:
            whisper("Lucky Cigarette Case: invalid card count")
            return
        else:
            notify("{} uses {} to search the top {} cards of their deck for a card to draw.".format(card.owner, card, count))
            searchTopDeck(card.owner.deck, card.owner.hand, count)

    elif card.Name == "Dark Ritual":
        if curseInCB() > 0 and card.markers[Curse] == 0: 
            count = askInteger("Seal how many Curse tokens from the chaos bag?", 5)
            if count is None or count <= 0 or count > 5 or count > curseInCB():
                whisper("Invalid Count")
                return
            inc = 0
            notify("{} uses {} to seal {} Curse tokens.".format(card.owner, card, count))
            card.markers[Curse] = count
            for t in shared.piles['Chaos Bag']:
                if t.Name != "Curse":
                    continue
                t.delete()
                inc += 1
                if inc == count:
                    break
            updateBlessCurse()
    elif card.Name == "Underworld Market":
        market = card.owner.piles['Secondary Deck']
        if len(market) > 1: #2nd option
            marketTop2 = [c for c in market[:2]]
            dlg = cardDlg(marketTop2)
            dlg.title = "Underworld Market"
            dlg.text = "Select a card:"
            dlg.min = 1
            dlg.max = 1
            cardsSelected = dlg.show()
            if cardsSelected is not None:
                c = cardsSelected[0]
                if Investigator(c.owner).markers[Resource] > 0:
                    notify("{} uses {} and pays 1 resource to draw a card".format(card.owner, card))
                    subResource(Investigator(card.owner))
                    c.moveTo(card.owner.hand)
                    marketTop2.remove(c)
            for c in marketTop2:
                c.moveToBottom(card.owner.piles['Secondary Deck'])
        else: #setup
            if 1 == askChoice("Use Underworld Market Setup ?", ["Yes","No"],["#000000","#000000"]):
                illicit = [card for card in card.owner.deck if
                    "Illicit." in card.Traits]
                if len(illicit) > 9:
                    dlg = cardDlg(illicit)
                    dlg.title = "Underworld Market"
                    dlg.text = "Select 10 cards:"
                    dlg.min = 10
                    dlg.max = 10
                    cardsSelected = dlg.show()
                    if cardsSelected is not None:
                        for c in cardsSelected:
                            c.moveTo(market)
                        shuffle(market)
                        market.viewState = "pile"
                else: 
                    whisper("Not enough Illicit cards in your deck!")
            shuffle(card.owner.deck)
            if 1 == askChoice('Draw opening hand ?', ['Yes', 'Not now'], ['#dd3737', '#d0d0d0']):
                drawOpeningHand(player)
    elif card.Name == "Kicking the Hornet's Nest":
        searchTopDeck(encounterDeck(), table, 9, traits="Enemy")
    elif card.Name == "Stylish Coat":
        exhaust(card, x, y)
        addResource(Investigator(card.owner))
    elif card.Name == "Bewitching":
        if card.highlight == "#ffffff":
            attachTo(card)
            searchTopDeck(card.owner.deck, table, traits="Trick")
            card.highlight = None
            drawOpeningHand(card.owner)
        else:
            exhaust(card, x, y)
            sets = askChoice("Pickpocketing", ["Draw 1 card","Search top 9 cards"],["#000000","#000000"])
            if sets == 0: return
            elif sets == 1:
                whisper("Manual Draw")
                return
            elif sets == 2:
                searchTopDeck(card.owner.deck, card.owner.hand, 9)
#############################################
#                                           #
#           Survivor Cards                  #
#                                           #
############################################# 
    elif card.Name == "Pushed to the Limit":
        list = [c for c in card.owner.piles['Discard Pile']
                    if any(trait in c.Traits for trait in ["Weapon.", "Tool."])]
        if list:
            dlg = cardDlg(list)
            dlg.title = "Pushed to the Limit"
            dlg.text = "Select a card"
            dlg.min = 1
            dlg.max = 1
            c = dlg.show()
            if c:
                c[0].moveTo(table)
                c[0].Subtype = c[0].Subtype + "ShuffleBack."
    elif card.Name == "Rabbit's Foot" and card.Level == "0":
        exhaust (card, x, y)
        draw(card.owner.deck)
    elif card.Name == "Resourceful":
        list = [c for c in card.owner.piles['Discard Pile']
                    if "Survivor" in c.Class and c.Name != "Resourceful"]
        if list:
            dlg = cardDlg(list)
            dlg.title = "Resourceful"
            dlg.text = "Select a card to return to your hand"
            dlg.min = 1
            dlg.max = 1
            c = dlg.show()
            if c:
                c[0].moveTo(card.owner.hand)
                notify("{} uses {} to return a card to their hand".format(card.owner, card))
        else: whisper("No relevant cards in the discard pile")
    elif card.Name == "Rabbit's Foot" and card.Level == "3":
        exhaust (card, x, y)
        count = askInteger("Failed by how much ?", 2)
        if count is None or count <= 0:
            whisper("Rabbit's Foot: invalid card count")
            return
        else:
            notify("{} uses {} to search the top {} cards of their deck for a card to draw.".format(card.owner, card, count))
            searchTopDeck(card.owner.deck, card.owner.hand, count)        
    elif card.Name == "Scavenging":
        exhaust (card, x, y)
        searchTopDeck(card.owner.piles['Discard Pile'], card.owner.hand, traits="Item")
    elif card.Name == "A Chance Encounter":
        # Solo
        if len(getPlayers()) == 1:
            searchTopDeck(card.owner.piles['Discard Pile'], table, traits="Ally")
            if len(cardsFound) > 0:
                notify("{} puts {} into play".format(card.owner, cardsFound[0]))
        else:
            choice_list = []
            color_list = []
            for i in range(0, len(getPlayers())): 
                # Add player names to the list
                choice_list.append(str(InvestigatorName(getPlayers()[i])))
                # Add players investigator color to the list
                color_list.append(InvestigatorColor(getPlayers()[i]))
            sets = askChoice("Choose a player:", choice_list, color_list)
            if sets == 0:
                return
            else:
                chosenPlayer = getPlayers()[sets - 1]
                notify("{} uses {} to search {}'s discard pile for an Ally to put in play.".format(card.owner, card, chosenPlayer.name))
                #Two-Handed solo option
                if chosenPlayer.piles['Discard Pile'].controller == me:
                    searchTopDeck(chosenPlayer.piles['Discard Pile'], table, traits="Ally")
                    if len(cardsFound) > 0:
                        notify("{} puts {} into play".format(card.owner, cardsFound[0]))
                else:
                    chosenPlayer.piles['Discard Pile'].controller = me
                    searchTopDeck(chosenPlayer.piles['Discard Pile'], table, traits="Ally")
                    notify("{}".format(len(cardsFound)))
                    if len(cardsFound) > 0:
                        notify("{} puts {} into play".format(card.owner, cardsFound[0]))
                    chosenPlayer.piles['Discard Pile'].controller = chosenPlayer
    elif card.Name == "Unrelenting":
        attachTo(card)
        card.sendToBack()
        if chaosBag().controller != card.owner:
            chaosBag().controller == card.owner
        list = [card for card in table
                    if (card.Type == 'Chaos Token') and (card.Subtype != 'Sealed')]
        for card in chaosBag():
            list.append(card)
        dlg = cardDlg(list)
        dlg.title = "Seal Chaos Token"
        dlg.text = "Select up to 3 Chaos Token to seal"
        dlg.min = 0
        dlg.max = 3
        tokensSelected = dlg.show()
        if tokensSelected == None:
            return
        else:
            inc = 0
            for cT in tokensSelected:
                cT.moveToTable(cardToAttachTo[0], cardToAttachTo[1])
                cT.Subtype = 'Sealed'
                cT.filter = "#99999999"
                notify("{} seals {}.".format(card.owner, cT))
                if len(tokensSelected) == 1:
                    cardToAttachTo = None
                else:
                    attachTo(cT)
                    inc += 1
                    if inc == len(tokensSelected):
                        cardToAttachTo = None
            updateBlessCurse()
    elif card.Name == "True Survivor":
        if len(card.owner.piles['Discard Pile']):
            searchTopDeck(card.owner.piles['Discard Pile'], card.owner.hand, traits="Innate")
    elif card.Name == "Short Supply":
        if 1 == askChoice("Discard the top 10 cards of your deck ?", ["Yes","No"],["#000000","#000000"]):
            for _ in range(10):
                discard(card.owner.deck.top())
    elif card.Name == "Scrounge for Supplies":
        list = [c for c in card.owner.piles['Discard Pile']
                    if c.Level == "0"]
        if list:
            dlg = cardDlg(list)
            dlg.title = "Scrounge for Supplies"
            dlg.text = "Select a card to return to your hand"
            dlg.min = 1
            dlg.max = 1
            c = dlg.show()
            if c:
                c[0].moveTo(card.owner.hand)
    elif card.Name == "Wendy's Amulet":
        Events = [e for e in card.owner.piles['Discard Pile']
        if e.Type == "Event"]
        if Events:
            if not "Advanced." in card.Text:
                topMostEvent = str(Events[0].name)
                whisper("Topmost event is {}.".format(Events[0]))
                if 1 == askChoice("Play the topmost event of your discard pile ?", ["Yes","No"],["#000000","#000000"], customButtons = [topMostEvent]):
                    playCard(Events[0])
            elif 1 == askChoice("Play an event from your discard pile ?", ["Yes","No"],["#000000","#000000"]):
                dlg = cardDlg(Events)
                dlg.title = "Wendy's Amulet"
                dlg.text = "Select an Event:"
                dlg.min = 1
                dlg.max = 1
                event = dlg.show()
                if event is not None:
                    notify("{} uses {} to play an event from their discard pile".format(card.owner, card))
                    playCard(Events[0])
        else: whisper("No events in the Discard Pile")
    elif card.Name == "William Yorick" and card.Type == "Investigator":
        choice_list = ['Trigger Elder Sign','Play an asset from discard']
        color_list = ['#46453E','#46453E']
        sets = askChoice("William Yorick", choice_list, color_list)
        if sets == 0:
            return
        if sets == 1:
            list = [c for c in card.owner.piles['Discard Pile']]
            if list:
                dlg = cardDlg(list)
                dlg.title = "William Yorick"
                dlg.text = "Choose 1 card to return to your hand:"
                dlg.min = 1
                dlg.max = 1
                cardToPlay = dlg.show()
                if cardToPlay:
                    cardToPlay[0].moveTo(card.owner.hand)
                    notify("{} uses {} elder sign to return {} to their hand".format(card.owner, card, cardToPlay[0]))
        if sets == 2:
            list = [c for c in card.owner.piles['Discard Pile']
                if c.Type == "Asset"]
            if list:
                dlg = cardDlg(list)
                dlg.title = "William Yorick"
                dlg.text = "Choose 1 asset to play from your discard:"
                dlg.min = 1
                dlg.max = 1
                cardToPlay = dlg.show()
                if cardToPlay:
                    x, y = firstInvestigator(card.owner).position
                    x += Spacing
                    y += Spacing
                    notify("{} uses {} to play {} from their discard pile".format(card.owner, card, cardToPlay[0]))
                    cardToPlay[0].moveToTable(x, y)
                    checkBoosts(card.owner)
            else:
                whisper("No assets in your discard")
    elif card.Name == "Patrice Hathaway" and card.Type == "Investigator":
        if 1 == askChoice("Trigger Elder Sign ?", ["Yes","No"],["#000000","#000000"]):
            dlg = cardDlg(card.owner.piles['Discard Pile'])
            dlg.title = "Patrice Hathaway"
            dlg.text = "Choose 1 card to leave in the discard:"
            dlg.min = 1
            dlg.max = 1
            leave = dlg.show()
            if leave is not None:
                for c in card.owner.piles['Discard Pile']:
                    if c != leave[0]:
                        c.moveTo(card.owner.deck)
                shuffle(card.owner.deck)
    elif card.Name == "Silas Marsh" and card.Type == "Investigator":
        if 1 == askChoice("Trigger Elder Sign ?", ["Yes","No"],["#000000","#000000"]):
            skills = [c for c in card.owner.piles['Discard Pile']
            if c.Type == "Skill"]
            dlg = cardDlg(skills)
            dlg.title = "Silas Marsh"
            dlg.text = "Choose 1 skill card to commit:"
            dlg.min = 1
            dlg.max = 1
            skill = dlg.show()
            if skill is not None:
                skill[0].moveToTable(card.position[0], card.position[1] - 100)
                skill[0].select()
    elif card.Name == "Salvage":
        items = [c for c in card.owner.piles['Discard Pile'] if
         "Item." in c.Traits]
        if items:
            dlg = cardDlg(items)
            dlg.title = "Salvage"
            dlg.text = "Select a card to play or remove from the game:"
            dlg.min = 1
            dlg.max = 1
            cardsSelected = dlg.show()
            if cardsSelected:
                c = cardsSelected[0]
                choice_list = ['Remove from the game','Play']
                color_list = ['#000000','#000000']
                sets = askChoice("Choose an option:", choice_list, color_list)
                if sets == 0:
                    return
                if sets == 1: #Remove for resources
                    Investigator(card.owner).markers[Resource] += int(c.Cost)
                    notify("{} uses {} to remove {} from the game and gain {} resources.".format(card.owner, card, c, c.Cost))
                    c.delete()
                if sets == 2: #Play
                    playCard(c)
                    notify("{} uses {} to play {} from their discard pile.".format(card.owner, card, c))
#############################################
#                                           #
#           Neutral Cards                   #
#                                           #
#############################################      
    elif card.Name == "Eldritch Tongue":
        parleyEvents = [c for c in card.owner.piles['Discard Pile']
            if c.Type == "Event" and "Parley." in c.Text]
        if parleyEvents:
            dlg = cardDlg(parleyEvents)
            dlg.title = "Eldritch Tongue"
            dlg.text = "Select a card to play"
            dlg.min = 1
            dlg.max = 1
            cardsSelected = dlg.show()
            if cardsSelected:
                c = cardsSelected[0]
                playCard(c)
                if c.group == table:
                    c.Subtype += "RemoveFromGame"
                    card.markers[Resource] -= 1
                    notify("{} uses {} to play {} from their discard pile".format(card.owner, card, c))
    elif card.Name == "Backpack" and card.Level == "0":
        attachTo(card)        
        searchTopDeck(card.owner.deck, table, 6, traits="Item,Supply")
    elif card.Name == "Backpack" and card.Level == "2":
        attachTo(card)    
        searchTopDeck(card.owner.deck, table, 12, traits="Item,Supply")
    elif card.Name == "Calling in Favors":
        notify("{} uses {} to search their deck for an Ally and play it.".format(card.owner, card))        
        searchTopDeck(card.owner.deck, table, 9, traits="Ally")
    elif card.Name == "Anna Kaslow":
        notify("{} uses {} to search their deck for a Tarot and put it in play.".format(card.owner, card))        
        searchTopDeck(card.owner.deck, table, traits="Tarot")
    elif card.Name == "Lucid Dreaming":
        searchTopDeck(card.owner.deck, card.owner.hand)
    elif card.Name == "Tekeli-li":
        remoteCall(specialDeck().controller, "toBottomMove", [card, specialDeck()])
        notify("{} is placed on the bottom of the Tekeli-li deck".format(card.name))
    elif card.Name == "Favor of the Moon":
        if card.Subtype != "Locked":
            sealXCurse(card, 3)
        elif 1 == askChoice("Trigger Favor of the Moon ?", ["Yes","No"],["#000000","#000000"]):
            exhaust(card, x=0,y=0)
            table.create('81df3f18-e341-401d-a6bb-528940a9c39e', ChaosTokenX, ChaosTokenY, quantity = 1, persist = True)
            card.markers[Curse] -= 1
            if not card.markers[Curse]:
                notify("{} has no Curse tokens left and is discarded.".format(card))
                discard(card)
            Investigator(card.owner).markers[Resource] += 1
    elif card.Name == "Favor of the Sun":
        if card.Subtype != "Locked":
            sealXBless(card, 3)
        elif 1 == askChoice("Trigger Favor of the Sun ?", ["Yes","No"],["#000000","#000000"]):
            exhaust(card, x=0,y=0)
            table.create('360db0ee-c362-4bbe-9554-b1fbf101d9ab', ChaosTokenX, ChaosTokenY, quantity = 1, persist = False)
            card.markers[Bless] -= 1
            if not card.markers[Bless]:
                notify("{} has no Bless tokens left and is discarded.".format(card))
                discard(card)
    elif card.Name == "Collected Works of Poe": # Automation doesn't account for location
        subResource(card, x, y)
        choice_list, color_list = InvestigatorList()
        sets = askChoice("Choose a player at your location:", choice_list, color_list)
        if sets == 0:
            return
        else:
            chosenPlayer = getPlayers()[sets - 1]
            notify("{} uses {} to let {} search the top 6 cards of their deck for Tekeli-li cards.".format(card.controller, card, chosenPlayer))
            if len(chosenPlayer.deck) < 6:
                count = len(chosenPlayer.deck)
            else:
                count = 6
            remoteCall(chosenPlayer, "searchTopDeck", [chosenPlayer.deck, table, count])
            update()
            for c in table:
                if c.Name == "Tekeli-li":
                    remoteCall(specialDeck().controller, "toBottomMove", [c, specialDeck()]) 
    elif card.set == "Edge of the Earth Campaign Expansion" and card.Type == "Scenario":
        if 1 == askChoice("Randomly kill an expedition member ?", ["Yes","No"],["#000000","#000000"]):
            cards = queryCard({"Encounter Set":"Expedition Team"})
            for m in cards:
                shared.piles['Temporary Shuffle'].create(m)
            expeditionTeam = [c for c in shared.piles['Temporary Shuffle']]
            dlg = cardDlg(expeditionTeam)
            dlg.title = "Expedition Team"
            dlg.text = "Select the DEAD members"
            dlg.min = 0
            dlg.max = 8
            dead = dlg.show()
            alive = [c for c in expeditionTeam if c not in dead]
            if alive:
                notify("Randomly killed : ")
                notify("{}".format(alive[rnd(0,len(alive)-1)]))
            for c in expeditionTeam:
                c.delete()
    elif card.set == "The Scarlet Keys Campaign Expansion" and card.Type == "Scenario":
        if 1 == askChoice("Generate the Red Coterie members ?", ["Yes","No"],["#000000","#000000"]):
            coterie = queryCard({"Encounter Set":"Red Coterie"})
            for c in coterie:
                encounterDeck().create(c)
            dlg = cardDlg(c for c in encounterDeck() if c.properties["Encounter Set"] == "Red Coterie")
            dlg.title = "You haven't seen the last of:"
            dlg.text = "Select 1 or more cards"
            dlg.max = len(coterie)
            members = dlg.show()
            if members:
                member = members.pop(rnd(0,len(members)-1))
                for c in encounterDeck():
                    if c.name != member.name and c.properties["Encounter Set"] == "Red Coterie":
                        c.delete()
                encounterDeck().shuffle()
                notify("1 Red Coterie member shuffled into the encounter deck.")
    elif card.set == "Undimensioned and Unseen" and card.Type == "Scenario":
        location = locationDeck()[rnd(0,5)]
        notify("{}".format(location))
    elif card.Name == "Mine Cart":
        turn = askChoice("Rotate", ["Left","Right"],["#000000","#000000"])
        if turn == 1: # Left
            rotateLeft(card)
        elif turn == 2:
            rotateRight(card)


    else:
        exhaustcard = re.search(r'[Ee]xhaust\s(X\s)?' + card.Name + r's?', card.Text)
        if exhaustcard:
            exhaust(card, x, y)

    
#############################################
#                                           #
#           Mythos Cards                    #
#                                           #
#############################################   
def shuffleTekelili(group=None, x=0, y=0):
    if len(specialDeck()) > 0:
         if specialDeck()[0].Name == "Tekeli-li":
            if len(getPlayers()) > 1:
                choice_list, color_list = InvestigatorList()
                sets = askChoice("Tekeli-li shuffle into:", choice_list, color_list)
                if sets == 0:
                    return
                specialDeck().controller = getPlayers()[sets - 1]
                rnd(0,1000)
                remoteCall(getPlayers()[sets - 1],"moveTekelili",[getPlayers()[sets - 1]])
            else:
                moveTekelili(me)
    else:
        whisper("The Tekeli-li deck is empty!")

def moveTekelili(player):
    specialDeck()[0].moveTo(player.deck)
    shuffle(player.deck)
    notify("{} shuffles a Tekeli-li card into their deck.".format(player))

#############################################
#                                           #
#           Character Cards                 #
#                                           #
#############################################      
def SefinaOpening(player):
    global cardToAttachTo
    drawMany(player.deck, 13)
    removeWeaknessCards()
    Sefina = [card for card in table
            if card.Name == "Sefina Rousseau" and card.Type == "Investigator" and card.owner == player]
    attachTo(Sefina[0])
    eventsToShow = [card for card in player.hand
            if card.Type == "Event"]
    dlg = cardDlg(eventsToShow)
    dlg.title = "Sefina Rousseau"
    dlg.text = "Select up to 5 events to attach to place under Sefina:"
    dlg.min = 0
    dlg.max = 5
    cardsSelected = dlg.show()
    if cardsSelected != None:
        inc = 0
        for card in cardsSelected:
            card.moveToTable(cardToAttachTo[0], cardToAttachTo[1])
            card.sendToBack()
            if len(cardsSelected) == 1:
                cardToAttachTo = None
            else:
                attachTo(card)
                inc += 1
                if inc == len(cardsSelected): # Resets cardToAttachTo
                    cardToAttachTo = None
    sizeHand = card.owner.counters['Maximum Hand Size'].value
    cardsInHand = len(card.owner.hand)
    if cardsInHand > sizeHand: #Hand Size Check
        discardCount = cardsInHand - sizeHand
        dlg = cardDlg(player.hand)
        dlg.title = "You have more than the allowed "+ str(sizeHand) +" cards in hand."
        dlg.text = "Select " + str(discardCount) + " Card(s):"
        dlg.min = 0
        dlg.max = discardCount
        cardsSelected = dlg.show()
        if cardsSelected is not None:
            for card in cardsSelected:
                discard(card)

def JoeOpening(player):
    for c in player.deck:
        if c.Name == "Unsolved Case":
            c.moveTo(player.piles['Secondary Deck'])
            break
    Insights = [card for card in player.deck
            if "Insight." in card.Traits and card.Type == "Event"]
    if len(Insights) < 10:
        whisper("Invalid Deck ! Not enough Insight events !")
        return
    dlg = cardDlg(Insights)
    dlg.title = "Hunch Deck"
    dlg.text = "Select 10 Insight events for your hunch deck:"
    dlg.min = 10
    dlg.max = 10
    cardsSelected = dlg.show()
    if cardsSelected is not None:
        for c in cardsSelected:
            c.moveTo(player.piles['Secondary Deck'])
        shuffle(player.piles['Secondary Deck'])
    player.piles['Secondary Deck'].viewState = "pile"