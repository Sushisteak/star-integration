from .const import DOMAIN
from .coordinator import StarCoordinator
from .bus_sensor import BusSensor

async def async_setup_entry(hass, config_entry, async_add_entities):

    coordinator = StarCoordinator(hass, config_entry)

    await coordinator.async_config_entry_first_refresh()

    entities = [
        BusSensor(coordinator, index=0),
        BusSensor(coordinator, index=1),
    ]
    async_add_entities(entities)
