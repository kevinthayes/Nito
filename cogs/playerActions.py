import discord
from discord.ext import commands
from discord.ext import tasks
import cogs.PlayerClass as PlayerClass
import cogs.RoundClass as RoundClass
import os

class playerActions(commands.Cog):
    '''
    This cog deals with commands that have to do with the user's Player
    object and its methods

    Loops:
        savePlayers: Saves player information every 3 minutes

    Commands:
        q!save_players: Saves player information
        q!establish_player: Initializes a player object for the user that
                            called the command
    '''
   
    # Import the player data if we have any
    allplayers = {}
    if os.stat("cogs/PlayerData.txt").st_size != 0:
        # Open the data file for reading
        playerdata = open("cogs/PlayerData.txt", "r")
        contents = playerdata.read()

        # Gather all the player data by guild
        # Each guild is separated by a @ character
        guilds = contents.split("@")

        # Loop through each guild
        for guild in guilds:
            # The users and Player objects are split by *
            all_data = guild.split("*")
            # The guild ID is the first element
            gid = int(all_data[0])
            # Make this dictionary nested
            allplayers[gid] = {}

            # Loop through all the users and re-establish Player objects
            # We count by twos so that we shift to the next user each time
            # instead of to a Player object
            for i in range(1, len(all_data) - 1, 2):
                user = int(all_data[i])
                playerobj = all_data[i + 1]
                allplayers[gid][user] = eval(playerobj)

    def __init__(self, bot):
        '''
        Initializer function that allows us to access the bot within this cog
        '''
        self.bot = bot
        self.autosavePlayers.start()

    @tasks.loop(minutes = 3)
    async def autosavePlayers(self):
        '''
        Saves player information every 3 minutes
        '''
        await self.save_players()

    @commands.command(aliases = ["savep", "sp", "saveplayers", "savePlayers"])
    async def save_players(self):
        '''
        Saves player information
        '''
        # We'll use this dictionary extensively here, so an alias is useful
        ap = playerActions.allplayers

        # Open the file to write
        playerfile = open("cogs/PlayerData.txt", "w")

        write_data = ""
        # Write the data so that guilds are separated by @ and users/player
        # objects are separated with *

        # Loop through and write all of the guild_ids
        for guild in ap:
            # We don't want the first character to be @
            if write_data == "":
                write_data += str(guild)
            else:
                write_data += "@" + str(guild)

            # Loop through the users and the Players and add them
            for user in ap[guild]:
                player = ap[guild][user]
                write_data += "*" + str(user)
                # Grab the initializer for this Player object
                write_data += "*" + player.getInitializer()

        # Write the updated dictionary to the file
        playerfile.write(write_data)
                
        # Close the file
        playerfile.close()

    @commands.command(aliases = ["ep", "establish", "establishplayer", "est"])
    async def establish_player(self, ctx):
        '''
	    Initializes a player object for the user that called this command
    	'''
        # Create an alias for the allplayers dictionary
        ap = playerActions.allplayers
        user = ctx.author # The author of the message
        guild_id = ctx.guild.id # Current guild

        # Make sure the user doesn't have multiple Player objects
        try:
            # result is True if the user already has a Player object
            result = False
            # flag is False unless we reach the end of the dictionary
            flag = False
            all_users = ap[guild_id].keys()
            numelements = len(all_users) - 1
            i = 0
            while result == False and flag == False:
                # Loop through the list of players until we find the user
                for person in ap[guild_id]:
                    if person == user.id:
                        result = True
                    if i  == numelements:
                        flag = True
                    i += 1
       
        # If a KeyError was produced, the guild isn't in the dictionary
        except:
            result = False
	
        if result == False:
            # Create a Player object
            newplayer = PlayerClass.Player(user.id)
            
            # Make sure this guild is in the dictionary
            try:
                ap[guild_id][user.id] = newplayer
            except:
                ap[guild_id] = {}
                ap[guild_id][user.id] = newplayer
           
           # This way, we can access a user's Player object using the
            # member object of the user
            await self.save_players()
            await ctx.send("Player established.")
        else:
            await ctx.send("Cannot establish player. Perhaps you already" +
            " used this command...")

def setup(bot):
    '''
    Allows the bot to load this cog
    '''
    bot.add_cog(playerActions(bot))
