import discord
import json
from utils import Main_checks
from discord.ext import commands


class Balance(Main_checks.MainChecks, commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["balance"])
    async def bal(self, ctx, user: discord.Member = None) -> None:
        """To allow user to see their and other user's balance"""
        user = user or ctx.author

        self.account_exist(user.id)
        user_data = self.load_data()

        # making an embed
        total = user_data[str(user.id)]['bank'] + \
            user_data[str(user.id)]['wallet']
        embed = discord.Embed(
            title=f"Current Balance of {user.name}", description=f"Wallet: {self.currency} {user_data[str(user.id)]['wallet']} \nBank: {self.currency} {user_data[str(user.id)]['bank']} \nTotal: {self.currency} {total}", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author}")

        # saving the new data
        self.save_data(user_data)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Balance(client))
