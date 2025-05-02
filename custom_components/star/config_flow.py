"""Support for STAR API."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .api import StarApi
from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_BUS_NUMBER
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

        data_schema = {
            vol.Required(CONF_API_KEY): str,
            vol.Required(CONF_BUS_NUMBER): vol.In(options),
        }

        return self.async_show_form(
            step_id="user", 
            data_schema=data_schema
        )