# Examples

Automations and dashboard cards for the Elering Estonia integration. They assume the
default entity, `sensor.electricity_price`, with **Price in cents** on, so thresholds are
in c/kWh.

More of them, as YAML files you can copy from, are in [`examples/`](examples/).

## Automations

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
          title: "Electricity is cheap"
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
          title: "Today's electricity prices"
          message: >
            Average: {{ state_attr('sensor.electricity_price', 'average') }} c/kWh
            Min: {{ state_attr('sensor.electricity_price', 'min') }} c/kWh
            Max: {{ state_attr('sensor.electricity_price', 'max') }} c/kWh
            Peak hours avg: {{ state_attr('sensor.electricity_price', 'peak_average') }} c/kWh
```

## Dashboard cards

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
title: Electricity prices
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
