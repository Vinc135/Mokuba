import os
import discord
from discord.ext import commands
import traceback
import sys
from info import send_error, limit_characters
import math
from discord.app_commands import AppCommandError
from discord import app_commands
import time
from dotenv import load_dotenv

load_dotenv()

class Mokuba(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix="mokuba!", case_insensitive=True, intents=discord.Intents.all())
        self.giveaways = False
        self.votes = False
        self.reminder = False

    async def on_message(self, msg):
        if msg.guild == None:
            return
        if msg.author.bot is True:
            return
        if msg.mentions:
            if msg.mentions[0] == bot.user:
                if msg.reference:
                    return
                #erwähnungsmessage senden? optional
                return await bot.process_commands(msg)
            else:
                await bot.process_commands(msg)
        await bot.process_commands(msg)

    async def setup_hook(self):
        try:
            geladen = 0
            fehler = 0
            await bot.load_extension("jishaku")
            
            for filename in os.listdir("cogs"):
                if filename.endswith(".py"):
                    try:
                        if f"cogs.{filename[:-3]}" == "cogs.event":
                            continue
                        await bot.load_extension(f"cogs.{filename[:-3]}")
                        geladen += 1
                    except:
                        fehler += 1
                        print(f'❌ cogs.{filename[:-3]} konnte nicht geladen werden', file=sys.stderr)
                        traceback.print_exc()		
                        print('\n\n--------------------------------------------\n\n')
     
            print(f"✅ {geladen}/{geladen + fehler} Cogs geladen")
        except Exception as e:
            print(f"❌ Es gab einen Fehler beim Laden der Cogs\n{e}")
        ##########                   ##########
        print("""
 __  __       _          _           
|  \/  |     | |        | |          
| \  / | ___ | | ___   _| |__   __ _ 
| |\/| |/ _ \| |/ / | | | '_ \ / _` |
| |  | | (_) |   <| |_| | |_) | (_| |
|_|  |_|\___/|_|\_\\__,_|_.__/ \__,_|""")
        
    async def on_ready(self):
        try:
            await bot.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.playing, name="YuGiOh"))
            print("✅ Status bereit")
        except:
            print("❌ Status nicht bereit")
        print("✅ Alle System sind nun bereit.")

bot = Mokuba()

@bot.event
async def on_error(ctx, error):
    return 

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await send_error("Fehlende Berechtigungen", "Du hast nicht die Rechte, diesen Command auszuführen.", interaction)
        return
    if isinstance(error,app_commands.CommandInvokeError):
        pass
    if isinstance(error,app_commands.MissingAnyRole):
        await send_error("Fehlende Berechtigungen", "Du brauchst eine bestimmte Rolle um dies zu tun.", interaction)
        return
    if isinstance(error,app_commands.MissingRole):
        await send_error("Fehlende Berechtigungen", "Du brauchst eine bestimmte Rolle um dies zu tun.", interaction)
        return
    if isinstance(error, app_commands.CommandOnCooldown):

        seconds_in_day = 86400
        seconds_in_hour = 3600
        seconds_in_minute = 60

        seconds = error.retry_after

        days = seconds // seconds_in_day
        seconds = seconds - (days * seconds_in_day)

        hours = seconds // seconds_in_hour
        seconds = seconds - (hours * seconds_in_hour)

        minutes = seconds // seconds_in_minute
        seconds = seconds - (minutes * seconds_in_minute)
        if math.ceil(error.retry_after) <= 60:  # seconds
            await send_error("Auf Cooldown", f"Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(seconds)}** Sekunden erneut.", interaction)
            return
        if math.ceil(error.retry_after) <= 3600:  # minutes
            await send_error("Auf Cooldown", f"Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(minutes)}** Minuten and **{math.ceil(seconds)}** Sekunden.", interaction)
            return
        if math.ceil(error.retry_after) <= 86400:  # hours
            await send_error("Auf Cooldown", f"Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(hours)}** Stunden, **{math.ceil(minutes)}** Minuten and **{math.ceil(seconds)}** Sekunden.", interaction)
            return
        if math.ceil(error.retry_after) >= 86400:  # days
            await send_error("Auf Cooldown", f"Dieser Command ist auf Cooldown. Bitte versuche es in **{math.ceil(days)}** Tagen, **{math.ceil(hours)}** Stunden, **{math.ceil(minutes)}** Minuten and **{math.ceil(seconds)}** Sekunden.", interaction)
            return
    if isinstance(error,app_commands.BotMissingPermissions):
        await send_error("Fehlende Berechtigungen", "Ich habe keine Berechtigungen um das zu tun.", interaction)
        return
    if isinstance(error,app_commands.CommandNotFound):
        return
    if isinstance(error,app_commands.NoPrivateMessage):
        await send_error("Kein Zugang", "Dieser Command funktioniert nur in Servern.", interaction)
        return
    if isinstance(error,app_commands.TransformerError):
        await send_error("Nicht gefunden", "Die ausgewählte Person o.Ä. konnte nicht gefunden werden.", interaction)
        return
    else:
        await send_error("Unbekannt", "Ein unbekannter Fehler ist aufgetreten.", interaction)
        guilds = bot.get_guild(1089328006880833626)
        channels = guilds.get_channel(1090568310178971668)

        traceback_string = traceback.format_exception(type(error), error, error.__traceback__)

        embed = discord.Embed(colour=discord.Colour.red(), title="Error (Application Command)", description=f"""
**Informationen**
{interaction.user.mention}
`{interaction.guild.name}` | {interaction.guild.id} ({interaction.guild.member_count})
{interaction.channel.mention}
<t:{int(time.time())}:R>
`/{interaction.command.name}`""")
        embed.add_field(name="Error", value=f"```py\n" + limit_characters(''.join(traceback_string[-1]), 1010) + "```", inline=False)
        embed.add_field(name="Traceback", value=f"```py\n" + limit_characters(''.join(traceback_string), 1010) + "```", inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/811730903822368833/823531509461942294/2000px-Dialog-error-round.svg.png")
        await channels.send(embed=embed)
        return

@bot.command()
async def sync(ctx, serverid: int=None):
    """Synchronisiere bestimmte Commands."""
    if ctx.author.id == 824378909985341451:
        if serverid is None:
            try:
                s = await bot.tree.sync()
                globalembed = discord.Embed(color=discord.Color.blue(), title="Synchronisierung", description=f"Die Synchronisierung von `{len(s)} Commands` wurde eingeleitet.\nEs wird ungefähr eine Stunde dauern, damit sie global angezeigt werden.")
                await ctx.send(embed=globalembed)
            except Exception as e:
                await ctx.send(f"**Synchronisierung fehlgeschlagen**\n```\n{e}```")
        if serverid is not None:
            guild = bot.get_guild(int(serverid))
            if guild:
                try:
                    s = await bot.tree.sync(guild=discord.Object(id=guild.id))
                    localembed = discord.Embed(color=discord.Color.blue(), title="Synchronisierung", description=f"Die Synchronisierung von `{len(s)} Commands` ist fertig.\nEs wird nur maximal eine Minute dauern, weil sie nur auf dem Server {guild.name} synchronisiert wurden.")
                    await ctx.send(embed=localembed)
                except Exception as e:
                    await ctx.send(f"**Synchronisierung fehlgeschlagen**\n```\n{e}```")
            if guild is None:
                await ctx.send(f"Der Server mit der ID `{serverid}` wurde nicht gefunden.")

bot.run(os.getenv("token"), reconnect=True)