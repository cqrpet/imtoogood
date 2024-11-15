import discord
from discord.ext import commands
import random
import gemini
import asyncio
import KEY

intents=discord.Intents.all()


client= commands.Bot(command_prefix = "&",intents = intents)



@client.event
async def on_ready():
    print("you turned me on :3")


@client.command()
async def hello(ctx):
    await ctx.send('you called me :3')


@client.event
async def on_message(message: discord.Message):
    if message.author.id == 1257628900939272252 :
        pass

    else:
        if message.content and message.content[0] != "&":
            channel = message.channel
            await asyncio.sleep(3)
            response = gemini.res(str(message.content))
            await channel.send(response)
        await client.process_commands(message)


@client.command()
async def uwu(ctx):
    await ctx.send('uwu')
    print(ctx)





client.run(KEY.DKEY)
