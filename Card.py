class Card:
    face = 0x1
    suit = ''
    faces = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    suit_converter = {
            'S': '\♠',
            'H': '\♥',
            'C': '\♣',
            'D': '\♦',
            'T': '\★'
    }
    face_names = {
        'A': 'Ace',
        '2': 'Two',
        '3': 'Three',
        '4': 'Four',
        '5': 'Five',
        '6': 'Six',
        '7': 'Seven',
        '8': 'Eight',
        '9': 'Nine',
        'T': 'Ten',
        'J': 'Jack',
        'Q': 'Queen',
        'K': 'King'
    }

    suit_names = {
        'S': 'Spades',
        'H': 'Hearts',
        'C': 'Clubs',
        'D': 'Diamonds',
        'T': 'Stars'
    }

    def __init__(self, new_face, new_suit):
        self.face = new_face
        #self.face = self.face_converter.get(new_face)
        self.suit = new_suit

    def display(self):
        #chars = self.face_converter2.get(self.face, str(int(self.face)))
        if self.face == 'T':
            chars = '10'
        else:
            chars = self.face
        chars+= self.suit_converter[self.suit]
        return chars

    def get_face(self):
        return self.face

    def get_suit(self):
        return self.suit

    def get_index(self):
        return self.faces.index(self.face)

    def get_name(self):
        return self.face_names[self.face] + ' of ' + self.suit_names[self.suit]

    def __eq__(self, other):
        return self.face == other.face and self.suit == other.suit

    def __repr__(self):
        return self.display()

