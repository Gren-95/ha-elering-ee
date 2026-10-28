<div align="center">
  <img src="logo.png" alt="Elering Estonia Logo" width="200"/>

  # Elering Estonia Electricity Price

  [![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
  [![GitHub Release](https://img.shields.io/github/release/Gren-95/ha-elering-ee.svg)](https://github.com/Gren-95/ha-elering-ee/releases)
  [![License](https://img.shields.io/github/license/Gren-95/ha-elering-ee.svg)](LICENSE)

  A comprehensive Home Assistant integration for Estonian electricity prices using real-time data from the Elering API (Nord Pool spot prices).
</div>

<p align="center">
  <img src="docs/dashboard.png" alt="Home Assistant dashboard with the current price, today's statistics and an hour-by-hour price chart" width="800"/>
</p>

---

## Features

### Core Functionality
- ⚡ **Real-time pricing** - Current electricity price updated hourly
- 📊 **Smart pricing in cents/kWh** - Easy-to-understand pricing (configurable)
- 💶 **Automatic VAT calculation** - Estonia's 22% VAT included by default
- 💰 **Additional costs support** - Add network fees or other charges
- 🔮 **Tomorrow's prices** - Next day prices (available after 1 PM)

### Intelligent Attributes
- 🎯 **is_cheap** - Boolean indicating if current price is below daily average
- 📈 **price_percent_to_average** - How current price compares to daily average (%)
- 🏆 **price_rank** - Current price ranking (e.g., "5/24" = 5th cheapest hour)
- 📊 **Statistics** - Min, max, average, median prices for today and tomorrow
- 🌙 **Peak/off-peak averages** - Separate averages for peak (7-23) and off-peak hours

### Smart Features
- 🚫 **No API key required** - Uses public Elering API
- 🔄 **Auto-updates** - Refreshes every hour
- 💾 **Database optimized** - Large price arrays excluded from recorder
- ⚙️ **UI configuration** - Easy setup through Home Assistant UI
- 🎛️ **Configurable precision** - Choose decimal places (0-6)

## Installation

### Option 1: Manual Installation

1. Copy the `elering_ee` folder to your `config/custom_components/` directory:
   ```
   config/
   └── custom_components/
       └── elering_ee/
           ├── __init__.py
           ├── config_flow.py
           ├── const.py
           ├── manifest.json
           ├── sensor.py
           └── README.md
   ```

2. Restart Home Assistant

3. Go to **Settings** → **Devices & Services** → **Add Integration**

4. Search for "Elering Estonia" and configure:
   - **VAT rate**: 0.22 (22%, default for Estonia)
   - **Price in cents**: Yes (shows c/kWh) or No (shows EUR/kWh, which the Energy dashboard needs)
   - **Additional costs**: Any fixed costs in EUR/MWh (e.g., network fees)
   - **Precision**: Number of decimal places (default: 2)

### Option 2: YAML Configuration (Legacy)

You can still use YAML, but UI configuration is recommended:

```yaml
sensor:
  - platform: elering_ee
```

Then configure via UI as described above.

## Configuration

### Settings Explained

| Setting | Default | Description |
|---------|---------|-------------|
| **VAT** | 0.22 (22%) | Estonia's VAT rate on electricity |
| **Price in cents** | Yes | Show price as c/kWh (easier to read) vs EUR/kWh (Energy dashboard) |
| **Additional costs** | 0.0 | Add network fees or other charges (in EUR/MWh) |
| **Precision** | 2 | Decimal places to display |

### Example Configurations

**Home user with network fees:**
- VAT: 0.22
- Price in cents: Yes
- Additional costs: 35.0 (EUR/MWh network fee)
- Result: ~12.5 c/kWh (spot price + VAT + network fee)

**Business user without VAT:**
- VAT: 0.0
- Price in cents: No
- Additional costs: 0.0
- Precision: 4
- Result: Shows the spot price in EUR/kWh, ready for the Energy dashboard

## Usage

### Sensor Entity

After setup, you'll have: `sensor.electricity_price`

**State**: Current electricity price (in c/kWh or EUR/kWh based on config)

### Available Attributes

```yaml
# Price Intelligence
is_cheap: true                      # Is price below average?
price_percent_to_average: 87.3      # Current price vs daily average
price_rank: "5/24"                  # 5th cheapest hour of the day

# Statistics - Today
average: 12.45                      # Average price today
min: 8.32                          # Minimum price today
max: 18.67                         # Maximum price today
median: 11.98                      # Median price today
peak_average: 13.21                # Average during peak hours (7-23)
off_peak_average: 9.87             # Average during off-peak (23-7)

# Statistics - Tomorrow
tomorrow_valid: true               # Are tomorrow's prices available?
average_tomorrow: 11.23            # Average price tomorrow
min_tomorrow: 7.45                # Minimum price tomorrow
max_tomorrow: 16.34               # Maximum price tomorrow

# Price Arrays
prices_today:                      # Hourly prices for today
  - time: "00:00"
    price: 9.32
  - time: "01:00"
    price: 8.87
  # ... (24 hours)

prices_tomorrow:                   # Hourly prices for tomorrow
  - time: "00:00"
    price: 10.12
  # ... (24 hours, available after ~13:00)

# Configuration Info
vat_rate: 0.22
additional_costs: 35.0
unit: "c/kWh"
currency: "EUR"
last_updated: "2024-01-15T14:30:00"
```

## Automation Examples

### Notify When Electricity is Cheap

```yaml
automation:
  - alias: "Cheap Electricity Alert"
    trigger:
      - platform: state
        entity_id: sensor.electricity_price
        attribute: is_cheap
        to: true
    action:
      - service: notify.notify
        data:
          title: "⚡ Electricity is Cheap!"
          message: >
            Current price: {{ states('sensor.electricity_price') }} c/kWh
            ({{ state_attr('sensor.electricity_price', 'price_percent_to_average') }}% of average)
```

### Run Dishwasher During Cheapest Hours

```yaml
automation:
  - alias: "Run Dishwasher When Cheap"
    trigger:
      - platform: time_pattern
        hours: "*"
    condition:
      - condition: template
        value_template: >
          {{ state_attr('sensor.electricity_price', 'price_rank').split('/')[0]|int <= 5 }}
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.dishwasher
```

### Charge EV During Cheapest Night Hours

```yaml
automation:
  - alias: "Charge EV During Cheap Night Hours"
    trigger:
      - platform: time_pattern
        hours: "*"
    condition:
      - condition: time
        after: "22:00"
        before: "06:00"
      - condition: numeric_state
        entity_id: sensor.electricity_price
        below: 10  # Below 10 c/kWh
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.ev_charger
```

### Daily Price Summary Notification

```yaml
automation:
  - alias: "Daily Electricity Price Summary"
    trigger:
      - platform: time
        at: "07:00"
    action:
      - service: notify.notify
        data:
          title: "📊 Today's Electricity Prices"
          message: >
            Average: {{ state_attr('sensor.electricity_price', 'average') }} c/kWh
            Min: {{ state_attr('sensor.electricity_price', 'min') }} c/kWh
            Max: {{ state_attr('sensor.electricity_price', 'max') }} c/kWh
            Peak hours avg: {{ state_attr('sensor.electricity_price', 'peak_average') }} c/kWh
```

## Lovelace Cards

### Simple Entity Card

```yaml
type: entity
entity: sensor.electricity_price
name: Electricity Price
icon: mdi:flash
```

### Detailed Statistics Card

```yaml
type: entities
title: ⚡ Electricity Prices
entities:
  - entity: sensor.electricity_price
    name: Current Price
    icon: mdi:flash
  - type: divider
  - type: attribute
    entity: sensor.electricity_price
    attribute: is_cheap
    name: Is Cheap?
    icon: mdi:tag
  - type: attribute
    entity: sensor.electricity_price
    attribute: price_rank
    name: Price Rank
    icon: mdi:podium
  - type: divider
  - type: attribute
    entity: sensor.electricity_price
    attribute: average
    name: Average Today
    suffix: c/kWh
  - type: attribute
    entity: sensor.electricity_price
    attribute: min
    name: Min Today
    suffix: c/kWh
  - type: attribute
    entity: sensor.electricity_price
    attribute: max
    name: Max Today
    suffix: c/kWh
```

### Apex Charts Card (requires custom card)

```yaml
type: custom:apexcharts-card
header:
  title: Electricity Prices
  show: true
graph_span: 2d
span:
  start: day
series:
  - entity: sensor.electricity_price
    name: Today
    data_generator: |
      return entity.attributes.prices_today.map((item) => {
        return [new Date().setHours(item.time.split(':')[0], 0, 0, 0), item.price];
      });
  - entity: sensor.electricity_price
    name: Tomorrow
    data_generator: |
      return entity.attributes.prices_tomorrow?.map((item) => {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        return [tomorrow.setHours(item.time.split(':')[0], 0, 0, 0), item.price];
      }) || [];
```

## Technical Details

### Data Source
- **API**: Elering (Estonian TSO) - https://dashboard.elering.ee/api/nps/price
- **Data**: Nord Pool spot prices for Estonia (EE price zone)
- **Update frequency**: Every hour
- **API Key**: Not required (public API)

### Price Calculation

```
Final Price = (Spot Price × (1 + VAT)) + Additional Costs
```

Then it is converted to the configured unit:
```
Final Price (EUR/kWh) = Final Price (EUR/MWh) / 1000
Final Price (c/kWh)   = Final Price (EUR/MWh) / 10
```

Example:
- Spot price: 100 EUR/MWh
- VAT: 22% (0.22)
- Additional costs: 35 EUR/MWh
- Result: (100 × 1.22) + 35 = 157 EUR/MWh = 15.7 c/kWh

### Data Retention
Large price arrays (`prices_today`, `prices_tomorrow`, `raw_today`, `raw_tomorrow`) are excluded from the Home Assistant database to save space while remaining accessible via attributes.

## Troubleshooting

### Prices not updating
- Check Home Assistant logs for errors
- Verify internet connection
- Elering API may be temporarily unavailable

### Tomorrow's prices not available
- Tomorrow's prices are published around 13:00-14:00 CET
- Before that time, `tomorrow_valid` will be `false`

### Using the Energy dashboard
- The Energy dashboard only accepts a price in EUR/kWh: turn **Price in cents** off in the integration's options

### Incorrect prices
- Verify VAT rate (Estonia: 22%)
- Check additional costs configuration
- Ensure correct unit selection (c/kWh vs EUR/kWh)
- With EUR/kWh, use a precision of 4 or more: at 2 decimals every price rounds to whole cents

## Support & Contributing

- **Issues**: Please report bugs or feature requests on GitHub
- **Data source**: Elering API documentation
- **License**: MIT

## Credits

Data provided by Elering (Estonian TSO) via their public API.

---

**Made with ⚡ in Estonia**
