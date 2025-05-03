"""Support for STAR API."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .api import StarApi
from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
    CONF_BUS_NUMBER,
    CONF_DIRECTION,
    CONF_STOP
)
_LOGGER = logging.getLogger(__name__)


class StarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example config flow."""
    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Get the API token and line number."""

        errors = {}

        # Get all bus lines
        raw_lines = await StarApi._fetch_bus_lines()

        if not raw_lines:
            errors["bus_number"] = "no_line_found"

        options = {code: f"{name}" for code, name in raw_lines}

        # Go to step direction
        if user_input is not None:
            self._config_flow_data = user_input
            return await self.async_step_direction()

        data_schema = vol.Schema({
                vol.Required(CONF_API_KEY): str,
                vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): int,
                vol.Required(CONF_BUS_NUMBER): vol.In(options),
            })

        return self.async_show_form(
            step_id="user", 
            data_schema=data_schema,
            errors=errors
        )
    
    # Etape 2 - Direction de la ligne choisie
    async def async_step_direction(self, user_input=None):
        """Get the direction of the line."""

        errors = {}

        bus_number = self._config_flow_data[CONF_BUS_NUMBER]
        _LOGGER.debug("Bus selected in previous step: %s", bus_number)
        directions = await StarApi._fetch_directions(bus_number)
        
        if not directions:
            errors["direction"] = "no_direction_found"

        _LOGGER.debug("All directions retrieve from _fetch_directions : %s", directions)

        # Crée les dictionnaires nécessaires
        direction_options = {}
        direction_destination = {}
        for direction_id, label, arrival in directions:
            direction_options[direction_id] = label
            direction_destination[direction_id] = arrival

        # Go to step stop
        if user_input is not None:
            _LOGGER.debug("User selected direction: %s", user_input)
            direction_id = user_input[CONF_DIRECTION]

            self._config_flow_data.update({
                CONF_DIRECTION: direction_id,
                "direction_label": direction_options[direction_id],
                "direction_arrival_stop": direction_destination[direction_id],
            })
            return await self.async_step_stop()
        
        data_schema = vol.Schema({
                vol.Required(CONF_DIRECTION): vol.In(direction_options),
            })
        
        return self.async_show_form(
            step_id="direction",
            data_schema=data_schema,
            errors=errors
        )
    
    # Etape 3 - Selection arret
    async def async_step_stop(self, user_input=None):
        """Get the stop of the line to monitor."""
        _LOGGER.debug("in async_step_stop function")
        
        errors = {}

        line_stops = await StarApi._fetch_stops(self._config_flow_data[CONF_DIRECTION])

        if not line_stops:
            errors["stop"] = "no_stop_found"
        
        _LOGGER.debug("All stops fetched : %s", line_stops)

        stop_options = {stop: stop for stop in line_stops}

        if user_input is not None:
            _LOGGER.debug("Stop selected : %s", user_input[CONF_STOP])
            self._config_flow_data.update({
                CONF_STOP: user_input[CONF_STOP]
            })
            title = f"{self._config_flow_data[CONF_BUS_NUMBER]} - {self._config_flow_data[CONF_STOP]} → \
                {self._config_flow_data['direction_arrival_stop']}"
            return self.async_create_entry(title=title, data=self._config_flow_data)

        data_schema = vol.Schema({
            vol.Required(CONF_STOP): vol.In(stop_options),
        })

        return self.async_show_form(
            step_id="stop",
            data_schema=data_schema,
            errors=errors
        )
        