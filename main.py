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


async def main(index_day):
    # if int(index_day) > 10:
        # raise ValueError("Days less 10.")
        # print(f"Days {index_day} more then 10")
        # sys.exit(f"Days {index_day} more then 10")
    d = datetime.now() - timedelta(days=index_day)
    shift = d.strftime("%d.%m.%Y")
    try:
        response = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={shift}')
        return response
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
    r = asyncio.run(main(get_argv))
    print(r)
