# functions:
# 1) The python script performes a request (every day in the morning) using the aiohttp module to the openalex api and gathers all the information in some form (json object - request_result.json()).
# The parameter url in the session.get() is an api url which contains all the filters embedded.

# 1. The first filter is by author. I suggest getting all the ORCIDs of the relevant authors, and extract the
# works based on the year filter (2026-) and based on the presence of the corresponding doi in the database.
# After I have extracted the results I should extract into a list a dictionary with the following keys - "doi","title" "authors","publication_year","abstract". After that i should store in the database only those results, which are not present in
# !!current database!! (filtering by doi). Next I should send 10-20 results to the user via Telegram bot !!which!! are not present in the !!bot_database!!

# 2. The second filter is based on the keywords:
# "Check the keywords and check if the doi is not present in the database. If its not, append the article metadata.


# 2) THe bot then sends a message containing this information to all the users


# 2) filter according to the keywords (entry fields)

###### The following filters are accessible: ######

# authorships.author.id         - Author's OpenAlex ID
# authorships.institutions.id   - Institution's OpenAlex ID
# primary_location.source.id    - Journal/source ID
# topics.id                     - Topic ID
# publication_year              - Year (integer)
# cited_by_count                - Citations (integer)
# is_oa                         - Open access (boolean)
# type                          - article, book, dataset, etc.
# has_fulltext                  - Has searchable fulltext (boolean)

### Common patterns
# 1) Searching by author
#
# # Step 1: Find author
# /authors?search=Heather+Piwowar
# # Step 2: Get works
# /works?filter=authorships.author.id:A5023888391

# header = ["id", "doi", "publication_year", "title"]
# results = results.json()["results"]
# for item in results:
# ...
#

####


import asyncio
import aiohttp
import logging
import sys
from dotenv import load_dotenv
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from openalex_ids import OPENALEX_IDS
from inverted_abstract_conversion import convert_inverted_abstract


load_dotenv()  # Load the environment variables

# # env variable - bot token is obtained from BOTFATHER #
# TOKEN = getenv("BOT_TOKEN")
# bot = Bot(token = TOKEN)

# dp = Dispatcher()


# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     await message.answer(
#         f"Hello. This is your litreview bot. I will send you a selection of the related articles on a daily basis"
#     )

# @dp.sendmessagepublication_year>0

extracted_articles = []
article_metadata = {}


async def main():
    async with aiohttp.ClientSession() as session:
        for OPENALEX_ID in OPENALEX_IDS:
            async with session.get(
                "https://api.openalex.org/works",
                params={
                    "filter": f"authorships.author.id:{OPENALEX_ID},publication_year:2026",
                    "per-page": 200,
                },
            ) as resp:
                if resp.status == 200:
                    results = await resp.json()
                    results = results["results"]
                    for item in results:
                        article_metadata["doi"] = item["doi"]
                        article_metadata["title"] = item["title"]
                        article_metadata["publication_year"] = item["publication_year"]
                        # Obtaining authors metadata #
                        authorship_objs = item["authorships"]
                        author_names = []
                        for authorhip_obj in authorship_objs:
                            author_name = authorhip_obj["author"]["display_name"]
                            author_names.append(author_name)
                        article_metadata["authors"] = " ".join(author_names)
                        article_metadata["abstract"] = convert_inverted_abstract(
                            item["abstract_inverted_index"]
                        )
                        extracted_articles.append(
                            article_metadata
                        )  # extracted_articles contains dictionaries with the article metadata


asyncio.run(main())


# async with session.get('https://')

# response = requests.get(url)


# if response.status_code == 200:
#     print("Excellent")


# all_references = {}
