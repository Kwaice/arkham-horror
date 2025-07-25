def setupHelper():
    #Look for Scenario cards
    cards = []
    for c in setupDeck():
        if c.Type == "Scenario":
            cards.append(c)

    s = cards[0].model
#############################################
#                                           #
#             Path to Carcosa               #
#                                           #
#############################################
    if s == '0d7300da-ddb1-4d9b-81b0-ceab0a459f54': #Black Stars Rise
        stacks = [['fada603a-e868-4c93-9ada-1a2d61e9b43c','6b5e4477-4b8f-4913-b799-1d2e2b497f6c',
                   'ee818778-2024-4969-b030-0e5855802f96','2caaba71-47a4-4c07-b60f-298b7a9d7e87'],
                  ['255c32f0-5c83-41c1-adb6-50c0dddc5fb7','a4ad2173-5ec7-44ea-af72-a00d99a072bb',
                   'e5af2b0f-1c64-4419-bc1d-4f6b49b027fb','330ea796-9967-4d58-9331-c52a88235d66']]
        r = rnd(0,1)
        if r:
            use = stacks[1]
            rm = stacks[0]
        else:
            use = stacks[0]
            rm = stacks[1]

        for c in setupDeck():
            if c.model in rm:
                c.delete()
            elif c.model in use and c.Type == "Agenda":
                if c.name == "Let The Storm Rage":
                    c.moveTo(agendaDeck(), 1)
                else:
                    c.moveTo(actDeck(), 1)
        if len(cards) == 1:
            return #no Return To
        #Otherwise we are playing Return to
        stacks = [['d8d74a85-4a6a-48ed-a1fb-757426ff9345','65db3c0e-b915-4bec-b787-9171a354487d'],
                  ['f454e1fe-8169-4909-9c83-31ba37773e63','76a049da-5d39-419e-b38a-ed64382f1a9a']]
        r = rnd(0,1)
        for c in setupDeck():
            if c.model in stacks[r]:
                c.delete()
        north = ["53d6ccfb-ff2b-4227-b98e-a123b4b9b6b2","76a9d31a-7568-44ff-88f3-e1b6fb6b2a75"]
        wall = ["c946f0fc-fbf3-4bc1-9b16-b05336f7ef52","6582dde5-ac08-4e4a-9be3-323e57ccc4de"]
        steps = ["0697e1cf-7cb3-442b-a57c-6b29aa820ede","23975c27-fd1d-4506-a467-d5ea277c0eb4"]
        locations = [north,wall,steps]
        for l in locations:
            l.pop(rnd(0,1))
        for c in setupDeck():
            if any(c.model in l for l in locations):
                c.delete()

    elif s == '4f27752a-ef71-47c0-9b1e-2d4a192dd8af': #Curtain Call
        strangers = ['bcac7d95-9727-48a6-9637-8b1cea4e9d09','25789be3-7924-4834-bf85-093a010025a9','362b14dc-33b6-438f-a880-0e1de96d2d15']
        if len(cards) == 2: # Return to
            strangers.append('ed238e6a-e591-4c98-aaa9-44ffd35f7342')
            strangers.append("080cb3f3-a9dc-4938-ae4c-fdb1ee3fb56c")
            strangers.append('ee878704-4147-4543-b93c-d2b9b709115d')
        r = rnd(0,len(strangers)-1)
        strangers.remove(strangers[r])
        for c in actDeck():
            if c.model in strangers:
                c.delete()
        notify("Second act has been randomly chosen during the setup")

    elif s == "e748e010-c470-4757-913b-3cdbd22ead1d": # The Pallid Mask
        if 1 == askChoice("The Pallid Mask Setup",["You awoke inside the catacombs","You entered the catacombs on your own"],["#000000","#000000"]):
            #Random starting catacomb
            starting = locationDeck()[rnd(0,len(locationDeck())-1)]
            starting.moveTo(table)
            addResource(starting)
            for c in setupDeck():
                if c.alternateProperty("B", "Name") == "The Gate to Hell":
                    c.moveTo(locationDeck())
                    break
        if len(cards) == 2:
            for _ in range(4):
                locationDeck()[rnd(0,len(locationDeck())-1)].delete()
            notify("4 Catacombs have been removed at random during setup")
        locationDeck().visibility = "none"

    elif s == "d789bb63-a4a4-478c-800f-9b618b76d0d9": # Echoes of the Past
        ground = ["7a50f11d-59c1-4109-86c4-06d483df7891","b60cff3c-de68-440f-95a7-ad5f0563bff8","2eb3f14e-8a82-44e3-8919-83e505af71d8"]
        first = ["3c1beb7e-4080-45e9-bc25-fbedb75586bc","8bf4b009-1ba2-4535-804c-d1df7b8bc01a","a46dd824-28ef-4e50-a08b-6615f606e9d5"]
        second = ["92d52f13-6801-4c56-92dd-871fe8eddb17","f40bcedc-8679-4525-b267-8acda4017da9","993bb8e9-34d5-40c3-a203-16527e8041b5"]
        ground = ground.pop(rnd(0,2))
        first = first.pop(rnd(0,2))
        second = second.pop(rnd(0,2))
        locations = [ground, first, second]
        if len(cards) == 2:
            basement = ["2f8afca9-39c3-47d7-b3e5-d808d7295e8b","3f365f4d-9dfb-4f71-a5e2-9f05f6265461","0fcd3a8c-9791-4b7c-8f29-ab196bb68c89"]
            basement = basement.pop(rnd(0,2))
            locations.append(basement)

        for c in setupDeck():
            if c.model in locations:
                c.delete()
            elif c.Type == "Location" and c.Name not in ["Quiet Halls","Entry Hall"]:
                c.moveTo(locationDeck())

    elif s == "195987b5-9d93-41ef-be97-6c53e31abb47": # Unspeakable Oath
        asylum1 = ["b337f881-96c3-47c2-8809-b3c2d25e6ec40","118a89f4-9f3f-4500-a4e7-4ccdad37ad24"]
        asylum2 = ["e85a3cc5-276b-4a43-bb1d-f7c5db005720","48039487-b26d-4f47-bfdd-e67fb4243890"]
        asylum1 = asylum1.pop(rnd(0,1))
        asylum2 = asylum2.pop(rnd(0,1))
        for c in setupDeck():
            if c.model in asylum1 or c.model in asylum2:
                c.delete()

    elif s == "2f2b29d1-5d89-4249-9a09-3e84d24f7590": # Phantom of Truth
        Montmartre = ["96eca2b7-5f82-42a0-a4c8-58b5fe7fda73","4987715d-a84d-4380-a478-3ad0b1ac0bfa"]
        Opera = ["a1e75f9c-befb-4cfb-aab4-5397f8f62c81","c5d57cb3-ceb7-4c8b-800e-818d65414cc0"]
        Marais = ["83e73174-af32-4f5a-be59-24013a471171","0a3df1e4-0f7b-43de-be8a-808f2008f1a1"]
        Montparnasse = ["495872f9-5461-435b-bd1b-f830279b18bc"]
        Guignol = ["42ae82fa-d26b-4b30-ae93-7cc3f2b81cea"]
        Cemetery = ["05f0bf91-29ce-4925-8e3e-38d3b03e2542"]
        Canal = ["cc707388-cd37-4fbd-a38d-b4ef160569d2"]
        NotreDame = ["945d67fb-f8f4-4fe1-b646-9a2894acda75"]
        Luxembourg = ["095ec4ac-d52e-4893-808d-acdaf9d97e47"]
        Gare = "851280fa-b807-493c-9c3d-048f70e8a05d"
        if len(cards) == 2: # return
            Montparnasse.append("a029b3dd-be49-4200-bb7a-e9135f261517")
            Guignol.append("b5186fd0-6adb-43be-ad2e-796edd4c2e56")
            Cemetery.append("40658768-c2ba-4232-9cef-77b9a3af790b")
            Canal.append("510420f2-b898-4467-a629-53afd946afab")
            NotreDame.append("a5b23b78-76ae-44d6-af03-b85e049c42a8")
            Luxembourg.append("db11be44-746d-4519-8fa9-4379b3d6d64d")
        Montmartre = Montmartre.pop(rnd(0,len(Montmartre)-1))
        Opera = Opera.pop(rnd(0,len(Opera)-1))
        Marais = Marais.pop(rnd(0,len(Marais)-1))
        Montparnasse = Montparnasse.pop(rnd(0,len(Montparnasse)-1))
        Guignol = Guignol.pop(rnd(0,len(Guignol)-1))
        Cemetery = Cemetery.pop(rnd(0,len(Cemetery)-1))
        Canal = Canal.pop(rnd(0,len(Canal)-1))
        NotreDame = NotreDame.pop(rnd(0,len(NotreDame)-1))
        Luxembourg = Luxembourg.pop(rnd(0,len(Luxembourg)-1))
        locations = [Montmartre, Opera, Marais, Montparnasse, Guignol, Cemetery, Canal, NotreDame, Luxembourg, Gare]
        for c in setupDeck():
            if c.Type == "Location" and (c.model not in locations):
                c.delete()
