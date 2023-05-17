from discord.ui import Button, View
import discord
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
    def __init__(self, ctx):
        super().__init__(timeout = 20)
        self.ctx = ctx
        
    @discord.ui.button(label = "random jokes", style=discord.ButtonStyle.green, emoji="😋")
    async def button_callback(self, button, interaction):
        button.disable = True
        await interaction.followup.send("so you choose " + button.label + "!")
        # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
        joke_imgs = []
        joke = jokes.joke_normalize_GPT(jokeList)
        await self.ctx.channel.send(joke)
        if len(joke.split(":")) > 1:
            joke = "".join(joke.split(":")[1:])
        joke = "\"" + joke.replace('"', '') + "\""
        Wallpaper.get_wallpaper(joke, "images")
        #await ctx.channel.send(os.listdir(os.getcwd() +"/images"))
        for file in os.listdir(os.getcwd() +"/images"):
            new_file = discord.File("images/" + file)
            joke_imgs.append(new_file)
            await self.ctx.channel.send(file = new_file)
    '''
    @MyButton(label = "dad jokes", style=discord.ButtonStyle.blurple, emoji="😎")
    async def callback(self, interaction):
    @MyButton(label = "anti jokes", style=discord.ButtonStyle.primary, emoji="🤪")
    async def callback(self, interaction):
    @MyButton(label = "dirty jokes", style=discord.ButtonStyle.gray, emoji="😍")
    async def callback(self, interaction):
    @MyButton(label = "long jokes", style=discord.ButtonStyle.secondary, emoji="😯")
    '''