from redbot.core import commands
from redbot.core import Config
import requests

class RegFox(commands.Cog):
    """RegFox cog, handles communication with RegFox registration platform"""
    def __init__(self, bot):
        self.config = Config.get_conf(self, identifier=3857064354, force_registration=True)
        default_guild = {
            "apiKey":"",
            "registrationLink":""
        }
        self.config.register_guild(**default_guild)
        self.bot = bot
    
    @commands.command()
    @commands.admin_or_permissions(manage_guild=True)
    async def setRegistrationLink(self,ctx,new_value):
        await self.config.guild(ctx.guild).registrationLink.set(new_value)
        await ctx.send("Registration link updated!")
    
    @commands.command()
    @commands.admin()
    async def setAPIKey(self,ctx,new_value):
        await self.config.guild(ctx.guild).apiKey.set(new_value)
        await ctx.send("RegFox API Key updated!")

    @commands.command()
    async def register(self,ctx):
        await ctx.send("Register for Sekaicon here: {}".format(self.config.guild(ctx.guild).registrationLink()))

    @commands.command()
    async def regcount(self,ctx):
        response = requests.get(url="https://api.webconnex.com/v2/public/forms/676/inventory", headers={"apiKey":"{}".format(self.config.guild(ctx.guild).apiKey())})
        payload = response.json()
        if response.status_code == requests.codes.ok:
            await ctx.send("{count} currently registered!".format(count=payload['data'][0]['sold']))
        elif response.status_code == requests.codes.bad:
            await ctx.send("Error, Webconnex API unavailable")
        else:
            await ctx.send("ERROR {code}".format(code=response.status_code))