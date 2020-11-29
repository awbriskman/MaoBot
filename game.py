import random
import Card
import Rules


class Game:
    deck = []
    discard = []
    players = {}
    deck_flag = False
    rules = {}
    cards_drawn = 0
    penalties = []
    list_of_rules = Rules.RulesList()
    phrases = []
    recording = False
    master_of_mao = ''
    editable_rules = False

    def __init__(self):
        self.deck = []
        self.discard = []
        self.players = {}
        self.list_of_rules.add_rules(self)
        self.master_of_mao = 'alex#8523'

    def shuffle(self):
        for __ in self.discard:
            self.deck.append(self.discard.pop())
        random.shuffle(self.deck)

    def new_deck(self):
        faces = 4 * "23456789TJQKA"
        suits = 13 * "HCSD"
        self.deck = []
        for i in range(0, 52):
            self.deck.append(Card.Card(faces[i], suits[i]))  # makes a new card object and adds it to the deck
        self.shuffle()  # shuffle the deck before use

    def deal_all(self, cards_to_hand):
        for player in self.players:
            self.players[player] = []
        self.new_deck()
        for player in self.players:
            self.deal(player, cards_to_hand)

    def deal(self, player, cards_to_hand):
        for __ in range(cards_to_hand):
            if self.deck:
                self.players[player].append(self.deck.pop())
            else:
                hold_card = self.discard.pop(-1)
                self.shuffle()
                self.discard = [hold_card]
                self.players[player].append(self.deck.pop())

    def add_player(self, new_player):
        self.players[new_player] = []

    def remove_player(self, player):
        del self.players[player]

    def clear_players(self):
        for player in self.players.keys():
            self.remove_player(player)

    def flip(self):
        if self.deck:
            self.discard.append(self.deck.pop())
        else:
            hold_card = self.discard.pop(-1)
            self.shuffle()
            self.discard = [hold_card]
            self.discard.append(self.deck.pop())

    def play(self, card, player):
        self.penalties = [0]
        for rule in self.rules:
            self.list_of_rules.EvaluateRules(rule, self, card, player, self.phrases)
        if self.penalties[0] != 0:
            self.players[player].remove(card)
            self.discard.append(card)
        return self.penalties

    def clean_hands(self):
        for player in self.players:
            for __ in self.players[player]:
                self.deck.append(self.players[player].pop())
