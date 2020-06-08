"""Support for switches which integrates with other components."""
import logging

import voluptuous as vol

from homeassistant.components.media_player import (
    ENTITY_ID_FORMAT,
    PLATFORM_SCHEMA,
    MediaPlayerEntity,
)
from homeassistant.components.media_player.const import (
    SUPPORT_NEXT_TRACK,
    SUPPORT_PAUSE,
    SUPPORT_PLAY,
    SUPPORT_PREVIOUS_TRACK,
    SUPPORT_STOP,
    SUPPORT_TURN_OFF,
    SUPPORT_TURN_ON,
    SUPPORT_VOLUME_MUTE,
    SUPPORT_VOLUME_STEP,
    SUPPORT_SELECT_SOURCE,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_FRIENDLY_NAME,
    CONF_ENTITY_PICTURE_TEMPLATE,
    CONF_ICON_TEMPLATE,
    CONF_VALUE_TEMPLATE,
    EVENT_HOMEASSISTANT_START,
    EVENT_HOMEASSISTANT_STOP,
    STATE_ON,
    STATE_OFF,
    STATE_IDLE,
    STATE_OFF,
    STATE_PAUSED,
    STATE_PLAYING,
    STATE_UNKNOWN,
)
from homeassistant.core import callback
from homeassistant.exceptions import TemplateError
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers.event import async_track_state_change
from homeassistant.helpers.script import Script

from . import extract_entities, initialise_templates
from .const import CONF_AVAILABILITY_TEMPLATE

_LOGGER = logging.getLogger(__name__)
_VALID_STATES = [STATE_ON, STATE_OFF, "true", "false", STATE_IDLE]

CONF_MEDIAPLAYER = "media_players"
ON_ACTION = "turn_on"
OFF_ACTION = "turn_off"
PLAY_ACTION = "play"
STOP_ACTION = "stop"
PAUSE_ACTION = "pause"
NEXT_ACTION = "next"
PREVIOUS_ACTION = "previous"
VOLUME_UP_ACTION = "volume_up"
VOLUME_DOWN_ACTION = "volume_down"
MUTE_ACTION = "mute"
CONF_INPUT_TEMPLATES = "input_templates"
CURRENT_SOURCE_TEMPLATE = "current_source_template"

