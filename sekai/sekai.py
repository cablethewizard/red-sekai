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
        await self.config.guild(ctx.guild).registrationLink.set(new_value)
        await ctx.send("Registration link updated!")

    @commands.hybrid_command(name="register")
    async def register(self,ctx):
        reglink = await self.config.guild(ctx.guild).registrationLink()
        await ctx.send("Register for Sekaicon here: {}".format(reglink))
