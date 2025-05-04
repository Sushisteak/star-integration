from .coordinator import StarCoordinator
from .bus_sensor import BusSensor


async def async_setup(hass, config):
    return True