#############################################
#                                           #
#               Forgotten Age               #
#                                           #
#############################################
    elif s == '3e01c1d4-8e5c-472b-b803-357c6474ca01': #Threads of Fate
        ab = [['c8d55c59-96cd-438b-afaa-366bfe19730c','896613e6-b4a2-488a-8460-929df1a72bf4'],
              ['c6b3c676-8d25-46d4-a43c-898324bbd6e0','d2aff041-a1f8-4b31-a630-651661ac22fc'],
              ['da71f372-8c2b-4616-aae2-008483386f6a','7a519eb0-846d-412d-8d23-bf773ec5b4a3'],
              ['71fc4500-eaf7-43b1-b6b4-165248055cdf','aa707a76-33be-4960-9a91-ce58e22b7728']]

        a = askChoice("Check Campaign Log",
                      ["Alejandro recovered the Relic of Ages","The investigators gave custody of the relic to Alejandro","The investigators gave custody of the relic to Harlan Earnstone"],
                      ["#000000","#000000","#000000"])
        if not a:
            return
        if a < 3:
            a = 0
        else:
            a = 1

        r = rnd(0,1)
        for c in actDeck():
            if c.model == ab[0][a] or c.model in ab[a+1]:
                c.delete()
            if a and c.model == ab[1][r]:
                c.delete()
            if not a and c.model == ab[2][r]:
                c.delete()
            if c.model == ab[3][r]:
                c.delete()

        cd = [['7a75e4c5-445e-4159-925f-957163e47e29','1a414a99-25cc-4ec4-8463-c7301a87e6e9'],
              ['a5a42d27-9725-4218-b8d3-eccb2523cd7c','4d53700c-093c-40fe-8019-4f88be99fe4e'],
              ['10a58a3d-9813-4947-8737-88f77b3e7a9a','c18e7c75-2d45-4e81-9df6-2d4a738c0992'],
              ['a67d45ac-5e24-4742-878c-4a5abab74085','7dbfd611-3f62-4dca-ad0d-2613b1ce58a7']]

        a = askChoice("Choose one",
                      ["Go to the Police to inform them about Alejandro's disappearance","Look for Alejandro on your own"],
                      ["#000000","#000000"])
        if not a:
            return
        a -= 1
        r = rnd(0,1)
        for c in actDeck():
            if c.model == cd[0][a] or c.model in cd[a+1]:
                c.delete()
            if a and c.model == cd[1][r]:
                c.delete()
            if not a and c.model == cd[2][r]:
                c.delete()
            if c.model == cd[3][r]:
                c.delete()

        ef = [['9055bfa1-1073-4150-8106-3a7de023f891','219d4017-96f6-4196-a72b-18330def361a'],
              ['1e0e7df5-4c67-42e4-b1c6-74f4805da1fd','dfd302e9-57ac-44ae-a817-54d195dc167f'],
              ['74372f0c-0743-4e05-a8bc-18502b57c988','9ce3c434-b63a-42d7-b986-4f502bbd5c52'],
              ['e5189103-fa67-4b13-8d55-673260fa4d8a','41c0621d-986b-454f-983a-868dc9d21330']]

        a = askChoice("Ichtaca's tale",
                      ["You listened to Ichtaca's tale","Ichtaca left without you"],
                      ["#000000","#000000"])
        if not a:
            return
        a -= 1
        r = rnd(0,1)
        for c in actDeck():
            if c.model == ef[0][a] or c.model in ef[a+1]:
                c.delete()
            if a and c.model == ef[1][r]:
                c.delete()
            if not a and c.model == ef[2][r]:
                c.delete()
            if c.model == ef[3][r]:
                c.delete()

        if len(cards) == 1:
            return #no Return To
        #Otherwise we are playing Return to
        gh = [['6986f0ca-fc8e-420e-ae92-6410fab73785','3faf9ca8-2d4a-4327-b365-2332cbf76401'],
              ['33b24489-91a6-4eae-9164-082b357abd14','24bf56dc-3b0f-45db-b633-6428a5ffd784'],
              ['af6113e6-6f03-4685-824f-11016b51b50f','2ac2cfc8-aa2b-406b-a950-1a273d7cb1cf'],
              ['9b2376a8-7317-4652-9f61-ff31c7d15e0b','0d36127e-b441-4f49-af22-7bf13aaa0253']]

        a = askChoice("Choose one",
                      ["Find the Source named in the Advertiser's story","Find the root of the problem"],
                      ["#000000","#000000"])
        if not a:
            return
        a -= 1
        r = rnd(0,1)
        for c in actDeck():
            if c.model == gh[0][a] or c.model in gh[a+1]:
                c.delete()
            if a and c.model == gh[1][r]:
                c.delete()
            if not a and c.model == gh[2][r]:
                c.delete()
            if c.model == gh[3][r]:
                c.delete()
    elif s == "6ea63fe0-6d47-49f8-aded-c891b70b6c63": # The Untamed Wilds
        if len(cards) == 2:
            l1 = ["b7b888ce-c247-4faf-9c0b-cb0908273f97","349742df-827a-4e18-9f0b-dd730e279ecb"]
            l2 = ["bd95f839-567b-4b3c-9720-0015498baaf8", "76498aac-ea82-4071-9d64-cebedeca1134"]
            l3 = ["1666bdb1-e21b-4f02-b4b3-564593f2181f","4cdb49bb-31ba-4767-89e5-689c9f6db133"]
            l4 = ["db538e9b-2c4e-4416-b41a-0c5972d46bd9","1c29d2f3-a5a8-4a37-997e-1d28dc399a33"]
            base = [l1,l2,l3,l4]
            l1 = l1.pop(rnd(0,1))
            l2 = l2.pop(rnd(0,1))
            l3 = l3.pop(rnd(0,1))
            l4 = l4.pop(rnd(0,1))
            locations = [l1,l2,l3,l4]
            for c in secondspecialDeck():
                if any(c.model in l for l in base):
                    c.delete()
                elif c.model in locations:
                    c.moveTo(locationDeck())
        locationDeck().visibility = "none"

    elif s == "1a76e271-589d-4e28-8d0e-015c4c81ebbc": # Hearts of the Elders part 1
        if any("The Jungle's Heart" in c.Name for c in agendaDeck()):
            ruins = ["c09da216-9316-4598-a4fa-d045889e367b","37b7a822-5ccc-4939-9810-f3f03cf8c6c2","52025ebe-feb2-4d76-b420-be511c642bf1"]
            ruin = ruins.pop(rnd(0,2))
            for c in secondspecialDeck():
                if c.model in ruins:
                    c.delete()
            if len(cards) == 2: # Return to
                l1 = ["b7b888ce-c247-4faf-9c0b-cb0908273f97","349742df-827a-4e18-9f0b-dd730e279ecb"]
                l2 = ["bd95f839-567b-4b3c-9720-0015498baaf8","76498aac-ea82-4071-9d64-cebedeca1134"]
                l3 = ["1666bdb1-e21b-4f02-b4b3-564593f2181f","4cdb49bb-31ba-4767-89e5-689c9f6db133"]
                l4 = ["db538e9b-2c4e-4416-b41a-0c5972d46bd9","1c29d2f3-a5a8-4a37-997e-1d28dc399a33"]
                base = [l1,l2,l3,l4]
                l1 = l1.pop(rnd(0,1))
                l2 = l2.pop(rnd(0,1))
                l3 = l3.pop(rnd(0,1))
                l4 = l4.pop(rnd(0,1))
                locations = [l1,l2,l3,l4]
                for c in secondspecialDeck():
                    if c.model in locations:
                        c.moveTo(locationDeck())
                    elif any(c.model in l for l in base):
                        c.delete()
            for c in secondspecialDeck():
                if c.model in ruin:
                    ruin = c
                    break
            if 1 == askChoice("The investigators mapped out the way forward ?",["Yes","No"],["#000000","#000000"]):
                ruin.moveTo(table)
            else: ruin.moveTo(locationDeck())
        elif any("The Lonely Caverns" in c.Name for c in agendaDeck()): # Part 2
            if len(cards) == 2: # Return to
                l1 = ["0f666fd7-4793-4812-a921-c3b427d4d1f1","dc233585-ff6b-4acd-8274-b37e62eb6d4f"]
                l2 = ["33b5d9ed-a1cd-49ad-bdc9-bb20aac1f55f","2b2a910b-fa55-493e-ad89-a1d5157efe76"]
                l3 = ["2b2a910b-fa55-493e-ad89-a1d5157efe76","aa5b4fb3-f7cc-4e5a-9242-4ed8952cef57"]
                l4 = ["1d1a577e-ac74-4865-bcf9-a6942e3d30f5","33a12c23-8414-45a5-b0a8-e1f8027684e3"]
                base = [l1,l2,l3,l4]
                l1 = l1.pop(rnd(0,1))
                l2 = l2.pop(rnd(0,1))
                l3 = l3.pop(rnd(0,1))
                l4 = l4.pop(rnd(0,1))
                locations = [l1,l2,l3,l4]
                for c in secondspecialDeck():
                    if c.model in locations:
                        c.moveTo(locationDeck())
                    elif any(c.model in l for l in base):
                        c.delete()
        locationDeck().visibility = "none"
