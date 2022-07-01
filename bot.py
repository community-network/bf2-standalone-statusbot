import asyncio
import re
import sys
from os import path, getenv
from opengsq.protocols import GameSpy3
import discord

"""BF4 ONLY"""
# CONFIG
BOT_TOKEN = getenv("token", "")
SERVER_IP = getenv("ip", "146.59.228.238")
SERVER_PORT = getenv("port", "29900")
GUILD_ID = getenv("guild", "770746735533228083")
EXP = getenv("exp", "SUPER@ - (.*?)$")

class LivePlayercountBot(discord.Client):
    """Discord bot to display the BL true playercount in the bot status"""
 
    async def on_ready(self):
        print(f"Logged on as {self.user}\n" f"Started monitoring server {SERVER_IP}:{SERVER_PORT}")
        status = ""
        current_servername = ""
        while True:
            try:
                server_info, server_name = await get_playercount()
                if server_info == None:
                    await self.change_presence(activity=discord.Game("¯\\_(ツ)_/¯ server not found"))
                else:
                    if server_info != status:  # avoid spam to the discord API
                        await self.change_presence(activity=discord.Game(server_info))
                        status = server_info
                        
                    if current_servername != server_name: # avoid spam to the discord API
                        x = re.search(EXP, server_name)

                        guild = self.get_guild(int(GUILD_ID))
                        await guild.me.edit(nick=x.group(1)[:32])
                        to_check = f"maps/{x.group(1)}"
                        if path.exists(f"{to_check}.jpg"):
                            map_slug = f"{to_check}.jpg"
                        elif path.exists(f"{to_check}.png"):
                            map_slug = f"{to_check}.png"
                        else:
                            map_slug = "maps/default.jpg"
                        
                        with open(map_slug, 'rb') as f:
                            await self.user.edit(avatar=f.read())
                            
                        current_servername = server_name
            except Exception as e:
                print(e)
            await asyncio.sleep(10)
 
async def get_playercount():
    try:
        source = GameSpy3(address=SERVER_IP, query_port=int(SERVER_PORT))
        data = await source.get_status()
        max_slots = int(data["info"]["maxplayers"])
        map_name = data['info']["mapname"]
        server_name = data['info']["hostname"]
        true_playercount = int(data["info"]["numplayers"])
        server_info = f"{true_playercount}/{max_slots} - {map_name}"  # discord status message
        return server_info, server_name
    except Exception as e:
        print(f"Error getting data from server: {e}")  # BL autism
        return None, None
 
if __name__ == "__main__":
    assert sys.version_info >= (3, 7), "Script requires Python 3.7+"
    assert SERVER_IP and SERVER_PORT and BOT_TOKEN and EXP and GUILD_ID, "Config is empty, pls fix"
    print("Initiating bot")
    LivePlayercountBot().run(BOT_TOKEN)

#https://eaassets-a.akamaihd.net/bl-cdn/cdnprefix/production-5766-20200917/public/base/bf4/map_images/335x160/xp0_firestorm.jpg