
import MetaTrader5 as mt5
import pandas as pd 
import threading as th
import time
import datetime

import math
import pytz
import numpy as np

print('run')


tehran_timezone = pytz.timezone('Asia/Tehran')

df_pross = pd.DataFrame(columns= ['time' ,  'pros' , 'sum_trade' , 'balance'])

def round_up(number, precision):

  return math.ceil(number * (10**precision)) / (10**precision)


def init():
    # mt5.initialize(path = r"C:\Program Files\LiteFinance MT5 real\terminal64.exe")
    # mt5.login(6910350 , password= 'Mahdi1400@' , server= 'LiteFinance-MT5-Live')
    # mt5.initialize(path = r"C:\Program Files\LiteFinance MT5 real 2\terminal64.exe")
    # mt5.login(6920086 , password= 'Mahdi1400@' , server= 'LiteFinance-MT5-Live')
    mt5.initialize(path = r"C:\Program Files\LiteFinance MT5 3\terminal64.exe")
    mt5.login(89373537 , password= 'Mahdi1400@' , server= 'LiteFinance-MT5-Demo')

def info():

    account_info=mt5.account_info()

    balance = account_info.balance
    equity  = account_info.equity
    profit  = account_info.profit
    
    return balance , equity , profit
    
def round_up(number, precision):

  return math.ceil(number * (10**precision)) / (10**precision)


def buy(symbol , lot , tp_ , sl_ , comment ):

    
    
    tp = abs(mt5.symbol_info_tick(symbol).bid + tp_ ) 
    sl = abs(mt5.symbol_info_tick(symbol).ask - sl_ ) 
    pos = mt5.ORDER_TYPE_BUY



    lot = round_up(lot, 2)
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    deviation = 100
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type":  pos ,
        "price": price,
        "deviation": deviation,
        "magic": 234002,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK ,
    }
     
    # send a trading request
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return ("failed . order_send failed, retcode={} {}".format(result.retcode ,request )) , False
        
    if result.retcode == 10009 :
        return result
    # if result:
    #     if result.retcode != mt5.TRADE_RETCODE_DONE:
    #         print("2. order_send failed, retcode={}".format(result.retcode))
    #         # request the result as a dictionary and display it element by element
    #         result_dict=result._asdict()
    #         for field in result_dict.keys():
    #             print("   {}={}".format(field,result_dict[field]))
    #             # if this is a trading request structure, display it element by element as well
    #             if field=="request":
    #                 traderequest_dict=result_dict[field]._asdict()
    #                 for tradereq_filed in traderequest_dict:
    #                     print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))


def sell(symbol , lot , tp_ , sl_, comment ):

    
    
    tp = abs(mt5.symbol_info_tick(symbol).ask - tp_  ) 
    sl = abs(mt5.symbol_info_tick(symbol).bid + sl_   ) 
    # tp = abs(mt5.symbol_info_tick(symbol).ask - tp_ -  (tp_ / 2 ) ) 
    # sl = abs(mt5.symbol_info_tick(symbol).bid + sl_ - ( tp_ / 2) ) 
    pos = mt5.ORDER_TYPE_SELL



    lot = round_up(lot, 2)
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    deviation = 100
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type":  pos ,
        "price": price,
        "deviation": deviation,
        "magic": 234002,
        "comment":  comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK ,
    }
     
    # send a trading request
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return ("failed . order_send failed, retcode={} {}".format(result.retcode ,request )) , False
        
    if result.retcode == 10009 :
        return result
    # if result:
    #     if result.retcode != mt5.TRADE_RETCODE_DONE:
    #         print("2. order_send failed, retcode={}".format(result.retcode))
    #         # request the result as a dictionary and display it element by element
    #         result_dict=result._asdict()
    #         for field in result_dict.keys():
    #             print("   {}={}".format(field,result_dict[field]))
    #             # if this is a trading request structure, display it element by element as well
    #             if field=="request":
    #                 traderequest_dict=result_dict[field]._asdict()
    #                 for tradereq_filed in traderequest_dict:
    #                     print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))


def close(ticket):
    
    
    
    def close_position(position):
        try:
            tick = mt5.symbol_info_tick(position.symbol)

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "position": position.ticket,
                "symbol": position.symbol,
                "volume": position.volume,
                "type": mt5.ORDER_TYPE_BUY if position.type == 1 else mt5.ORDER_TYPE_SELL,
                "price": tick.ask if position.type == 1 else tick.bid,  
                "deviation": 100,
                "magic": 234002,
                "comment": "Gu",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK ,
            }

            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                result ("Close failed . order_send failed, retcode={} {}".format(result.retcode ,request ))
                return False
            if result.retcode == 10009 :
                return True
        except Exception as e:
            print(f'Close : Eror in def close {e}')

    positions = mt5.positions_get()
    for position in positions:
        # print(position)
        
        if position.ticket == ticket :
            try:
                
                doit =  close_position(position)
                return doit
                time.sleep(0.1)

            except Exception as e:
                print(f'Clsoe : Eror for Clsoe {e}')
            time.sleep(0.05)

