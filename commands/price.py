import discord
import asyncio
from discord.ext import commands
from discord.commands import slash_command, Option
import configparser
from PIL import Image, ImageDraw, ImageFont

import stock_modules.fetch as fetch
import stock_modules.utils as utils
import stock_modules.figure as figure
import stock_modules.indicate as indicate

class Price(commands.Cog):
    @slash_command(
        name='chart',
        description='Check symbol chart.'
    )
    async def getChart(self, ctx, *, symbol = "SHI"):
        start_date = "2019-01-01"
        end_date = "2022-01-24"
        len = 30

        loader = fetch.DataLoader(symbol, start_date, end_date)
        data = loader.fetchPrice()

        figure.drawFigure(data, symbol, length=len, drawMA=True, drawBB=True, drawVol=True, drawRSI=True, drawMACD=True)
        
        await ctx.send(file=discord.File('index.png'), delete_after=60)
        await ctx.respond(f"Biểu đồ của {symbol} trong {len} ngày gần đây!", delete_after=60)