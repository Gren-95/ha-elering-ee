"""Tests for the electricity price sensor."""
from datetime import timedelta
import re

from homeassistant.core import HomeAssistant
import homeassistant.util.dt as dt_util
from pytest_homeassistant_custom_component.common import MockConfigEntry
from pytest_homeassistant_custom_component.test_util.aiohttp import AiohttpClientMocker

from custom_components.elering_ee.const import DOMAIN, ELERING_API_URL


def _two_days_of_prices() -> dict:
    """An API answer with an hourly price for today and tomorrow."""
    start = dt_util.start_of_local_day(dt_util.now())
    prices = []
    for hour in range(48):
        moment = start + timedelta(hours=hour)
        prices.append({"timestamp": int(moment.timestamp()), "price": 100.0 + hour})
    return {"success": True, "data": {"ee": prices}}


async def test_price_is_fetched_through_the_shared_session(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """The sensor uses Home Assistant's shared session.

    aioclient_mock only intercepts sessions from async_get_clientsession, so a
    sensor that opened its own ClientSession would never reach the mocked
    answer and the sensor would end up unavailable.
    """
    aioclient_mock.get(re.compile(re.escape(ELERING_API_URL)), json=_two_days_of_prices())

    entry = MockConfigEntry(domain=DOMAIN, data={})
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert aioclient_mock.call_count == 1
    state = hass.states.get("sensor.electricity_price")
    assert state is not None
    assert state.state not in ("unavailable", "unknown")
    assert float(state.state) > 0
    assert len(state.attributes["prices_today"]) == 24
    assert len(state.attributes["prices_tomorrow"]) == 24
