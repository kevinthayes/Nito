import discord
from discord.ext import commands
import cogs.RoundClass as RoundClass

class roundCreator(commands.Cog):
    '''
    This cog deals with the actions involved in managing rounds

    Commands:
        q!create_round: Creates a new round or reactivates an existing one
        q!end_round: Ends the currently active round
    '''

## TRY ADDING A FUNCTION THAT GRABS THE GUILD_ID, CHANNEL_ID, AND
## USER_ID FOR YOU INSTEAD OF COPYING AND PASTING THE CODE IN EACH COMMAND

    # Stores the Round objects in the format
    # {GUILD_ID : {CHANNEL_ID : ROUNDOBJ}}
    allRounds = {}

    def __init__(self, bot):
        '''
        Initializer function that allows us to access the bot within this cog
        '''
        self.bot = bot # now we can interact with the bot using self.bot

    @commands.command()
    async def create_round(self, ctx):
        '''
        Generate a round with you set as the owner of the round
        '''
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id
        round_owner = ctx.author

        # If the round doesn't exist for this channel in this guild, we
        # will get an error. We handle that here
        try:
            this_round = roundCreator.allRounds[guild_id[channel_id]]
        except:
            this_round = None

        # One round object is created for each channel and then is activaated
        # and deactivated subsequently so we check if one already exists

        # If the round exists, start it
        if this_round:
            this_round.startRound(round_owner)
            await ctx.send("Round created.")
        # If no round exists, create a new one, add it to the list, then
        # start it
        elif this_round == None:
            new_round = RoundClass.Round()
            roundCreator.allRounds[guild_id[channel_id]] = new_round
            new_round.startRound(round_owner)
            await ctx.send("New round created")
        else:
            await ctx.send("An error occurred trying to create a round.")

    @commands.command()
    async def end_round(self, ctx):
        '''
        End the round generated by the create_round command and displays the
        leaderboard
        '''
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id

        # Check to make sure the round object exists and get its status
        try:
            this_round = roundCreator.allRounds[guild_id[channel_id]]
            status = this_round.getRoundStatus()
        except:
            this_round = None
            status = None

        # If the round exists
        if this_round:
            # Active round
            if status == True:
                this_round.endRound()
                await ctx.send("Round ended.")
            # Inactive round
            elif status == False:
                await ctx.send("This round was never started...")
            # How did you get here
            else:
                await ctx.send("An error occurred trying to end a round")
        # If the round doesn't exist
        elif not this_round:
            await ctx.send("Error: no round found.")
        # How would you even get here
        else:
            await ctx.send("Super error. How did you get here?")

## FINISH WITH PERMISSIONS
    @commands.command()
    async def join(self, ctx):
        '''
        Request to join a currently established round
        '''
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id
        new_player = ctx.author

        # Check to make sure the round object exists and is active
        try:
            this_round = roundCreator.allRounds[guild_id[channel_id]]
            status = this_round.getRoundStatus()
        except:
            this_round = None
            status = None

        # Refer to if statement in the function above for logic
        if this_round:
            if status == True:
                # CREATE A FUNCTION TO ASK THE ROUND_OWNER FOR PERMISSION
                await ctx.send ("I need implementation :(")
            elif status == False:
                await ctx.send("No active round found.")
            else:
                await ctx.send("An error occurred trying to join a round")
        elif not this_round:
            await ctx.send("Error: no round found.")
        else:
            await ctx.send("Congratulations, you unlocked a rare error!")

    @commands.command()
    async def leave(self, ctx):
        '''
        Leave the round you are currently in
        '''
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id
        old_player = ctx.author

        # Check to make sure the round object exists and is active
        try:
            this_round = roundCreator.allRounds[guild_id[channel_id]]
            status = this_round.getRoundStatus()
        except:
            this_round = None
            status = None

        # The same nested if as above
        if this_round:
            if status == True:
                this_round.removePlayer(old_player)
            elif status == False:
                await ctx.send("No active round found.")
            else:
                await ctx.send("An error occurred trying to leave a round")
        elif not this_round:
            await ctx.send("Error: no round found.")
        else:
            await ctx.send("You triggered a mega-error!")

def setup(bot):
    '''
    Allows the bot to load this cog
    '''
    bot.add_cog(roundCreator(bot))
