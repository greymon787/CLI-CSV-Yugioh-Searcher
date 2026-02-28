from deck_editor import CardSearch, Deck
import os.path
from argparse import Namespace

#Time to implement some tests, 1-2 for each method by checking output.
#Also check command line for correct error handling

def test_deck_and_card():
    """Testing the initialization of a Card object via the Deck class"""
    #First checking if the deck is initalized within deck
    d = Deck()
    assert d.deck == []
    #Now checking if adding creates a Card object
    d.AddtoDeck("Junk Warrior")
    for attr in ["name", "level", "attribute", "cardtype", "border", "text", "attack", "defense"]:
        assert hasattr(d.deck[0], attr), f"Card object should have a {attr} attribute"
    assert d.deck[0].name == "Junk Warrior"
    assert d.deck[0].level == "5"
    assert d.deck[0].attribute == "dark"
    assert d.deck[0].border == "monster" 
    
    #Checking Spells
    d.AddtoDeck("Pot of Greed")
    for attr in ["name", "level", "attribute", "cardtype", "border", "text", "attack", "defense"]:
        assert hasattr(d.deck[1], attr), f"Card object should have a {attr} attribute"
    assert d.deck[1].name == "Pot of Greed"
    assert d.deck[1].level == "nan"
    assert d.deck[1].attribute == "nan"
    assert d.deck[1].cardtype == "normal"
    assert d.deck[1].border == "spell"
    
    #Checking if card was removed from deck by checking deck status
    d.RemoveFromDeck("Pot of Greed")
    length, decklist, legal = d.DeckStatus()
    assert length == 1
    assert decklist == [d.deck[0]]
    assert legal == "Illegal -> Less than 40 Cards"
    
    #Checking if exporting works
    results = d.DeckExporter("test")
    assert results == "Deck exported successfully"
    try:
        fpath = (R'test.txt')
        testfile = os.path.isfile(fpath)
        assert testfile == True
        #Note: Please delete the test file 
    except:
        raise RuntimeError("No file exists")

def test_card_search():
    """Checking if search logic is working properly"""
    args = Namespace(text=['wind'], name=None, level=None, attribute=None, type=None, border=None, attack=None, defense=None)
    searchResults = CardSearch.CardLookerUpper(args)
    assert searchResults == ['Sky Striker Ace - Hayate']
    
    args = Namespace(text=['Wind'], name=['Dragon'], level=None, attribute=None, type=None, border=None, attack=None, defense=None)    
    searchResults = CardSearch.CardLookerUpper(args)
    assert searchResults == "No cards match"
    
    args = Namespace(text=[], name=['Dragon'], level='8', attribute='Wind', type=['Dragon'], border='Monster', attack='2500', defense='2000')
    searchResults = CardSearch.CardLookerUpper(args)
    assert searchResults == ["Stardust Dragon"]