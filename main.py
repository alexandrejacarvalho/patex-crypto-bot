import discord
import os

from system import config

from pycoingecko import CoinGeckoAPI

from models.base import session, Coin

from modules.coingecko import CoinGeckoHelpers

client = discord.Client()

pc = "!"
commands = [
        {
            "command": "hello",
            "description": "Warup?",
            "help": f"📄 {pc}hello",
        },
        {
            "command": "price",
            "description": "ℹ️ Check the price of a coin by its symbol.",
            "help": f"📄 {pc}price <symbol\*> <quote_symbol={config.CURRENCY}>",
        },
        {
            "command": "coins",
            "description": "ℹ️ Check the coins library. The coins listed here are constantly checked for fluctuations on the market that reveal a good oportunity of profit.",
            "help": f"📄 {pc}coins",
        },
        {
            "command": "addcoin",
            "description": "ℹ️ Add coins to the library.",
            "help": f"📃 {pc}addcoin <symbol\*> <quote_symbol={config.CURRENCY}>",
        },
        {
            "command": "removecoin",
            "description": "ℹ️ Remove coins to the library.",
            "help": f"📃 {pc}removecoin <symbol\*>",
        },
    ]

@client.event
async def on_ready():
    print('I have logged in as {0.user}'.format(client))
        
@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return

    elif message.content.startswith(f"{pc}commands"):  # Commands List Command
        message_body = ""
        for command in commands:
            message_body += f"**{pc}{command['command']}**\n" \
                            f"{command['description']}\n" \
                            f"{command['help']}\n\n"

        await message.channel.send(message_body)

    elif message.content.startswith(f"{pc}{commands[0]['command']}"):  # Hello Command
        # TODO greetings message containing news, the biggest bulls and bears of the day, list coin library prices, ..
        await message.channel.send('Hello!')

    elif message.content.startswith(f"{pc}{commands[1]['command']}"):  # Price Command
        message_elements = message.content.split()

        try:
            symbol = message_elements[1]

            if symbol == "help":
                await message.channel.send(commands[1]['help'])
                return
        except IndexError:
            await message.channel.send("🥱 Sorry, no Coin Symbol as been specified.")
            return
        
        try:
            quote_symbol = message_elements[2]
        except IndexError:
            quote_symbol = config.CURRENCY

        cgh = CoinGeckoHelpers()
        coin_gecko_id, coin_gecko_name = cgh.get_coin_by_symbol(symbol)
        print(coin_gecko_id)
        if not coin_gecko_id and not coin_gecko_name:
            await message.channel.send("😵 Sorry, could not find this Coin Symbol in the database.")
            return

        cg = CoinGeckoAPI()
        price_result = cg.get_price(ids=coin_gecko_id, vs_currencies=quote_symbol)
        price = price_result[coin_gecko_id][quote_symbol]

        last_day_chart_data_result = cg.get_coin_market_chart_by_id(coin_gecko_id, quote_symbol, 1)
        day_ago_price = last_day_chart_data_result["prices"][0][-1]
        print(day_ago_price)
        print(price)

        last_day_hours_flutuation_percentage = (price - day_ago_price) / day_ago_price * 100
        
        await message.channel.send(f"💸 Price for **{coin_gecko_name}** {symbol.upper()}: {price} {quote_symbol.upper()} `({round(float(last_day_hours_flutuation_percentage), 2)} %)`")

    elif message.content.startswith(f"{pc}{commands[2]['command']}"):  # Coins Command
        # TODO send coin list
        try:
            argument = message_elements[1]

            if argument == "help":
                await message.channel.send(commands[2]['help'])
        except IndexError:
            pass

        

    elif message.content.startswith(f"{pc}{commands[3]['help']}"):  # Add Coin Command
        message_elements = message.content.split()

        try:
            symbol = message_elements[1]

            if symbol == "help":
                await message.channel.send(commands[3]['help'])
        except IndexError:
            await message.channel.send("🥱 Sorry, no Coin ID as been specified. Check the channel pinned messages for Coin ID's.")
        
        try:
            quote_symbol = message_elements[2]
        except IndexError:
            quote_symbol = config.CURRENCY

        cgh = CoinGeckoHelpers()
        coin_gecko_id, coin_gecko_name = cgh.get_coin_by_symbol(symbol)

        cg = CoinGeckoAPI()
        result = cg.get_price(ids=coin_gecko_id, vs_currencies=quote_symbol)
        if len(result) == 0:
            await message.channel.send("😵 Sorry, could not find this Coin ID on CoinGecko. Check the channel pinned messages for Coin ID's.")
            return

        if coin_gecko_id:
            ed_coin = Coin(id_coingecko=coin_gecko_id, symbol=symbol, name=coin_gecko_name)
            session.add(ed_coin)
            session.commit()

        await message.channel.semd("✅ Coin added to the library.")

    elif message.content.startswith(f"{pc}{commands[4]['command']}"):  # Remove Coin Command
        message_elements = message.content.split()

        try:
            symbol = message_elements[1]

            if symbol == "help":
                await message.channel.send(f"📃 {pc}{commands[4]['help']} <symbol*>")
        except IndexError:
            await message.channel.send("🥱 Sorry, no Coin ID as been specified. Type !coins for Coin ID's in the library.")

        if coin_gecko_id:
            ed_coin = session.query(Coin).filter(symbol==symbol).first()
            session.delete(ed_coin)
            session.commit()

        await message.channel.send("✅ Coin removed from the library.")

client.run(config.DISCORD_BOT_TOKEN)
