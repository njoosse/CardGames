# ---------------------------------------------------------
#
# deck_of_cards.py
# Created by N. Joosse
# Started Dec. 4, 2018
# Class handlers for a deck of standard playing cards,
#   meant to be imported somewhere else
#
# ---------------------------------------------------------

# Import Statements
import copy
import random

# Class to store the attibutes of the playing cards
class Card():
    def __init__(self, suit, value):
        self.suit = suit
        self.val = value
        if self.suit in ['Hearts', 'Diamonds']:
            self.color = 'Red'
        else:
            self.color = 'Black'

    # Returns a string telling what the card is
    def readCard(self):
        cardString = '{} of {}'.format(self.val, self.suit)
        return cardString


# Class to store a deck of cards
class Deck():
    def __init__(self):
        self.cardsInHands = []
        self.discarded = []
        self.unplayed = []

        # Creates one card of every suit/value pair, they are
        #   put in discarded since that is what will be shuffled after
        for suits in ['Hearts', 'Clubs', 'Diamonds', 'Spades']:
            for val in [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']:
                self.discarded.append(Card(suits, val))

        # Initial shuffle of the deck
        self.shuffle()

    # Removes the last card in unplayed, puts it in cardsInHands
    def drawCard(self):
        if len(self.unplayed) > 0:
            card = self.unplayed.pop()
            self.cardsInHands.append(card)
            return card
        # If there are not any cards in the deck,
        #   shuffles the discard pile and then draws
        else:
            self.shuffle()
            self.drawCard()

    # Randomly shuffles the discard pile
    def shuffle(self):
        self.unplayed = copy.deepcopy(self.discarded)
        self.discarded = []
        random.shuffle(self.unplayed)

    # Removes cards from a hand and puts them in the discard
    # If a card is not specified, all cards are discarded
    def discard(self, card=None):
        if card == None:
            self.discarded.extend(self.cardsInHands)
            return 0
        else:
            # If a card is specified, discards that one
            if card in self.cardsInHands:
                self.cardsInHands.pop(self.cardsInHands.index(card))
                self.discarded.append(card)
                return 1
            # There is not really any way for this to be called,
            #   but just in case...
            else:
                print('Card not in any hand')
                return -1
