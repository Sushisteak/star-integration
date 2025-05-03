"""Support for STAR API."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .api import StarApi
from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_BUS_NUMBER,
    CONF_DIRECTION
)
_LOGGER = logging.getLogger(__name__)


class StarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example config flow."""
    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Get the API token and line number."""

        # Get all bus lines
        raw_lines = await StarApi._fetch_bus_lines()
        options = {code: f"{name}" for code, name in raw_lines}

        # Go to step direction
        if user_input is not None:
            self._first_step_data = user_input
            return await self.async_step_direction()

        data_schema = vol.Schema({
                vol.Required(CONF_API_KEY): str,
                vol.Required(CONF_BUS_NUMBER): vol.In(options),
            })

        return self.async_show_form(
            step_id="user", 
            data_schema=data_schema
        )
    
    # Etape 2 - Direction de la ligne choisie
    async def async_step_direction(self, user_input=None):
        """Get the direction of the line."""

        bus_number = self._first_step_data[CONF_BUS_NUMBER]
        _LOGGER.debug("Bus selected in previous step: %s", bus_number)
        directions = await StarApi._fetch_directions(bus_number)
        _LOGGER.debug("All directions retrieve from _fetch_directions : %s", directions)

        # Crée les dictionnaires nécessaires
        direction_options = {}
        direction_arrivals = {}
        for direction_id, label, arrival in directions:
            direction_options[direction_id] = label
            direction_arrivals[direction_id] = arrival

        data_schema = vol.Schema({
                vol.Required(CONF_DIRECTION): vol.In(direction_options),
            })
        
        return self.async_show_form(
            step_id="direction",
            data_schema=data_schema
        )