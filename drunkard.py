from random import shuffle


class Card:
    suits = ["пикей", "червей", "бубей", "треф"]
    values = [None, None,"2", "3", "4", "5", "6", "7", "8", "9",
              "10", "валета", "даму", "короля", "туз"]

    def __init__(self, value, suit):
        """suit и value – целые числа"""
        self.value = value
        self.suit = suit

    def __lt__(self, other):
        if self.value < other.value:
            return True
        if self.value == other.value:
            if self.suit < other.suit:
                return True
            else:
                return False
        return False

    def __gt__(self, other):
        if self.value > other.value:
            return True
        if self.value == other.value:
            if self.suit > other.suit:
                return True
            else:
                return False
        return False

    def __repr__(self):
        return self.values[self.value] + " " + self.suits[self.suit]


class Deck:
    def __init__(self):
        self.cards = []
        for i in range(2, 15):
            for j in range(4):
                self.cards.append(Card(i, j))
        shuffle(self.cards)

    def remove_card(self):
        if len(self.cards) == 0:
            return
        return self.cards.pop()


class Player:
    def __init__(self, name):
        self.wins = 0
        self.card = None
        self.name = name


class Game:
    def __init__(self):
        name1 = input("имя игрока 1: ")
        name2 = input("имя игрока 2: ")
        self.deck = Deck()
        self.player1 = Player(name1)
        self.player2 = Player(name2)

    def play_game(self):
        cards = self.deck.cards
        print("Поехали!")
        response = None
        while len(cards) >= 2:
            response = input('Нажмите Х для выхода. Нажмите любую другую клавишу для начала игры.')
            if response == 'Х':
                break
            player1_card = self.deck.remove_card()
            player2_card = self.deck.remove_card()
            print("{} кладет {}, а {} кладет {}.".format(self.player1.name, player1_card, self.player2.name, player2_card))
            if player1_card > player2_card:
                self.player1.wins += 1
                print("{} забирает карты".format(self.player1.name))
            else:
                self.player2.wins += 1
                print("{} забирает карты".format(self.player2.name))
        print("Игра окончена. {} выиграл!".format(self.winner(self.player1, self.player2)))

    def winner(self, player1, player2):
        if player1.wins > player2.wins:
            return player1.name
        if player1.wins < player2.wins:
            return player2.name
        return "Ничья!"

game = Game()
