import logging
import aiohttp
import async_timeout
from datetime import timedelta
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed
)

from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_UPDATE_INTERVAL,
    CONF_BUS_NUMBER,
    CONF_STOP,
    HORAIRE_API_URL,
    COORDINATES_BUS_API_URL
)

_LOGGER = logging.getLogger(__name__)

class StarCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass, config_entry):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} ({config_entry.unique_id})",
            config_entry=config_entry,
            update_interval=timedelta(seconds=self.update_interval_seconds),
            always_update=True
        )
        self.api_key = config_entry.data[CONF_API_KEY]
        self.bus_number = config_entry.data[CONF_BUS_NUMBER]
        self.stop = config_entry.data[CONF_STOP]
        self.direction = config_entry.data["direction_arrival_stop"]


    async def _async_update_data(self):
        _LOGGER.debug("↻ Rafraîchissement des données horaires en cours...")
        _LOGGER.debug(self)
        url_formatte = HORAIRE_API_URL.format(bus_number=self.bus_number, stop=self.stop, \
                                              direction=self.direction, api_key=self.api_key)

        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    _LOGGER.debug(f"Fetch next bus url: {url_formatte}")
                    async with session.get(url_formatte) as response:
                        if response.status != 200:
                            raise UpdateFailed(f"Erreur HTTP {response.status}")
                        data = await response.json()

                        results = data.get("results", [])

                        # Pour chaque départ, enrichir avec les coordonnées si possible
                        for result in results:
                            idbus = result.get("idbus")
                            if idbus:
                                coordinates_url = COORDINATES_BUS_API_URL.format(idbus=idbus, \
                                                                            api_key=self.api_key)
                                _LOGGER.debug(f"Fetch next bus coordinates url: {coordinates_url}")
                                async with session.get(coordinates_url) as coordinates_response:
                                    if coordinates_response.status == 200:
                                        coordinates_data = await coordinates_response.json()
                                        coords = coordinates_data.get(
                                            "results", [{}]
                                            )[0].get("coordonnees")
                                        if coords:
                                            result["coordonnees"] = coords
                            else:
                                result.pop("coordonnees", None)

                        return {"results": results}

        except Exception as err:
            raise UpdateFailed(f"Erreur lors de la récupération des données: {err}")