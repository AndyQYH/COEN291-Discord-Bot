from typing import Any
from discord.ui import Button, View
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
    def __init__(self, ctx, timeout = 20):
        super().__init__(timeout = timeout)
        self.ctx = ctx
        
    @discord.ui.button(label = "random jokes", style=discord.ButtonStyle.green, emoji="😋")
    async def button_callback(self,  button: discord.Button, interaction: discord.Interaction):
        
        await interaction.response.send_message("so you choose " + button.label + " !")
        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        await joke_to_dc(self.ctx)
        self.stop()
    
    @discord.ui.button(label = "dad jokes", style=discord.ButtonStyle.blurple, emoji="😎")
    async def button2_callback(self,  button: discord.Button, interaction: discord.Interaction):
        await interaction.response.send_message("so you choose " + button.label + " !")
        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        await joke_to_dc(self.ctx, file = "dadjokes.txt")
        self.stop()
    @discord.ui.button(label = "anti jokes", style=discord.ButtonStyle.primary, emoji="🤪")
    async def button3_callback(self,  button: discord.Button, interaction: discord.Interaction):
        await interaction.response.send_message("so you choose " + button.label + " !")
        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        await joke_to_dc(self.ctx, file = "antijokes.txt")
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
    async def button5_callback(self,  button: discord.Button, interaction: discord.Interaction):
        await interaction.response.send_message("so you choose " + button.label + " !")
        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        await joke_to_dc(self.ctx, file = "long_jokes.txt")
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
    
    
async def joke_to_dc(ctx, file = "all_jokes.txt", path = joke_path):
    jokeList = jokes.get_jokes_raw(file, path)
    jokeList = jokes.joke_preprocess(jokeList)
    jokeList = jokes.joke_generate(jokeList)
    joke_imgs = []
    joke = ''
    if file == "dirtyjokes.txt":
        joke = jokes.joke_normalize_GPT(jokeList, prompt = "Here is a joke: {joke} \n Can you modify this joke to be appropriate? I want the rewritten joke to have a similar number of words to the original joke.  \n")
    else:
        joke = jokes.joke_normalize_GPT(jokeList)
        
    await ctx.channel.send(joke)
    joke_prompt = jokes.joke_prompitize_GPT(joke)
    await ctx.channel.send(joke_prompt)
    if len(joke.split(":")) > 1:
        joke = "".join(joke.split(":")[1:])
    joke = "\"" + joke.replace('"', '') + "\""
    Wallpaper.get_wallpaper(quote = joke, prompt = joke_prompt, image_path = "images", source = "prompthero")
    #await ctx.channel.send(os.listdir(os.getcwd() +"/images"))
    for file in os.listdir(os.getcwd() +"/images"):
        new_file = discord.File("images/" + file)
        joke_imgs.append(new_file)
        await ctx.channel.send(file = new_file)
    Wallpaper.get_wallpaper(quote = joke, prompt = joke_prompt, image_path = "images")
    for file in os.listdir(os.getcwd() +"/images"):
        new_file = discord.File("images/" + file)
        joke_imgs.append(new_file)
        await ctx.channel.send(file = new_file)
    
    