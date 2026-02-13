# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