MEDIA_PLAYER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_VALUE_TEMPLATE): cv.template,
        vol.Optional(CONF_ICON_TEMPLATE): cv.template,
        vol.Optional(CONF_ENTITY_PICTURE_TEMPLATE): cv.template,
        vol.Optional(CONF_AVAILABILITY_TEMPLATE): cv.template,
        vol.Required(ON_ACTION): cv.SCRIPT_SCHEMA,
        vol.Required(OFF_ACTION): cv.SCRIPT_SCHEMA,
        vol.Optional(PLAY_ACTION): cv.SCRIPT_SCHEMA,
        vol.Optional(STOP_ACTION): cv.SCRIPT_SCHEMA,
        vol.Optional(PAUSE_ACTION): cv.SCRIPT_SCHEMA,
        vol.Optional(NEXT_ACTION): cv.SCRIPT_SCHEMA,
        vol.Optional(PREVIOUS_ACTION): cv.SCRIPT_SCHEMA,
        vol.Optional(VOLUME_UP_ACTION): cv.SCRIPT_SCHEMA,
        vol.Optional(VOLUME_DOWN_ACTION): cv.SCRIPT_SCHEMA,
        vol.Optional(MUTE_ACTION): cv.SCRIPT_SCHEMA,
        vol.Optional(ATTR_FRIENDLY_NAME): cv.string,
        vol.Optional(ATTR_ENTITY_ID): cv.entity_ids,
        vol.Optional(CONF_INPUT_TEMPLATES, default={}): vol.Schema(
            {cv.string: cv.SCRIPT_SCHEMA}
        ),
        vol.Optional(CURRENT_SOURCE_TEMPLATE): cv.template,
    }
)
SUPPORT_TEMPLATE = SUPPORT_TURN_OFF | SUPPORT_TURN_ON

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_MEDIAPLAYER): cv.schema_with_slug_keys(MEDIA_PLAYER_SCHEMA)}
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Template switch."""
    media_players = []

    for device, device_config in config[CONF_MEDIAPLAYER].items():
        friendly_name = device_config.get(ATTR_FRIENDLY_NAME, device)
        state_template = device_config[CONF_VALUE_TEMPLATE]
        icon_template = device_config.get(CONF_ICON_TEMPLATE)
        entity_picture_template = device_config.get(CONF_ENTITY_PICTURE_TEMPLATE)
        availability_template = device_config.get(CONF_AVAILABILITY_TEMPLATE)
        on_action = device_config[ON_ACTION]
        off_action = device_config[OFF_ACTION]
        play_action = device_config.get(PLAY_ACTION)
        stop_action = device_config.get(STOP_ACTION)
        pause_action = device_config.get(PAUSE_ACTION)
        next_action = device_config.get(NEXT_ACTION)
        previous_action = device_config.get(PREVIOUS_ACTION)
        volume_up_action = device_config.get(VOLUME_UP_ACTION)
        volume_down_action = device_config.get(VOLUME_DOWN_ACTION)
        mute_action = device_config.get(MUTE_ACTION)
        input_templates = device_config[CONF_INPUT_TEMPLATES]
        current_source_template = device_config.get(CURRENT_SOURCE_TEMPLATE)

        templates = {
            CONF_VALUE_TEMPLATE: state_template,
            CONF_ICON_TEMPLATE: icon_template,
            CONF_ENTITY_PICTURE_TEMPLATE: entity_picture_template,
            CONF_AVAILABILITY_TEMPLATE: availability_template,
            CURRENT_SOURCE_TEMPLATE: current_source_template,
        }

        initialise_templates(hass, templates)
        entity_ids = extract_entities(
            device, "media_player", device_config.get(ATTR_ENTITY_ID), templates,
        )

        media_players.append(
            MediaPlayerTemplate(
                hass,
                device,
                friendly_name,
                state_template,
                icon_template,
                entity_picture_template,
                availability_template,
                on_action,
                off_action,
                play_action,
                stop_action,
                pause_action,
                next_action,
                previous_action,
                volume_up_action,
                volume_down_action,
                mute_action,
                entity_ids,
                input_templates,
                current_source_template,
            )
        )

    async_add_entities(media_players)


class MediaPlayerTemplate(MediaPlayerEntity):
    """Representation of a Template switch."""

    def __init__(
        self,
        hass,
        device_id,
        friendly_name,
        state_template,
        icon_template,
        entity_picture_template,
        availability_template,
        on_action,
        off_action,
        play_action,
        stop_action,
        pause_action,
        next_action,
        previous_action,
        volume_up_action,
        volume_down_action,
        mute_action,
        entity_ids,
        input_templates,
        current_source_template,
    ):
        """Initialize the Template switch."""
        self.hass = hass
        self.entity_id = async_generate_entity_id(
            ENTITY_ID_FORMAT, device_id, hass=hass
        )
        self._name = friendly_name
        self._template = state_template
        self._current_source_template = current_source_template
        self._on_script = Script(hass, on_action)
        self._off_script = Script(hass, off_action)
        self._play_script = None
        if play_action is not None:
            self._play_script = Script(hass, play_action)

        self._stop_script = None
        if stop_action is not None:
            self._stop_script = Script(hass, stop_action)

        self._pause_script = None
        if pause_action is not None:
            self._pause_script = Script(hass, pause_action)

        self._next_script = None
        if next_action is not None:
            self._next_script = Script(hass, next_action)

        self._previous_script = None
        if previous_action is not None:
            self._previous_script = Script(hass, previous_action)

        self._volume_up_script = None
        if volume_up_action is not None:
            self._volume_up_script = Script(hass, volume_up_action)

        self._volume_down_script = None
        if volume_down_action is not None:
            self._volume_down_script = Script(hass, volume_down_action)

        self._mute_script = None
        if mute_action is not None:
            self._mute_script = Script(hass, mute_action)
        self._state = False
        self._icon_template = icon_template
        self._entity_picture_template = entity_picture_template
        self._availability_template = availability_template
        self._icon = None
        self._entity_picture = None
        self._entities = entity_ids
        self._available = True
        self._source_list = list(input_templates.keys())
        self._source_mapping = input_templates
        self._current_source = None
        # self._reverse_mapping = {value: key for key, value in input_templates.items()}

    async def async_added_to_hass(self):
        """Register callbacks."""

        @callback
        def template_switch_state_listener(entity, old_state, new_state):
            """Handle target device state changes."""
            self.async_schedule_update_ha_state(True)

        @callback
        def template_switch_startup(event):
            """Update template on startup."""
            async_track_state_change(
                self.hass, self._entities, template_switch_state_listener
            )

            self.async_schedule_update_ha_state(True)

        self.hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_START, template_switch_startup
        )

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._state

    @property
    def should_poll(self):
        """Return the polling state."""
        return False

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return self._icon

    @property
    def entity_picture(self):
        """Return the entity_picture to use in the frontend, if any."""
        return self._entity_picture

    @property
    def supported_features(self):
        """Flag media player features that are supported."""

        support = SUPPORT_TEMPLATE
        if self._play_script is not None:
            support |= SUPPORT_PLAY
        if self._stop_script is not None:
            support |= SUPPORT_STOP
        if self._pause_script is not None:
            support |= SUPPORT_PAUSE
        if self._next_script is not None:
            support |= SUPPORT_NEXT_TRACK
        if self._previous_script is not None:
            support |= SUPPORT_PREVIOUS_TRACK
        if self._volume_up_script is not None:
            support |= SUPPORT_VOLUME_STEP
        if self._mute_script is not None:
            support |= SUPPORT_VOLUME_MUTE
        if self._source_list.__len__() > 0:
            support |= SUPPORT_SELECT_SOURCE
        return support

    @property
    def available(self) -> bool:
        """Return if the device is available."""
        return self._available

    async def async_turn_on(self):
        """Fire the on action."""
        await self._on_script.async_run(context=self._context)

    async def async_turn_off(self):
        """Fire the off action."""
        await self._off_script.async_run(context=self._context)

    async def async_volume_up(self):
        """Fire the off action."""
        await self._volume_up_script.async_run(context=self._context)

    async def async_volume_down(self):
        """Fire the off action."""
        await self._volume_down_script.async_run(context=self._context)

    async def async_mute_volume(self, mute):
        """Fire the off action."""
        await self._mute_script.async_run(context=self._context)

    async def async_media_play(self):
        """Fire the off action."""
        await self._play_script.async_run(context=self._context)

    async def async_media_stop(self):
        """Fire the off action."""
        await self._stop_script.async_run(context=self._context)

    async def async_media_pause(self):
        """Fire the off action."""
        await self._pause_script.async_run(context=self._context)

    async def async_media_next_track(self):
        """Fire the off action."""
        await self._next_script.async_run(context=self._context)

    async def async_media_previous_track(self):
        """Fire the off action."""
        await self._previous_script.async_run(context=self._context)

    @property
    def source_list(self):
        """List of available input sources."""
        return self._source_list

    async def select_source(self, source):
        """Set the input source."""
        if source in self._source_list:
            source_script = Script(self.hass, self._source_mapping[source])
            await source_script.async_run(context=self._context)
            if self._current_source_template is None:
                self._current_source = source

    @property
    def source(self):
        """Return the current input source of the device."""
        return self._current_source

    @property
    def state(self):
        """Return the state of the player."""
        if self._state is None:
            return None
        if self._state == "idle":
            return STATE_IDLE
        return STATE_OFF

    async def async_update(self):
        """Update the state from the template."""

        try:
            state = self._template.async_render().lower()

            if state in _VALID_STATES:
                self._state = state
            elif state == STATE_UNKNOWN:
                self._state = None
            else:
                _LOGGER.error(
                    "Received invalid vacuum state: %s. Expected: %s.",
                    state,
                    ", ".join(_VALID_STATES),
                )
                self._state = None

            if self._current_source_template is not None:
                current_source = self._current_source_template.async_render()
                if current_source in self._source_list:
                    self._current_source = current_source

        except TemplateError as ex:
            _LOGGER.error(ex)
            self._state = None

        for property_name, template in (
            ("_icon", self._icon_template),
            ("_entity_picture", self._entity_picture_template),
            ("_available", self._availability_template),
        ):
            if template is None:
                continue

            try:
                value = template.async_render()
                if property_name == "_available":
                    value = value.lower() == "true"
                setattr(self, property_name, value)
            except TemplateError as ex:
                friendly_property_name = property_name[1:].replace("_", " ")
                if ex.args and ex.args[0].startswith(
                    "UndefinedError: 'None' has no attribute"
                ):
                    # Common during HA startup - so just a warning
                    _LOGGER.warning(
                        "Could not render %s template %s, the state is unknown.",
                        friendly_property_name,
                        self._name,
                    )
                    return

                try:
                    setattr(self, property_name, getattr(super(), property_name))
                except AttributeError:
                    _LOGGER.error(
                        "Could not render %s template %s: %s",
                        friendly_property_name,
                        self._name,
                        ex,
                    )