def all_close():
    
    
    
    def close_position(position):
        try:
            tick = mt5.symbol_info_tick(position.symbol)

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "position": position.ticket,
                "symbol": position.symbol,
                "volume": position.volume,
                "type": mt5.ORDER_TYPE_BUY if position.type == 1 else mt5.ORDER_TYPE_SELL,
                "price": tick.ask if position.type == 1 else tick.bid,  
                "deviation": 100,
                "magic": 234002,
                "comment": "Gu",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK ,
            }

            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                result ("Close failed . order_send failed, retcode={} {}".format(result.retcode ,request ))
                return False
            if result.retcode == 10009 :
                return True
        except Exception as e:
            print(f'Close : Eror in def close {e}')

    positions = mt5.positions_get()
    for position in positions:
        # print(position)
        
        
        try:
            
            doit =  close_position(position)
            time.sleep(0.1)

        except Exception as e:
            print(f'Clsoe : Eror for Clsoe {e}')
        time.sleep(0.05)

def close_(ticket , volume , comment):
    comment = str(comment)
    volume = round(volume , 2)
    
    def close_position(position , volume , comment):
        try:
            tick = mt5.symbol_info_tick(position.symbol)

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "position": position.ticket,
                "symbol": position.symbol,
                "volume": volume,
                "type": mt5.ORDER_TYPE_BUY if position.type == 1 else mt5.ORDER_TYPE_SELL,
                "price": tick.ask if position.type == 1 else tick.bid,  
                "deviation": 100,
                "magic": 234002,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK ,
            }

            result = mt5.order_send(request)
            # if result.retcode != mt5.TRADE_RETCODE_DONE:
            #     result ("Close failed . order_send failed, retcode={} {}".format(result.retcode ,request ))
            #     return False
            print(result , request)
        except Exception as e:
            print(f'Close : Eror in def close 219 {e}')

    positions = mt5.positions_get()
    for position in positions:
        # print(position)
        
        if position.ticket == ticket :
            try:
                
                close_position(position , volume , comment)
                return 'clsoe'
                time.sleep(0.1)

            except Exception as e:
                print(f'Clsoe : Eror for Clsoe 233 {e}')
            time.sleep(0.05)


def order_close(symbol):
    orders=mt5.orders_get(symbol = symbol)
    

    if orders :
        request = {

            'action' : mt5.TRADE_ACTION_REMOVE , 
            'order'  : mt5.orders_get(symbol = symbol)[0].ticket

        }
        
        result =  mt5.order_send(request)
        if result is None:
            print("No orders with group=\"*GBP*\", error code={}".format(mt5.last_error()))
        else:

            if result.retcode == 10009 :

                return  True


main_win = {}

def close_pos(tickit_one_one, tickit_one_tow, tickit_tow_one, tickit_tow_tow ):
    

    positions_one_one = mt5.positions_get(ticket=tickit_one_one.order)[0]
    positions_one_tow = mt5.positions_get(ticket=tickit_one_tow.order)[0]
    positions_tow_one = mt5.positions_get(ticket=tickit_tow_one.order)[0]
    positions_tow_tow = mt5.positions_get(ticket=tickit_tow_tow.order)[0]

    
    
    while True:
        time.sleep(0.02)

        if mt5.positions_get(ticket=tickit_one_one.order) == None  or   mt5.positions_get(ticket=tickit_one_tow.order) == None :
            if mt5.positions_get(ticket=tickit_tow_one.order)  is not None  or  mt5.positions_get(ticket=tickit_tow_tow.order) is not None :
                close(tickit_tow_one.order)
                close(tickit_tow_tow.order)

            break

        else:


            if mt5.positions_get(ticket=tickit_one_one.order)[0].profit  + mt5.positions_get(ticket=tickit_one_tow.order)[0].profit  >=  6 : 
                close(tickit_one_one.order)
                close(tickit_one_tow.order)
                main_win['win'] += 1


                if mt5.positions_get(ticket=tickit_tow_one.order) == None  or  mt5.positions_get(ticket=tickit_tow_tow.order) == None :
                    break        

                while True:
                    time.sleep(0.02)
                    if mt5.positions_get(ticket=tickit_tow_one.order)[0].profit  + mt5.positions_get(ticket=tickit_tow_tow.order)[0].profit  >=  0 : 
                        close(tickit_tow_one.order)
                        close(tickit_tow_tow.order)
                        break

        






        if mt5.positions_get(ticket=tickit_tow_one.order) == None  or  mt5.positions_get(ticket=tickit_tow_tow.order) == None :
            if mt5.positions_get(ticket=tickit_one_one.order)  is not None  or  mt5.positions_get(ticket=tickit_one_tow.order) is not None :
                close(tickit_one_one.order)
                close(tickit_one_tow.order)

            break

        else:

            if mt5.positions_get(ticket=tickit_tow_one.order)[0].profit  + mt5.positions_get(ticket=tickit_tow_tow.order)[0].profit  >=  6 : 
                close(tickit_tow_one.order)
                close(tickit_tow_tow.order)
                main_win['win'] += 1


                if mt5.positions_get(ticket=tickit_one_one.order) == None  or   mt5.positions_get(ticket=tickit_one_tow.order) == None :
                    break

                while True:
                    time.sleep(0.02)
                    if mt5.positions_get(ticket=tickit_one_one.order)[0].profit  + mt5.positions_get(ticket=tickit_one_tow.order)[0].profit  >=  0 : 
                        close(tickit_one_one.order)
                        close(tickit_one_tow.order)
                        break




