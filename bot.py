import asyncio
import sys
from os import path, environ
from opengsq.protocols import GameSpy3
import discord

"""BF4 ONLY"""
# CONFIG
BOT_TOKEN = environ['token']
SERVER_IP = environ['ip']
SERVER_PORT = environ['port']
GUILD_ID = environ['guild']

class LivePlayercountBot(discord.Client):
    """Discord bot to display the BL true playercount in the bot status"""
 
    async def on_ready(self):
        print(f"Logged on as {self.user}\n" f"Started monitoring server {SERVER_IP}:{SERVER_PORT}")
        status = ""
        current_servername = ""
        current_mapname = ""
        while True:
            try:
                server_info, map_name, server_name = await get_playercount()
                if server_info == None:
                    await self.change_presence(activity=discord.Game("¯\\_(ツ)_/¯ server not found"))
                else:
                    if server_info != status:  # avoid spam to the discord API
                        await self.change_presence(activity=discord.Game(server_info))
                        status = server_info
                        
                    if current_servername != server_name: # avoid spam to the discord API
                        guild = self.get_guild(int(GUILD_ID))
                        await guild.me.edit(nick=server_name[:32])
                        current_servername = server_name
                        
                    if current_mapname != map_name: # avoid spam to the discord API
                        to_check = f"maps/{map_name.lower().replace(' ', '_')}"
                        if path.exists(f"{to_check}.jpg"):
                            map_slug = f"{to_check}.jpg"
                        if path.exists(f"{to_check}.png"):
                            map_slug = f"{to_check}.png"
                        else:
                            map_slug = "maps/default.jpg"
                        
                        with open(map_slug, 'rb') as f:
                            await self.user.edit(avatar=f.read())
                        current_mapname = map_name
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
        return server_info, map_name, server_name
    except Exception as e:
        print(f"Error getting data from server: {e}")  # BL autism
        return None, None, None
 
if __name__ == "__main__":
    assert sys.version_info >= (3, 7), "Script requires Python 3.7+"
    assert SERVER_IP and SERVER_PORT and BOT_TOKEN, "Config is empty, pls fix"
    print("Initiating bot")
    LivePlayercountBot().run(BOT_TOKEN)

#https://eaassets-a.akamaihd.net/bl-cdn/cdnprefix/production-5766-20200917/public/base/bf4/map_images/335x160/xp0_firestorm.jpg