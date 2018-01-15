import requests
import time
from datetime import datetime, timedelta
from coincast.api.base_exchange import Excahnge
import configparser
import base64
import json
import hashlib
import hmac

class CoinoneExchange(Excahnge):
    def __init__(self, access_token=None, secret_key=None, username=None):
        if access_token is None or secret_key is None or username is None:
           raise Exception("Need to access token or secret_key.")

        else :
            self.access_token = access_token
            self.secret_key = secret_key

        self.host = "https://api.coinone.co.kr"
        self.username = username


    def get_username(self):
        return self.username

    def get_nonce(self):
        return int(time.time()*1000)

    def get_token(self):
        if self.access_token is not None:
            return self.access_token
        else:
            raise Exception("Need to set_token")

    def set_token(self, grant_type="refresh_token"):
        """
        set token
        grant_type: password, refresh_token

        saved self.access_token, self.refresh_token, self.token_type
        """
        pass

    def get_ticker(self, coin_type=None):
        """
        Get Ticker

        args:
            coin_type
        Returns:
            timestamp
            last
            high
            low
            volume
        """
        ticker_api_path = '/ticker/'
        url_path = self.host + ticker_api_path
        params = {"currency": coin_type}
        res = requests.get(url_path, params=params)
        response_json = res.json()
        result = {}
        result["timestamp"] = str(response_json["timestamp"])
        result["last"] = response_json["last"]
        result["high"] = response_json["high"]
        result["low"] = response_json["low"]
        result["volume"] = response_json["volume"]
        return result

    def get_filled_orders(self, coin_type=None, per="minute"):
        """
        List of filled orders

        Keyword arguments:
        per -- last time minute,hour,day

        Returns:
            api response
        """
        pass

    def get_constants(self):
        """
        Get constant values

        Keyword arguments:

        Returns:
            api response
        """
        pass


    def get_signature(self, encoded_payload, secret_key):
        signature = hmac.new(secret_key, encoded_payload, hashlib.sha512)
        return signature.hexdigest()

    def get_wallet_status(self):
        """
        Get wallet_status
        """
        time.sleep(1)
        wallet_status_api_path = "/v2/account/balance"
        url_path = self.host + wallet_status_api_path
        payload = {
            "access_token": self.access_token,
            'nonce': self.get_nonce()
        }
        dumped_json = json.dumps(payload)
        encoded_payload = base64.b64encode(dumped_json.encode('utf-8'))

        headers = {'Content-type': 'application/json',
                   'X-COINONE-PAYLOAD': encoded_payload,
                   'X-COINONE-SIGNATURE': self.get_signature(encoded_payload, self.secret_key.encode('utf-8'))}

        res = requests.post(url_path, headers=headers, data=payload)
        result = res.json()
        wallet_status = {}
        wallet_status["btc"] = result["btc"]
        wallet_status["eth"] = result["eth"]
        wallet_status["etc"] = result["etc"]
        wallet_status["bch"] = result["bch"]
        wallet_status["qtum"] = result["qtum"]
        wallet_status["krw"] = result["krw"]
        wallet_status["xrp"] = result["xrp"]
        wallet_status["iota"] = result["iota"]
        wallet_status["ltc"] = result["ltc"]
        return wallet_status


    def get_list_my_orders(self, coin_type=None):
        """
        Get my order list
        """
        list_api_path = "/v2/order/limit_orders/"
        url_path = self.host + list_api_path
        payload ={
            "access_token":self.access_token,
            "currency":coin_type,
            'nonce': self.get_nonce()
        }
        dumped_json = json.dumps(payload)
        encoded_payload = base64.b64encode(dumped_json.encode('utf-8'))

        headers = {'Content-type': 'application/json',
                   'X-COINONE-PAYLOAD': encoded_payload,
                   'X-COINONE-SIGNATURE': self.get_signature(encoded_payload, self.secret_key.encode('utf-8'))}

        res = requests.post(url_path, headers=headers, data=payload)
        result = res.json()
        return result

    def get_my_order_status(self, coin_type=None, order_id=None):
        """
        get list my transaction history
        """
        list_api_path = "/v2/order/order_info/"
        url_path = self.host + list_api_path
        payload = {
            "access_token": self.access_token,
            "currency": coin_type,
            "order_id": order_id,
            'nonce': self.get_nonce()
        }
        dumped_json = json.dumps(payload)
        encoded_payload = base64.b64encode(dumped_json.encode('utf-8'))

        headers = {'Content-type': 'application/json',
                   'X-COINONE-PAYLOAD': encoded_payload,
                   'X-COINONE-SIGNATURE': self.get_signature(encoded_payload, self.secret_key.encode('utf-8'))}

        res = requests.post(url_path, headers=headers, data=payload)
        result = res.json()
        return result

    def buy_coin_order(self, coin_type=None, price=None, qty=None, order_type="limit"):
        """
        buy_coin_order
        """
        if order_type != "limit":
            raise Exception("Coinone order type support only limit.")
        time.sleep(1)
        buy_limit_api_path ="/v2/order/limit_buy/"
        url_path = self.host + buy_limit_api_path
        payload ={
            "access_token" : self.access_token,
            "price" : int(price),
            "qty" : float(qty),
            "currency":coin_type,
            'nonce' : self.get_nonce()
        }
        dumped_json = json.dumps(payload)
        encoded_payload = base64.b64encode(dumped_json.encode('utf-8'))

        headers = {'Content-type': 'application/json',
                   'X-COINONE-PAYLOAD': encoded_payload,
                   'X-COINONE-SIGNATURE': self.get_signature(encoded_payload, self.secret_key.encode('utf-8'))}

        res = requests.post(url_path, headers=headers, data=payload)
        result = res.json()
        return result

    def sell_coin_order(self, coin_type=None, price=None, qty=None, order_type="limit"):
        """
        sell_coin_order
        """
        if order_type != "limit":
            raise Exception("Coinone order type support only limit.")
        time.sleep(1)
        sell_limit_api_path ="/v2/order/limit_sell/"
        url_path = self.host + sell_limit_api_path
        payload ={
            "access_token" : self.access_token,
            "price" : int(price),
            "qty" : float(qty),
            "currency":coin_type,
            'nonce' : self.get_nonce()
        }
        dumped_json = json.dumps(payload)
        encoded_payload = base64.b64encode(dumped_json.encode('utf-8'))

        headers = {'Content-type': 'application/json',
                   'X-COINONE-PAYLOAD': encoded_payload,
                   'X-COINONE-SIGNATURE': self.get_signature(encoded_payload, self.secret_key.encode('utf-8'))}

        res = requests.post(url_path, headers=headers, data=payload)
        result = res.json()
        return result

    def cancel_coin_order(self, coin_type=None, price=None, qty=None, order_type="limit", order_id=None):
        """
        cancel_coin_order
        """
        if coin_type is None or price is None or qty is None or order_type is None or order_id is None:
            raise Exception("Need to parameter")
        time.sleep(1)
        cancel_api_path ="/v2/order/cancel/"
        url_path = self.host + cancel_api_path
        if order_type == "sell":
            is_ask = 1
        else:
            is_ask = 0
        payload ={
            "access_token" : self.access_token,
            "order_id" : order_id,
            "price" : int(price),
            "qty" : float(qty),
            "currency":coin_type,
            "is_ask": is_ask,
            'nonce' : self.get_nonce()
        }
        dumped_json = json.dumps(payload)
        encoded_payload = base64.b64encode(dumped_json.encode('utf-8'))

        headers = {'Content-type': 'application/json',
                   'X-COINONE-PAYLOAD': encoded_payload,
                   'X-COINONE-SIGNATURE': self.get_signature(encoded_payload, self.secret_key.encode('utf-8'))}

        res = requests.post(url_path, headers=headers, data=payload)
        result = res.json()
        return result




