# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import jokes
import Wallpaper
import settings
from dc_mod import MyView

load_dotenv()
dc_token = os.getenv("DISCORD_TOKEN")
dc_secret = os.getenv("DISCORD_SECRET")
logger = settings.logging.getLogger("bot")
channel_ids = ['1107902507587477525', '863688065590493185']



def run_bot(token):
    # GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents = intents)
    

    # EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
    @bot.event
    async def on_ready():
        
        #print(f'Bot connected as {bot.user}')
        
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        await bot.sync_commands()
        
        #print("____________________")
        
        

    # EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
    '''
    @bot.event
    async def on_message(message):
        # CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
        print(message.content)
        if message.content.lower() == "hello":
            # SENDS BACK A MESSAGE TO THE CHANNEL.
            await message.channel.send("hey dirtbag")
            
        # INCLUDES THE COMMANDS FOR THE BOT. WITHOUT THIS LINE, YOU CANNOT TRIGGER YOUR COMMANDS.
        await bot.process_commands(message)
    '''
    # COMMAND !PING. INVOKES ONLY WHEN THE MESSAGE "$PING" IS SEND IN THE DISCORD SERVER.
    # ALTERNATIVELY !BOT.COMMAND(NAME="PING") CAN BE USED IF ANOTHER FUNCTION NAME IS DESIRED.
    @bot.command(
        # ADDS THIS VALUE TO THE !HELP PING MESSAGE.
        help="Uses come crazy logic to determine if pong is actually the correct value or not.",
        # ADDS THIS VALUE TO THE !HELP PING MESSAGE.
        decription="PING PING PONG PONG",
        # ADDS THIS VALUE TO THE !HELP MESSAGE.
        brief="Prints pong back to the channel."
    )
    async def ping(ctx:commands.Context):
        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        
        await ctx.channel.send("pong " + ctx.author.name)

    # COMMAND !PRINT. THIS TAKES IN A LIST OF ARGUMENTS FROM THE USER AND SIMPLY PRINTS THE VALUES BACK TO THE CHANNEL.
    @bot.command(
        # ADDS THIS VALUE TO THE !HELP PRINT MESSAGE.
        help="Looks like you need some help.",
        # ADDS THIS VALUE TO THE !HELP PING MESSAGE.
        decription="PRINT THE MESSAGE",
        # ADDS THIS VALUE TO THE !HELP MESSAGE.
        brief="Prints the list of values back to the channel."
    )
    async def print(ctx:commands.Context, *args):
        response = ""

        # LOOPS THROUGH THE LIST OF ARGUMENTS THAT THE USER INPUTS.
        for arg in args:
            response = response + " " + arg

        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        await ctx.channel.send(response)
        
    # COMMAND !joke. THIS TAKES IN A LIST OF ARGUMENTS FROM THE USER AND SIMPLY PRINTS THE VALUES BACK TO THE CHANNEL.
    @bot.slash_command(
        # ADDS THIS VALUE TO THE !HELP PRINT MESSAGE.
        description="Looks like you need some help ON JOKING AROUND.",
        
       
    )   
    async def joke(ctx:commands.Context):
        # given users some choices to choose from joke categories
        
        if str(ctx.channel.id) in channel_ids:
            # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
            new_view = MyView(ctx, timeout = 100)
            await ctx.respond("Make a Choice", view = new_view)
        else:
            await ctx.respond("Command not valid in this channel! For permission please ask the host {host}!".format(host = '<@' + str(ctx.guild.owner_id) + '>'))
        
        
        
    # EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.

    bot.run(token = token)

if __name__ == "__main__":
    run_bot(dc_token)