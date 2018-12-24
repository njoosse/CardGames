# ---------------------------------------------------------
#
# blackjack.py
# Created by N. Joosse
# Started Dec. 4, 2018
# Plays blackjack between the player and the computer
#
# ---------------------------------------------------------

# Import statements
import math
import time

from deck_of_cards import Card, Deck
deck = Deck()

playerStartCredits = 500

class Hand():
    def __init__(self):
        self.cards = []

    def readCard(self, card):
        cardString = '{} of {}'.format(card.val, card.suit)
        return cardString

    # Draws a card
    def addCards(self, count = 1):
        for _ in range(count):
            self.cards.append(deck.drawCard())
    
    # Removes the cards from the hand and moves them to 
    #   the discard pile in the Deck
    def discard(self):
        for card in self.cards:
            deck.discard(card)
        self.cards = []

    def getTotalScore(self):
        score = 0
        aces = []
        for card in self.cards:
            # Standard number cards
            if card.val in range(2, 11):
                score += card.val
            # Aces need to be counted last so that the player doesn't bust
            elif card.val == 'Ace':
                aces.append(card)
                # Ace is worth 1 or 11 points, no reason to bust on 11 or higher
            # Face cards
            else:
                score += 10
        for _ in aces:
            # The more aces, the higher the overall score, this could be detrimental
            #   by setting the limit to include the number of uncounted aces
            #   it will make more aces 1's
            for a in range(len(aces)):
                # Gets the number of remaining aces, not all of the aces each time
                if score >= 10+len(aces)-a:
                    score += 1
                else:
                    score += 11
        return score

# Class for every player wanting to play
class player():
    def __init__(self, credits = playerStartCredits):
        self.credits = credits
        self.bet = 0
        self.hand = Hand()

    def showCards(self):
        return [card.readCard() for card in self.hand.cards]

# Slightly different from the player in that they only show their first 
#   card until their turn, there is not a credit count since the casino
#   has infinite credits
class dealer():
    def __init__(self):
        self.hand = Hand()
        self.standValue = 17

    # Only shows the first card
    def showFirstCard(self):
        if len(self.hand.cards) > 0:
            return self.hand.cards[0].readCard()

    # Shows all cards
    def showCards(self):
        return [card.readCard() for card in self.hand.cards]

def playerWins():
    print('You Won!')
    if p1.hand.getTotalScore() == 21 and len(p1.hand.cards) == 2:
        # You keep the chips you had as well as the 1.5x winnings
        p1.credits += int(math.floor(p1.bet*1.5))+p1.bet
    else:
        # Keep the credits and then get the winnings
        p1.credits += int(p1.bet*2)
    
    # Remove all the cards
    p1.hand.discard()
    d.hand.discard()

p1 = player()
d = dealer()

def placeBets():
    betPlaced = False
    while not betPlaced:
        try:
            betValue = int(input('How many credits would you like to bet?\n({} credits remaining) > '.format(p1.credits)))
        except ValueError:
            print('Invalid Entry')
        if betValue == 0:
            print('Cannot bet 0 credits')
        elif betValue <= p1.credits:
            p1.bet = betValue
            p1.credits -= betValue
            betPlaced = True
        else:
            print('You do not have that many credits')

def gameplay():
    placeBets()

    # Deals 2 cards to each player
    p1.hand.addCards(2)
    d.hand.addCards(2)

    # Initial description of hands
    print('Dealer has a {}'.format(d.showFirstCard()))
    score =  p1.hand.getTotalScore()
    print('You have',str(p1.showCards())[1:-1].replace("'",'')+':', score, 'points')

    print('Options: [H]it, [S]tand')

    # Handles the player interaction
    standing = False
    # If the player gets an Ace and a card worth 10 in the deal,
    #   player gets a blackjack (1.5x payout)
    if score == 21:
        print('Blackjack!')
        playerWins()
        return

    # While the player is not standing and has not busted
    while not standing and p1.hand.getTotalScore() < 21:
        action = input('What would you like to do?\n> ')
        # Draws a card and displays the new card list and score
        if 'h' in action.lower():
            p1.hand.addCards()
            print('You drew a {}'.format(p1.hand.cards[-1].readCard()))
            score =  p1.hand.getTotalScore()
            print('You have',str(p1.showCards())[1:-1].replace("'",'')+':', score, 'points')
            if score > 21:
                print('You are over 21, you lose')
        # Standing, just waiting for the dealer to take their turn
        elif 's' in action.lower():
            standing = True
        # common, only 2 options
        else:
            print('Command not recognized')

    time.sleep(1)

    score =  d.hand.getTotalScore()
    print('Dealer has',str(d.showCards())[1:-1].replace("'",'')+':', score, 'points')
    while score < d.standValue:
        d.hand.addCards()
        print('\nDealer drew a {}'.format(p1.hand.cards[-1].readCard()))
        score =  d.hand.getTotalScore()
        print('Dealer has',str(d.showCards())[1:-1].replace("'",'')+':', score, 'points')
        time.sleep(1)

    # The dealer loses
    if score > 21:
        print('Dealer has busted')
        if p1.hand.getTotalScore() <= 21:
            playerWins()
        else:
            print('No Winners')
            p1.credits += p1.bet
            # p1.bet = 0
    elif score > p1.hand.getTotalScore():
        print('Dealer has won')
        # p1.bet = 0
        # Remove all the cards
    elif score < p1.hand.getTotalScore() <= 21:
        playerWins()
    elif score == p1.hand.getTotalScore():
        p1.credits += p1.bet
        # p1.bet = 0
    p1.hand.discard()
    d.hand.discard()
    return

def main():
    playing = True
    while playing:
        gameplay()
        # If statement to continue the game
        continueAnswer = False
        while not continueAnswer:
            if p1.credits > 0:
                answer = input('\nContinue Playing? Y/n\n> ')
            else:
                answer = input('\nYou are out of credits, play again? Y/n\n> ')
            if 'n' in answer.lower():
                playing = False
                continueAnswer = True
            elif 'y' in answer.lower():
                if p1.credits == 0:
                    p1.credits = playerStartCredits
                continueAnswer = True
                print('\nDealing')
            else:
                print('Unrecognized Command')

main()