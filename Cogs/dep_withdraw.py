import discord
import json
from utils import Main_checks
from discord.ext import commands


class DepAndWith(Main_checks.MainChecks, commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["with", "wit"])
    async def withdraw(self, ctx, amount: float = 10) -> None:
        """To allow user to withdraw"""

        self.account_exist(ctx.author.id)
        user_data = self.load_data()

        if user_data[str(ctx.author.id)]["bank"] > amount:
            user_data[str(ctx.author.id)]["wallet"] += amount
            user_data[str(ctx.author.id)]["bank"] -= amount
            await ctx.send(f"<@{ctx.author.id}> withdrew {amount}")

        else:
            await ctx.send(f"You don't have that much money, Are you good ? <@{ctx.author.id}>")

    @commands.command(aliases=["deposit", "dep max", "dep all", "depmax", "depall"])
    async def dep(self, ctx, amount: float = 10) -> None:
        """To allow users to deposit"""
        self.account_exist(ctx.author.id)
        user_data = self.load_data()

        if user_data[str(ctx.author.id)]["bank"] > amount:
            user_data[str(ctx.author.id)]["wallet"] -= amount
            user_data[str(ctx.author.id)]["bank"] += amount
            await ctx.send(f"<@{ctx.author.id}> deposited {amount}")

        else:
            await ctx.send(f"You don't have that much money, Are you good ? <@{ctx.author.id}>")


def setup(client):
    client.add_cog(DepAndWith(client))
