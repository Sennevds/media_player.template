# media_player.template
media_player template for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![License][license-shield]](LICENSE.md)

![Project Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]

[![Community Forum][forum-shield]][forum]

## Configuration

This media player has to be configured at your configuration.yaml file.
YAML keys surrounded by brackets "[]" have to be replaced.

There are two ways to configure the media player sources which can be selected.
* Using inputs which enables you to define scripts for each input (e.g. Switch TV to input "HDMI1", turn on bluray player, etc.)
* Using a default sources list and a single action to handle the source selection (for example when the template media player is used to combine differend extisting media players in HA)


```yaml
media_players:
  - platform: media_player_template
    media_players:
      [media_player_entity_id]:
        # static configuration
        unique_id: # a UUID to enable HA UI to configure the entity and enable voice assistant UI.
        friendly_name: "My media player" # This is the displayed entity name
        device_class: receiver
        
        # Templates
        availability_template: "" # Availability information
        media_content_type_template: "" # Content type of playing media (valid template results: music, movie, video, tv_show)
        title_template: "" # Title of playing media
        artist_template: "" # Artist of playing media
        album_template: "" # Album name of playing media
        album_art_template: "" # Album art of playing media
        media_image_url_template: "" # Media image URL
        media_episode_template: "" # Episode title of playing media
        media_season_template: "" # Season title of playing media
        media_series_title_template: "" # Series title of playing media
        media_album_artist_template: "" # Album artist of playing media
        current_volume_template: "" # Current playback position
        current_is_muted_template: "" # Boolean value if player is muted or not
        current_source_template: "" # Currently selected source
        source_list_template: "" # Source list (will enable select_source action and overrides inputs configuration)
        sound_modes: "" # List of available sound modes
        current_sound_mode_template: "" # Current sound mode
        current_position_template: "" # Current playback position
        media_duration_template: "" # Media duration
        
        # Inputs (only if you are not using source_list_template)
        inputs:
          [source_name_1]: # Script to be executed in case of selecting it
          [source_name_2]: # Script to be executed in case of selecting it
          [Source_name_N]: # Script to be executed in case of selecting it

        # Actions - all of the following configurations are scripts
        turn_on: # Turn on the player
        turn_off: # Turn off the player
        play: # Start playback
        pause: # Pause playback
        stop: # Stop playback
        previous: # Jump to previous track
        next: # Jump to next track
        seek: # Seek to playback position (Variable: position)
        play_media: # Play a media url (Variables: media_type, media_id)
        volume_down: # Decrease volume
        volume_up: # Increase volume
        set_volume: # Set volume to (Variable: volume)
        mute: # Mute or unmute the player (Variable: is_muted)
        select_source: # Select a source (only used when you are using source_list_template, variable: source)
```

[commits-shield]: https://img.shields.io/github/commit-activity/m/Sennevds/media_player.template?style=for-the-badge
[commits]: https://github.com/sennevds/media_player.template/commits/master
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/t/media-player-template/203062
[license-shield]: https://img.shields.io/github/license/sennevds/media_player.template.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/maintenance/yes/2021.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/sennevds/media_player.template.svg?style=for-the-badge
[releases]: https://github.com/sennevds/media_player.template/releases
