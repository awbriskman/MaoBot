import game
import Card
import os
import asyncio

from discord.ext import commands

bot = commands.Bot(command_prefix='$')
Mao = game.Game()


@bot.command()
async def test(ctx, *args):
    message = ""
    for arg in args:
        message = message + arg + " "
    await ctx.send(message)


@bot.command()
async def deck(ctx):
    Mao.deck_flag = True
    await ctx.send("Are you sure want to see the deck? Its technically cheating....")


@bot.command()
async def yesImSure(ctx):
    if Mao.deck_flag:
        display_string = '|'
        for card in Mao.deck:
            display_string = '|' + card.display() + display_string
        Mao.deck_flag = False
        await ctx.send(display_string)
    else:
        await ctx.send("No, you have to *ask* first!")


@bot.command()
async def draw(ctx):
    Mao.deal(ctx.author, 1)
    if Mao.active_player == ctx.author:
        # TODO
        Mao.cards_drawn += 1
    await ctx.send(str(ctx.author) + " takes a card")
    await ctx.author.send(
        "You drew a: |" + Mao.players[ctx.author][-1].display() + '|')  # tell the player what they drew


@bot.command()
async def maoBeginsNow(ctx, arg):
    if Mao.master_of_mao not in Mao.players:
        Mao.master_of_mao = ctx.author
    Mao.deal_all(int(arg))
    await ctx.send(str(arg) + " cards to " + str(len(Mao.players.keys())) + " players.")
    Mao.flip()
    await ctx.send("The top card is now: " + Mao.discard[-1].display())  # displays the top card of the discard pile
    for player in Mao.players:
        display_string = "Your starting hand is: |"
        for card in Mao.players[player]:
            display_string += card.display() + "|"
        await player.send(display_string)  # tells each player the cards in their hand
        await player.send(
            "The top card is now: " + Mao.discard[-1].display())  # displays the top card of the discard pile


@maoBeginsNow.error
async def maoBeginsNow_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify a number of cards for each player to draw")


@bot.command()
async def join(ctx):
    if not Mao.players.get(ctx.author, False):
        Mao.add_player(ctx.author)
        await ctx.send("Welcome to the game " + str(ctx.author) + "!")


@bot.command()
async def quit(ctx):
    if Mao.players.get(ctx.author, False):
        Mao.remove_player(ctx.author)
        await ctx.send("Goodbye " + str(ctx.author))


@bot.command()
async def resetPlayers():
    for player in Mao.players:
        Mao.remove_player(player)


@bot.command()
async def rules(ctx):
    active_rules = []
    for rule in Mao.rules:
        if Mao.rules[rule]:
            active_rules.append(rule)
    await ctx.send("the current rules are:")
    for rule in active_rules:
        await ctx.send(rule)


@bot.command()
async def allRules(ctx):
    await ctx.send("the current rules are:")
    for rule in Mao.rules:
        await ctx.send(str(rule) + ": " + str(Mao.rules[rule]))


@bot.command()
async def hand(ctx):
    display_string = "|"
    for card in Mao.players[ctx.author]:
        display_string = display_string + card.display() + "|"
    await ctx.author.send(display_string)  # tell the player the cards in their hand


@bot.command()
async def players(ctx):
    await ctx.author.send(str(len(Mao.players)) + " players:")
    for player in Mao.players:
        await ctx.author.send(str(player) + " has " + str(len(Mao.players[player])) + " cards")

@bot.command()
async def addRule(ctx, arg):
    if Mao.editable_rules:
        if ctx.author == Mao.master_of_mao:
            if arg in Mao.rules:
                if not Mao.rules[arg]:
                    Mao.rules[arg] = True
                    await ctx.send("Rule added: "+str(arg))
                    Mao.editable_rules = False
                await ctx.send("That rule is already active. You an check the state of possible rules with $allRules.")
            await ctx.send("That's not a valid rule to choose. You an check the list of possible rules with $allRules.")
        await ctx.send("Only the master of mao can edit rules.")
    await ctx.send("You can only change the rules when you win a game.")


