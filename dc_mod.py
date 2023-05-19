from typing import Any
from discord.ui import Button, View ,Select
import discord.interactions
import discord
import jokes
import Wallpaper
import os


joke_path = "jokes/"

class MyButton(Button):
    def __init__(self, label, style = discord.ButtonStyle.gray, emoji = None):
        super().__init__(label = label, style=style, emoji= emoji)
    async def callback(self, button, interaction):
        self.disabled = True
        await interaction.followup.send("So you choose " + button.label + "!")
        self.disabled = False
        
class MyView(View):
    def __init__(self, ctx, timeout = 50):
        super().__init__(timeout = timeout)
        self.ctx = ctx
        
    @discord.ui.button(label = "random jokes", style=discord.ButtonStyle.green, emoji="😋")
    async def button1_callback(self,  button: discord.Button, interaction: discord.Interaction):
        
        await interaction.response.send_message(content = "Here it is: \n\n")
        joke = joke_to_dc()
        joke_new = joke.split('\n')[2].split(':')[1]
        print("jokes: \n", joke)
        await interaction.edit_original_response(content = "Here it is: \n\n" + joke + '\n', view = MyJokeView(self.ctx, joke_new))
        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        
        self.stop()
    
    @discord.ui.button(label = "dad jokes", style=discord.ButtonStyle.blurple, emoji="😎")
    async def button2_callback(self,  button: discord.Button, interaction: discord.Interaction):
        await interaction.response.send_message(content = "Here it is: \n\n")
        joke = joke_to_dc(file="dadjokes.txt")
        #print("jokes: \n", joke)
        await interaction.edit_original_response(content = "Here it is: \n\n" + joke + '\n', view = MyJokeView(self.ctx, joke))
        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        
        self.stop()
    @discord.ui.button(label = "anti jokes", style=discord.ButtonStyle.primary, emoji="🤪")
    async def button3_callback(self,  button: discord.Button, interaction: discord.Interaction):
        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        await interaction.response.send_message(content = "Here it is: \n\n")
        joke = joke_to_dc(file="antijokes.txt")
        #print("jokes: \n", joke)
        await interaction.edit_original_response(content = "Here it is: \n\n" + joke + '\n', view = MyJokeView(self.ctx, joke))
        self.stop()

    '''
    @discord.ui.button(label = "dirty jokes", style=discord.ButtonStyle.gray, emoji="😍")
    async def button4_callback(self,  button: discord.Button, interaction: discord.Interaction):
        await interaction.response.send_message("so you choose " + button.label + " !")
        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        await joke_to_dc(self.ctx, file = "dirtyjokes.txt")
        self.stop()
    '''
    @discord.ui.button(label = "long jokes", style=discord.ButtonStyle.secondary, emoji="😯")
    async def button4_callback(self,  button: discord.Button, interaction: discord.Interaction):
        
        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        await interaction.response.send_message(content = "Here it is: \n\n")
        joke = joke_to_dc(file="long_jokes.txt")
        print("jokes: \n", joke)
        await interaction.edit_original_response(content = "Here it is: \n\n" + joke + '\n', view = MyJokeView(self.ctx, joke))
        
        self.stop()
        
    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        
        await self.message.edit(view = self)
    async def on_timeout(self):
        await self.ctx.send("Timeout!")
        await self.disable_all_items()

    async def on_error(self, interaction, error, item):
        await interaction.response.send_message(str(error))
        
class MyJokeView(View):
    def __init__(self, ctx, joke, timeout = 100):
        super().__init__(timeout = timeout)
        self.ctx = ctx
        self.joke = joke
        
    @discord.ui.button(label = "Go with this", style=discord.ButtonStyle.blurple, emoji="✅")
    async def buttonG_callback(self,  button: discord.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Cool let's generate an image for your joke next !", view = MySelectView(self.ctx, joke = self.joke))
        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        #await joke_to_dc(self.ctx)
        self.stop()
    
    @discord.ui.button(label = "New One Please", style=discord.ButtonStyle.blurple, emoji="❌")
    async def buttonR_callback(self,  button: discord.Button, interaction: discord.Interaction):
        
        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        await interaction.response.send_message(content = "Here is a new one: \n\n")
        joke = ""
        if button.label == "random jokes":
            joke = joke_to_dc()
        elif button.label == "dad jokes":
            joke = joke_to_dc(file = "dadjokes.txt")
        elif button.label == "anti jokes":
            joke = joke_to_dc(file = "antijokes.txt")
        else:
            joke = joke_to_dc(file = "long_jokes.txt")
        print("jokes: \n", joke)
        await interaction.edit_original_response(content = "Here it a new one: \n\n" + joke + '\n', view = MyJokeView(self.ctx, joke = joke))
        
        
        self.stop()
    
        
    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        
        await self.message.edit(view = self)
    async def on_timeout(self):
        await self.ctx.send("Timeout!")
        await self.disable_all_items()

    async def on_error(self, interaction, error, item):
        await interaction.response.send_message(str(error))
        
class MySelectView(View):
    def __init__(self, ctx, joke, timeout = 100):
        super().__init__(timeout = timeout)
        self.ctx = ctx
        self.joke = joke
        
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a Model for Art Generation!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 2, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="PromptHero/OpenJourney",
                description="Pick this if you like more photo realistic art!",
                emoji = '⛵'
            ),
            discord.SelectOption(
                label="Stability.ai Stable Diffusion SD XL",
                description="Pick this if you like more casual art!",
                emoji = '🧢'
            )
        ]
    )
    async def select_callback(self, select:discord.ui.select, interaction:discord.interactions): # the function called when the user is done selecting options
        
        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too! \n\n ")
        await joke_pic_to_dc(self.ctx, self.joke, pic_source=select.values[0])
        new_view = MyView(self.ctx, timeout = 100)
        await self.ctx.channel.send(view = new_view)
    
def joke_to_dc(file = "all_jokes.txt", path = joke_path) -> str:
    jokeList = jokes.get_jokes_raw(file, path)
    jokeList = jokes.joke_preprocess(jokeList)
    jokeList = jokes.joke_generate(jokeList)
    
    joke = ''
    if file == "dirtyjokes.txt":
        joke = jokes.joke_normalize_GPT(jokeList, prompt = "Here is a joke: {joke} \n Can you modify this joke to be appropriate? I want the rewritten joke to have a similar number of words to the original joke.  \n")
    else:
        joke = jokes.joke_normalize_GPT(jokeList)
        
    return joke

async def joke_pic_to_dc(ctx, joke, pic_source = "Stability.ai Stable Diffusion SD XL"):
    joke_imgs = []
    joke_prompt = jokes.joke_prompitize_GPT(joke, prompt= "Open Journey")
  
    await ctx.channel.send("Here is the prompt for the joke pic: \n\n" + joke_prompt)
    
    Wallpaper.get_wallpaper(quote = joke, prompt = joke_prompt, image_path = "images", source = pic_source)
    #await ctx.channel.send(os.listdir(os.getcwd() +"/images"))
    for file in os.listdir(os.getcwd() +"/images"):
        new_file = discord.File("images/" + file)
        joke_imgs.append(new_file)
        await ctx.channel.send(file = new_file)
    
    