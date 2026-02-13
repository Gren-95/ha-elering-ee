# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
