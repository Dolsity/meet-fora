import discord
from discord.ext import commands
from discord_components import *
from requests import Session
from typing import TextIO
import json
import dateutil.parser as parser
from datetime import time
from difflib import SequenceMatcher
import time
import os
from dotenv import load_dotenv

# Loading data from .env file
load_dotenv()
key = os.getenv('NASA_API')

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

class Space(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # WGERE IS THE ISS?
    @commands.command()
    async def iss(self, ctx):
        await ctx.trigger_typing()
        session = Session()
        """Track the ISS."""
        get_pos = json.loads(session.get(f"http://api.open-notify.org/iss-now.json").text)
        iss_lat = get_pos['iss_position']['latitude']
        iss_lon = get_pos['iss_position']['longitude']
        location = ''

        try:
            location = json.loads(session.get(f"https://nominatim.openstreetmap.org/reverse?format=json&lat={iss_lat}"
                                            f"&lon={iss_lon}&zoom=0&namedetails=1").text)
        except json.JSONDecodeError:
            iss = (f"Currently over an unknown land! ({iss_lat}, {iss_lon})")
        if "error" in location:
            iss = (f"Currently over the ocean \N{WATER WAVE} ({iss_lat}, {iss_lon})")

        else:
            try:
                iss = (f"Currently over "f"{location['namedetails']['name:en']}! ({iss_lat}, {iss_lon})")

            except KeyError:
                iss = (f"Currently over "f"{location['namedetails']['name']}! ({iss_lat}, {iss_lon})")

            except Exception:
                iss = (f"Currently over an unknown land!"f"({iss_lat}, {iss_lon})")

        embed = discord.Embed(title=":satellite_orbital: ISS Info", colour = discord.Color.dark_blue())
        embed.add_field(name=f"ISS location:", value=f"{iss}", inline=True)
        embed.set_image(url="https://media.discordapp.net/attachments/926974353105629234/926974482382487562/nasa01.JPEG")
        await ctx.send(embed=embed)

    @commands.command(aliases=['stream'])
    async def camera(self, ctx):
        await ctx.trigger_typing()
        session = Session()
        """Get a view from the ISS's official livestream."""
        chan = json.loads(session.get("https://api.ustream.tv/channels/17074538.json").text)
        embed = discord.Embed(title=f"Want to see the ISS's official livestream? Click here.", color=0x000000,
                              url="https://eol.jsc.nasa.gov/ESRS/HDEV/", description="If the image is totally black"
                              ", that means the ISS is currently over an area where it is night-time.")
        embed.set_image(url=f"{chan['channel']['thumbnail']['live'].replace('192x108', '640x360')}?{time.time()}")
        # This is kinda horrible, but it's necessary to get an updated image.
        embed.set_author(name="Still image from a camera aboard the ISS",
                         icon_url=self.bot.user.avatar_url)
        embed.set_footer(text="Happy spotting!")
        await ctx.send(embed=embed)

    @commands.command()
    async def apod(self, ctx):
        await ctx.trigger_typing()
        session = Session()
        """Get NASA's Astronomy Picture of the Day!"""
        request = json.loads(session.get(f"https://api.nasa.gov/planetary/apod?api_key={key}").text)
        title = request['title']
        if "copyright" in request:
            title += f" by {request['copyright']}"
        embed = discord.Embed(title=title, description=request['explanation'], color=0x000000, url=request['hdurl'])
        embed.set_author(name="Astronomy Picture of the Day", icon_url=self.bot.user.avatar_url)
        embed.set_image(url=request['url'])
        await ctx.send(embed=embed)

    @commands.command(aliases=['mw', 'mweather', 'marsw'])
    async def marsweather(self, ctx, *, arg: str = None):
        await ctx.trigger_typing()
        session = Session()
        """Get the weather on Mars."""
        request = json.loads(session.get(f"http://cab.inta-csic.es/rems/wp-content/plugins/marsweather-widget/"
                                        f"api.php").text)
        sol = ''
        embed = discord.Embed(title="Data obtained from REMS on the Curiosity rover.", color=0x000000)
        embed.set_thumbnail(url="https://space.is-for.me/i/gsre.png")

        if arg is None:
            sol = request['soles'][0]
            embed.set_footer(text="Note: This is the most recent weather data. Weather data is only sent once in "
                                "a while. You can, however, look at weather for certain dates by searching their "
                                "Mars sol or Earth date with this command.")
        else:
            for idx, d in enumerate(request['soles']):
                if d['sol'] == arg:
                    sol = request['soles'][idx]
                    break
                else:
                    pass
            # If it's not a sol, check if it's an earth date
            if sol is '':
                try:
                    parsed_date = parser.parse(arg).date().isoformat()
                    for idx, d in enumerate(request['soles']):
                        if d['terrestrial_date'] == parsed_date:
                            sol = request['soles'][idx]
                            break
                        else:
                            pass
                except ValueError:
                    pass

        # if sol is '':
        if sol == '':
            await ctx.send(f"**Error:** Your argument couldn't be parsed as a valid Mars sol or Earth date. Proper "
                        f"sols range from {request['soles'][-1]['sol']} to {request['soles'][0]['sol']}. Proper "
                        f"dates range from {request['soles'][-1]['terrestrial_date']} to "
                        f"{request['soles'][0]['terrestrial_date']}.")
        else:
            max_temp_f = int(9.0 / 5.0 * int(sol['max_temp']) + 32)
            min_temp_f = int(9.0 / 5.0 * int(sol['min_temp']) + 32)
            embed.set_author(name=f"Weather on Mars for Sol {sol['sol']}",
                            icon_url=self.bot.user.avatar_url)
            embed.add_field(name="Mars sol", value=sol['sol'], inline=True)
            embed.add_field(name="Earth date", value=sol['terrestrial_date'], inline=True)
            embed.add_field(name="Season", value=sol['season'], inline=True)
            embed.add_field(name="Solar longitude", value=sol['ls'], inline=True)
            embed.add_field(name="High temperature", value=f"{sol['max_temp']}°C, {max_temp_f}°F", inline=True)
            embed.add_field(name="Low temperature", value=f"{sol['min_temp']}°C, {min_temp_f}°F", inline=True)
            embed.add_field(name="Pressure", value=f"{sol['pressure']} pascals", inline=True)
            embed.add_field(name="Relative humidity", value=sol['abs_humidity'], inline=True)
            embed.add_field(name="Wind speed", value=sol['wind_speed'], inline=True)
            embed.add_field(name="Wind direction", value=sol['wind_direction'], inline=True)
            embed.add_field(name="Sunrise", value=sol['sunrise'], inline=True)
            embed.add_field(name="Sunset", value=sol['sunset'], inline=True)
            await ctx.send(embed=embed)

    @commands.command(name="spacex", aliases=['spacex.launch', 'sx.launches', 'spacex.launches', 'sxlaunch', 'sx.launch'])
    async def spacex(self, ctx, *, arg: str = None):
        await ctx.trigger_typing()
        session = Session()
        """Get basic information about SpaceX's launches."""
        launch = None
        request = json.loads(session.get(f"https://api.spacexdata.com/v2/launches").text)
        # If the arg is nothing, just get the most recent launch
        if arg is None:
            launch = request[-1]
        else:
            # If the arg is a number, try to find a flight number
            try:
                if request[0]['flight_number'] <= int(arg) <= request[-1]['flight_number']:
                    launch = request[int(arg) - 1]
                else:
                    pass
            except ValueError:
                pass
            # If the arg is a date, find a flight by that date
            try:
                for idx, flight in enumerate(request):
                    if parser.parse(arg).date() == parser.parse(flight['launch_date_local']).date():
                        launch = request[idx]
                    else:
                        pass
            except (ValueError, OverflowError):
                pass
            # If the arg is a mission name, try to find that mission name
            try:
                for idx, flight in enumerate(request):
                    if arg.lower() == flight['mission_name'].lower():
                        launch = request[idx]
                        break
                    elif similar(arg.lower(), flight['mission_name'].lower()) >= 0.7:
                        launch = request[idx]
                        break
                    else:
                        pass
            except ValueError:
                pass
        # When all else fails...
        if launch is None:
            await ctx.send("**Error:** Couldn't determine a SpaceX launch from the information provided.\n\n"
                        f"You can search by flight number (currently {request[0]['flight_number']} to "
                        f"{request[-1]['flight_number']}), flight date, or mission name.")
        else:
            embed = discord.Embed(title=f"\N{ROCKET} {launch['mission_name']}", color=0x000000,
                                description=launch['details'])
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url=launch['links']['mission_patch'])
            embed.add_field(name="Time", value=parser.parse(launch['launch_date_local']), inline=True)
            embed.add_field(name="Rocket Name", value=launch['rocket']['rocket_name'], inline=True)
            embed.add_field(name="Launch Site", value=launch['launch_site']['site_name'], inline=True)
            embed.add_field(name="Launch Successful?", value=launch['launch_success'], inline=True)
            payload_num = 1
            for payload in launch['rocket']['second_stage']['payloads']:
                embed.add_field(name=f"Payload {payload_num} ID", value=payload['payload_id'], inline=True)
                embed.add_field(name=f"Payload {payload_num} Nationality", value=payload['nationality'], inline=True)
                embed.add_field(name=f"Payload {payload_num} Manufacturer", value=payload['manufacturer'], inline=True)
                embed.add_field(name=f"Payload {payload_num} Type", value=payload['payload_type'], inline=True)
                embed.add_field(name=f"Payload {payload_num} Mass",
                                value=f"{payload['payload_mass_kg']}kg ({payload['payload_mass_lbs']}lbs)", inline=True)
                embed.add_field(name=f"Payload {payload_num} Lifespan",
                                value=f"{payload['orbit_params']['lifespan_years']} years", inline=True)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Space(bot))