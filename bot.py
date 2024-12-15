
import discord
from discord.ext import commands
import asyncio
import KEY
import gemini
import google.generativeai as genai
import random

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]
intents=discord.Intents.all()
client= commands.Bot(command_prefix = "&",intents = intents)

@client.event
async def on_ready():
    print("you turned me on :3")

@client.command()
async def hello(ctx):
    await ctx.send('you called me :3')

async def get_type(a: str):
    recmodel = genai.GenerativeModel(
        "gemini-1.5-flash",
        safety_settings == safety_settings,
        system_instruction="you will recieve message in quotes and you have to determine it to be either greeting, sayonara, sad, neutral, happy, angry and reply with that specific keyword in lowercase",
    )
    response = recmodel.generate_content(f'"{a}"')
    return response.text

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    try:
        # 40% chances to react on a message
        if random.randint(1, 100) > 40:
            return
        emoji = "🙂"
        msg_type = await get_type(message.content)
        msg_type = msg_type.strip()
        if not msg_type or msg_type not in [
            "sad",
            "happy",
            "angry",
            "greeting",
            "sayonara",
            "neutral",
        ]:
            return

        if msg_type == "sad":
            emoji = random.choice(["\U0001F480", "\U00002620"])  
        elif msg_type == "greeting" or msg_type == "sayonara":
            emoji = random.choice(["\U0001F44B", "\U0001F44B", "\U0001F91D", "\U0001F917"])  
        elif msg_type == "angry":
            emoji = random.choice(["\U0001F9C2", "\U0001F926", "\U0001F921", "\U0001F412"])  
        elif msg_type == "happy":
            emoji = random.choice(["\U0001F60F", "\U0001F633", "\U0001F975", "\U0001F4A6"])  
        elif msg_type == "neutral":
            emoji = random.choice(["\U0001F6B6", "\U0001F468\u200D\U0001F9AF"]) 

        await message.add_reaction(emoji)
        await asyncio.sleep(3)
    except Exception as e:
        await message.channel.send(str(e))

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
