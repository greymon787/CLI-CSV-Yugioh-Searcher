import csv
from argparse import ArgumentParser
from pprint import pprint

#Card looking class
class CardSearch:
    @staticmethod
    def CardLookerUpper(args):
        with open('ygo_cards.csv', 'r', encoding="utf8") as f:
            csvfile = csv.reader(f)
            items = []
            next(csvfile)
            for row in csvfile:
            #unpack row
                realname, name, lvl, attribute, cardtype, border, text, attack, defense = row
                
                #Card Text Filter
                if args.text:
                    userText = " ".join(args.text).lower()
                    if userText not in text and userText not in name:
                        continue
                
                #Name Filter 
                if args.name:
                    userText = " ".join(args.name).lower()
                    if userText not in name:
                        continue
                
                #Level filter
                if args.level:
                    if args.level not in lvl:
                        continue
                
                #Attribute Filter
                if args.attribute:
                    if args.attribute.lower() != attribute:    
                        continue
                
                #Card Type filter
                if args.type:
                    userText = " ".join(args.type).lower()
                    if userText not in cardtype:
                        continue
                
                #Card supertype/border filter
                if args.border:    
                    if args.border.lower() not in border:
                        continue
                
                #Attack filter
                if args.attack:
                    if args.attack != attack:
                        continue
                
                #Defense filter
                if args.defense:
                    if args.defense != defense:
                        continue
                
                #appends
                items.append(realname)

        if items:
            return list(set(items))
        else:
            return "No cards match"

class Deck:
    #Deck adder class
    def __init__(self):
        self.deck = []
    
    def AddtoDeck(self, givenname):
        #create card object, add card object to array
        flag = False  
        if givenname != "":
            with open('ygo_cards.csv', 'r', encoding="utf8") as f:
                    csvfile = csv.reader(f)
                    next(csvfile)
                    flag = True
                    for row in csvfile:
                        realName, name, lvl, attribute, cardType, border, text, attack, defense = row
                        if givenname.lower() == name:
                            card = Card(realName, lvl, attribute, cardType, border, text, attack, defense)
                            self.deck.append(card)   
                            break
                    else:  
                        card = Card(givenname)
                        self.deck.append(card) 
        return flag

    def RemoveFromDeck(self, givenname):
        flag = False
        for card in self.deck:
            if card.name.lower() == givenname.lower():
                self.deck.remove(card)
                flag = True
                break
        return flag

    def DeckStatus(self):
        deckSize = len(self.deck)
        if deckSize < 40:
            legality = "Illegal -> Less than 40 Cards"
        elif deckSize > 60:
            legality = "Illegal -> More than 60 cards"
        else:
            legality = "Legal"    
        return len(self.deck), self.deck, legality

    def CardStatus(self, objName):
        cardToFind = next((card for card in self.deck if card.name.lower() == objName.lower()), None)
        if cardToFind:
            return cardToFind
    
    def DeckExporter(self, deckname):
        with open(f'{deckname}.txt', 'w') as f:
            for card in self.deck:
                f.write(f"{card}\n")
        return "Deck exported successfully"
   
class Card:
    def __init__(self, name, level = None, attribute = None, cardtype = None, border = None, text = None, attack = None, defense = None):
        self.name = name
        self.level = level
        self.attribute = attribute
        self.cardtype = cardtype
        self.border = border
        self.text = text
        self.attack = attack
        self.defense = defense
    
    def __repr__(self):
        return f"{self.name!r}"
    
    def __str__(self):
        return self.name


def parse_args(arglist):
    """ Parse command-line. """
    parser = ArgumentParser(description='Prints Yu-Gi-Oh cards that match the description')
    #Default
    parser.add_argument('text', type=str, nargs='*', help='Text on card')
    #Filters
    parser.add_argument('-n', '--name', nargs='*',type=str, metavar='', help='Search with card name')
    parser.add_argument('-lvl', '--level', type=str, metavar='', help='Level, Rank, Link rating, and Pendulum Scale')
    parser.add_argument('-a', '--attribute', type=str, metavar='', help='Attribute (Wind, Fire, etc.)')
    parser.add_argument('-ty','--type', nargs='*', type=str, metavar='', help='Card Type (Warrior, effect, quick-play, Synchro, etc.)')
    parser.add_argument('-b', '--border', type=str, metavar='', help='Border of card (Monster, Spell, or Trap)')
    parser.add_argument('-atk', '--attack', type=str, metavar='', help='Attack stat of card')
    parser.add_argument('-def', '--defense', type=str, metavar='', help='Defense stat of card')

    args = parser.parse_args(arglist)
    return args

if __name__ == "__main__":
    
    print("Press Enter to end script")
    inp = input("Which mode would you like to access? (Deckmode: 1, Searchmode: 2): ")
    #deck editor
    
    if inp == '1':
        #initialize Deck class
        currentdeck = Deck()
        while True:
            inp = input("What would you like to do? (add, delete, view deck, view card, export): ") 
            
            if not inp:
                break
            elif inp == "add":
                inp = input("\tPlease name a card to add: ") 
                added = currentdeck.AddtoDeck(inp)  
                if added:
                    print("\tCard Added")
                else:
                    print("\tNothing Added") 
            
            elif inp == "delete":
                inp = input("\tPlease name a card to remove: ")
                removed = currentdeck.RemoveFromDeck(inp)
                if removed:
                    print("\tCard removed")
                else:
                    print("\tNo card removed")
            
            elif inp == "view deck":
                deckLength, deckList, isLegal = currentdeck.DeckStatus()
                print(f"\tHere is your deck:\n\t{deckList}" +
                      f"\n\tDeck length: {deckLength}" +
                      f"\n\tLegality: {isLegal}")
            
            elif inp == "view card":
                inp = input("\tWhich card would you like to see?: ").lower().strip()
                cardAttributes = currentdeck.CardStatus(inp)
                if cardAttributes:
                    pprint(vars(cardAttributes))
                else:
                    print("\tNo card found")
            
            elif inp == "export":
                inp = input("\tPlease provide the name of your deck/textfile: ")
                result = currentdeck.DeckExporter(inp)
                print("\t", result)
            else:
                print("\tPlease provide valid input")       

    #card searcher
    elif inp == '2': 
        while True:
            print("Type -h for help") 
            inp = input("What card are you looking for? ").strip()
            if not inp:
                break
            else:
                args = parse_args(inp.split())
                print("\nHere are the cards that matches your search:") 
                results = CardSearch.CardLookerUpper(args)
                print(results, "\n") 