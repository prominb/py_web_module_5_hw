import sys
from datetime import datetime, timedelta

import httpx
import asyncio
import platform


class HttpError(Exception):
    pass


async def request(url: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        if r.status_code == 200:
            result = r.json()
            return result
        else:
            raise HttpError(f"Error status: {r.status_code} for {url}")


def normalize_response(response):
    result_list = list()
    # print(type(response))
    # for key, value in response.items():
    #     # print(key, value)
    #     current_date = key['date']
    # print(current_date)
    
    # return response
    current_date = None
    for rate in response.get('exchangeRate', []):
        if rate.get('currency') in ['EUR', 'USD']:
            currency = rate['currency']
            date = response['date']
            if date != current_date:
                result_list.append(date)
                current_date = date
            result_list.append(f"\n{{'{currency}': {{\n"
                                  f"  'sale': {rate.get('saleRateNB', 0)},\n"
                                  f"  'purchase': {rate.get('purchaseRateNB', 0)}\n}}}}")

    return result_list


async def main(index_day):
    res_exchange_list = list()
    d = datetime.now() - timedelta(days=index_day)
    shift = d.strftime("%d.%m.%Y")
    
    try:
        for index in range(index_day + 1):  # AAAAAAAAAAAAAAAAAAAAAAAAA
            response = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={shift}')
            res_exchange_list.append(response)
        result_r = normalize_response(res_exchange_list)
        return result_r
    except HttpError as err:
        print(err)
        return None


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    if len(sys.argv) < 2:
        sys.exit("You need enter Days.")
    get_argv = int(sys.argv[1])
    if get_argv > 10:
        sys.exit(f"Days {get_argv} more then 10.")
    result = asyncio.run(main(get_argv))
    # print(r)
    for exchange_day in result:
        print(exchange_day)
