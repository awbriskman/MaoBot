import Card


class RulesList:
    top_card = Card.Card('A', 'S')
    list_of_rules = {'Uno': True, 'MagicCard': True, 'CloseEnough': False, 'ExcellentWeather': False, 'Mao': True,
                     'LittleRedBook': False, 'ProperRespect': True, "Names": True, "Taps": True,
                     "TwinkleTwinkle": False}
    tap_count = 0

    def EvaluateRules(self, rule, game, card, player, phrases):
        if game.rules[rule]:
            getattr(self, rule)(game, card, player, phrases)

    def Uno(self, game, card, player, phrases):
        if card.face == game.discard[-1].face or card.suit == game.discard[-1].suit:
            game.penalties[0] = 1

    def MagicCard(self, game, card, player, phrases):
        if card.get_face() == '8' and game.penalties[0] != 1:
            game.penalties[0] = 2
            if str(player) + 'Magic card' not in phrases:
                game.penalties.append("Failure to say 'Magic card'")
        elif str(player) + 'Magic card' in phrases:
            game.penalties.append("Should not have said 'Magic card'")

    def close(self, first_card, second_card):
        if abs(first_card.get_index() - second_card.get_index()) == 1:
            if (first_card.suit == "H" and second_card.suit == "D" or
                    first_card.suit == "D" and second_card.suit == "H" or
                    first_card.suit == "S" and second_card.suit == "C" or
                    first_card.suit == "C" and second_card.suit == "S"):
                return True
            elif self.game.rules["TwinkleTwinkle"] and (first_card.suit == "T" and second_card.suit != "T" or
                                                         first_card.suit != "T" and second_card.suit == "T"):
                return True
        return False

    def CloseEnough(self, game, card, player, phrases):
        if game.penalties[0] != 1 and self.close(card, game.discard[-1]):
            game.penalties[0] = 2
            if str(player) + 'Close enough' not in phrases:
                game.penalties.append("Failure to say 'Close enough'")
        elif str(player) + 'Close enough' in phrases:
            game.penalties.append("Should not have said 'Close enough'")

    def Mao(self, game, card, player, phrases):
        if len(game.players[player]) == 2:
            if str(player) + 'Mao' not in phrases:
                game.penalties.append("Failure to say 'Mao'")
        elif str(player) + 'Mao' in phrases:
            game.penalties.append("Should not have said 'Mao'")

    def seven_count(self, game):
        if game.discard[-1].face == '7': # top card of discard is a 7
            i = 1
            while game.discard[(i * -1)].face == '7': # while each successive card is a 7
                i += 1
                if len(game.discard) <= i: # check to keep from reading off the end of the discard pile
                    break
            return i - 1
        else: return 0

    def ExcellentWeather(self, game, card, player, phrases):
        sevens = self.seven_count(game) # number of sevens already played and thus cards should have drawn total
        cards_to_draw = sevens - game.cards_drawn # number of cards that should have been drawn but weren't
        if cards_to_draw > 0:
            penalty_phrase = "failure to draw "
            if cards_to_draw > 1:
                penalty_phrase += str(cards_to_draw) + " cards. Here are the cards you should have drawn."
            else:
                penalty_phrase += "a card. Here is the card you should have drawn."
            game.penalties[1] = penalty_phrase
            for __ in range(cards_to_draw - 1):  # pad the penalties with the extra card draws
                game.penalties.append("<Missed card draw>")
        elif game.discard[-1].face == '7' and game.rules['LittleRedBook']:  # check that previous 7's were acknowledged
            penalty_phrase = str(player) + "Thank you "
            if sevens > 1:
                penalty_phrase += ((sevens - 1) * "very ") + "much "
            penalty_phrase += "citizen"
            if penalty_phrase not in phrases:
                game.penalties.append("Failure to say '" + penalty_phrase + "'")
        if card.face() == '7':  # check for a valid(ated) 7
            sevens += 1
            penalty_string = str(player) + 'Have a ' + ((sevens - 1) * 'very ') + 'nice day'
            if game.rules['LittleRedBook']: #little red book modifies this phrase
                penalty_string += ' citizen'
            if penalty_string not in phrases:
                penalty_flag = False
                for very_test_num in range(6): #checking variations in length in case they said the wrong num of very's
                    test_phrase = str(player) + 'Have a ' + ((very_test_num - 1) * 'very ') + 'nice day'
                    if game.rules['LittleRedBook']:
                        test_phrase += ' citizen'
                    if test_phrase in phrases:
                        game.penalties.append(
                            "should have said '" + penalty_string[len(str(player)):] + "' instead of '"
                            + test_phrase[len(str(player)):] + "'")
                        penalty_flag = True  # make sure only one penalty given and not both
                if not penalty_flag:
                    game.penalties.append("failure to say '" + penalty_string + "'")

    def ProperRespect(self, game, card, player, phrases):
        if card.face == 'K':
            if str(player) + 'Hail to the chairman' not in phrases:
                game.penalties.append("failure to say 'Hail to the chairman'")
        elif card.face == 'Q':
            if str(player) + 'Hail to the chairwoman' not in phrases:
                game.penalties.append("failure to say 'Hail to the chairwoman'")
        else:
            if str(player) + 'Hail to the chairman' in phrases:
                game.penalties.append("Should not have said 'Hail to the chairman'")
            if str(player) + 'Hail to the chairwoman' in phrases:
                game.penalties.append("Should not have said 'Hail to the chairwoman'")

    def Names(self, game, card, player, phrases):
        if card.suit == "S":
            if str(player) + card.get_name() not in phrases:
                if str(player) + card.suit + " of " + card.suit_names[card.suit] not in phrases:
                    game.penalties.append("Failure to say " + card.get_name())
            pass

    def Taps(self, game, card, player, phrases):
        if card.face == game.discard[-1].face: # a tap is required
            if self.tap_count > 2: # single tap case
                if str(player) + "*tap* *tap*" in phrases: # double tapping a single tap
                    game.penalties.append("Excessive tapping of the deck")
                    self.tap_count = 0 # reset on all double taps
                elif str(player) + "*tap*" not in phrases: # not tapping a single tap
                    game.penalties.append("Failure to tap the deck")
                else: # single tapping correctly
                    self.tap_count += 1
            else: # double tap case
                if str(player) + "*tap* *tap*" not in phrases: # not double tapping
                    if str(player) + "*tap*" in phrases: # instead single tapping
                        self.tap_count = 0 # count not reset if no tap made
                    game.penalties.append("Failure to tap the deck")
                else: # double tap correctly
                    self.tap_count = 0 # reset the count
        elif str(player) + "*tap*" in phrases or str(player) + "*tap* *tap*" not in phrases:
                game.penalties.append("Tapping out of turn") #tapping out of turn

    def TwinkleTwinkle(self, game, card, player, phrases):
        pass

    def star_shuffle(self):
        pass

    def add_rules(self, game):
        game.rules.update(self.list_of_rules)
