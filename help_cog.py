import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot=bot
        self.embedOrange=0xeab148
        
    @commands.Cog.listener()
    async def on_ready(self):
        sendToChannels=[]
        for guild in self.bot.guilds:
            channel=guild.text_channels[0]
            sendToChannels.append(channel)
        helloEmbed=discord.Embed(
            title="Hello There!",
            description="""
            Hello, I'm Spot The Bot! You can type any Command after typing my prefix **`'!'`** to  activate them.
            Use **`help`** to some see command options.""",
            color=self.embedOrange
        )
        for channel in sendToChannels:
            await channel.send(embed=helloEmbed)
    @commands.command(
            name="help",
            aliases=["h"],
            help="Provides a description of all commands or a longer description of an inputted command"
        )
    async def help(self,ctx):
            helpCog=self.bot.get_cog('help_cog')
            musicCog=self.bot.get_cog('music_cog')
            commands=helpCog.get_commands()+musicCog.get_commands()
            
            # commandDescription="**`!help(command)`** - Provides a description of all commands or a longer description of an inputted command\n\n"
            commandDescription=""
            for c in commands:
                message=c.help
                commandDescription+=f"**`!{c.name}`**  {message}\n\n"
            commandEmbed=discord.Embed(
                title="Commands List",
                description=commandDescription,
                color=self.embedOrange
            )
            await ctx.send(embed=commandEmbed)
def setup(bot):
    bot.add_cog(help_cog(bot))