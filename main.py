import discord
import os

from system import config

from pycoingecko import CoinGeckoAPI

client = discord.Client()

@client.event
async def on_ready():
    print('I have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!price'):
        message_elements = message.content.split()

        try:
            symbol = message_elements[1]
        except IndexError:
            await message.channel.send("Sorry, no coin ID as been specified. Send **!coins** to get all coins and ID's.")
        
        try:
            currency = message_elements[2]
        except IndexError:
            currency = config.CURRENCY

        cg = CoinGeckoAPI()
        result = cg.get_price(ids=symbol, vs_currencies=currency)

        if len(result) == 0:
            await message.channel.send("Sorry, could not find this coin ID on CoinGecko. Send **!coins** to get all coins and ID's.")
            return

        price = result[symbol][currency]
        
        await message.channel.send(f"Price for {symbol}: {price} {currency.upper()}")

    elif message.content.startswith("!coins"):
        return
        cg = CoinGeckoAPI()
        result = cg.get_coins_list()
    
        messages = []
        message_body = ""
        for coin in result:
            if len(message_body) > 1500:
                messages.append(message_body)
                message_body = ""
                
            message_body += f"""**{coin["name"]}**
Symbol: {coin["symbol"]}
ID: {coin["id"]}

"""

        for message_body in messages:
            await message.channel.send(message_body)

client.run(config.DISCORD_BOT_TOKEN)
