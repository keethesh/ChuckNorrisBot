from aiohttp import ClientSession
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context
from lxml import html
from dotenv import load_dotenv
import os

client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print(f"Logged on as {client.user}!")


async def get_fact():
    async with ClientSession() as session:
        async with session.get("https://chucknorrisfacts.fr/facts/random") as response:
            response = await response.read()

    doc = html.fromstring(response)
    facts = doc.xpath("//p[@class='card-text']")
    return facts[0].text


@client.command()
async def chuck(ctx: Context):
    fact = await get_fact()
    embed = Embed(title="Chuck Fact", description=fact, color=0x0440B9)
    await ctx.send(embed=embed)

load_dotenv()
client.run(os.getenv('BOT_TOKEN'))
