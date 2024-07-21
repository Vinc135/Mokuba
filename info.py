import discord
import datetime
from typing import Literal
import random
import datetime
   
def limit_characters(string: str, limit: int):
    if len(string) > limit:
        return string[:limit-3] + "..."
    return string

async def send_error(title, description, interaction):
    embed = discord.Embed(colour=discord.Colour.red(), title=title, description=description)
    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
    try:
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except:
        try:
            await interaction.response.send_message("** Mir fehlt die Berechtigung 'Nachrichten einbetten'.**", ephemeral=True)
        except:
            pass