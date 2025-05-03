import logging
import aiohttp
from .const import (
    LINE_API_URL,
    DIRECTIONS_API_URL,
    ARRETS_API_URL
)


_LOGGER = logging.getLogger(__name__)

class StarApi():
    # Récupération des lignes pour l'étape 1
    async def _fetch_bus_lines() -> dict[str, str]:
        """Call STAR API to get all the lines."""
        _LOGGER.error("Calling _fetch_bus_lines function")
        async with aiohttp.ClientSession() as session:
            async with session.get(LINE_API_URL) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    _LOGGER.error("Lines API error %s: %s", resp.status, text)
                    return []
                data = await resp.json()
                _LOGGER.error("_fetch_bus_lines data : %s", data)
                return [
                    (item["nomcourt"], f'{item["nomcourt"]} - {item["nomlong"]}')
                    for item in data.get("results", [])
                ]

    # Récupération des directions de la ligne choisie pour l'étape 2
    async def _fetch_directions(nomcourt: str) -> list[tuple[str, str]]:
        """Call STAR API to get all direction of one line."""
        _LOGGER.debug("Fetching directions for line: %s", nomcourt)
        async with aiohttp.ClientSession() as session:
            async with session.get(DIRECTIONS_API_URL.format(ligne=nomcourt)) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    _LOGGER.error("Direction API error %s: %s", resp.status, text)
                    return []
                data = await resp.json()
                _LOGGER.debug("Directions API result: %s", data)
                return [
                    (item["id"], item["libellelong"], item["nomarretarrivee"])
                    for item in data.get("results", [])
                ]

    # Récupération des arrêts de la ligne choisie pour l'étape 3
    async def _fetch_stops(idparcours: str) -> list[str]:
        """Call STAR API to get all stops of one line."""
        _LOGGER.debug("Fetching stops for parcours: %s", idparcours)
        async with aiohttp.ClientSession() as session:
            async with session.get(ARRETS_API_URL.format(parcours=idparcours)) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    _LOGGER.error("Stops API error %s: %s", resp.status, text)
                    return []
                data = await resp.json()
                return [item["nomarret"] for item in data.get("results", [])]
