# ServerLock
A Mordhau RCON script that locks and unlocks your server, useful for those who don't want a passworded server, but still want to use it privately at times. 
When the server is locked, only players who have been added to the admins list in lock.py can connect. Players who were already in the server will **not** be kicked, but can not reconnect if they leave the server. <br> ServerLock uses a modified version of Richard Neumann's [RCON library](https://github.com/conqp/rcon)

<h2>Using ServerLock</h2>

1. Make sure your Mordhau server is configured for RCON
2. Clone this repository
3. Add your server's IP, RCON Port & RCON Password to config.py
4. Add yourself to the admin list in lock.py
5. Run main.py
6. Connect to your Mordhau server and type !lock to toggle ServerLock

<h2>Credits</h2>

[10xJSChad](https://github.com/10xJSChad) - ServerLock <br>
[Richard Neumann](https://github.com/conqp) - Python RCON Library
