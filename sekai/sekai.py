from redbot.core import commands
from redbot.core import Config

class Sekai(commands.Cog):
    """Sekai cog, handles attendee issues and questions"""
    def __init__(self, bot):
        self.config = Config.get_conf(self, identifier=4858734564, force_registration=True)
        default_guild = {
            "registrationLink":""
        }
        self.config.register_guild(**default_guild)
        self.bot = bot
    
    @commands.hybrid_command(name="setregistrationlink")
    @commands.admin_or_permissions(manage_guild=True)
    async def setRegistrationLink(self,ctx,new_value):
        """Set the registration link for your event."""
        await self.config.guild(ctx.guild).registrationLink.set(new_value)
        await ctx.send("Registration link updated!")

    @commands.hybrid_command(name="register")
    async def register(self,ctx):
        """Get the registration link for the event."""
        reglink = await self.config.guild(ctx.guild).registrationLink()
        await ctx.send("Register for Sekaicon here: {}".format(reglink))

    @commands.hybrid_command(name="info")
    async def info(self,ctx):
        """See what Mecha-Parker can do for you"""
        await ctx.send("Hi, I'm Mecha-Parker! Use .help for general information, or use /register to get a link to register for Sekaicon!")