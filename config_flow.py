"""Config flow for Elering Estonia integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_VAT,
    CONF_PRICE_IN_CENTS,
    CONF_ADDITIONAL_COSTS,
    CONF_PRECISION,
    DEFAULT_VAT,
    DEFAULT_PRICE_IN_CENTS,
    DEFAULT_ADDITIONAL_COSTS,
    DEFAULT_PRECISION,
)

_LOGGER = logging.getLogger(__name__)


class EleringEstoniaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Elering Estonia."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            await self.async_set_unique_id("elering_ee_price")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="Elering Estonia Electricity Price",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_VAT,
                        default=DEFAULT_VAT,
                    ): vol.All(vol.Coerce(float), vol.Range(min=0, max=1)),
                    vol.Optional(
                        CONF_PRICE_IN_CENTS,
                        default=DEFAULT_PRICE_IN_CENTS,
                    ): bool,
                    vol.Optional(
                        CONF_ADDITIONAL_COSTS,
                        default=DEFAULT_ADDITIONAL_COSTS,
                    ): vol.Coerce(float),
                    vol.Optional(
                        CONF_PRECISION,
                        default=DEFAULT_PRECISION,
                    ): vol.All(vol.Coerce(int), vol.Range(min=0, max=6)),
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> EleringEstoniaOptionsFlow:
        """Get the options flow for this handler."""
        return EleringEstoniaOptionsFlow(config_entry)


class EleringEstoniaOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Elering Estonia."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_VAT,
                        default=self.config_entry.options.get(
                            CONF_VAT,
                            self.config_entry.data.get(CONF_VAT, DEFAULT_VAT),
                        ),
                    ): vol.All(vol.Coerce(float), vol.Range(min=0, max=1)),
                    vol.Optional(
                        CONF_PRICE_IN_CENTS,
                        default=self.config_entry.options.get(
                            CONF_PRICE_IN_CENTS,
                            self.config_entry.data.get(
                                CONF_PRICE_IN_CENTS, DEFAULT_PRICE_IN_CENTS
                            ),
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_ADDITIONAL_COSTS,
                        default=self.config_entry.options.get(
                            CONF_ADDITIONAL_COSTS,
                            self.config_entry.data.get(
                                CONF_ADDITIONAL_COSTS, DEFAULT_ADDITIONAL_COSTS
                            ),
                        ),
                    ): vol.Coerce(float),
                    vol.Optional(
                        CONF_PRECISION,
                        default=self.config_entry.options.get(
                            CONF_PRECISION,
                            self.config_entry.data.get(CONF_PRECISION, DEFAULT_PRECISION),
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=0, max=6)),
                }
            ),
        )
