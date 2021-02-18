import discord
import json
from utils import Main_checks
from discord.ext import commands

# TODO: Add coins

class DepAndWith(Main_checks.MainChecks, commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["with", "wit"])
    async def withdraw(self, ctx, amount: float = 10) -> None:
        """To allow user to withdraw"""

        self.account_exist(ctx.author.id)
        user_data = self.load_data()

        # check whether the user had enough money
        if user_data[str(ctx.author.id)]["bank"] >= amount:
            user_data[str(ctx.author.id)]["wallet"] += amount
            user_data[str(ctx.author.id)]["bank"] -= amount

            # making an embed
            total = user_data[str(ctx.author.id)]['bank'] + \
                user_data[str(ctx.author.id)]['wallet']
            embed = discord.Embed(
                title=f"{ctx.author.name} has withdrawn {self.currency} {amount}", description="", color=discord.Colour.random())
            embed.add_field(name=self.current_balance,
                            value=f"Wallet: {self.currency} {user_data[str(ctx.author.id)]['wallet']} \nBank: {self.currency} {user_data[str(ctx.author.id)]['bank']} \nTotal: {self.currency} {total}", inline=False)
            embed.set_footer(text=f"{amount} withdrawn by {ctx.author.name}")
            # saving the new data
            self.save_data(user_data)
            msg = await ctx.send(embed=embed)
            return await msg.add_reaction(self.reaction_coin)

        total = user_data[str(ctx.author.id)]['bank'] + \
            user_data[str(ctx.author.id)]['wallet']
        embed = discord.Embed(
            title=f"You don't have enough money in the bank to withdraw {self.currency} {amount}", description="", color=discord.Colour.random())
        embed.add_field(name=self.current_balance,
                        value=f"Wallet: {self.currency} {user_data[str(ctx.author.id)]['wallet']} \nBank: {self.currency} {user_data[str(ctx.author.id)]['bank']} \nTotal: {self.currency} {total}", inline=False)
        embed.set_footer(text=f"{ctx.author.name} couldn't withdraw {self.currency} {amount}")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(self.reaction_coin)

    @commands.command(aliases=["deposit", "dep max", "dep all", "depmax", "depall"])
    async def dep(self, ctx, amount: float = 10) -> None:
        """To allow users to deposit"""

        self.account_exist(ctx.author.id)
        user_data = self.load_data()

        # check whether the user had enough money
        if user_data[str(ctx.author.id)]["wallet"] >= amount:
            user_data[str(ctx.author.id)]["wallet"] -= amount
            user_data[str(ctx.author.id)]["bank"] += amount

            total = user_data[str(ctx.author.id)]['bank'] + \
                user_data[str(ctx.author.id)]['wallet']
            embed = discord.Embed(
                title=f"{ctx.author.name} has deposited {self.currency} {amount}", description="", color=discord.Colour.random())
            embed.add_field(name=self.current_balance,
                            value=f"Wallet: {self.currency} {user_data[str(ctx.author.id)]['wallet']} \nBank: {self.currency} {user_data[str(ctx.author.id)]['bank']} \nTotal: {self.currency} {total}", inline=False)

            embed.set_footer(text=f"{amount} deposited by {ctx.author.name}")
            # saving the new data
            self.save_data(user_data)
            msg = await ctx.send(embed=embed)
            return await msg.add_reaction(self.reaction_coin)

        total = user_data[str(ctx.author.id)]['bank'] + \
            user_data[str(ctx.author.id)]['wallet']
        embed = discord.Embed(
            title=f"You don't have enough money in your wallet to deposit {self.currency} {amount}", description="", color=discord.Colour.random())
        embed.add_field(name=self.current_balance,
                        value=f"Wallet: {self.currency} {user_data[str(ctx.author.id)]['wallet']} \nBank: {self.currency} {user_data[str(ctx.author.id)]['bank']} \nTotal: {self.currency} {total}", inline=False)
        embed.set_footer(text=f"{ctx.author.name} couldn't deposit {self.currency} {amount}")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(self.reaction_coin)


def setup(client):
    client.add_cog(DepAndWith(client))
