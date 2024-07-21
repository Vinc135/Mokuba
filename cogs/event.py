import datetime
import discord
from discord.ext import commands
import typing
from discord import app_commands
import aiosqlite
from table2ascii import table2ascii as t2a, PresetStyle

#########
async def duellanten_liste(page, liste):
    duellantenliste = ""
    if page == 1:
        von = 0
        bis = 10
        
    if page != 1:
        von = (page - 1) * 10
        bis = von + 10
    
    duellantenliste += "```"
    duellanten = []
    for index, duellant in enumerate(liste):
        if index <= bis and index >= von:
            duellanten.append([duellant['Rang'], duellant['Duellant'], duellant['Wins / Losses'], duellant['Duelle gesamt'], duellant['Winratio']])

    output = t2a(
        header=["Rang", "Duellant", "W/L", "Duelle", "Winratio"],
        body=duellanten,
        first_col_heading=True
    )

    duellantenliste += output
    duellantenliste += "```"
    return duellantenliste

async def stats_liste(page, liste):
    matchliste = ""
    if page == 1:
        von = 0
        bis = 10

    if page != 1:
        von = (page - 1) * 10
        bis = von + 10

    matchliste + "\n**Match-Verläufe**\n"
    for index, match in enumerate(liste):
        if index <= bis and index >= von:
            spieler1 = match['Spieler 1']
            spieler2 = match['Spieler 2']
            spieler1score = match['Spieler 1 Score']
            spieler2score = match['Spieler 2 Score']
            datum = match['Datum']

            if spieler1 and spieler2:
                matchliste += f"{spieler1.mention} vs {spieler2.mention} {spieler1score}:{spieler2score}"
            else:
                matchliste += f"{spieler1.mention} vs Unknown {spieler1score}:{spieler2score}"

            matchliste += f" - {datum}\n"
    return matchliste

