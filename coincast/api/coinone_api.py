import simplejson as json
import httplib2


def get_response(url):
    headers = {
        'Content-type': 'application/json',
    }
    http = httplib2.Http()
    response, content = http.request(url, 'GET', headers=headers)
    return content


def get_result(url):
    content = get_response(url)
    content = json.loads(content)
    return content


def get_ticks_for(currency='all'):
    URL = 'https://api.coinone.co.kr/ticker/?currency='+currency
    return get_result(URL)


from coincast.model import coinone_tick
if __name__ == '__main__':

    print(get_ticks_for()['bch'])
    ticks_dict = get_ticks_for()
    ticks_list = coinone_tick.api2orm_list(ticks_dict)

    print(ticks_list)
