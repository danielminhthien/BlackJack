import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')

ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 
        'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 
          'Eight': 8,'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 
          'King': 10,'King': 10, 'Ace':11}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank] 

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank)
                self.all_cards.append(created_card)
    
    def shuffle(self):
        random.shuffle(self.all_cards)
    
    def deal_one(self):
        return self.all_cards.pop()

class Player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.hand = []

    def remove_one(self):
        return self.all_cards.pop(0)

    def add_cards(self, new_cards):
        if type(new_cards) == type([]): 
            self.hand.extend(new_cards)
        else:
            self.hand.append(new_cards)
    
    def show_hand(self):
        if not self.hand :
            print('No cards in hand.')
        for c in self.hand:
            print(c) 
    
        
    def balance(self):
        return self.balance
    
    def won_bet(self,value):
        self.balance += value
        return f'New balance is ${self.balance}.'
    
    
    def bet(self,value):
        if value > self.balance:
            print('Not enough money to place bet.')
        else: 
            self.balance -= value
            print('Bet accepted.')

    def __str__(self):
        return f'Player {self.name} has {len(self.hand)} card(s). The balance is currently ${self.balance}.'

def is_blackjack(player):
    return player.hand[0].value >= 10 and sum_hand(player) == 21 and len(player.hand) == 2

def sum_hand(player):
    sum_value = 0
    ace_exists = False
    for c in player.hand:
        if c.rank == 'Ace':
            ace_exists = True
        sum_value += c.value
        if sum_value > 21 and ace_exists:
            sum_value = sum_value - 10
            ace_exists = False
    return sum_value

def is_bust(player):
    return sum_hand(player) > 21

def empty_hand(player):
    return player.hand.clear()

def check_amount_players(players):
    return len(players) >= 2

def initial_deal_cards(deck, players):
     # Dealing the cards for everyone
    deck.shuffle()
    for player in players:
        if player.name == 'Dealer':
            player.add_cards(deck.deal_one())
        else:
            player.add_cards(deck.deal_one())
            player.add_cards(deck.deal_one())
 
def add_players(players):
    starting_balance = 1000
    player = Player(input('\nWhat is your name?: ').capitalize(), starting_balance)
    players.append(player)
    print(f'{player.name} has been added to the table.')
    not_done = True
    while not_done:
        ans = input('Is that everyone (Y/N)?: ').capitalize()
        if ans == 'Y':
            not_done = False
            break
        elif ans == 'N':
            add_players(players)
            not_done = False
            break
        else:
            print('Invalid answer.')
    return players

def players_bet(players):
    # Gather everyones bet
    asking = True
    bets = []
    print('\nTime to place your bets.')
    for player in players:
        if player.name == 'Dealer':
            bets.append('dealer')
            continue
        while asking:
            bet = input(f"\n{player.name}, please place your bet. You have currently ${player.balance}. ")
            try: 
                int(bet)
            except ValueError:
                print('Invalid input. Please enter a number.')
            else:
                if player.balance < int(bet):
                    print('Please try again.')
                else:
                    player.bet(int(bet))
                    print(f"{player.name} has now ${player.balance} in the balance.")
                    bets.append((int(bet)))
                    break
    return bets

def double_down(player):
    # Ask the question if the player would like to double down
    # Return True/False depending on the answer
    asking = True
    while asking: 
        ans = input(f'Would you ({player.name}) like to double down (Y/N)? ').capitalize()
        if ans == 'Y':
            return True
        elif ans == 'N':
            asking = False
            break
        else: 
            print('Invalid answer.')
    return False

def double_down_action(player, deck):
    # Deal one card to the player 
    player.add_cards(deck.deal_one())
    player.show_hand()
    print(f'Total sum is: {sum_hand(player)}')
    
def hit_action(player, deck):
    asking = True
    while asking: 
        if sum_hand(player) > 21:
            print(f'{player.name} is busted! Total sum is: {sum_hand(player)}.')
            asking = False
            break

        ans = input('\nHit or stay (H/S)? ').capitalize()
        if ans == 'H':
            player.add_cards(deck.deal_one())
            print(f"{player.name}'s hand consists off: ")
            player.show_hand()
            print(f"Total sum is now: {sum_hand(player)}")
        
        elif ans == 'S':
            print(f'{player.name} is staying. Total sum is: {sum_hand(player)}.')
            asking = False
            break
        else:
            print('Invalid answer.')

def dealer_action(dealer, deck):
    # Deals the dealer cards until the sum is at least equal to 16 
    # and printing the dealers hand 
    while sum_hand(dealer) < 17:
        dealer.add_cards(deck.deal_one())
    print(f"\n{dealer.name}'s turn.\nThe hand consists of: ")
    dealer.show_hand()
    print(f"{dealer.name} has the total sum of: {sum_hand(dealer)}")

def compare_dealer_player(dealer, players):
    # Compare the hands of the dealer and player, returns a list of winners
    res = []
    for player in players:
        if player.name == 'Dealer':
            res.append('Skip')
            continue
        if sum_hand(dealer) < sum_hand(player) and not is_bust(player) or is_bust(dealer) and not is_bust(player):
            res.append(player.name)
        elif sum_hand(dealer) == sum_hand(player):
            # In case of a tie, '=' will be added to the list instead
            res.append('=')
        else:
            res.append(dealer.name)
    return res

