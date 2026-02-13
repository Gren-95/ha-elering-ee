"""Sensor platform for Elering Estonia electricity prices."""
from __future__ import annotations

from datetime import datetime, timedelta
import logging
from typing import Any
from statistics import median

import aiohttp
import async_timeout

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import Throttle

from .const import (
    DOMAIN,
    ELERING_API_URL,
    CONF_VAT,
    CONF_PRICE_IN_CENTS,
    CONF_ADDITIONAL_COSTS,
    CONF_PRECISION,
    DEFAULT_VAT,
    DEFAULT_PRICE_IN_CENTS,
    DEFAULT_ADDITIONAL_COSTS,
    DEFAULT_PRECISION,
    SCAN_INTERVAL_MINUTES,
    MIN_UPDATE_INTERVAL_MINUTES,
    UNRECORDED_ATTRIBUTES,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=SCAN_INTERVAL_MINUTES)
MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=MIN_UPDATE_INTERVAL_MINUTES)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform from a config entry."""
    async_add_entities([EstonianElectricityPriceSensor(entry)], True)


class EstonianElectricityPriceSensor(SensorEntity):
    """Representation of Estonian electricity price sensor."""

    _attr_has_entity_name = True
    _attr_name = "Electricity Price"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:flash"
    _unrecorded_attributes = UNRECORDED_ATTRIBUTES

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_electricity_price"

        # Get configuration with fallback to defaults
        self._vat = self._get_config(CONF_VAT, DEFAULT_VAT)
        self._price_in_cents = self._get_config(CONF_PRICE_IN_CENTS, DEFAULT_PRICE_IN_CENTS)
        self._additional_costs = self._get_config(CONF_ADDITIONAL_COSTS, DEFAULT_ADDITIONAL_COSTS)
        self._precision = self._get_config(CONF_PRECISION, DEFAULT_PRECISION)

        # Set unit based on configuration
        if self._price_in_cents:
            self._attr_native_unit_of_measurement = "c/kWh"
        else:
            self._attr_native_unit_of_measurement = "€/MWh"

        # State variables
        self._state = None
        self._attributes = {}
        self._available = True
        self._raw_today = []
        self._raw_tomorrow = []

    def _get_config(self, key: str, default: Any) -> Any:
        """Get configuration value from options or data."""
        if self._entry.options:
            return self._entry.options.get(key, default)
        return self._entry.data.get(key, default)

    def _convert_price(self, price_eur_mwh: float) -> float:
        """Convert price from EUR/MWh to configured unit with VAT and additional costs."""
        # Add VAT
        price_with_vat = price_eur_mwh * (1 + self._vat)

        # Add additional costs (assumed to be in EUR/MWh)
        price_total = price_with_vat + self._additional_costs

        # Convert to cents/kWh if configured
        if self._price_in_cents:
            # EUR/MWh to cents/kWh: divide by 10
            price_total = price_total / 10

        return round(price_total, self._precision)

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self._state

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return self._attributes

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    # Get data for yesterday, today and tomorrow
                    current_time = datetime.now()
                    yesterday = current_time - timedelta(days=1)
                    tomorrow = current_time + timedelta(days=1)

                    start_date = yesterday.strftime("%Y-%m-%d")
                    end_date = tomorrow.strftime("%Y-%m-%d")

                    url = f"{ELERING_API_URL}?start={start_date}&end={end_date}"

                    async with session.get(url) as response:
                        if response.status != 200:
                            _LOGGER.error(
                                "Error fetching electricity price: HTTP %s", response.status
                            )
                            self._available = False
                            return

                        data = await response.json()

                        if not data or "data" not in data or "ee" not in data["data"]:
                            _LOGGER.error("Invalid data structure received from API")
                            self._available = False
                            return

                        ee_prices = data["data"]["ee"]

                        if not ee_prices:
                            _LOGGER.error("No price data available for Estonia")
                            self._available = False
                            return

                        # Process prices
                        current_price_raw = None
                        prices_today = []
                        prices_tomorrow = []
                        self._raw_today = []
                        self._raw_tomorrow = []

                        for price_entry in ee_prices:
                            timestamp = datetime.fromtimestamp(price_entry["timestamp"])
                            price_raw = price_entry["price"]
                            price_converted = self._convert_price(price_raw)

                            # Current hour price
                            if (timestamp.date() == current_time.date() and
                                timestamp.hour == current_time.hour):
                                current_price_raw = price_raw

                            # Today's prices
                            if timestamp.date() == current_time.date():
                                self._raw_today.append(price_raw)
                                prices_today.append({
                                    "time": timestamp.strftime("%H:%M"),
                                    "price": price_converted,
                                })
                            # Tomorrow's prices
                            elif timestamp.date() == tomorrow.date():
                                self._raw_tomorrow.append(price_raw)
                                prices_tomorrow.append({
                                    "time": timestamp.strftime("%H:%M"),
                                    "price": price_converted,
                                })

                        # Set current price
                        if current_price_raw is None and ee_prices:
                            current_price_raw = ee_prices[-1]["price"]
                            _LOGGER.warning("Using latest available price as fallback")

                        self._state = self._convert_price(current_price_raw) if current_price_raw else None
                        self._available = True

                        # Calculate statistics
                        self._attributes = self._calculate_attributes(
                            prices_today,
                            prices_tomorrow,
                            current_time,
                        )

        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching electricity price: %s", err)
            self._available = False
        except Exception as err:
            _LOGGER.error("Unexpected error fetching electricity price: %s", err)
            self._available = False

    def _calculate_attributes(
        self,
        prices_today: list[dict],
        prices_tomorrow: list[dict],
        current_time: datetime,
    ) -> dict[str, Any]:
        """Calculate sensor attributes."""
        attributes = {
            "last_updated": current_time.isoformat(),
            "currency": "EUR",
            "unit": self._attr_native_unit_of_measurement,
            "vat_rate": self._vat,
            "additional_costs": self._additional_costs,
            "raw_today": self._raw_today,
            "raw_tomorrow": self._raw_tomorrow,
        }

        # Today's prices
        if prices_today:
            attributes["prices_today"] = prices_today
            today_values = [p["price"] for p in prices_today]

            avg_today = sum(today_values) / len(today_values)
            min_today = min(today_values)
            max_today = max(today_values)
            median_today = median(today_values)

            attributes["average"] = round(avg_today, self._precision)
            attributes["min"] = round(min_today, self._precision)
            attributes["max"] = round(max_today, self._precision)
            attributes["median"] = round(median_today, self._precision)

            # Current price intelligence
            if self._state is not None:
                # Is current price cheap? (below average)
                attributes["is_cheap"] = self._state < avg_today

                # Price percentage relative to average
                if avg_today > 0:
                    price_ratio = (self._state / avg_today) * 100
                    attributes["price_percent_to_average"] = round(price_ratio, 1)

                # Rank current price
                sorted_prices = sorted(today_values)
                rank = sorted_prices.index(self._state) + 1 if self._state in sorted_prices else None
                if rank:
                    attributes["price_rank"] = f"{rank}/{len(sorted_prices)}"

            # Peak/off-peak (simplified: peak 7-23, off-peak 23-7)
            peak_hours = [p for p in prices_today if 7 <= int(p["time"].split(":")[0]) < 23]
            off_peak_hours = [p for p in prices_today if int(p["time"].split(":")[0]) < 7 or int(p["time"].split(":")[0]) >= 23]

            if peak_hours:
                peak_values = [p["price"] for p in peak_hours]
                attributes["peak_average"] = round(sum(peak_values) / len(peak_values), self._precision)

            if off_peak_hours:
                off_peak_values = [p["price"] for p in off_peak_hours]
                attributes["off_peak_average"] = round(sum(off_peak_values) / len(off_peak_values), self._precision)

        # Tomorrow's prices
        if prices_tomorrow:
            attributes["prices_tomorrow"] = prices_tomorrow
            tomorrow_values = [p["price"] for p in prices_tomorrow]
            attributes["tomorrow_valid"] = True
            attributes["min_tomorrow"] = round(min(tomorrow_values), self._precision)
            attributes["max_tomorrow"] = round(max(tomorrow_values), self._precision)
            attributes["average_tomorrow"] = round(sum(tomorrow_values) / len(tomorrow_values), self._precision)
        else:
            attributes["tomorrow_valid"] = False

        return attributes