#############################################
#                                           #
#             Dunwich                       #
#                                           #
#############################################
    elif s == 'b08a7c06-5d1b-4bcb-b207-ff248bcf634d': # Extracurricular Activity
        if len(cards) == 2:
            triangle = ["4ff2fd3f-fa5c-41f0-87c9-6408cc8dbf6d","7fbec8f4-d389-4249-8b5c-aa86ee49cd38"]
            t = triangle.pop(rnd(0, 1))
            for c in setupDeck():
                if c.model in t:
                    c.delete()

    elif s == '293a7805-47b3-41a8-96af-14bcb19f93f7': # The House Always Wins
        if len(cards) == 2:
            lounge = ["6b14f253-95a4-4dbe-819d-afb8bdba7fbf","7ab63941-b149-4aaf-98de-704e97b07070"]
            t = lounge.pop(rnd(0, 1))
            for c in setupDeck():
                if c.model in t:
                    c.delete()
    
    elif s == '28c2a525-24cd-4069-bdc6-f97e4031a656': # Blood on the Altar
        bishop = ["6b110514-f482-490e-b3e5-d7b96c575b7a","4d7ef39b-570f-4b93-853b-f4570e4e95a9"]
        ruins = ["49cd47ae-cc2a-4f7f-bf4a-b8bc4f386196","b8dc246f-c196-47d9-9c09-746c1565ec79"]
        osborn = ["b0b080ab-d255-43fc-b5da-2e1d76901d38","a5a2c5c1-f6d6-40a5-8330-26bcda3e3479"]
        church = ["0c7bdb0a-e12e-43e9-a0da-b4aa7fe56164","b4eeeeda-f04f-4062-a820-50c7d7d78b49"]
        house = ["d5324db3-3a33-4881-967f-d71b2c29ea7c","f61cd747-b294-4725-9ff8-b02b7c5bbcdf"]
        school = ["6f988818-7adc-4736-aafc-d6882c42adcd","88a10412-58ac-49c6-888c-a1397baba22d"]
        if len(cards) == 2: #return
            bishop.append("07c26c59-f752-4300-bd1d-5b637c497f42")
            church.append("5197081e-569a-4093-802f-8e4f22f592d9")
            school.append("d7ec503a-473a-4f3f-87dc-b76caf8454b9")
            osborn.append("73664ed1-d664-4a91-8c09-8e2cac562424")
            ruins.append("343b7334-2bdd-49f6-90f5-6f4549dc3abf")
            house.append("c29a7228-7b52-47d8-bc05-3160f1c6445b")
        bishop = bishop.pop(rnd(0,len(bishop)-1))
        church = church.pop(rnd(0,len(church)-1))
        school = school.pop(rnd(0,len(school)-1))
        osborn = osborn.pop(rnd(0,len(osborn)-1))
        ruins = ruins.pop(rnd(0,len(ruins)-1))
        house = house.pop(rnd(0,len(house)-1))
        locations = [bishop, church, school, osborn, ruins, house]
        locations.remove(locations[rnd(0,5)])
        for c in setupDeck():
            if c.Type == "Location" and (c.Name != "Village Commons") and (c.model not in locations):
                c.delete()

    elif s == "f35868ff-263e-4a06-91d4-49fb17e22700": # Miskatonic
        if len(cards) == 2: # Return to
            for _ in range(2):
                locationDeck()[rnd(0,len(locationDeck())-1)].delete()
        notify("Exhibit Halls have already been randomized.")

        security = ["1558f7ef-ed17-4c45-90dd-9ca90e428a18","4940ec52-e8c5-4d39-9ef4-e1705843a082"]
        administration = ["75af5ab5-15c4-419d-98c8-47186cf79fa4","bb44f38a-06a8-4889-8be6-0511504199b5"]
        security = security.pop(rnd(0,1))
        administration = administration.pop(rnd(0,1))
        for c in setupDeck():
            if c.model in security or c.model in administration:
                c.delete()
        notify("Security and Administration locations have been randomly picked.")

    elif s == "40b38553-7230-4d42-a49a-6a0642043795": # The Essex County Express
        cars = ["eaa8917a-54ff-4331-a871-e76b08991946","077e592c-dce6-4c53-9884-c4e48c808040","a53c0178-2f86-4181-b10c-ed7fc19a3d22","d55e31c2-01e5-453b-bbc5-10f40b7378b7","2a28733d-97b3-4fd7-a622-d324b88b4c5f","185db0e8-83d8-4eb1-893e-efc8fc29957c","54373a69-f67d-411e-871f-da380d1a0f6f","dbacf932-2cdc-41b0-b66e-0e1bc1b27ea6"]
        engines = ["f9a869b9-eaba-4399-a2fc-028f4405ffe2","3188db25-0991-49a3-85ec-649aa625d496","b0945cec-dda6-49de-b46f-863e00c340e9"]
        if len(cards) == 2: #Return
            cars.extend(["a152582d-bd8f-48ee-9939-7e8383067d95","0fa20844-7237-4ff4-be80-0f31fe6accfc"])
            engines.append("c81f849a-64d5-4444-bc1a-314870e5ba56")
            notify("Automatically randomized locations for Return to")
        pickCars = []
        pickEngine = []
        for _ in range(6):
            pickCars.append(cars.pop(rnd(0,len(cars)-1)))
        pickEngine.append(engines.pop(rnd(0,len(engines)-1)))
        for c in setupDeck():
            if (c.Name == "Train Car" and c.model not in pickCars) or (c.Name == "Engine Car" and c.model not in pickEngine):
                c.delete()
            elif (c.Name == "Train Car" and c.model in pickCars) or (c.Name == "Engine Car" and c.model in pickEngine):
                c.moveTo(locationDeck())
        notify("Train cars and engines have been automatically randomized")

    elif s == "ab96d62c-14e4-39c4-d955-40a6c1e9928c": # Undimensioned and Unseen

        village = ["c1d5868b-aef1-3882-5ebc-ea834ef47bb3","95fa8c11-b1bb-31fe-8635-f069109a05da"]
        glen = ["801efeb6-d38d-39ca-79fd-55308253777c","b88ffce0-0506-341a-9ccd-1f3cd44846ed"]
        meadow = ["70743e57-162c-358f-225e-1198e23f43f2","570aa337-9cd2-3184-40c7-5c3a91dd1517"]
        blasted = ["b3481c64-4e50-302c-b557-81bab39e044b","16e6efe0-2ed2-3d90-6ba1-6262f05231b8"]
        ruins = ["77cafa34-0d3b-366d-47e1-5614a5e7291c","19139758-ff4e-3728-7bd9-8524b115a0e2"]
        devil = ["133dea2e-5ded-3c05-59f7-4a7ba47256b3","d7ff2904-e1fd-3c21-bccc-207ac14bf965"]

        village = village.pop(rnd(0,1))
        glen = glen.pop(rnd(0,1))
        meadow = meadow.pop(rnd(0,1))
        blasted = blasted.pop(rnd(0,1))
        ruins = ruins.pop(rnd(0,1))
        devil = devil.pop(rnd(0,1))

        locations = [village, glen, meadow, blasted, ruins, devil]

        for c in setupDeck():
            if c.model in locations:
                c.moveTo(locationDeck())

    elif s == "03fe08bf-2232-336d-c9b6-2eb4d6d7cbab": # Where Doom Awaits
        altered = ["c7b0add2-3f51-3956-2de1-e41cdbb7bcf5","7fd45260-1c98-3d6a-feb0-2689ff51e1c4","25b6e5e5-a0cf-3fdb-252b-1dd2e676d2c0"]
        diverging = ["8ff015b2-9c54-3500-e748-9496efb74949","37f30f94-f621-3b6e-b8f9-9da7404504d6","c366685d-37e4-3b81-6c4e-37797290dea1"]
        if len(cards) == 2:
            altered.extend(["ba8e0fa8-e151-3a57-f1d0-7707cc7e8f7c","f29036d6-eb41-433e-af3a-6f4ac14a2429"])
            diverging.extend(["4bdb897e-7b25-3990-420c-8f629cd15c6b","10ad9b62-60a3-46b2-bfa7-98cd0810a68a"])

        altered.remove(altered[rnd(0,len(altered)-1)])
        diverging.remove(diverging[rnd(0,len(diverging)-1)])
        if len(cards) == 2:
            altered.remove(altered[rnd(0,3)])
            diverging.remove(diverging[rnd(0,3)])

        for c in secondspecialDeck():
            if c.Type == "Location":
                if c.model not in altered and c.model not in diverging:
                    c.delete()
        for c in secondspecialDeck():
            if c.Type == "Location":
                c.moveTo(locationDeck())

