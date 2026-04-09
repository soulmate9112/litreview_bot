# get_openalex_ids.py
import aiohttp
import asyncio
from orcids_list import ORCIDS


async def main():
    openalex_ids = []

    async with aiohttp.ClientSession() as session:
        for orcid in ORCIDS:
            async with session.get(
                f"https://api.openalex.org/authors/https://orcid.org/{orcid}"
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    author_id = data.get("id", "").split("/")[-1]
                    openalex_ids.append(author_id)

    with open("openalex_ids.py", "w") as f:
        f.write(f"OPENALEX_IDS = {openalex_ids}\n")


asyncio.run(main())
