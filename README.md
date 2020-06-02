# media_player.template
media_player template for Home Assistant

Current implemented features:
* on_action
* off_action
* play_action
* pause_action
* next_action
* previous_action
* volume_up_action
* volume_down_action
* mute_action

Preview config:

```yaml
media_player:
  - platform: template
    media_players:
      receiver:
        friendly_name: Receiver
        value_template: >
          {% if is_state("input_boolean.receiver_on", "on") -%}
            on
          {%- else -%}
            off
          {%- endif %}
        turn_on:
          service: switch.turn_on
          data_template:
            entity_id: switch.receiver_on
        turn_off:
          service: switch.turn_on
          data_template:
            entity_id: switch.receiver_off
        volume_up:
          service: switch.turn_on
          data_template:
            entity_id: switch.volume_up
        volume_down:
          service: switch.turn_on
          data_template:
            entity_id: switch.vol
```