####################################
#######       TCU         ##########
####################################

    elif s == "ea36d8dc-fefc-43d2-93e5-6fe903c7ee4a": # The Witching Hour
        nbWoods = len([c for c in setupDeck() if c.Name == "Witch-Haunted Woods"])
        for _ in range(nbWoods - 5):
            indexWoods = [i for i in range(len(setupDeck())) if "Witch-Haunted Woods" in setupDeck()[i].Name]
            i = indexWoods[rnd(0,len(indexWoods)-1)]
            setupDeck()[i].delete()
        for c in setupDeck():
            if c.Name == "Witch-Haunted Woods":
                c.moveTo(locationDeck())

    elif s == "a263c7a7-7641-479b-bb07-926c93371e15": # The Wages of Sin
        gallows = ["e22800b9-b238-4887-8289-35cf0c978363","028d377a-a1ad-44ee-91f7-ee1baa5210c2"]
        graves = ["68d6765d-2d4d-4882-be2a-9d569ef2e662","d54acf40-23db-4210-bd8d-a1aa9ee84ad1"]
        crypt = ["4adf6b60-a149-458e-b677-fb9c1662d719","949842f1-b1f1-46da-8656-0357e77df332"]
        attic = ["8b5a93f4-6782-4263-92cd-0c141e6ffb7d","ea209a3c-ba80-469e-9966-f01d35a550d1"]
        locations = [gallows, graves, crypt, attic]
        if len(cards) == 2: # Return to
            hangman = ["3353c57b-4def-4ddb-93bc-5c58ec8be27c","86b08ac8-715e-4c28-a6a4-aca1a38f65e9"]
            locations.append(hangman)
        for l in locations:
            l.remove(l[rnd(0,1)])
        for c in setupDeck():
            if any(c.model in l for l in locations):
                c.delete()

        notify("Locations have been randomly chosen")

        nbHeretic = len([c for c in secondspecialDeck() if c.Name == "Heretic"])
        for _ in range(nbHeretic - 4):
            indexHeretics = [i for i in range(len(secondspecialDeck())) if "Heretic" in secondspecialDeck()[i].Name]
            i = indexHeretics[rnd(0,len(indexHeretics)-1)]
            secondspecialDeck()[i].delete()
        shuffle(secondspecialDeck())
        notify("Heretics have already been randomized")
    
    elif s == "af187725-013f-47b5-8f23-36439c776663": # In the Clutches of Chaos
        french = ["5b1b97df-7bc1-42e8-aa55-c45ab8e4129d","96e24b77-d561-4726-a36a-fdc0c8d14cea"]
        rivertown = ["a98aea8f-073e-41e0-a739-78599ece71b2","4c511cf5-07d3-4c4a-94ac-f3b392d863b8"]
        southside = ["939cecea-c846-4ffd-bb1b-39e848b75710","af069455-dd28-47ba-9e14-0c559695332b"]
        uptown = ["e8f91327-fe0a-4a84-b953-2e78bef56ac0","73b8bb44-802b-47ec-9bb8-ec31836671e7"]
        church = ["c2bb0fb9-fa46-4f7b-b33d-c0c0776050b8","94a14d03-9193-4f51-99dc-b08f8817d33c"]
        merchant = ["140e4849-4849-4cb8-9888-0d7647da8a50","8fc7e31e-9a02-4896-8c98-7f7202bbd4ee"]
        if len(cards) == 2:
            french.append("808efdba-610f-4683-b351-174fb6cebb33")
            rivertown.append("44341ac7-e4ea-4a7c-ba3f-44ca6dfccc6d")
            southside.append("31c1123a-b0fd-4a2f-9fff-2cf6639068d1")
            uptown.append("8357c994-e6f2-4bcc-86dd-2ee926027092")
            church.append("0c631f75-3130-418a-bf61-e553c3a3bb82")
            merchant.append("87dfbcf4-49b2-47a2-af19-c9cc3f3ba32a")
        locations = [french, rivertown, southside, uptown, church, merchant]
        for l in locations:
            l.pop(rnd(0,len(l)-1))
        for c in setupDeck():
            if any(c.model in l for l in locations):
                c.delete()

    elif s == "33bfb887-f781-43f9-a8a5-4677f811ca24" : # The Secret Name
        for _ in range(len(locationDeck())-6):
            locationDeck()[rnd(0,len(locationDeck())-1)].delete()
        notify("Unknown Places have been automatically randomly chosen")

    elif s == "37bb6382-1e06-43f8-98c1-9f4c46eae6ae": # For the Greater Good
        if len(cards) == 2: #Return
            lounge = ["d31e3e02-9b3b-476e-b37f-80a80480c6bd","d5380250-d0e7-4314-93ca-d109717c32c7"]
            lounge = lounge.pop(rnd(0,1))
            for c in setupDeck():
                if c.model in lounge:
                    c.delete()
                    break


