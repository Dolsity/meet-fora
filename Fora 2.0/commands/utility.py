from discord.ext import commands
import discord
import asyncpg
from dotenv import load_dotenv
import os
from database.levels import *
import platform

load_dotenv()
password = os.getenv('PASSWORD')
user = "Jay"

default_prefix = '.'

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #PING PONG LATENCY COMMAND
    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(title=f":ping_pong: Pong! {round(self.bot.latency*1000)}ms", color=0xffffff)
        await ctx.send(embed=embed)
    
    # Set server prefix
    @commands.command(aliases=['setpre'])
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, new_prefix=None):
        if new_prefix is None:
            return await ctx.send(':no_entry: Please provide a prefix')
        await self.bot.db.execute('UPDATE prefixes SET prefix = $1 WHERE "guild_id" = $2', new_prefix, ctx.guild.id)
        await ctx.send(f"Prefix was updated to {new_prefix}")

    # Info about your guild
    @commands.command()
    async def about(self, ctx):
        # Connect to database --
        self.bot.db = await asyncpg.create_pool(database = "fora", user = user, password = password)

        # Finds guild prefix in database -- can use this for anything like levels / xp
        prefix = await self.bot.db.fetch('SELECT prefix FROM prefixes WHERE "guild_id" = $1', ctx.guild.id)
        
        # If the prefix is none it will insert a prefix --
        if len(prefix) == 0:
            await self.bot.db.execute('INSERT INTO prefixes("guild_id", prefix) VALUES ($1, $2)', ctx.guild.id, default_prefix)
            prefix = default_prefix

        # Else it will get the prefix --
        else:
            prefix = prefix[0].get("prefix")
        embed = discord.Embed(title="Basic information about Fora", color=0xffffff)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Fora Developers", value='Dolsity#5720 | <@795969792778698763>', inline=True)
        embed.add_field(name="Total Servers", value=f"{len(self.bot.guilds)}", inline=True)
        embed.add_field(name="Total Channels", value=f"{sum((1 for c in self.bot.get_all_channels()))}", inline=True)
        embed.add_field(name="Total Users", value=f"{sum(1 for c in self.bot.users)}", inline=True)
        embed.add_field(name="Default Prefix", value=f"{default_prefix}", inline=True)
        embed.add_field(name="Server Prefix", value=f"{prefix}", inline=True)
        embed.add_field(name="Python version", value=f"{platform.python_version()}", inline=True)
        await ctx.send(embed=embed)

    # Tells you basic information about someone in your guilds
    @commands.command()
    async def whois(self, ctx, member: discord.Member = None):

            if member is None:
                member = ctx.author

            user_data_guild = await get_user_data_guild(self.bot.db, member.id, ctx.guild.id)
            user_data_global = await get_user_data_global(self.bot.db, member.id)

            roles = [role for role in member.roles[1:]]  # don't get @everyone
            
            embed = discord.Embed(title=f"Basic information about {member.display_name}", color=0xffffff)
            embed.set_author(name=member.display_name, icon_url=member.avatar_url)
            embed.add_field(name="Member", value=f"Name: {member.display_name} | ID: {member.id}", inline=True)
            embed.add_field(name="Joined", value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC"), inline=True)
            embed.add_field(name="Registered", value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"), inline=True)
            embed.add_field(name= "Status", value= (f"Website Status - {member.web_status} / Mobile Status - {member.mobile_status} / Desktop Status - {member.desktop_status}"), inline= False)
            embed.add_field(name="Roles", value="".join([role.mention for role in roles]), inline=False)
            embed.add_field(name="Highest Role", value=member.top_role.mention, inline=False)
            embed.add_field(name="Guild Level / XP", value=f"Level: {user_data_guild['level']} / XP : {user_data_guild['xp']}", inline=True)
            embed.add_field(name="Global Level / XP", value=f"Level: {user_data_global['level']} / XP : {user_data_global['xp']}", inline=True)
            embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utility(bot))