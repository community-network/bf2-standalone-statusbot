import asyncio
import sys
from opengsq.protocols import GameSpy3
import discord
import os
import aiohttp

"""BF4 ONLY"""
# CONFIG
BOT_TOKEN = os.environ['token']
SERVER_IP = os.environ['ip']
SERVER_PORT = os.environ['port']
BF2_MAPS = ['Dalian Plant', 'Daqing Oilfields', 'Dragon Valley', 'Fushe Pass', 'Greatwall', 'Gulf Of Oman',
            'Highway Tampa', 'Kubra Dam', 'Mashtuur City', 'Midnight Sun', 'Operation Blue Pearl',
            'Operation Clean Sweep', 'Operation Harvest', 'Operation Road Rage', 'Operation Smoke Screen',
            'Road To Jalalabad', 'Sharqi Peninsula', 'Songhua Stalemate', 'Strike At Karkand', 'Taraba Quarry',
            'Wake Island 2007', 'Zatar Wetlands']

class LivePlayercountBot(discord.Client):
    """Discord bot to display the BL true playercount in the bot status"""
 
    async def on_ready(self):
        print(f"Logged on as {self.user}\n" f"Started monitoring server {SERVER_IP}:{SERVER_PORT}")
        status = ""
        current_mapname = ""
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    server_info, map_name = await get_playercount(session)
                    if server_info == None:
                        await self.change_presence(activity=discord.Game("¯\\_(ツ)_/¯ server not found"))
                    else:
                        if server_info != status:  # avoid spam to the discord API
                            await self.change_presence(activity=discord.Game(server_info))
                            status = server_info
                        if current_mapname != map_name:
                            if map_name in BF2_MAPS:
                                map_slug = map_name.lower().replace(' ', '_')+'.jpg'
                            else:
                                map_slug = "default.jpg"
                            
                            with open(f"maps/{map_slug}", 'rb') as f:
                                await self.user.edit(avatar=f.read())
                            current_mapname = map_name
                except Exception as e:
                    print(e)
                await asyncio.sleep(10)
 
async def get_playercount(session):
    try:
        source = GameSpy3(address=SERVER_IP, query_port=int(SERVER_PORT))
        data = await source.get_status()
        max_slots = int(data["info"]["maxplayers"])
        map_name = data['info']["mapname"]
        true_playercount = int(data["info"]["numplayers"])
        server_info = f"{true_playercount}/{max_slots} - {map_name}"  # discord status message
        return server_info, map_name
    except Exception as e:
        print(f"Error getting data from server: {e}")  # BL autism
        return None, None
 
if __name__ == "__main__":
    assert sys.version_info >= (3, 7), "Script requires Python 3.7+"
    assert SERVER_IP and SERVER_PORT and BOT_TOKEN, "Config is empty, pls fix"
    print("Initiating bot")
    LivePlayercountBot().run(BOT_TOKEN)

#https://eaassets-a.akamaihd.net/bl-cdn/cdnprefix/production-5766-20200917/public/base/bf4/map_images/335x160/xp0_firestorm.jpg