class bestenliste(discord.ui.View):
    def __init__(self, liste):
        super().__init__(timeout=None)
        self.liste = liste
        if int(len(liste)) < 10:
            self.max_pages = 1
        else:
            self.max_pages: int = round((int(len(liste))) / 10)

    @discord.ui.button(label='Zurück', style=discord.ButtonStyle.red, custom_id="grth676zetwerf43e", emoji="⬅️")
    async def zurück(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            p = int(str(interaction.message.embeds[0].footer.text)[6])
            page = f"{p}{int(str(interaction.message.embeds[0].footer.text)[7])}"
            int(page)
        except:
            page = int(str(interaction.message.embeds[0].footer.text)[6])
        new_page = page - 1
        if new_page <= 0:
            new_page = self.max_pages
        embed = discord.Embed(title='Event Duellanten Ranking', description=await duellanten_liste(new_page, self.liste),
                            colour=discord.Colour.blue()).set_footer(text=f'Seite {new_page} von {self.max_pages}')
        await interaction.response.edit_message(embed=embed, content="")
    
    @discord.ui.button(label='Weiter', style=discord.ButtonStyle.green, custom_id="fewgwrgwrtgtg", emoji="➡️")
    async def vor(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            p = int(str(interaction.message.embeds[0].footer.text)[6])
            page = f"{p}{int(str(interaction.message.embeds[0].footer.text)[7])}"
            int(page)
        except:
            page = int(str(interaction.message.embeds[0].footer.text)[6])
        new_page = page + 1
        if new_page > int(self.max_pages):
            new_page = self.max_pages
        embed = discord.Embed(title='Event Duellanten Ranking', description=await duellanten_liste(new_page, self.liste),
                            colour=discord.Colour.blue()).set_footer(text=f'Seite {new_page} von {self.max_pages}')
        await interaction.response.edit_message(embed=embed, content="")
    
class statsliste(discord.ui.View):
    def __init__(self, user, liste):
        super().__init__(timeout=None)
        self.liste = liste
        self.user = user
        if int(len(liste)) < 10:
            self.max_pages = 1
        else:
            self.max_pages: int = round((int(len(liste))) / 10)

    @discord.ui.button(label='Zurück', style=discord.ButtonStyle.red, custom_id="fsrdrgr", emoji="⬅️")
    async def zurück(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            p = int(str(interaction.message.embeds[0].footer.text)[6])
            page = f"{p}{int(str(interaction.message.embeds[0].footer.text)[7])}"
            int(page)
        except:
            page = int(str(interaction.message.embeds[0].footer.text)[6])
        new_page = page - 1
        if new_page <= 0:
            new_page = self.max_pages
        embed = discord.Embed(title=f'Duellant {self.user.display_name}', description=await stats_liste(new_page, self.liste),
                            colour=discord.Colour.blue()).set_footer(text=f'Seite {new_page} von {self.max_pages}')
        await interaction.response.edit_message(embed=embed, content="")
    
    @discord.ui.button(label='Weiter', style=discord.ButtonStyle.green, custom_id="bsbgbdtg", emoji="➡️")
    async def vor(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            p = int(str(interaction.message.embeds[0].footer.text)[6])
            page = f"{p}{int(str(interaction.message.embeds[0].footer.text)[7])}"
            int(page)
        except:
            page = int(str(interaction.message.embeds[0].footer.text)[6])
        new_page = page + 1
        if new_page > int(self.max_pages):
            new_page = self.max_pages
        embed = discord.Embed(title=f'Duellant {self.user.display_name}', description=await stats_liste(new_page, self.liste),
                            colour=discord.Colour.blue()).set_footer(text=f'Seite {new_page} von {self.max_pages}')
        await interaction.response.edit_message(embed=embed, content="")

class duellstats(discord.ui.View):
    def __init__(self, user_a, user_b, liste):
        super().__init__(timeout=None)
        self.liste = liste
        self.user_a = user_a
        self.user_b = user_b
        if int(len(liste)) < 10:
            self.max_pages = 1
        else:
            self.max_pages: int = round((int(len(liste))) / 10)

    @discord.ui.button(label='Zurück', style=discord.ButtonStyle.red, custom_id="fsrdrgr", emoji="⬅️")
    async def zurück(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            p = int(str(interaction.message.embeds[0].footer.text)[6])
            page = f"{p}{int(str(interaction.message.embeds[0].footer.text)[7])}"
            int(page)
        except:
            page = int(str(interaction.message.embeds[0].footer.text)[6])
        new_page = page - 1
        if new_page <= 0:
            new_page = self.max_pages
        embed = discord.Embed(title=f'{self.user_a.display_name} vs {self.user_b.display_name}', description=await stats_liste(new_page, self.liste),
                            colour=discord.Colour.blue()).set_footer(text=f'Seite {new_page} von {self.max_pages}')
        await interaction.response.edit_message(embed=embed, content="")
    
    @discord.ui.button(label='Weiter', style=discord.ButtonStyle.green, custom_id="bsbgbdtg", emoji="➡️")
    async def vor(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            p = int(str(interaction.message.embeds[0].footer.text)[6])
            page = f"{p}{int(str(interaction.message.embeds[0].footer.text)[7])}"
            int(page)
        except:
            page = int(str(interaction.message.embeds[0].footer.text)[6])
        new_page = page + 1
        if new_page > int(self.max_pages):
            new_page = self.max_pages
        embed = discord.Embed(title=f'{self.user_a.display_name} vs {self.user_b.display_name}', description=await stats_liste(new_page, self.liste),
                            colour=discord.Colour.blue()).set_footer(text=f'Seite {new_page} von {self.max_pages}')
        await interaction.response.edit_message(embed=embed, content="")

class duellbestätigung(discord.ui.View):
    def __init__(self, spieler1, spieler2, score_spieler_1, score_spieler_2, bot=None):
        super().__init__(timeout=None)
        self.spieler1 = spieler1
        self.spieler2 = spieler2
        self.score_spieler_1 = score_spieler_1
        self.score_spieler_2 = score_spieler_2
        self.bot = bot

    @discord.ui.button(label='Bestätigen', style=discord.ButtonStyle.green, custom_id="IZTSFOUZWGIZDSGWUZDFIZ", emoji="✅")
    async def bestätigen(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.spieler2:
            return await interaction.response.send_message("**❌ Du kannst dies nicht tun.**", ephemeral=True)

        async with aiosqlite.connect("eventdb.db") as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS duelle(spieler1ID TEXT, spieler2ID TEXT, spieler1score INT, spieler2score INT, datum TEXT)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS spieler(userID TEXT, wins INT, losses INT)")
            c = await cursor.execute("SELECT userID FROM spieler WHERE userID = ?", (self.spieler1.id,))
            result = await c.fetchone()
            if result is None:
                await cursor.execute("INSERT INTO spieler(userID, wins, losses) VALUES (?, ?, ?)", (self.spieler1.id, self.score_spieler_1, self.score_spieler_2))
            else:
                await cursor.execute("UPDATE spieler SET wins = wins + ?, losses = losses + ? WHERE userID = ?", (self.score_spieler_1, self.score_spieler_2, self.spieler1.id))
            
            c2 = await cursor.execute("SELECT userID FROM spieler WHERE userID = ?", (self.spieler2.id,))
            result2 = await c2.fetchone()
            if result2 is None:
                await cursor.execute("INSERT INTO spieler(userID, wins, losses) VALUES (?, ?, ?)", (self.spieler2.id, self.score_spieler_2, self.score_spieler_1))
            else:
                await cursor.execute("UPDATE spieler SET wins = wins + ?, losses = losses + ? WHERE userID = ?", (self.score_spieler_2, self.score_spieler_1, self.spieler2.id))
            
            await cursor.execute("INSERT INTO duelle(spieler1score, spieler2score, spieler1ID, spieler2ID, datum) VALUES(?, ?, ?, ?, ?)", (self.score_spieler_1, self.score_spieler_2, self.spieler1.id, self.spieler2.id, datetime.datetime.now().strftime("%d.%m.%Y")))
            await cursor.commit()

        embed = discord.Embed(color=discord.Color.blue(), title="Event Match-Ergebnis")
        embed.add_field(name=f"{self.spieler1.display_name} vs {self.spieler2.display_name}", value=f"{self.score_spieler_1}:{self.score_spieler_2}")
        embed.add_field(name="Bestätigung", value=f"✅ {self.spieler2.display_name} hat dieses Spiel bestätigt.")

        await interaction.response.edit_message(content=None, embed=embed, view=None)


    @discord.ui.button(label='Abbrechen', style=discord.ButtonStyle.red, custom_id="67D799H969i69796HDiiU7", emoji="❌")
    async def ablehnen(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.spieler2 and interaction.user != self.spieler1:
            return await interaction.response.send_message("**❌ Du kannst dies nicht tun.**", ephemeral=True)

        await interaction.response.edit_message(content=f"**❌ Vorgang abgebrochen durch {interaction.user.mention}**", view=None, embed=None)

class event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def eventduell(self, interaction: discord.Interaction, gegner: discord.Member, meine_wins: typing.Literal[0, 1, 2, 3, 4, 5], meine_loses: typing.Literal[0, 1, 2, 3, 4, 5]):
        """Registriere einen Spielstand eines Spieles."""
        if gegner.id == interaction.user.id:
            return await interaction.response.send_message("Du kannst nicht gegen dich selbst spielen.", ephemeral=True)
        embed = discord.Embed(color=discord.Color.blue(), title="Event Match-Ergebnis")
        embed.add_field(name=f"{interaction.user.display_name} vs {gegner.display_name}", value=f"{meine_wins}:{meine_loses}")

        embed.add_field(name="Spielstand-Überprüfung", value=f"Duell zwischen {interaction.user.mention} und {gegner.mention}")
        embed.set_footer(text=f"{gegner.display_name} muss das Ergebnis bestätigen, damit die Werte gelten.")

        try:
            await interaction.response.send_message(gegner.mention, embed=embed, view=duellbestätigung(interaction.user, gegner, meine_wins, meine_loses))
        except:
            pass

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def eventbestenliste(self, interaction: discord.Interaction):
        """Schau dir die besten Spieler an."""
        async with aiosqlite.connect("eventdb.db") as connection:
            cursor = await connection.execute("SELECT userID, wins, losses FROM spieler ORDER BY wins DESC")
            result = await cursor.fetchall()

            embed = discord.Embed(color=discord.Color.blue(), title="Event Duellanten Ranking")
            embed.set_footer(text=f"Seite 1")

            all_players = []
            duellanten = []
            for index, eintrag in enumerate(result, start=1):
                player_id = eintrag[0]
                player = interaction.guild.get_member(int(player_id))
                if player:
                    player_name = player.display_name if len(player.display_name) <= 15 else player.display_name[:12] + "..."
                else:
                    player_name = str(player_id)
                wins = eintrag[1]
                losses = eintrag[2]
                total_duels = wins + losses
                win_ratio = (wins / (wins + losses) * 100 if (wins + losses) > 0 else 0)


                player_info = {
                    "Rang": index,
                    "Duellant": player_name,
                    "Wins / Losses": f"{wins}/{losses}",
                    "Duelle gesamt": total_duels,
                    "Winratio": f"{win_ratio:.2f}%",
                }
                all_players.append(player_info)

                if index <= 10:
                    duellanten.append([player_info["Rang"], player_info["Duellant"], player_info["Wins / Losses"], player_info["Duelle gesamt"], player_info["Winratio"]])
            
            output = t2a(
                header=["Rang", "Duellant", "W/L", "Duelle", "Winratio"],
                body=duellanten,
                first_col_heading=True
            )
            embed.description = "```" + output + "```"

            await interaction.response.send_message(embed=embed, view=bestenliste(all_players))



    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def eventstats(self, interaction: discord.Interaction, user: discord.Member=None):
        """Zeigt die Statistiken und den Spielverlauf eines Benutzers an."""
        if not user:
            user = interaction.user
        
        async with aiosqlite.connect("eventdb.db") as connection:
            cursor = await connection.execute("SELECT userID, wins, losses FROM spieler WHERE userID = ?", (user.id,))
            result = await cursor.fetchone()

            embed = discord.Embed(color=discord.Color.blue(), title=f"Duellant {user.display_name}")
            embed.set_footer(text=f"Seite 1")

            player_id = result[0]
            player = interaction.guild.get_member(int(player_id))
            if player:
                player_name = player.display_name if len(player.display_name) <= 15 else player.display_name[:12] + "..."
            else:
                player_name = str(player_id)
            wins = result[1]
            losses = result[2]
            total_duels = wins + losses
            win_ratio = (wins / (wins + losses) * 100 if (wins + losses) > 0 else 0)

            output = t2a(
                header=["Duellant", "W/L", "Duelle", "Winratio"],
                body=[[player_name, f"{wins}/{losses}", total_duels, f"{win_ratio:.2f}%"]],
                first_col_heading=True
            )
            embed.description = "```" + output + "```"

            cursor = await connection.execute("""
                SELECT spieler1ID, spieler2ID, spieler1score, spieler2score, datum
                FROM duelle
                WHERE spieler1ID = ? OR spieler2ID = ?
            """, (player_id, player_id))
            match_results = await cursor.fetchall()
            
            embed.description += "\n**Match-Verläufe**\n"
            all_matches = []
            text = ""
            for index, match in enumerate(match_results, start=1):
                spieler1ID = match[0]
                spieler2ID = match[1]
                spieler1score = match[2]
                spieler2score = match[3]
                datum = match[4]

                spieler1 = interaction.guild.get_member(int(spieler1ID))
                spieler2 = interaction.guild.get_member(int(spieler2ID))

                if index <= 5:
                    if spieler1 and spieler2:
                        text += f"{spieler1.mention} vs {spieler2.mention} {spieler1score}:{spieler2score}"
                    else:
                        text += f"{user.mention} vs Unknown {spieler1score}:{spieler2score}"

                    text += f" - {datum}\n"

                match_info = {
                    "Spieler 1": spieler1,
                    "Spieler 2": spieler2,
                    "Spieler 1 Score": spieler1score,
                    "Spieler 2 Score": spieler2score,
                    "Datum": datum
                }
                all_matches.append(match_info)

            embed.description += f"{text}\n"

            await interaction.response.send_message(embed=embed, view=statsliste(user, all_matches))


    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.checks.cooldown(1, 3, key=lambda i: (i.guild_id, i.user.id))
    async def eventduellstats(self, interaction: discord.Interaction, user_a: discord.Member, user_b: discord.Member):
        """Zeigt die Duell-Ergebnisse zwischen zwei Benutzern an."""
        async with aiosqlite.connect("eventdb.db") as connection:
            cursor = await connection.execute("SELECT userID, wins, losses FROM spieler WHERE userID = ?", (user_a.id,))
            result = await cursor.fetchone()

            cursor = await connection.execute("SELECT userID, wins, losses FROM spieler WHERE userID = ?", (user_b.id,))
            result2 = await cursor.fetchone()

            embed = discord.Embed(color=discord.Color.blue(), title=f"{user_a.display_name} vs {user_b.display_name}")
            embed.set_footer(text=f"Seite 1")

            player_id = result[0]
            player = interaction.guild.get_member(int(player_id))
            if player:
                player_name = player.display_name if len(player.display_name) <= 15 else player.display_name[:12] + "..."
            else:
                player_name = str(player_id)
            wins = result[1]
            losses = result[2]
            total_duels = wins + losses
            win_ratio = (wins / (wins + losses) * 100 if (wins + losses) > 0 else 0)

            player_id2 = result2[0]
            player2 = interaction.guild.get_member(int(player_id2))
            if player2:
                player_name2 = player2.display_name if len(player2.display_name) <= 15 else player2.display_name[:12] + "..."
            else:
                player_name2 = str(player_id2)
            wins2 = result2[1]
            losses2 = result2[2]
            total_duels2 = wins + losses
            win_ratio2 = (wins2 / (wins2 + losses2) * 100 if (wins2 + losses2) > 0 else 0)

            output = t2a(
                header=["Duellant", "W/L", "Duelle", "Winratio"],
                body=[[player_name, f"{wins}/{losses}", total_duels, f"{win_ratio:.2f}%"], [player_name2, f"{wins2}/{losses2}", total_duels2, f"{win_ratio2:.2f}%"]],
                first_col_heading=True
            )
            embed.description = "```" + output + "```"

            cursor = await connection.execute("""
                SELECT spieler1ID, spieler2ID, spieler1score, spieler2score, datum
                FROM duelle
                WHERE spieler1ID = ? AND spieler2ID = ? OR spieler2ID = ? AND spieler1ID = ?
            """, (user_a.id, user_b.id, user_a.id, user_b.id))
            match_results = await cursor.fetchall()
            
            embed.description += "\n**Match-Verläufe**\n"
            all_matches = []
            text = ""
            for index, match in enumerate(match_results, start=1):
                spieler1ID = match[0]
                spieler2ID = match[1]
                spieler1score = match[2]
                spieler2score = match[3]
                datum = match[4]

                spieler1 = interaction.guild.get_member(int(spieler1ID))
                spieler2 = interaction.guild.get_member(int(spieler2ID))

                if index <= 5:
                    if spieler1 and spieler2:
                        text += f"{spieler1.mention} vs {spieler2.mention} {spieler1score}:{spieler2score}"
                    else:
                        text += f"{user_a.mention} vs Unknown {spieler1score}:{spieler2score}"

                    text += f" - {datum}\n"

                match_info = {
                    "Spieler 1": spieler1,
                    "Spieler 2": spieler2,
                    "Spieler 1 Score": spieler1score,
                    "Spieler 2 Score": spieler2score,
                    "Datum": datum
                }
                all_matches.append(match_info)

            embed.description += f"{text}\n"

            await interaction.response.send_message(embed=embed, view=duellstats(user_a, user_b, all_matches))



async def setup(bot):
    await bot.add_cog(event(bot))