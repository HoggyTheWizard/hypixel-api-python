from src.hypxiel_api_python.utils.requests import get
from src.hypxiel_api_python.hypixel import HypixelAPI

# SUPPORT FOR NAMES NEEDS TO BE ADDED.


class HypixelGuild:
    def __init__(
            self,
            hypixel_api: HypixelAPI,
            params: dict[str: str] = {}
    ):
        self.guild = await get(hypixel_api=hypixel_api, endpoint="guild", params=params)["guild"]
        self.raw = self.guild
        self.members = HypixelGuildMembers(hypixel_guild=self.guild)
        self.ranks = self.guild["ranks"]
        self.game_gxp = self.guild["guildExpByGameType"]
        self.tag = self.guild["tag"]
        self.achievements = self.guild["achievements"]
        self.info = {
            "name": self.guild["name"],
            "description": self.guild.get("description"),
            "id": self.guild["_id"],
            "created": self.guild["created"],
        }
        self.settings = {
            "joinable": self.guild.get("joinable"),
            "publiclyListed": self.guild.get("publiclyListed"),
        }
        self.legacy = {
            "legacyRanking": self.guild.get("legacyRanking"),
            "coins": self.guild.get("coins", 0),
            "coinsEver": self.guild.get("coinsEver", 0),
        }


class HypixelGuildMembers:
    def __init__(
            self,
            hypixel_guild: HypixelGuild,
    ):
        self.members = hypixel_guild.guild["members"]

    async def raw(self) -> list:
        return self.members

    async def order_by_daily_exp(self):
        return sorted(
            [member for member in self.members],
            key=lambda member: list(member["expHistory"])[0],
            reverse=True
        )

    async def order_by_weekly_exp(self):
        return sorted(
            [member for member in self.members],
            key=lambda member: sum(list(member["expHistory"])),
            reverse=True
        )

    async def order_by_quest_participation(self):
        return sorted(
            [member for member in self.members],
            key=lambda member: member["questParticipation"],
            reverse=True
        )

    async def members_with_guild_rank(self, guild_rank: str):
        return [member for member in self.members if member["rank"] == guild_rank]
