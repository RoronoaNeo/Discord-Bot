import discord
from discord.ext import commands
#il faut installer: discord /discord.py /  avec *pip install*

tokenfile = open("token.txt", 'r')
token = tokenfile.read()
tokenfile.close()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents,command_prefix="!")


@bot.event    
async def on_ready():
	print("Bot connected")
#***


@bot.command() #Commande permettant d'intérroger le bot.
async def Luffy(ctx): 
    await ctx.send('le roi des pirates ce sera moi !')
    await bot.change_presence(activity=discord.Game(name="Je suis là pour toi !"))


@bot.command() #Commande permettant d'avoir des informations sur le serveur.
async def serverInfo(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    serverDescription = server.description
    numberOfPerson = server.member_count
    serverName = server.name
    message = f"Le serveur **{serverName}** contient *{numberOfPerson}* membres. \nLa description du serveur {serverDescription}. \nCe serveur possède *{numberOfTextChannels}* salons écrit ainsi que *{numberOfVoiceChannels}* vocaux."
    await ctx.send(message)

@bot.command() #Commande répétant ce que l'on dit.
async def say(ctx, texte):
    if len(texte) < 2:
        await ctx.send('drôlement court quand même, écrit un peu plus !')
    else:
         await ctx.send(texte)

@bot.event   #Evenement qui détecte quand l'utilisateur rejoint le serveur.
async def on_member_join(member):
    channel = bot.get_channel(#mettez le channel id)
    await member.send("Bienvenue dans mon équipage ! Utilise !help pour savoir ce que tu peux faire comme commande ! J'espère que tu vas bien t'amuser et, bon voyage !!")
    await channel.send( "Bienvenue dans l'équipage !!!")

    @bot.event   #Evenement qui détecte quand un utilisateur quitte le serveur.
    async def on_member_remove(member):
      channel = bot.get_channel(#mettez le channel id)
      await channel.send("Oh, j'espère te revoir vite !")

@bot.command()  #permet de nettoyer un nombre défini de message.
async def clear(ctx, nombre:int):
    messages = await ctx.channel.history(limit = nombre + 1 ).flatten()
    for m in messages:
        await m.delete()  # trouver une solution pour renvoyer un message à l'erreur.

@bot.command()
async def kick(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason = reason)
    await ctx.send(f"{user} à été kick pour la raison suivante : **{reason}**.")
    await user.send("Tu as été kick ! Essaye de changer ton comportement !")

@bot.command()
async def ban(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason = reason)
    await ctx.send(f"{user} à été ban pour la raison suivante : **{reason}**.")
    await user.send("Tu as été ban ! Tu as dépassé les bornes !!")

@bot.command()
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    userName, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await ctx.guild.unban(i.user, reason = reason)
            await ctx.send(f"{user} a été unban.")
            return
    #si l'utilisateur n'est pas ban.
    await ctx.send(f"L'utilisateur {user} n'a pas été banni.")
    



bot.run(token)