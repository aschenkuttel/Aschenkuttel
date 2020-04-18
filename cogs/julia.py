from discord.ext import commands
import discord


class Julia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="summon")
    async def summon_(self, ctx):
        try:
            own_channel = ctx.author.voice.channel
        except AttributeError:
            msg = "Du befindest dich nicht in einem Voice Channel"
            return await ctx.send(msg)

        channel_id = self.bot.config.get_item(ctx.guild.id, 'move')
        channel = self.bot.get_channel(channel_id)
        if not channel:
            msg = "Der Server hat keinen aktiven Move Channel"
            return await ctx.send(msg)

        for member in channel.members:
            try:
                await member.move_to(own_channel)
            except discord.Forbidden:
                continue
            finally:
                await ctx.message.delete()

    @commands.command(name="mirror")
    async def mirror_(self, ctx, member: discord.Member = None):
        url = member.avatar_url if member else ctx.author.avatar_url
        embed = discord.Embed()
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(name="icon")
    async def icon_(self, ctx):
        embed = discord.Embed(color=discord.Color.gold())
        embed.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(name="profile", aliases="ausweis")
    async def profile_(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        creation_date = member.created_at.strftime("%d.%m.%Y")
        desc = f"**Spitzname:** {member.display_name}\n" \
               f"**Höchste Rolle:** {member.top_role}\n" \
               f"**Account erstellt am:** {creation_date}"
        embed = discord.Embed(description=desc, color=member.colour)
        date = member.joined_at.strftime("%d.%m.%Y - %H:%M:%S")
        embed.set_footer(text=f"Mitglied seit {date}")
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Julia(bot))
