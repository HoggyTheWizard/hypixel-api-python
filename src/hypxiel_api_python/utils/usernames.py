from aiohttp import ClientSession
from src.hypxiel_api_python.hypixel import HypixelAPI
from datetime import datetime


# As of now the `users` cache isn't purged - this will need to be handled.
async def username_to_uuid(hypixel_api: HypixelAPI, username: str, uuid: str) -> str or None:
    """Converts a Minecraft username to a UUID"""
    """https://mojang-api-docs.netlify.app/no-auth/username-to-uuid-get.html"""
    if uuid:
        return uuid

    elif not uuid and not username:
        raise ValueError("You must provide a username or UUID")

    elif username in hypixel_api.users:
        return hypixel_api.users[username]["uuid"]

    async with ClientSession() as session:
        async with session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}") as request:

            if request.status == 200:
                hypixel_api.users[username] = {
                    "username": username,
                    "uuid": request.json()["id"],
                    "timestamp": int(datetime.now().timestamp())
                }
                return request.json()["id"]

            elif request.status in [204, 400]:
                return None

            elif request.status == 405:
                raise PermissionError("Failed to convert username -> uuid due to a lack of permissions.")

            elif request.status == 429:
                raise ConnectionError("You were ratelimited while converting a username -> uuid.")

            else:
                raise Exception("An unknown error occurred while converting a username -> uuid.")
