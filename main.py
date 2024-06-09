from typing import Final
import os 
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response, embedded
import discord
from tiles import blank, cross, circle, one, two , three, four, five , six , seven, eight, nine

load_dotenv()
TOKEN: Final[str] = os.getenv('TOKEN')

# BOT SETUP 
intents: Intents = Intents.default()
intents.message_content = True
intents.reactions = True
client: Client = Client(intents = intents)

id_game_map = {}

class ttt :
    def __init__(self, user, opp) -> None : 
        self.grid = [blank , blank , blank , '\n' , blank , blank , blank , '\n' , blank , blank , blank]
        self.user1 = user
        self.user2 = opp
        self.turn = self.user2
        self.embedd = None
        print(self.user1, self.user2)

    def toggleTurn(self) -> None:
        if(self.user1 == self.turn) : self.turn = self.user2
        else : self.turn = self.user1
    
    def reset(self) : 
        self.grid = [blank , blank , blank , '\n' , blank , blank , blank , '\n' , blank , blank , blank]
        # self.embedd = discord.Embed(title="Tic Tac Toe", description=''.join(self.grid), color=0xff69b4)
        # return self.embedd
    def get_turn(self) -> str:
        return self.turn

    def update(self, pos) :
        x = circle
        if(self.get_turn() == self.user1) : x = cross
        if(self.grid[pos] == blank) : self.grid[pos] = x
        self.embedd = discord.Embed(title="Tic Tac Toe", description=''.join(self.grid), color=0xff69b4)
        return self.embedd

    def drawGrid(self):
        self.embedd = discord.Embed(title="Tic Tac Toe", description=''.join(self.grid), color=0xff69b4)
        return self.embedd

    def checkWin(self) : 
        if(self.grid[0] == self.grid[1] == self.grid[2] and self.grid[0] != blank): return True
        if(self.grid[4] == self.grid[5] == self.grid[6] and self.grid[4] != blank): return True
        if(self.grid[8] == self.grid[9] == self.grid[10] and self.grid[8] != blank): return True
        if(self.grid[4] == self.grid[0] == self.grid[8] and self.grid[4] != blank): return True
        if(self.grid[1] == self.grid[5] == self.grid[9] and self.grid[1] != blank): return True
        if(self.grid[2] == self.grid[6] == self.grid[10] and self.grid[2] != blank): return True
        if(self.grid[0] == self.grid[5] == self.grid[10] and self.grid[0] != blank): return True
        if(self.grid[8] == self.grid[5] == self.grid[2] and self.grid[8] != blank): return True
        return False

    def checkDraw(self) -> bool :
        for elm in self.grid :
            if elm==blank : return False
        return True
 
async def send_message(message: Message, user_message: str) -> None :
    if not user_message: 
        print('Empty message or intents not enabled')
        return
    global game

    private = user_message[0] == ';'
    valid = user_message[0] == '>'
    user_message = user_message[1:]

    user = str(message.author)
    mchannel = message.channel

    try:
        response = get_response(user_message)
        if(private) :
            await message.author.send(embed=response)
        elif(valid) : 
            if(user_message.startswith('ttt')):
                opp = user_message[4:]
                game = ttt(user, opp)
                gamemsg = await mchannel.send(embed = game.drawGrid(), content = str(game.get_turn()) + "'s turn")
                # print(gamemsg)
                id_game_map[gamemsg.id] = game
                array = [one, two, three, four, five, six, seven, eight, nine]
                for rcn in array : 
                    await gamemsg.add_reaction(rcn)

                print(gamemsg.id)
            else :
                await mchannel.send(embed=response)

    except Exception as e : 
        print(e)
    
@client.event
async def on_ready() -> None : 
    print(f'{client.user} is running')

@client.event
async def on_message(message : Message) -> None : 
    if(message.author == client.user) : return

    uname = str(message.author)
    umessage = str(message.content)
    channel = str(message.channel)

    # print(f'')
    await send_message(message, umessage)


@client.event
async def on_reaction_add(reaction, user) :
    if(user == client.user) : return

    global id_game_map
    msg = reaction.message
    # print("Reaction |", user,'|', game.get_turn())
    allreactions = [one, two, three, 'b' , four, five, six, 'l', seven, eight, nine]
    print(msg.id)


    if(id_game_map.get(msg.id) != None):
        game = id_game_map[msg.id];
        for (idx, rct) in enumerate(allreactions) :
            if(str(reaction.emoji) == str(rct) and game.grid[idx]==blank) : 
                if(str(game.get_turn()) == str(user)) :
                    print("Correct turn")
                    await msg.edit(embed = game.update(idx))
                    await msg.remove_reaction(user)
                    await msg.remove_reaction
                    if(game.checkWin()) : 
                        response = f"{game.turn} wins"
                        await msg.edit(embed = embedded(response), content = "")
                        # await msg.edit(embed =embedded("G A M E O V E R"))
                        del id_game_map[msg.id]
                        break
                    elif(game.checkDraw()) : 
                        await msg.edit(embed = embedded("D R A W"), content = "")
                        # await msg.edit(embed =embedded("G A M E O V E R"))
                        del id_game_map[msg.id]
                        break
                    game.toggleTurn()
                    await msg.edit(content = str(game.get_turn()) + "'s turn")
                else: 
                    print("Not your turn")

            
def main() -> None : 
    client.run(token = TOKEN)

if __name__ == '__main__' : 
    main()