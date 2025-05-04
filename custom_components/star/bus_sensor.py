import re
import logging
import unicodedata
from datetime import datetime, timezone
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .coordinator import StarCoordinator

_LOGGER = logging.getLogger(__name__)

def slugify(text: str) -> str:
    """Format names"""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s]+", "_", text)

class BusSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: StarCoordinator, index: int,):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.index = index

        bus_number = coordinator.bus_number
        stop = coordinator.stop
        direction = coordinator.direction

        self._bus_number = slugify(bus_number)
        self._direction = slugify(direction)
        self._stop = slugify(stop)

        # Construire un nom lisible
        suffix = "Prochain départ" if index == 0 else "Deuxième départ"
        self._attr_name = f"{bus_number} - {stop} → {direction} - {suffix}"



    @property
    def unique_id(self):
        return f"{self._bus_number}_{self._stop}_{self._direction}_depart_{self.index + 1}"


    @property
    def name(self):
        return self._attr_name

    @property
    def state(self):

        try:
            depart_str = self.coordinator.data["results"][self.index]["depart"]
            depart_time = datetime.fromisoformat(depart_str)
            now = datetime.now(depart_time.tzinfo or timezone.utc)
            delta = (depart_time - now).total_seconds() / 60
            return max(0, round(delta))

        except Exception as e:
            _LOGGER.warning(f"Erreur dans le calcul de state : {e}")
            return None

    @property
    def unit_of_measurement(self):
        return "min"

    @property
    def available(self):
        return self.coordinator.last_update_success

    @property
    def extra_state_attributes(self):
        attributes = {
            "ligne": self.coordinator.bus_number,
            "arrêt": self.coordinator.stop,
            "direction": self.coordinator.direction,
        }
        try:
            result = self.coordinator.data["results"][self.index]
            attributes["départ_brut"] = result.get("depart")
        except (IndexError, KeyError, TypeError):
            pass

        try:
            result = self.coordinator.data["results"][self.index]
            attributes["départ_brut"] = result.get("depart")

            coords = result.get("coordonnees")
            if coords:
                attributes["latitude"] = coords.get("lat")
                attributes["longitude"] = coords.get("lon")
        except (IndexError, KeyError, TypeError):
            pass

        return attributes