@bot.command()
async def removeRule(ctx, arg):
    if Mao.editable_rules:
        if ctx.author == Mao.master_of_mao:
            if arg in Mao.rules:
                if Mao.rules[arg]:
                    Mao.rules[arg] = False
                    await ctx.send("Rule added: "+str(arg))
                    Mao.editable_rules = False
                await ctx.send("That rule is already removed. You an check the state of possible rules with $allRules.")
            await ctx.send("That's not a valid rule to choose. You an check the list of possible rules with $allRules.")
        await ctx.send("Only the master of mao can edit rules.")
    await ctx.send("You can only change the rules when you win a game.")


@bot.command()
async def play(ctx, arg):
    card_to_play = Card.Card(arg[0], arg[1])
    hand_flag = False
    for card in Mao.players[ctx.author]:
        if card_to_play == card:
            hand_flag = True
    if not hand_flag:
        await ctx.send("You tried to play a " + card_to_play.display())
        await ctx.send("That card was not in your hand. Take another card, maby *that* will actually be it instead.")
        Mao.deal(ctx.author, 1)  # give the penalty card
    else:
        await ctx.send("You are trying to play the " + card_to_play.display() + " on the " + Mao.discard[-1].display())

        def fromPlayer(message):
            return message.author == ctx.author

        reply_flag = True
        while reply_flag:  # resets countdown timer for gamephrase inputs
            reply_flag = False
            try:
                reply = await bot.wait_for('message', check=fromPlayer,
                                           timeout=7)  # resetting 6 second timeout counter for replies
                if reply:
                    Mao.phrases.append(
                        str(reply.author) + str(reply.content))  # add player message to list of game phrases
                    reply_flag = True
            except asyncio.TimeoutError:
                pass
        print(Mao.phrases)
        penalties = Mao.play(card_to_play, ctx.author)  # attempt to play the card and return a list of
        # applicable penalties
        Mao.phrases = []  # clear phrases now that they've been used
        if penalties[0] == 0:  # card was not a valid play
            await ctx.send("That was not a valid play. Take a penalty card.")
            Mao.deal(ctx.author, 1)  # give the penalty card
        else:
            Mao.cards_drawn = 0
            if penalties != [1] and penalties != [2]:  # checking card wasn't played completely correctly
                for penalty in penalties[1:]:
                    await ctx.send(penalty)  # announce the penalty
                    Mao.deal(ctx.author, 1)  # give the penalty card
                penalty_num = len(penalties) - 1
                if Mao.cards_to_draw > 1:
                    penalty_num += Mao.cards_to_draw - 1 # 1 penalty will be awarded via message already
                penalty_string = str(ctx.author) + " has received " + str(penalty_num) + " penalty card"
                if penalty_num > 2:
                    penalty_string += 's'  # adds plural to card(s)
                await ctx.send(penalty_string + ".")
    if not Mao.players[ctx.author]:  # check if the player just won
        await asyncio.sleep(.5)
        await ctx.send(str(ctx.author) + " is out of cards.")
        await ctx.send(str(ctx.author) + " is the new Chairman of Mao and the game is over.")
        Mao.clean_hands()
        Mao.editable_rules = True
    else:
        Mao.cards_to_draw = 0 # reset penalty draws
        await ctx.send("The top card is now: " + Mao.discard[-1].display())  # displays the top card of the discard pile
        display_string = "Your hand is now: |"
        for card in Mao.players[ctx.author]:
            display_string = display_string + card.display() + "|"
        await ctx.author.send(display_string)  # tell the player the cards in their hand


@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify a card to play")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Thats not a valid command")
    if ctx.author == 'Patchup#6299':
        await ctx.send("...Anthony!")
    if ctx.author == 'snark-bot#5580':
        await ctx.send("Way to bring us bots down here, Snark-Bot")



@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    await bot.process_commands(message)


# @bot.event
# async def on_message(message):
#    if message.author == bot.user:
#        return
#    if Mao.recording:
#        Mao.phrases.append(str(message.author)+str(message.content))

bot.run(os.environ["CLIENT_TOKEN"])
