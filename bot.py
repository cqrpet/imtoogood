import discord
from discord.ext import commands
import gemini
import asyncio
import KEY
import google.generativeai as genai

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

@client.command(name="chat", help="chat with ai")
async def chat_command(ctx: commands.Context, *, message: str):
    # default history
    if not hasattr(client, "chat_history"):
        client.chat_history = [
            {"role": "user", "parts": "hello "},
            {"role": "model", "parts": "sup? what you doing"},
        ]
    generation_config = {
            "temperature": 1.5,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 80,
            "response_mime_type": "text/plain",
        }
    safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
    model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            safety_settings=safety_settings,
            system_instruction="your dull and you don't like talking at all and your an genderless bot who specializes in python and acts cool you play games like minecraft osu and valorant you dont have alot of friends irl but you have whole different online social life with alot of friends your good at any games you play you dont like helping other people your lazy but your loving \n",
        )
    await ctx.defer()
    async with ctx.typing():
        chat = model.start_chat(history=client.chat_history)

        user_message = {"role": "user", "parts": message}
        client.chat_history.append(user_message)
        response = chat.send_message(message)

        model_message = {"role": "model", "parts": response.text}
        client.chat_history.append(model_message)
        if len(client.chat_history) > 20:
            client.chat_history = client.chat_history[-20:]

        await ctx.send(response.text)




client.run(KEY.DKEY)
