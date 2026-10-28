"""Constants for the Elering Estonia integration."""

DOMAIN = "elering_ee"

# API
ELERING_API_URL = "https://dashboard.elering.ee/api/nps/price"

# Configuration
CONF_VAT = "vat"
CONF_PRICE_IN_CENTS = "price_in_cents"
CONF_ADDITIONAL_COSTS = "additional_costs"
CONF_PRECISION = "precision"

# Defaults
DEFAULT_VAT = 0.22  # Estonia VAT is 22%
DEFAULT_PRICE_IN_CENTS = True
DEFAULT_ADDITIONAL_COSTS = 0.0
DEFAULT_PRECISION = 2

# Update intervals
SCAN_INTERVAL_MINUTES = 60
MIN_UPDATE_INTERVAL_MINUTES = 30

# Attributes that should not be recorded in the database
UNRECORDED_ATTRIBUTES = frozenset({
    "raw_today",
    "raw_tomorrow",
    "prices_today",
    "prices_tomorrow",
})