####################################
####### Innsmouth         ##########
####################################

    elif s == "2c405797-c45b-4aa6-9ebf-2372c40641f0": # The Vanishing of Elina Harper
        suspects = ["e8d46363-6c2c-4b5b-a5f0-a383e2040b66","d5482954-c76e-4896-aa13-d234b8abcd4c","76c27387-96fd-4f9b-9195-cd15319705e7","e741caac-306b-4333-9822-b53c1ab377f4","1ca29b57-de4b-419d-b4f1-aae9951407ab","ebe93147-cad6-40d9-acc7-5e33f817b6d5","f9baf474-3eb5-402a-b890-7650269259f3","5c297695-9ed2-407f-8a3d-98713704851c","cac596cf-b4b7-4373-9613-021b9f489741"]
        hideouts = ["c3222800-fc66-4be0-9820-5beaba110878","783ba29e-a4fd-42a6-a589-7052a0c5a969","aca1cd78-f945-4e64-a0eb-712f4cffaf6d","59fdfe35-a045-4867-9aee-176d0111cd0a","8d11b6b4-7942-41f6-8ebe-7705419dd800","65f7bf50-bc13-46d7-a005-efdb8fa06d53"]
        if len(cards) == 1:
            suspect = suspects.pop(rnd(0,5))
        else: #Return to
            suspect = suspects.pop(rnd(0,8))
        hideout = hideouts.pop(rnd(0,5))

        for c in secondspecialDeck():
            if c.model in suspect or c.model in hideout:
                c.moveToTable(0, 0, True)
            elif c.model in suspects or c.model in hideouts:
                c.moveTo(locationDeck())
        locationDeck().visibility = "none"

    elif s == "1d4c41d9-5fed-46ef-8f22-0d4384cb713a": # Devil Reef
        ruins = [c for c in secondspecialDeck() if c.alternateProperty("B", "Name") == "Cyclopean Ruins"]
        grottos = [c for c in secondspecialDeck() if c.alternateProperty("B", "Name") == "Deep One Grotto"]
        temples = [c for c in secondspecialDeck() if c.alternateProperty("B", "Name") == "Temple of the Union"]
        ruin = ruins.pop(rnd(0,1))
        grotto = grottos.pop(rnd(0,1))
        temple = temples.pop(rnd(0,1))
        locations = [ruin, grotto, temple]
        for c in secondspecialDeck():
            if c in locations:
                c.delete()
        notify("Unfathomable Depths have been randomized")

    elif s == "04f948de-7ecd-4518-baab-436377114b48": # Horror in High Gear
        if len(cards) == 2: # Return to
            for _ in range(2):
                locationDeck()[rnd(0,len(locationDeck()))].delete()
            notify("2 random Innsmouth Road locations have been removed from the location deck.")

    elif s == "911eb331-94e6-4391-8a5c-21a9fd1e54bb": # The Lair of Dagon
        if len(cards) == 2: # Return to
            doorways = [c for c in secondspecialDeck() if c.Name == "Tidal Tunnel"]
            for _ in range(2):
                c = doorways.pop(rnd(0,len(doorways)-1))
                c.delete()
            doorways[0].moveTo(locationDeck())
            notify("2 Doorways to the Depth have been randomly removed")
