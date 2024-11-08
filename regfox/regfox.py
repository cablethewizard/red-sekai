from redbot.core import commands
from redbot.core import Config
import requests

class RegFox(commands.Cog):
    """RegFox cog, handles communication with RegFox registration platform"""
    def __init__(self, bot):
        self.config = Config.get_conf(self, identifier=3857064354, force_registration=True)
        default_guild = {
            "apiKey":"",
            "registrationLink":"",
            "pageid":0
        }
        self.config.register_guild(**default_guild)
        self.bot = bot
    
    @commands.hybrid_command(name="setregistrationlink")
    @commands.admin_or_permissions(manage_guild=True)
    async def setRegistrationLink(self,ctx,new_value):
        await self.config.guild(ctx.guild).registrationLink.set(new_value)
        await ctx.send("Registration link updated!")
    
    @commands.hybrid_command(name="setapikey")
    @commands.admin()
    async def setAPIKey(self,ctx,new_value):
        await self.config.guild(ctx.guild).apiKey.set(new_value)
        await ctx.send("RegFox API Key updated!")

    @commands.hybrid_command(name="setpageid")
    @commands.admin()
    async def setPageID(self,ctx,new_value):
        await self.config.guild(ctx.guild).pageid.set(new_value)
        await ctx.send("RegFox page ID updated!")

    @commands.hybrid_command(name="register")
    async def register(self,ctx):
        reglink = await self.config.guild(ctx.guild).registrationLink()
        await ctx.send("Register for Sekaicon here: {}".format(reglink))

    @commands.hybrid_command(name="regcount")
    async def regcount(self,ctx):
        pageidconf = await self.config.guild(ctx.guild).pageid()
        apikeyconf = self.config.guild(ctx.guild).apiKey()
        try:
            response = requests.get(url="https://api.webconnex.com/v2/public/forms/{pageid}/inventory".format(pageid=pageidconf), headers={"apiKey":"{key}".format(key=apikeyconf)})
        except ConnectionError:
            await ctx.send("Connection error, unable to reach RegFox")
        payload = response.json()
        if response.status_code == requests.codes.ok:
            await ctx.send("{count} currently registered!".format(count=payload['data'][0]['sold']))
        elif response.status_code == requests.codes.bad:
            await ctx.send("Error, Webconnex API unavailable")
        else:
            await ctx.send("ERROR {code}".format(code=response.status_code))