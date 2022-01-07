import stock.fetch as fetch
import stock.utils as utils

import plotly.graph_objects as go
from plotly.subplots import make_subplots

def drawCandleStick(data, start_date, end_date, 
                    colors=['green', 'red'], w=800, h=600, 
                    vol=None, rsi=None):
    # init
    symbol = list(data.columns.levels[1])[0]
    # calc break day
    dt_breaks = utils.calc_break_day(data, symbol, start_date, end_date)
    data.columns = ['high', 'low', 'open', 'close', 'volume']
    title = '{} stock price & volume from {} to {}'.format(symbol, start_date, end_date)
    
    # draw plot
    fig = make_subplots(rows=2, cols=1, 
                        shared_xaxes=True, vertical_spacing=0.02, row_heights=[0.6, 0.4])

    fig.append_trace(go.Candlestick(
            x=data.index,
            open=data['open'], high=data['high'],
            low=data['low'], close=data['close'],
            increasing_line_color=colors[0],
            decreasing_line_color=colors[1]
        ),
        row=1, col=1)

    # hide dates with no values
    fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])

    # show volume
    if vol is not None:
        fig.append_trace(go.Bar(
                x=data.index,
                y=vol,
                name='Volume'
            ),
            row=2, col=1)
        
    # if rsi is not None:
    #     fig.append_trace(go.Scatter(
    #             x=data.index,
    #             y=rsi,
    #             name='RSI'
    #         ),
    #         row=2, col=1)

    # update plot layout
    fig.update_layout(
        title=title,
        yaxis_title='Price',
        xaxis_title='Date',
        width=w,
        height=h,
        showlegend=False)

    # show plot
    fig.show()