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
        _LOGGER.debug("Calling _fetch_bus_lines function")
        async with aiohttp.ClientSession() as session:
            async with session.get(LINE_API_URL) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    _LOGGER.error("Error retrieving bus lines : %s - %s", resp.status, text)
                    return []
                data = await resp.json()
                _LOGGER.debug("Lines retreived : %s", data)
                return [
                    (item["nomcourt"], f'{item["nomcourt"]} - {item["nomlong"]}')
                    for item in data.get("results", [])
                ]

    # Récupération des directions de la ligne choisie pour l'étape 2
    async def _fetch_directions(nomcourt: str) -> list[tuple[str, str]]:
        """Call STAR API to get all direction of one line."""
        _LOGGER.debug("Calling _fetch_directions function")
        async with aiohttp.ClientSession() as session:
            async with session.get(DIRECTIONS_API_URL.format(ligne=nomcourt)) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    _LOGGER.error("Error retrieving directions for line %s : %s - %s", nomcourt, resp.status, text)
                    return []
                data = await resp.json()
                _LOGGER.debug("Directions for line %s retrevied : %s", nomcourt, data)
                return [
                    (item["id"], item["libellelong"], item["nomarretarrivee"])
                    for item in data.get("results", [])
                ]

    # Récupération des arrêts de la ligne choisie pour l'étape 3
    async def _fetch_stops(idparcours: str) -> list[str]:
        """Call STAR API to get all stops of one line."""
        _LOGGER.debug("Calling _fetch_stops function")
        async with aiohttp.ClientSession() as session:
            async with session.get(ARRETS_API_URL.format(parcours=idparcours)) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    _LOGGER.error("Error retrieving stops for parcours %s : %s - %s", idparcours, resp.status, text)
                    return []
                data = await resp.json()
                _LOGGER.debug("Stops for parcours %s retrevied : %s", idparcours, data)
                return [item["nomarret"] for item in data.get("results", [])]
