import json
from typing import Type
from aiohttp import web
from schema import CreateAdvert, UpdateAdvert
from pydantic import ValidationError

from models import engine, Advert, Base, Session
from sqlalchemy.exc import IntegrityError

app = web.Application()


async def orm_context(app: web.Application):
    print('START')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Drop all data in db
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print('WORK END')


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request['session'] = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


async def get_advert(advert_id: int, session: Session):
    advert = await session.get(Advert, advert_id)
    if advert is None:
        raise web.HTTPNotFound(
            content_type='application/json',
            text=json.dumps({'error': 'Advert not found, try again ^_^'})
        )
    return advert


class HttpError(web.HTTPError):
    status_code = 400


def validate(schema: Type[CreateAdvert] | Type[UpdateAdvert], json_data: dict):
    try:
        model = schema(**json_data)
        validate_data = model.model_dump(exclude_none=True)
    except ValidationError as er:
        raise HttpError(
            content_type='application/json',
            text=json.dumps(er.errors()),
        )
    return validate_data


class AdvertView(web.View):

    @property
    def session(self) -> Session:
        return self.request['session']

    @property
    def advert_id(self) -> int:
        return int(self.request.match_info['id'])

    async def post(self):
        json_data = await self.request.json()
        json_data = validate(CreateAdvert, json_data)  # validate json here
        advert = Advert(**json_data)
        try:
            self.session.add(advert)
            await self.session.commit()
        except IntegrityError:
            raise web.HTTPConflict(
                content_type='application/json',
                text=json.dumps({'error': 'Advert title not unique. Try another title'})
            )
        return web.json_response({'Success created id': advert.id})

    async def get(self):
        advert = await get_advert(self.advert_id, self.session)
        return web.json_response({
            'Advert status': 'OK',
            'title': advert.title,
            'description': advert.description,
            'owner': advert.owner,
            'creation_date': advert.creation_date.isoformat(),
        })

    async def delete(self):
        advert = await get_advert(self.advert_id, self.session)
        await self.session.delete(advert)
        await self.session.commit()
        return web.json_response({'Success deleted id': advert.id})

    async def patch(self):
        json_data = await self.request.json()
        json_data = validate(UpdateAdvert, json_data)  # validate json here
        advert = await get_advert(self.advert_id, self.session)

        for field, value in json_data.items():
            setattr(advert, field, value)

        try:
            self.session.add(advert)
            await self.session.commit()
        except IntegrityError:
            raise web.HTTPConflict(
                content_type='application/json',
                text=json.dumps({'error': 'Advert title not unique. Try another title'})
            )

        return web.json_response({'Success modified id': advert.id})


app.add_routes([
    web.post('/advert', AdvertView),
    web.get('/advert/{id:\d+}', AdvertView),
    web.delete('/advert/{id:\d+}', AdvertView),
    web.patch('/advert/{id:\d+}', AdvertView),
])

web.run_app(app, port=5000)
