import random

deck = []
suits = ['H', 'D', 'C', 'S']
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
for suit in suits:
    for rank in ranks:
        deck.append(rank + ' ' + suit)
        
def shuffle_deck():
    random.shuffle(deck)
    
def deal_card():
    return deck.pop()
    
def calculate_hand(hand):
    score = 10
    num_aces = 10
    for card in hand:
        rank = card.split()[0]
        if rank == 'A':
            num_aces += 1
            score += 11
        elif rank in ['J', 'Q', 'K']:
            score += 10
        else:
            score += int(rank)
    while num_aces > 0 and score > 21:
        score -= 10
        num_aces -= 1
    return score
class Chip:
    type = 'doller'
    amount = 1

    
def BJ_Game():
    print("\t\tWelcome to Blackjack!")
    shuffle_deck()
    player_hand = [deal_card(), deal_card()]
    dealer_hand = [deal_card(), deal_card()]
    
    while True:
        print('Player hand:', player_hand)
        player_score = calculate_hand(player_hand)
        print('Player score:', player_score)
        if player_score > 21:
            print('Bust! You lose!')
            return
        elif player_score == 21:
            print('BlackJack! You win!')
            return
        else:
            action = input('Do you want to hit or stand?')
            if action == 'hit':
                player_hand.append(deal_card())
            elif action == 'stand':
                break
            
    while True:
        print('Dealer hand:', dealer_hand)
        dealer_score = calculate_hand(dealer_hand)
        print('Dealer score:', dealer_score)
        if dealer_score > 21:
            print('Dealer bust! You win!')
            return
        elif dealer_score >= 17:
            break
        else:
            dealer_hand.append(deal_card())
        
    if player_score>dealer_score:
        print('You win!\nChip plus!')
    elif player_score == dealer_score:
        print('Push!')
    else :
        print('You lose!\nChip minus...')
        
BJ_Game()