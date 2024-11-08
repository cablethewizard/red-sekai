from redbot.core import commands
from redbot.core import Config
from redbot.core.utils import chat_formatting
import requests
from fake_useragent import UserAgent

class RegFox(commands.Cog):
    """RegFox cog, handles communication with RegFox registration platform"""
    def __init__(self, bot):
        self.config = Config.get_conf(self, identifier=3857064354, force_registration=True)
        default_guild = {
            "apiKey":"",
            "pageid":0
        }
        self.config.register_guild(**default_guild)
        self.bot = bot
        self.useragent = UserAgent()
    """
    async def regfoxRequest(self, ctx, url):
        apikeyconf = await self.config.guild(ctx.guild).apiKey()
        requrl = url
        headers = {
            "apiKey": "{}".format(apikeyconf),
            "User-Agent": self.useragent.random
        }
        try:
            response = requests.get(url=requrl, headers=headers)
        except ConnectionError:
            payload = "ERROR: Unable to reach WebConnex"
            return payload
        else:
            if response.status_code == requests.codes.ok:
                try:
                    payload = response.json()
                except requests.JSONDecodeError:
                    payload = "JSON Decode Error"
                    return payload
                else:
                    return payload
            else:
                payload = "ERROR {code}".format(code=response.status_code)
                return
    """
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

    @commands.hybrid_command(name="regcount")
    async def regcount(self,ctx):
        pageidconf = await self.config.guild(ctx.guild).pageid()
        apikeyconf = await self.config.guild(ctx.guild).apiKey()
        url = "https://api.webconnex.com/v2/public/forms/{pageid}/inventory".format(pageid=pageidconf)
        headers = {
            "apiKey": "{}".format(apikeyconf),
            "User-Agent": self.useragent.random
        }
        try:
            response = requests.get(url=url, headers=headers)
        except ConnectionError:
            await ctx.send("Connection error, unable to reach RegFox")
        else:
            if response.status_code == requests.codes.ok:
                try:
                    payload = response.json()
                except requests.JSONDecodeError:
                    await ctx.send("JSON Decoding error")
                else:
                    await ctx.send("{count} currently registered!".format(count=payload['data'][1]['sold']))
            else:
                errorfile = chat_formatting.text_to_file(response.text,filename='error.txt',spoiler=False,encoding='utf-8')
                await ctx.send("ERROR {code}".format(code=response.status_code), file=errorfile)
    
    @commands.hybrid_command(name="connectiontest")
    @commands.admin()
    async def connectiontest(self,ctx):
        apikeyconf = await self.config.guild(ctx.guild).apiKey()
        url = "https://api.webconnex.com/v2/public/ping"
        headers = {
            "apiKey": "{}".format(apikeyconf),
            "User-Agent": self.useragent.random
        }
        try:
            response = requests.get(url=url, headers=headers)
        except ConnectionError:
            await ctx.send("Connection error, unable to reach RegFox")
        else:
            try:
                payload = response.json()
            except requests.JSONDecodeError:
                jsonerror = chat_formatting.text_to_file(response.text,filename='jsonerror.txt',spoiler=False,encoding='utf-8')
                await ctx.send("JSON Decoding error", file=jsonerror)
            else:
                await ctx.send("Code {code}, MSG {data}".format(code=response.status_code, data=payload['data']))