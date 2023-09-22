import configparser
import requests
import httpx
import asyncio
import aiohttp
from cryptography.fernet import Fernet

config = configparser.ConfigParser()
config.read('config.ini')
app_name = config['general']['app_name']
connName = config['general']['connName']
version = config['general']['version']
tokenApp = config['general']['tokenApp']

class masterHook:

	connList:str = {}
		
	async def fetch_data(self,url):
		async with aiohttp.ClientSession() as session:
			async with session.post(url) as response:
				return await response.json()
				
	async def passCDNconnect(self,arg0:str,arg1:str):
		# URL de la API que deseas consultar
		url = f"http://192.168.71.189:60000/sys/auth?appName={arg0}"
		data = await self.fetch_data(url)
		print(len(data))
		for i in range(0,len(data)):
			self.connList['name'] = data[int(i)]['connName']
			self.connList['host'] = data[int(i)]['host']
			self.connList['user'] = data[int(i)]['usr']
			self.connList['password'] = data[int(i)]['pass']
			self.connList['db'] = data[int(i)]['db']
			self.connList['key'] = data[int(i)]['clever']
		return(self.connList)

def normalizer(mensaje_encriptado, clave):
	f = Fernet(clave)
	return f.decrypt(mensaje_encriptado).decode()

conectionData = asyncio.run(masterHook().passCDNconnect(app_name,connName))

print(conectionData)



#normalizer(conectionData['host'],conectionData['key'])