if __name__ == '__main__':
    exchange = CoinoneExchange(username='test')
    #print(exchange.set_token(grant_type='init'))
    #print(exchange.get_wallet_status())
    order_list = exchange.get_list_my_orders(coin_type='btc')
    #order = order_list['limitOrders'][0]
    #print(order_list)
    #print(exchange.get_my_order_status(coin_type='btc',order_id=order['orderId']))

    print(exchange.buy_coin_order(coin_type='etc',price=1000,qty=1))
    order_list = exchange.get_list_my_orders(coin_type='etc')
    order2 = order_list['limitOrders'][0]
    print(order_list)
    print(exchange.get_my_order_status(coin_type='etc', order_id=order2['orderId']))

    print(exchange.sell_coin_order(coin_type='iota',price=10000,qty=1))
    order_list = exchange.get_list_my_orders(coin_type='iota')
    order3 = order_list['limitOrders'][0]
    print(order_list)
    print(exchange.get_my_order_status(coin_type='iota', order_id=order3['orderId']))

    print(exchange.cancel_coin_order(coin_type='etc',price=1000,qty=1,order_type='buy',order_id=order2['orderId']))
    print(exchange.cancel_coin_order(coin_type='iota', price=10000, qty=1, order_type='sell', order_id=order3['orderId']))