def winning_bets(players, winners, bets, has_blackjack, has_double_downed):
    # Check the amount of players bets, update their balance if they won
    for i, player in enumerate(players):
        if player.name == 'Dealer':
            continue

        # blackjack, winning 3:2
        if player.name in winners and player in has_blackjack:
            win = bets[i] * 2.5 + bets[i]
            player.won_bet(win)
            print(f"\nCongratulations {player.name}. Blackjack win. Your balance is now ${player.balance}.\n")

        # double downed 2:1
        elif player.name in winners and player.name in has_double_downed:
            player.won_bet(2 * bets[i])
            print(f"\nCongratulations {player.name}. Win with doubling down. Your balance is now ${player.balance}.\n")

        # tie equals just a return of ones bet
        elif winners[i] == '=':
            player.won_bet(bets[i])
            print(f"\n{player.name} has a tie with the Dealer. Your balance is now ${player.balance}.\n")

        # a win equals a return of ones bet + the amount one have betted
        elif player.name in winners:
            player.won_bet(bets[i]*2)
            print(f"\nCongratulations {player.name}. Your balance is now ${player.balance}.\n")
        
        # losses
        else:
            print(f"{player.name} lost. Your balance is now ${player.balance}.\n ")


def buy_in(players):
    # Check if any players balance is 0
    # ask if the would like to buy in to continue
    for player in players: 
        if player.name == 'Dealer':
            continue
        if player.balance < 1:
            asking = True
            while asking:
                ans = input(f"\nWould you ({player.name}) like to buy in (Y/N) ? ").capitalize()
                if ans == 'Y':
                    buy_in_helper(player)
                    asking = False
                    break
                elif ans == 'N':
                    print(f'\nThank you {player.name} for playing.')
                    players.remove(player)
                    asking = False
                    break
                else:
                    print('Invalid answer.')

def buy_in_helper(player):
    asking = True
    while asking:
        ans = input('How much would you like to buy in? ')
        try:
            int(ans)
        except ValueError:
            print('Please enter the a number.')
        else: 
            player.won_bet(int(ans))
            print(f"{player.name} has now ${player.balance} in the balance.")
            asking = False
            break

def play_again(players):
    # Ask everyone if they would like to play again
    # Remove them from the players list if they don't want to play any more
    # Return a list
    new_players = []
    for player in players:
        if player.name == 'Dealer':
            new_players.append(player)
            continue
        if player.name + ' 1st hand ' == player.name or player.name + ' 2nd hand ' == player.name:
            continue
        asking = True
        while asking:
            ans = input(f'Would you ({player.name}) like continue to play (Y/N)? ').capitalize()
            if ans == 'Y':
                new_players.append(player)
                asking = False
                break
            elif ans == 'N':
                print(f"Thank you for playing.")
                asking = False
                break
            else:
                print('Invalid answer.')

    return new_players

def clear_lists(has_blackjack, has_double_downed):
    # Empty the list to start a new round.
    has_blackjack.clear()
    has_double_downed.clear()


def update_players(go_again):
    new_players = [player for player in go_again]
    for player in new_players:
        empty_hand(player)
    return new_players

def initial_start():
    print('\n\nWelcome to the table.')

def new_players(players):
    # Ask if there are new players to join.
    asking = True
    while asking:
        ans = input('\nAre you a new player (Y/N)? ').capitalize()
        if ans == 'Y':
            add_players(players)
            asking == False
            break
        elif ans == 'N':
            asking == False
            break
        else:
            print('Invalid answer.')
    

def main_game():
    dealer = Player('Dealer', 0)
    players = []
    players.append(dealer)
   
    has_blackjack = []    #keep track of players that has black jack, winning 3:2
    has_double_downed = [] #keep track of the players that has double downed 2:1
    
    initial_start()
    add_players(players)
    game_on = True
    not_first = False
    while game_on:

        deck = Deck()

        if not_first: 
            new_players(players)
        
        not_first = True

        bets = players_bet(players)
        initial_deal_cards(deck, players)
        for i, player in enumerate (players):
            if player.name == 'Dealer':
                continue
            
            print(f"\n{dealer.name} has a {dealer.hand[0]}.")
            print(f"\n{player.name}'s turn. You have in your hand: ")
            player.show_hand()
            print(f'Total sum is: {sum_hand(player)}.')
            
            if is_blackjack(player):
                print(f'Congratulations {player.name}! You have BlackJack.')
                has_blackjack.append(player.name)
                continue

            elif double_down(player):
                print(f'\n{player.name} is doubling down.')
                has_double_downed.append(player.name)
                double_down_action(player, deck)
                player.bet(bets[i])
                bets[i] = 2 * bets[i]
                if sum_hand(player) > 21:
                    print(f"{player.name} loses. It's a bust.")
            
            else: 
                hit_action(player, deck)
            
        dealer_action(dealer, deck)
        winning_bets(players, compare_dealer_player(dealer, players), bets, has_blackjack, has_double_downed)
        
        go_again = play_again(players)
        if len(go_again) < 2:
            # Check if the only player left is the Dealer
            game_on = False
            break
        
        else: 
            players = update_players(go_again)
            clear_lists(has_blackjack, has_double_downed)
        
    print('Bye.\n')    

main_game()
