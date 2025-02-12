import discord
from discord.ext import commands, tasks
from datetime import datetime

# Configuration
TOKEN = "MTMzODg3NTc2MTUzNjQwNTU3NQ.GEZgsW.SOiig8IqG0rvTIWz1jNkpggd24d7uH9ITva0rg"
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Liste des devoirs
devoirs = []

# Commande pour ajouter un devoir
@bot.command()
async def ajouter(ctx, *, devoir: str):
    date_ajout = datetime.now().strftime("%d/%m/%Y %H:%M")
    devoirs.append((devoir, date_ajout))
    embed = discord.Embed(
        title="\ud83d\udcc2 Nouveau Devoir Ajouté",
        description=f"**\ud83d\udd39 Devoir :** {devoir}\n**\u23f0 Date d'ajout :** {date_ajout}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

# Commande pour afficher la liste des devoirs
@bot.command()
async def liste(ctx):
    if not devoirs:
        embed = discord.Embed(
            title="\u2709 Liste des Devoirs",
            description="\ud83d\uddf3 Aucun devoir en cours.",
            color=discord.Color.blue()
        )
    else:
        embed = discord.Embed(
            title="\ud83d\udcc3 Liste des Devoirs",
            color=discord.Color.blue()
        )
        for i, (devoir, date) in enumerate(devoirs, start=1):
            embed.add_field(name=f"{i}. \ud83d\udd39 {devoir}", value=f"Ajouté le {date}", inline=False)
    await ctx.send(embed=embed)

# Commande pour supprimer un devoir par son index
@bot.command()
async def supprimer(ctx, index: int):
    if 0 < index <= len(devoirs):
        supprime = devoirs.pop(index - 1)
        embed = discord.Embed(
            title="\u274c Devoir Supprimé",
            description=f"**\ud83d\udd39 {supprime[0]}** a été supprimé.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="\u26a0 Erreur",
            description="Index invalide. Veuillez donner un numéro valide.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

# Commande d'aide
@bot.command(name="aide")
async def aide(ctx):
    embed = discord.Embed(
        title="\ud83d\udca1 Commandes Disponibles",
        color=discord.Color.purple()
    )
    embed.add_field(name="!ajouter [texte]", value="Ajoute un devoir 📂", inline=False)
    embed.add_field(name="!liste", value="Affiche la liste des devoirs en cours 📋", inline=False)
    embed.add_field(name="!supprimer [num]", value="Supprime un devoir par son numéro ❌", inline=False)
    embed.add_field(name="!aide", value="Affiche cette aide 💡", inline=False)
    await ctx.send(embed=embed)


# Rappel automatique toutes les 24 heures
@tasks.loop(hours=24)
async def rappel_devoirs():
    canal_rappel = bot.get_channel(1339167372854169682)  # Remplace par l'ID du canal
    if devoirs:
        embed = discord.Embed(
            title="\u23f0 Rappel des Devoirs",
            color=discord.Color.orange()
        )
        for i, (devoir, date) in enumerate(devoirs, start=1):
            embed.add_field(name=f"{i}. \ud83d\udd39 {devoir}", value=f"Ajouté le {date}", inline=False)
        await canal_rappel.send(embed=embed)
    else:
        await canal_rappel.send("\ud83d\uddf3 Aucun devoir en cours.")

# Commande pour afficher la semaine actuelle
@bot.command()
async def semaine(ctx):
    semaine_actuelle = datetime.now().isocalendar()[1]
    embed = discord.Embed(
        title="📅 Semaine Actuelle",
        description=f"Nous sommes actuellement en **semaine {semaine_actuelle}**.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

# Rappel automatique de la semaine chaque lundi à 8h
@tasks.loop(hours=168)  # 168 heures = 1 semaine
async def rappel_semaine():
    timezone = pytz.timezone("Europe/Paris")
    maintenant = datetime.now(timezone)
    if maintenant.weekday() == 0 and maintenant.hour == 8:
        canal_rappel = bot.get_channel(1339167372854169682)  # Remplace par l'ID du canal
        semaine_actuelle = maintenant.isocalendar()[1]
        embed = discord.Embed(
            title="⏰ Rappel de la Semaine",
            description=f"Nous sommes maintenant en **semaine {semaine_actuelle}** ! Bonne semaine !",
            color=discord.Color.orange()
        )
        await canal_rappel.send(embed=embed)

# Lancer le rappel automatique après le démarrage du bot
@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user.name}")
    rappel_devoirs.start()

bot.run(TOKEN)
