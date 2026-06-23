#File for storing wiki summary of company which updates faster than Claude
#wiki library for company summary
import wikipediaapi
import datetime
#return errors instead of raw exeptions
from fastapi import HTTPException
#import wiki object
from models import WikiPayload
import asyncio
from config import Wiki_TTL

from cache import cache_get, cache_set

#wikipedia summary for claude to to base information off of, updates for newer companies due to ai knowledge cutoff
async def fetch_wiki(company_name: str) -> WikiPayload:
    #get the key wiki:company to prevent naming conflicts
    cached = cache_get(f"wiki:{company_name}")
    if cached is not None:
        wiki_summary, wiki_source = cached
        return WikiPayload(
        summary = wiki_summary,
        fetched_at = datetime.datetime.now(),
        source = wiki_source
    )
    #user agent parameter so wikipedia knows who is making the request, not strict
    wiki = wikipediaapi.Wikipedia(user_agent='Empower/1.0', language='en')

    #async multithreading function that sends the blocking synchronous function to a seperate thread and awaits result
    page = await asyncio.get_event_loop().run_in_executor(None, lambda: wiki.page(company_name))


    #if the page exists, return the data provenance object, as well as put the information in the cache
    if page.exists():
        #set the key to be set:company to prevent naming conflicts
        cache_set(f"wiki:{company_name}", page.summary, Wiki_TTL, page.fullurl)
        return WikiPayload(
            summary= page.summary,
            fetched_at= datetime.datetime.now(),
            source= page.fullurl
        )
    #otherwise return error code 404 to the user
    raise HTTPException(status_code=404, detail="No Wikipedia page found for this company")
