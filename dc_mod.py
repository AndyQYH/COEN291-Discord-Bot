from typing import Any
from discord.interactions import Interaction
from discord.ui import Button, View
import discord
from discord.ui.item import Item
import jokes
import Wallpaper
import os

jokeList = jokes.get_jokes_raw()
jokeList = jokes.joke_preprocess(jokeList)
jokeList = jokes.joke_generate(jokeList)

class MyButton(Button):
    def __init__(self, label, style = discord.ButtonStyle.gray, emoji = None):
        super().__init__(label = label, style=style, emoji= emoji)
    async def callback(self, button, interaction):
        self.disabled = True
        await interaction.followup.send("So you choose " + button.label + "!")
        self.disabled = False
        
class MyView(View):
    def __init__(self, ctx, timeout = 20 ):
        super().__init__(timeout = timeout)
        self.ctx = ctx
        
    @discord.ui.button(label = "random jokes", style=discord.ButtonStyle.green, emoji="😋")
    async def button_callback(self, interaction: discord.Interaction, button: discord.Button):
        button.disabled = True
        await interaction.response.send_message("so you choose " + button.label + " !")
        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        await joke_to_dc(self.ctx, jokeList)
            
    
    @discord.ui.button(label = "dad jokes", style=discord.ButtonStyle.blurple, emoji="😎")
    async def button2_callback(self, button: discord.Button, interaction: discord.Interaction ):
        await interaction.response.send_message("so you choose " + button.label + " !")
    @discord.ui.button(label = "anti jokes", style=discord.ButtonStyle.primary, emoji="🤪")
    async def button3_callback(self, button: discord.Button, interaction: discord.Interaction ):
        await interaction.response.send_message("so you choose " + button.label + " !")
    @discord.ui.button(label = "dirty jokes", style=discord.ButtonStyle.gray, emoji="😍")
    async def button4_callback(self, button: discord.Button, interaction: discord.Interaction ):
        await interaction.response.send_message("so you choose " + button.label + " !")
    @discord.ui.button(label = "long jokes", style=discord.ButtonStyle.secondary, emoji="😯")
    async def button5_callback(self, button: discord.Button, interaction: discord.Interaction ):
        await interaction.response.send_message("so you choose " + button.label + " !")
        
    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view = self)
        
    async def on_timeout(self):
        await self.ctx.send("Timeout!")
        await self.disable_all_items()

    async def on_error(self, interaction, error, item):
        await interaction.response.send_message(str(error))
    
    
async def joke_to_dc(ctx, jokeList):
    joke_imgs = []
    joke = jokes.joke_normalize_GPT(jokeList)
    await ctx.channel.send(joke)
    if len(joke.split(":")) > 1:
        joke = "".join(joke.split(":")[1:])
    joke = "\"" + joke.replace('"', '') + "\""
    Wallpaper.get_wallpaper(joke, "images")
    #await ctx.channel.send(os.listdir(os.getcwd() +"/images"))
    for file in os.listdir(os.getcwd() +"/images"):
        new_file = discord.File("images/" + file)
        joke_imgs.append(new_file)
        await ctx.channel.send(file = new_file)