# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.2] - 2026-10-28

### Changed
- `hacs.json` sets `country` to `EE`, since the prices are Estonian only

## [2.1.1] - 2026-10-28

### Changed
- The integration now lives in `custom_components/elering_ee/`, the standard layout, instead of the repository root. Nothing changes for installed copies: HACS installs to the same place
- Validation runs Home Assistant's hassfest instead of a hand-written check, plus a weekly scheduled run
- README: HACS install steps, and manual install from `custom_components/elering_ee`
- `codeowners` set in the manifest

## [2.1.0] - 2026-10-28

### Fixed
- Prices covered only the last ~12 hours: the API is now asked for the whole of today and tomorrow, so daily statistics, `price_rank` and tomorrow's prices are complete. The 400 errors from 2.0.3 came from an unencoded `+00:00` offset; times are now sent as UTC with a `Z` suffix
- Tomorrow's prices only count once the day is (nearly) complete, so the early first hour Nord Pool publishes no longer sets `tomorrow_valid`
- The "Price in cents" option is honoured again: c/kWh when on, EUR/kWh when off
- Home Assistant warned that a `monetary` sensor cannot use the `measurement` state class; the device class is removed
- Hours are grouped in Home Assistant's time zone rather than the host's
- A current price of exactly 0 is reported as 0 instead of unknown
- Changing options more than once set the sensor up twice ("does not generate unique IDs"): reloads now go through Home Assistant
- README and example cards used `sensor.elering_ee_electricity_price`; the entity is `sensor.electricity_price`
- The options dialog failed with a 500 error on current Home Assistant releases (the options flow assigned `config_entry`, which Home Assistant now provides)
- HACS validation: brand icons are now provided in `brand/`

### Changed
- With "Price in cents" on (the default), the sensor reports c/kWh. Turn it off to keep using the sensor in the Energy dashboard
- Requires Home Assistant 2024.11 or newer, for the options flow fix

## [2.0.4] - 2026-02-13

### Fixed
- Energy dashboard compatibility: Changed unit to EUR/kWh (was c/kWh)
- Sensor now appears in Energy dashboard price selector
- Proper conversion: EUR/MWh ÷ 1000 = EUR/kWh

### Changed
- Price display format now shows EUR/kWh for better compatibility
- Example: 125 EUR/MWh now displays as 0.125 EUR/kWh

## [2.0.3] - 2026-02-13

### Fixed
- Sensor showing "unavailable" status
- Removed invalid API URL parameters (start/end) that caused 400 errors
- Properly handle 15-minute price intervals from Elering API
- Average 15-minute intervals to provide clean hourly prices
- Fixed tomorrow date calculation for next day prices

### Changed
- Simplified API call to use endpoint without parameters
- Improved price aggregation logic for better accuracy

## [2.0.2] - 2026-02-13

### Added
- Material Design lightning bolt icons for integration branding
- Icon support for both light and dark modes
- High-resolution icon variants (@2x)
- Logo format for integration pages
- Brands repository submission files ready for official Home Assistant branding

### Documentation
- Icon structure and usage guide
- Brands repository submission instructions
- Icon design templates and suggestions

## [2.0.1] - 2026-02-13

### Fixed
- Config flow 500 error: Changed `bool` to `cv.boolean` for proper Home Assistant form validation
- Integration can now be configured through the UI without errors

## [2.0.0] - 2026-02-13

### Added
- Initial release of Elering Estonia integration
- Real-time Nord Pool spot prices from Elering API
- Automatic VAT calculation (22% Estonian VAT)
- Price display in cents/kWh or EUR/MWh
- Smart attributes:
  - `is_cheap` - Boolean indicating if current price is below average
  - `price_percent_to_average` - Price comparison to daily average
  - `price_rank` - Hour ranking (e.g., "5/24")
- Peak/off-peak statistics
- Tomorrow's prices support (available after ~13:00)
- Additional costs support for network fees
- UI-based configuration with config flow
- Database optimization (large arrays excluded from recorder)
- Complete documentation with examples
- HACS compatibility

### Features
- No API key required (uses public Elering API)
- Configurable VAT rate
- Configurable precision (0-6 decimal places)
- Hourly automatic updates
- Comprehensive error handling and logging

### Documentation
- Detailed README with installation instructions
- Example automations for common use cases
- Example Lovelace cards
- Troubleshooting guide

---

## Release Notes Template

When creating a new release, copy this template:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes

### Removed
- Removed features
```
