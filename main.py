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
    # input_day = 3
    result_list = [(datetime.now() - timedelta(days=index-1)) for index in range(1, input_day + 1)]
    # print(result)
    for index in range(len(result_list)):
        # print(mymy.strftime("%d.%m.%Y"))
        result_list[index] = result_list[index].strftime("%d.%m.%Y")
    # print(result_list)
    return result_list


async def main(index_day):
    res_exchange_list = list()
    # dates_list = list()
    # d = datetime.now() - timedelta(days=int(index_day))
    # shift = d.strftime("%d.%m.%Y")
    # for index in range(1, index_day + 1):
    #     d = datetime.now() - timedelta(days=int(index - 1))
    #     dates_list.append(d.strftime("%d.%m.%Y"))
    # return dates_list
    # await get_date_async(index_day)
    # print(get_date)
    dates_list = get_date(index_day)
    try:
        # current_date = await get_date(index_day)
        for cur_date in dates_list:  # AAAAAAAAAAAAAAAAAAAAAAAAA
            # get_date = await get_date_async(index_day)
            # print(date)
            # shift = get_date.strftime("%d.%m.%Y")
            response = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={cur_date}')
            res_exchange_list.append(response)
        # result_r = normalize_response(res_exchange_list)
        return res_exchange_list
        # return await asyncio.gather(*res_exchange_list)
        # return response
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
    print(result)
    # for exchange_day in result:
    #     print(exchange_day)
    # get_date(get_argv)
