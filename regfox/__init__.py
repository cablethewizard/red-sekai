from .regfox import RegFox

async def setup(bot):
    await bot.add_cog(RegFox(bot))