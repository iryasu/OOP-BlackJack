import random


class Player:
    def __init__(self, name='You'):
        self.money = 500
        self.hand = 0
        self.name = name
        self.soft = False

    def __str__(self):
        return f"{self.name} currently have {self.money} $"

    def update_hand(self, card):
        """
            Adds the value of the card to the hand of the player
        :param card: the value of the card being picked
        :return: Nothing
        """
        # card = random.randint(1, 13)
        if card == 11:
            self.hand += 10
            print(f" {self.name} picked a Jack\n")
        elif card == 12:
            self.hand += 10
            print(f" {self.name} picked a Queen\n")
        elif card == 13:
            self.hand += 10
            print(f" {self.name} picked a King\n")
        elif card == 1:
            self.hand += 11
            self.soft = True
            print(f" {self.name} picked an Ace\n")
        else:
            self.hand += card
            print(f" {self.name} picked a {card}\n")
        if self.soft and self.hand > 21:
            self.hand -= 10
            self.soft = False
        print(f" current hand is at value {self.hand}\n")

    def restart_hand(self):
        """
            Restarts hand value to 0
        :return: Nothing
        """
        self.hand = 0
        self.soft = False


class Deck:
    def __init__(self):
        self.cards = 4*list(range(1, 14))

    def __str__(self):
        return f"the deck contains {len(self.cards)} cards"

    def pick_card(self):
        """
            Picks a random card from the deck
        :return: the card value
        """
        random.shuffle(self.cards)
        return self.cards.pop()


def game_loop():
    """
    Main game loop
    :return: Nothing
    """
    print("Welcome to the BlackJack game !\n"
          "You will be playing against a bot dealer that will play after you finish your turn\n"
          "Good luck !\n")

    player = Player()
    comp = Player(name='comp')

    while True:
        print(player)
        if player.money == 0:
            print("You're out of money, you can't play anymore !\n")
            break
        print(comp)
        if comp.money == 0:
            print("Computer is out of money, he can't play anymore and you win !\n"
                  "Enjoy your wealth $$$$  !")
            break
        player.restart_hand()
        comp.restart_hand()
        deck = Deck()

        while True:
            try:
                bet = int(input("How much do you want to bet ? :  "))
                assert 0 < bet <= player.money
            except AssertionError:
                print("You can't bet more than you currently have ! Please enter a correct amount\n")
            except ValueError:
                print("Please enter a correct positive amount that is less than you currently have\n")
            else:
                break

        print(f" You're betting {bet}$ and the computer is betting {bet if bet <= comp.money else comp.money}$\n")
        stand = False
        while not stand:
            card = deck.pick_card()
            player.update_hand(card)
            if player.hand == 21:
                print(" BlackJack !\n")
                stand = True
                continue
            elif player.hand > 21:
                print("You busted\n")
                stand = True
                continue

            stand = input("Would you like to hit or stand ? (h/s)") == 's'
        if player.hand > 21:
            print(f"You lose {bet}$")
            comp.money += bet
            player.money -= bet
            continue

        print("##########################################")
        print(" Computer turn will start now :\n")

        busted = False
        while not busted:
            card = deck.pick_card()
            comp.update_hand(card)
            if comp.hand == 21:
                print(" BlackJack !")
                break
            elif comp.hand > player.hand:
                break
            elif comp.hand > 21:
                print("Computer busted !")
                busted = True

        if busted or player.hand > comp.hand:
            print("Congrats you win this round !\n")
            print(f"You win {bet if comp.money >= bet else comp.money}$\n")
            player.money += bet if comp.money >= bet else comp.money
            comp.money -= bet if comp.money >= bet else comp.money
        elif player.hand == comp.hand:
            print("This is a tie !\n")
        else:
            print("Sorry you lose this round !\n")
            print(f"You lose {bet}$\n")
            comp.money += bet
            player.money -= bet
    print("Thank you for playing ! Don't forget to treat your money reasonably $$ !")


if __name__ == '__main__':
    game_loop()
