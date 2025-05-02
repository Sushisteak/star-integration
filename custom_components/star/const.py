DOMAIN = "star"

# STEP USER
CONF_API_KEY = "api_key"
CONF_UPDATE_INTERVAL = "update_interval"

LINE_API_URL = "https://data.explore.star.fr/api/explore/v2.1/catalog/datasets/tco-bus-topologie-li\
    gnes-td/records?select=nomcourt%2Cnomlong&where=nomfamillecommerciale%3D%27CHRONOSTAR%27%20OR%2\
        0%27Urbaine%27%20OR%20%27Inter-quartiers%27%20OR%20%27M%C3%A9tropolitaine%27&order_by=nomco\
            urt&limit=100&offset=0&timezone=Europe%2FParis&include_links=false&include_app_metas=fa\
                lse"
DIRECTIONS_API_URL = "https://data.explore.star.fr/api/explore/v2.1/catalog/datasets/tco-bus-topolo\
    gie-parcours-td/records?select=nomcourtligne%2C%20id%2C%20nomarretarrivee%2C%20libellelong%2C%2\
        0type&where=nomcourtligne%3D%27{ligne}%27&limit=100&offset=0&timezone=UTC&include_links=fal\
            se&include_app_metas=false"
ARRETS_API_URL = "https://data.explore.star.fr/api/explore/v2.1/catalog/datasets/tco-bus-topologie-\
    dessertes-td/records?select=nomcourtligne%2C%20nomarret%2C%20idparcours&where=idparcours%3D%27{\
        parcours}%27&order_by=ordre&limit=100&offset=0&timezone=UTC&include_links=false&include_app\
            _metas=false"