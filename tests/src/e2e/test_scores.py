# from http import HTTPStatus
#
# import pytest
#
#
# @pytest.mark.asyncio
# async def test_view_progress_post_request(
#     aiohttp_session, user_settings, aiohttp_manual
# ):
#     # Отправляем черех API просмотренный фрейм
#     film_id = "dc3825a9-8668-400e-b083-97aa24081352"
#     host = f"http://127.0.0.1:8000/api/v1/score-film/{film_id}"
#     user_id = user_settings["user_id"]
#     body = {"score": 9}
#     async with aiohttp_manual.post(host, json=body) as resp:
#         assert resp.status == HTTPStatus.OK
#         api_result = await resp.json()
#
#     # assert body["viewed_frame"] in frames
#
#
# @pytest.mark.asyncio
# async def test_view_progress_get_request(
#     aiohttp_session, user_settings, aiohttp_manual
# ):
#     # Отправляем черех API просмотренный фрейм
#     film_id = "b18d7b24-f2db-4f2a-b584-55da3cad8b26"
#     host = f"http://127.0.0.1:8000/api/v1/score-film/{film_id}"
#     user_id = user_settings["user_id"]
#     body = {"score": 9}
#     # async with aiohttp_manual.post(host, json=body) as resp:
#     #     assert resp.status == HTTPStatus.OK
#
#     async with aiohttp_manual.get(host) as resp:
#         assert resp.status == HTTPStatus.OK
#         api_result = await resp.json()
#
#     assert api_result.content == []
