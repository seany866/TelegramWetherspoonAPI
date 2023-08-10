# TelegramWetherspoonAPI
first dive into telegram and wetherspoon API

Enter your own telegram API token and a new channel will be setup so that you can query pubs and drinks for prices:

Begin the telegram bot. Message your bot with **/start**

**/pub** - you can enter the area you are in and it details addresses.

**/pub Dublin**

Output:

Pub Name: Keavan's Port 
Address: 1 Camden Street Upper, Dublin, County Dublin, D02 TC61
Telephone: 01 405 4790
Pub Number: 7381
Pub ID: c3673de0-59f4-4766-84fc-ef844320bd49
URL: /pubs/all-pubs/republic-of-ireland/county-dublin/keavans-port
---

==============================================================

**/id** - this will let you query the pub number for drink prices:

**/id 7381 doom bar**

Output:

Name: Doom Bar
Portion: Half pint
Price: €1.00
Portion: Pint
Price: €1.99
