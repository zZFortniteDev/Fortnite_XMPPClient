import aiohttp # aiohttp is the wss client
import asyncio#importing the asyncio module as this is Async code
import uuid, base64 #two imports to use
import urllib.parse #importing the urllib.parse module to parse the Displaynames in MAC message.

class XMPP_connection:
    def __init__(self, session:aiohttp.ClientSession) -> None:
        #self.connection_pool = []
        #self.connection_number = 7
        #useless
        self.server = "prod.ol.epicgames.com"
        loop = asyncio.get_event_loop()
        if not loop.is_running():
            print("Create in the object in async funcion.")
            return
        session = session or aiohttp.ClientSession()
        #asyncio.create_task(self.UpdatePool())
    async def CloseXMPP(self, ws:aiohttp.ClientWebSocketResponse):
        await ws.close()
        del ws
        return
    async def CreateWS(self):
        ws = await self.session.ws_connect(f"wss://xmpp-service-{self.server}", protocols=['xmpp'])
        #<open xmlns="urn:ietf:params:xml:ns:xmpp-framing" to="prod.ol.epicgames.com" version="1.0" />
        await ws.send_str(f'<open xmlns="urn:ietf:params:xml:ns:xmpp-framing" to="{self.server}" version="1.0" />')
        await ws.receive()
        await ws.receive()
        return ws

    async def get_connection(self) -> aiohttp.ClientWebSocketResponse:
        return await self.CreateWS()
    #All of this are useless as it take around 2sec to open new connection:
    #This part of the pool but no pool uses.
        #l = self.connection_pool
        #if len(l) > 0:
        #    asyncio.create_task(self.UpdatePool())
        #    return l.pop()
        #else:
        #    return self.CreateWS()
    #this funciton is not needed. its Heartbeat that will make sure you have ready connection at any time. its useless as xmpp will force close the connection after 30 seconds without login.
    #async def HeartBeat(self):
    #    while True:
    #        for i in range(2):
    #            for ws in list(self.connection_pool):
    #                uid = (uuid.uuid4().hex).upper()
    #                await ws.send_str(f'<iq id="{(uuid.uuid4().hex).upper()}" type="get" to="{self.server}" from="{uid}"><ping xmlns="urn:xmpp:ping"/></iq>')
    #            await asyncio.sleep(10)
    #        await self.ReCreatePool()
    #part of pool
    #async def UpdatePool(self):
    #    new_pool_ = []
    #    for _ in range(self.connection_number):
    #        new_pool_.append(self.CreateWS())
    #    self.connection_pool = await asyncio.gather(*new_pool_)
    #async def ReCreatePool(self):
    #    new_pool_ = []
    #    for _ in range(self.connection_number):
    #        new_pool_.append(self.CreateWS())
    #    delete_sockets = list(self.connection_pool)
    #    self.connection_pool = await asyncio.gather(*new_pool_)
    #    for ws in delete_sockets:
    #        await ws.close()
    #        del ws
    async def Login(self, ws:aiohttp.ClientWebSocketResponse, account):
        uid = (uuid.uuid4().hex).upper()
        account_id = account['account_id']
        auth = account['access_token']
        login = base64.b64encode(f"\x00{account_id}\x00{auth}".encode()).decode()
        await ws.send_str(f'<auth mechanism="PLAIN" xmlns="urn:ietf:params:xml:ns:xmpp-sasl">{login}</auth>')
        await ws.receive()
        await ws.send_str(f'<open xmlns="urn:ietf:params:xml:ns:xmpp-framing" to="{self.server}" version="1.0" />')
        await ws.receive()
        await ws.receive()
        await ws.send_str(f'<iq id="_xmpp_bind1" type="set"><bind xmlns="urn:ietf:params:xml:ns:xmpp-bind"><resource>V2:Fortnite:WIN::{uid}</resource></bind></iq>')
        await ws.receive()
        await ws.send_str('<iq id="_xmpp_session1" type="set"><session xmlns="urn:ietf:params:xml:ns:xmpp-session"/></iq>')
        return uid
    
    async def JoinParty(self, ws:aiohttp.ClientWebSocketResponse, account, uid, party_id):
        name = urllib.parse.quote(account['displayName'])
        account_id = account['account_id']
        muc_join = f'<presence to="Party-{party_id}@muc.prod.ol.epicgames.com/{name}:{account_id}:V2:Fortnite:WIN::{uid}"><x xmlns="http://jabber.org/protocol/muc"><history maxstanzas="50"/></x></presence>'
        await ws.send_str(muc_join)

    async def Send_Party_Msg(self, ws:aiohttp.ClientWebSocketResponse, party_id, msg):
        await ws.send_str(f'<message to="Party-{party_id}@muc.prod.ol.epicgames.com" type="groupchat"><body>{msg}</body></message>')

    async def Send_Whisper_Msg(self, ws:aiohttp.ClientWebSocketResponse, friend_id, msg):
        await ws.send_str(f'<message to="{friend_id}@prod.ol.epicgames.com" type="chat"><body>{msg}</body></message>')

    async def SetPresence(self, ws:aiohttp.ClientWebSocketResponse, status):
        status = {"Status":status,"ProductName":"Fortnite"}
        await ws.send_str('<presence><status>{0}</status></presence>'.format(status))

    async def Connect_HeartBeat(self, ws:aiohttp.ClientWebSocketResponse, jid, Flag:bool = True): #flag if needed to stop the heartbeat
        #Create as Task not as main thingi
        while Flag:
            #send heartbeat every 60 seconds
            await asyncio.sleep(60)
            #only errros can be is connection is closed
            #it can come in alot of ways. network error, client close, server close, etc.
            try:
                await ws.send_str(f'<iq id="{(uuid.uuid4().hex).upper()}" type="get" to="{self.server}" from="{jid}"><ping xmlns="urn:xmpp:ping"/></iq>')
            except:
                break