def clean():

    while True:
        time.sleep(0.5)

        if main_win.get('win', 0) // 10 == 1:
            should_break = False  # متغیر کمکی برای کنترل خروج از حلقه‌ها
            for pros in dic_order:
                for i in pros:
                    positions_0 = mt5.positions_get(ticket=i[0].order)
                    positions_1 = mt5.positions_get(ticket=i[1].order)
                    
                    # اطمینان حاصل کنید که هر دو پوزیشن معتبر و دارای سود می‌باشند
                    if positions_0 and positions_1:
                        profit_0 = positions_0[0].profit
                        profit_1 = positions_1[0].profit
                        
                        # اصلاح شرط ترکیبی
                        if -30 < profit_0 + profit_1 < -20:
                            close(i[0].order)
                            close(i[1].order)
                            should_break = True  # تنظیم متغیر کمکی برای خروج از حلقه‌ها
                            break
                if should_break:
                    break  # خروج از حلقه بیرونی اگر متغیر کمکی تنظیم شده باشد


            





def sod_sang(tickit_one_one, tickit_one_tow, tickit_tow_one, tickit_tow_tow):


    while True:
        try : 
            th.Thread(target=close_pos , args=(tickit_one_one, tickit_one_tow, tickit_tow_one, tickit_tow_tow)).start()
            break








        except Exception as e:
            print(f" Error 350 : {e}")
            time.sleep(1)


def close_nith():
    while True:
        time.sleep(0.2)
        try :
            dic_tick = {}
            jam = 0
            
            positions = mt5.positions_get()
            for position in positions:
                # print(position)
                
                dic_tick[position.ticket] = position.profit
                jam = jam + position.profit
            print('nith close' , jam)
            if jam >= 0 :
                for i in dic_tick:
                    time.sleep(0.2)
                    close(i)
                    break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)


def run_one():

    tickit_one_one =  buy('GBPUSD_o', 2.6 , 0 , 0 , 'one')
    tickit_one_tow =  sell('EURUSD_o',  3 , 0 , 0 , 'one')

    return tickit_one_one , tickit_one_tow 


def run_tow():
    
    tickit_tow_one =  sell('GBPUSD_o', 2.6 , 0 , 0 , 'tow')
    tickit_tow_tow =  buy('EURUSD_o',  3 , 0 , 0 , 'tow')

    return  tickit_tow_one , tickit_tow_tow


def run():
    init()

    
    now = datetime.datetime.now(tehran_timezone)
    if 0 < now.hour < 24   :
        try:

            if len(mt5.positions_get(symbol='GBPUSD_o')) < 20 :
                tickit_one_one =  buy('GBPUSD_o', 0.17 , 0 , 0 , 'one')
                tickit_one_tow =  sell('EURUSD_o', 0.2 , 0 , 0 , 'one')
                tickit_tow_one =  sell('GBPUSD_o', 0.17 , 0 , 0 , 'tow')
                tickit_tow_tow =  buy('EURUSD_o', 0.2 , 0 , 0 , 'tow')

                return tickit_one_one , tickit_one_tow , tickit_tow_one , tickit_tow_tow
                
                
            # else:
            #     close_nith()
            #     break

            # if len(mt5.positions_get(symbol='GBPUSD_o')) == 0 and len(mt5.positions_get(symbol='EURUSD_o')) == 0:

            #     tickit_tow_one =  th.Thread(target=buy  , args=('GBPUSD_o', 1, 0 , 0 , 'tow')).start()
            #     tickit_tow_tow =  th.Thread(target=sell , args=('EURUSD_o', 1, 0 , 0 , 'tow' )).start()






        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)  # Wait for 1 minute before retrying


dic_order = {}
        
def main():
    num_trade = 0
    while True:

        print(datetime.datetime.now(tehran_timezone))
        tickit_one_one , tickit_one_tow , tickit_tow_one , tickit_tow_tow = run()
        dic_order[num_trade] = [[tickit_one_one , tickit_one_tow ], [tickit_tow_one , tickit_tow_tow]]
        num_trade += 1

        if tickit_one_one and tickit_one_tow and tickit_tow_one and tickit_tow_tow :
            

            sod_sang(tickit_one_one , tickit_one_tow , tickit_tow_one , tickit_tow_tow)
        time.sleep(1800)


main()


# init()
# all_close()