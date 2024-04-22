<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>XMPP Connection Library</title>
</head>
<body>
  <h1>XMPP Connection Library</h1>

  <p>This Python library provides asynchronous functionality for establishing and interacting with XMPP (Extensible Messaging and Presence Protocol) connections. It is specifically designed for integrating with the Epic Games services, such as Fortnite.</p>

  <h2>Features</h2>

  <ul>
    <li>Asynchronous connection handling using <code>aiohttp</code> library.</li>
    <li>Methods for logging in, joining parties, sending messages, setting presence, and maintaining a heartbeat.</li>
    <li>Flexible and easy-to-use interface for interacting with XMPP services.</li>
  </ul>

  <h2>Usage</h2>

  <p>Here's a basic example of how to use the library:</p>

  <pre><code class="python">
import aiohttp
import asyncio
from xmpp_connection import XMPP_connection

async def main():
    async with aiohttp.ClientSession() as session:
        xmpp = XMPP_connection(session)
        ws = await xmpp.get_connection()
        await xmpp.Login(ws, account)
        await xmpp.JoinParty(ws, account, uid, party_id)
        await xmpp.Send_Party_Msg(ws, party_id, "Hello from XMPP!")
        await xmpp.SetPresence(ws, "Online")
        await xmpp.Connect_HeartBeat(ws, jid)

asyncio.run(main())
  </code></pre>

  <h2>Contributing</h2>

  <p>Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.</p>

  <h2>License</h2>

  <p>This project is licensed under the MIT License - see the <a href="LICENSE">LICENSE</a> file for details.</p>
</body>
</html>
