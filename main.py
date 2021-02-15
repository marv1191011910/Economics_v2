import keep_live  # to keep the bot alive
import discord
from discord.ext import commands
import os
import traceback
import json

PREFIX_PATH = "./Json/prefixes.json"


# to get the prefix
def get_prefix(client, message):
    with open(PREFIX_PATH, "r") as f:
        prefixes = json.load(f)
    return prefixes.get(str(message.guild.id), "%")


client = commands.Bot(command_prefix=get_prefix)

# deleting the default `%help`
client.remove_command('help')


# to see whether the bot is running or not
@client.event
async def on_ready():
    '''shows that the bot is working'''

    print("\n\nIts working !!\n\n")


@client.event
async def on_message(message):
    '''prints out what was typed'''

    author = message.author  # the author
    content = message.content  # the content
    print(f"{author}: {content}")

    if "787331712601686017" in str(content) and str(message.author.id) != "787331712601686017":
        await message.channel.send(f"My prefix: `{get_prefix(client, message)}`, send `{get_prefix(client, message)}help` to see all the commands <@{author.id}>")

    if "@everyone" in str(content) \
            and str(author.id) != "759129467414380554" \
            and str(message.channel.id) in ["793839165464117268", "793839120643522603"] \
            and str(author.id) != "787331712601686017":

        await message.channel.purge(limit=1)
        msg = await message.channel.send(f"<@{message.author.id}> don't you dare do `@everyone` <:emoji_24:810580802848686102>")
        await msg.add_reaction("<:emoji_24:810580802848686102>")

    if "https://top.gg/bot/" in str(content) \
            and str(message.author.id) != "759129467414380554" \
            and str(message.channel.id) in ["793839165464117268", "793839120643522603"]:

        await message.channel.purge(limit=1)
        await message.channel.send("That url is banned in this server")

    # to see what command was given
    await client.process_commands(message)


@client.command(aliases=["reload"])
async def re_load_ext(ctx, *name_of_ext):
    """To reload extension(s)"""

    if str(ctx.author.id) == "759129467414380554":
        try:
            for i in name_of_ext:
                client.reload_extension(i)

        except Exception as err:
            await ctx.message.reply(err)

        else:
            await ctx.message.reply(f"{name_of_ext} was successfully reloaded")

    else:
        await ctx.message.reply(f"You don't have perms <@{ctx.author.id}>, _why would you do it though ?_")


@client.command(aliases=["load"])
async def load_ext(ctx, *name_of_ext):
    """To load extension(s)"""

    if str(ctx.author.id) == "759129467414380554":
        try:
            for i in name_of_ext:
                client.load_extension(i)

        except Exception as err:
            await ctx.message.reply(err)

        else:
            await ctx.message.reply(f"{name_of_ext} was successful loaded")

    else:
        await ctx.message.reply(f"You don't have perms <@{ctx.author.id}>, _why would you do it though ?_")


@client.command(aliases=["unload"])
async def unload_ext(ctx, *name_of_ext):
    """To unload extension(s)"""

    if str(ctx.author.id) == "759129467414380554":
        try:
            for i in name_of_ext:
                client.unload_extension(i)

        except Exception as err:
            await ctx.message.reply(err)

        else:
            await ctx.message.reply(f"{name_of_ext} was successful unloaded")

    else:
        await ctx.message.reply(f"You don't have perms <@{ctx.author.id}>, _why would you do it though ?_")


# when bot is added to other server
@client.event
async def on_guild_join(guild):
    with open(PREFIX_PATH, "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "%"

    # storing the data
    with open(PREFIX_PATH, "w") as f:
        json.dump(prefixes, f, indent=4)


# when bot removed from server
@client.event
async def on_guild_remove(guild):
    with open(PREFIX_PATH, "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    # storing the data
    with open(PREFIX_PATH, "w") as f:
        json.dump(prefixes, f, indent=4)


@client.command(aliases=["set_prefix", "setprefix", "changeprefix"])
@commands.has_permissions(administrator=True)
async def change_prefix(ctx, prefix):
    """To allow the prefix to be changed"""

    with open(PREFIX_PATH, "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix
    # storing the data
    with open(PREFIX_PATH, "w") as f:
        json.dump(prefixes, f, indent=4)

    await ctx.message.reply(f"Prefix has been changed to **{prefix}**")


def _load_ext(i: str) -> (Exception or None):
    """Loads all the extensions"""

    try:
        print(f"Loaded: {i}")
        client.load_extension(i)

    except Exception:
        print(f"Couldn't load {i}")
        traceback.print_exc()


if __name__ == '__main__':
    file_to_ignore = ("__init__.py", )

    # loading the extensions
    economic_etx = [f"Cogs.{i[:-3]}" for i in os.listdir(
        "Cogs") if i[-3:] == ".py" and not i in file_to_ignore]

    for e in economic_etx:
        _load_ext(e)

    # loading the tokens
    TOKEN = os.environ.get('bot_Token')

    client.run(TOKEN)
