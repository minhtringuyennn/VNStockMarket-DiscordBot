import discord, asyncio, requests, random, configparser, os
from discord.ext import commands
from discord.commands import slash_command, Option
from PIL import Image, ImageDraw, ImageFont

import stock_modules.fetch as fetch
import stock_modules.utils as utils
import stock_modules.figure as figure
import stock_modules.indicate as indicate
import commands.constants as constants

class Price(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        read_config = configparser.ConfigParser()
        path = os.path.join(os.path.abspath(__file__+"/../../"),"config", "config.ini")
        read_config.read(path)
        self.__TIMEOUT = read_config.get("config", "TIME_OUT")
        
    @discord.slash_command(
        name='price',
        description='Check symbol price.'
    )
    async def getStockPrice(self, ctx, *, symbol):
        data = fetch.call_api_vietstock(symbol.upper())
        
        mess = ""
        if data["ColorId"] == 2:
            mess = random.choice(constants.MESS_CE)
        if data["ColorId"] == -2:
            mess = random.choice(constants.MESS_FL)
        if data["ColorId"] == 1:
            mess = random.choice(constants.MESS_UP)
        if data["ColorId"] == -1:
            mess = random.choice(constants.MESS_DOWN)
        if data["ColorId"] == 0:
            mess = random.choice(constants.MESS_TC)
            
        price_str = str(data["LastPrice"])
        percent_change = str(data["PerChange"])
        mess = mess.replace("#code#",symbol.upper()).replace("#price#", price_str)
        
        await ctx.respond("Giá của " + symbol.upper() + " là: " + str(data["LastPrice"]) + " tăng/giảm: " + percent_change + "%" + "\n" + mess, delete_after=self.__TIMEOUT)

    @discord.slash_command(
        name='briefstats',
        description='Check symbol brief stats.'
    )
    async def getStockBrief(self, ctx, *, symbol):
        data = fetch.call_api_vietstock(symbol)
        await ctx.respond("EPS: " + str(data["EPS"]) + "\n" + "P/E: " + str(data["PE"]) + "\n" + "P/B: " + str(data["PB"]), delete_after=self.__TIMEOUT)
        
    @slash_command(
        name='chart',
        description='Check symbol chart.'
    )
    async def getChart(self, ctx, *, symbol):
        len = 30
        start_date = utils.get_last_year_date()
        end_date = utils.get_today_date()

        loader = fetch.DataLoader(symbol, start_date, end_date)
        data = loader.fetchPrice()

        figure.drawFigure(data, symbol, length=len)
        
        await ctx.send(file=discord.File('./images/index.png'), delete_after=self.__TIMEOUT)
        await ctx.respond(f"Biểu đồ của {symbol} trong {len} ngày gần đây!", delete_after=self.__TIMEOUT)