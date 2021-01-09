# media_player.template
media_player template for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
[![License][license-shield]](LICENSE.md)

![Project Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]

[![Community Forum][forum-shield]][forum]



Current implemented features:
* on_action
* off_action
* play_action
* stop_action
* pause_action
* next_action
* previous_action
* volume_up_action
* volume_down_action
* mute_action
* source list
* current source
* title
* artist
* album
* current volume
* set_volume action
* play_media action (not tested)
* media_content_type_template
* media_image_url_template
* media_episode_template
* media_season_template
* media_series_title_template
* media_album_artist_template

media_content_type_template can be one of the following values:
* tv_show
* music
* movie
* video

based on this value other parameters are shown ex artist is only shown when type is music

## Variables used:
set_volume:
* {volume}

play_media:
* {media_type}
* {media_id}

## Preview config:

```yaml
media_player:
  - platform: media_player_template
    media_players:
      receiver:
        friendly_name: Receiver
        current_source_template: "{{ states('input_text.selected_source') }}"
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
        inputs:
          source 1:
            service: input_boolean.turn_on
            data_template:
              entity_id: input_boolean.source_1
          source 2:
            service: input_boolean.turn_on
            data_template:
              entity_id: input_boolean.source_2
        set_volume:
          service: input_text.set_value
          data:
            entity_id: input_text.selected_volume
            value: "{{volume}}"
        album_art_template: "{{ states('input_text.album_art') }}"
        title_template: "{{ states('input_text.title') }}"
        album_template: "{{ states('input_text.album') }}"
        artist_template: "{{ states('input_text.artist') }}"
```

[commits-shield]: https://img.shields.io/github/commit-activity/m/Sennevds/media_player.template?style=for-the-badge
[commits]: https://github.com/sennevds/media_player.template/commits/master
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/t/media-player-template/203062
[license-shield]: https://img.shields.io/github/license/sennevds/media_player.template.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/maintenance/yes/2021.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/sennevds/media_player.template.svg?style=for-the-badge
[releases]: https://github.com/sennevds/media_player.template/releases
