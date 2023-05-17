# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import jokes
import Wallpaper
import settings

load_dotenv()
dc_token = os.getenv("DISCORD_TOKEN")
dc_secret = os.getenv("DISCORD_SECRET")
logger = settings.logging.getLogger("bot")
jokeList = jokes.get_jokes_raw()
jokeList = jokes.joke_preprocess(jokeList)
jokeList = jokes.joke_generate(jokeList)


def run_bot(token):
    # GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents = intents)


    # EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
    @bot.event
    async def on_ready():
        
        #print(f'Bot connected as {bot.user}')
        
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
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
    async def ping(ctx):
        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        print(type(ctx))
        await ctx.channel.send("pong")

    # COMMAND !PRINT. THIS TAKES IN A LIST OF ARGUMENTS FROM THE USER AND SIMPLY PRINTS THE VALUES BACK TO THE CHANNEL.
    @bot.command(
        # ADDS THIS VALUE TO THE !HELP PRINT MESSAGE.
        help="Looks like you need some help.",
        # ADDS THIS VALUE TO THE !HELP PING MESSAGE.
        decription="PRINT THE MESSAGE",
        # ADDS THIS VALUE TO THE !HELP MESSAGE.
        brief="Prints the list of values back to the channel."
    )
    async def print(ctx, *args):
        response = ""

        # LOOPS THROUGH THE LIST OF ARGUMENTS THAT THE USER INPUTS.
        for arg in args:
            response = response + " " + arg

        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        await ctx.channel.send(response)
        
    # COMMAND !joke. THIS TAKES IN A LIST OF ARGUMENTS FROM THE USER AND SIMPLY PRINTS THE VALUES BACK TO THE CHANNEL.
    @bot.command(
        # ADDS THIS VALUE TO THE !HELP PRINT MESSAGE.
        help="Looks like you need some help ON JOKING AROUND.",
        # ADDS THIS VALUE TO THE !HELP MESSAGE.
        brief="Randomly generates a joke that can either be super good or super bad."
    )   
    async def joke(ctx):
        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        joke_imgs = []
        joke = jokes.joke_normalize_GPT(jokeList)
        await ctx.channel.send(joke)
        if len(joke.split(":")) > 1:
            joke = "".join(joke.split(":")[1:])
        joke = "\"" + joke.replace('"', '') + "\""
        Wallpaper.get_wallpaper(joke, "images")
        #await ctx.channel.send(os.listdir(os.getcwd() +"/images"))
        for file in os.listdir(os.getcwd() +"/images"):
            if file == "created_image.png":
                new_file = discord.File("images/" + file)
                joke_imgs.append(new_file)
        await ctx.channel.send(files = joke_imgs)
    
    # EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.

    bot.run(token = token, root_logger=True)

if __name__ == "__main__":
    run_bot(dc_token)