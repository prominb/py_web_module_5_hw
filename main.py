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


# async def get_date_async(input_day):
#     await asyncio.sleep(0.5)
#     # get_date, = list(filter(lambda user: user["id"] == uid, fake_users))
#     get_date_list = [(datetime.now() - timedelta(days=index-1)) for index in range(1, input_day + 1)]
#     get_date = [get_date.strftime("%d.%m.%Y") for get_date in get_date_list]
#     print(get_date)
#     # return get_date


# def normalize_response(response):
#     result_list = list()
#     return result_list

def get_date(input_day):
    result_list = [(datetime.now() - timedelta(days=index-1)) for index in range(1, input_day + 1)]
    for index in range(len(result_list)):
        result_list[index] = result_list[index].strftime("%d.%m.%Y")
    return result_list

# async def get_date_async(input_day):
    # r = []
    # for i in range(input_day + 1):
    #     r.append(get_user_async(i))
    # return await asyncio.gather(*r)
    # cur_date, = list(lambda cur_date: cur_date, d_list)
    # return cur_date

async def main(index_day):
    res_exchange_list = list()
    dates_list = get_date(index_day)
    # print(dates_list)
    try:
        # for idx in range(index_day + 1):
        for cur_date in dates_list:
            # cur_date = await get_date_async(idx)
            response = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={cur_date}')
            res_exchange_list.append(response)
        # result_r = normalize_response(res_exchange_list)
        # return res_exchange_list
        return await asyncio.gather(*res_exchange_list)
        # return response
    except HttpError as err:
        print(err)
        return None
    # return res_exchange_list


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    if len(sys.argv) < 2:
        sys.exit("You need enter Days.")
    get_argv = int(sys.argv[1])
    if get_argv > 10:
        sys.exit(f"Days {get_argv} more then 10.")
    result = asyncio.run(main(get_argv))
    print(result)
    # for exchange_day in result:
    #     print(exchange_day)
    # get_date(get_argv)
