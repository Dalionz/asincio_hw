import asyncio
import itertools
import aiohttp
import validators
from models import engine, Session, Base, SwapiPeople
from more_itertools import chunked

MAX_CHUNK =10

async def get_people(people_id):
    session = aiohttp.ClientSession()
    response = await session.get(f"https://swapi.dev/api/people/{people_id}")
    json_data = await response.json()
    await session.close()
    print(json_data)
    return json_data


async def link_to_data(link, is_film: str):
    session = aiohttp.ClientSession()
    response = await session.get(link)
    json_data = await response.json()
    await session.close()
    if is_film == 'films':
        return json_data['title']
    else:
        return json_data['name']
    print(json_data['title'])
    print(json_data['name'])


async def data_normalization(person_json):
    prepared_data = {}
    for key, value in dict(itertools.islice(person_json.items(), 12)).items():
        if key == 'detail':
            continue
        if type(value) is list:
            tmp_list = []
            for i in value:
                if validators.url(i):
                    data = await link_to_data(i, is_film=key)
                tmp_list.append(data)
            value = ', '.join(tmp_list)
        elif validators.url(value):
            value = await link_to_data(value, is_film=key)
        prepared_data[key] = value
    return prepared_data


async def paste_to_db(json_data):
    async with Session() as session:
        orm_objects = [SwapiPeople(**json_data)]
        session.add_all(orm_objects)
        await session.commit()


async def main():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

    for chunk in chunked(range(1, 100), MAX_CHUNK):
        for person_id in chunk:
            person = await get_people(person_id)
            prepared_data = await data_normalization(person)
            asyncio.create_task(paste_to_db(prepared_data))
            tasks = asyncio.all_tasks() - {asyncio.current_task(),}
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