####################################
####### TDE               ##########
####################################

    elif s == "003e29bb-e6d0-4c1c-bf00-42f4f60eca04": # Beyond the Gates of Sleep
        woods = [c.model for c in secondspecialDeck() if c.Name == "Enchanted Woods"]
        wood = woods.pop(rnd(0,6))
        for c in secondspecialDeck():
            if c.model in wood:
                c.delete()
                break

####################################
####### The Scarlet Keys  ##########
####################################

    elif s == "60da06a9-90df-4649-88e6-587aeae479d4": # Shades of Suffering
        shadow = ["6b427932-daf5-4dc5-84f0-16082976fd1c", "93c1ff18-70fc-4b8f-a739-d47005e66926"]
        miner = ["f7c00398-484f-46cc-8c19-3091d4a5dee2","e9cf0cdb-a2a5-4973-9834-e8022adfe197"]
        foreman = ["ce3caa43-5810-45b5-8520-0ab4d9d0ec4f","50c14dd5-dd3d-4ff3-b589-79ac948173dd"]
        shadow = shadow.pop(rnd(0,1))
        miner = miner.pop(rnd(0,1))
        foreman = foreman.pop(rnd(0,1))
        geists = [shadow, miner, foreman]
        for c in specialDeck():
            if c.model in geists:
                c.delete()

