import asyncio
import aiohttp

URL = "http://127.0.0.1:5000/advert"


async def main():
    async with aiohttp.ClientSession() as session:
        print('Add advert 1')
        post_1 = await session.post(URL,
                                    json={
                                        'title': 'title 1',
                                        'description': 'description 1',
                                        'owner': 'owner 1',
                                    },
                                    )
        print('Add advert 2')
        post_2 = await session.post(URL,
                                    json={
                                        'title': 'title 2',
                                        'description': 'description 2',
                                        'owner': 'owner 2',
                                    },
                                    )
        print('Add advert 3')
        post_3 = await session.post(URL,
                                    json={
                                        'title': 'title 3',
                                        'description': 'description 3',
                                        'owner': 'owner 3',
                                    },
                                    )
        print(post_1.status, await post_1.json())
        print(post_2.status, await post_2.json())
        print(post_3.status, await post_3.json())

        print('Path advert 1')
        path_1 = await session.patch(URL + '/1',
                                     json={
                                         'title': 'Superhero',
                                         # 'description': 'Anytime powerful game',
                                     },
                                     )
        print(path_1.status, await path_1.json())

        print('Path advert 3')
        path_1 = await session.patch(URL + '/3',
                                     json={
                                         'title': 'Superhero',
                                         'description': 'Anytime powerful game',
                                         'owner': 'owner 3',
                                     },
                                     )
        print(path_1.status, await path_1.json())

        print('Get advert 1')
        get_1 = await session.get(URL + '/1')
        print(get_1.status, await get_1.json())

        print('Delete advert 2')
        del_1 = await session.delete(URL + '/2')
        print(del_1.status, await del_1.json())


print('Script START')
asyncio.run(main())
print('Script END')
