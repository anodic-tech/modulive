""" . """
from functools import partial
from .utils import catch_exception, get_commands, get_name
from .modulive_component import ModuliveComponent


class ClipWrapper(ModuliveComponent):
    """ClipWrapper component"""

    @catch_exception
    def __init__(self, clip, track, module):
        super().__init__()

        self._clip = clip
        self._track = track
        self._module = module

        self._trigger_callbacks = []
        self._add_listeners()

    def get_name(self):
        """Get main track name"""
        return get_name(self._clip.name)

    def get_color_index(self):
        """Get track color index"""
        return self._clip.color_index

    def get_is_playing(self):
        """Return true if clip is playing"""
        return self._clip.is_playing

    def get_is_triggered(self):
        """Return true if clip is triggered"""
        return self._clip.is_triggered

    def get_track(self):
        """."""
        return self._track

    def _commands(self):
        """."""
        return get_commands(self._clip.name)

    @catch_exception
    def select(self):
        """Calls clip's select actions"""
        if len(self._commands()) == 0:
            self.fire()
            return
        for command in self._commands():
            if command == ClipCommandTypes.HOLD:
                self.fire()

    @catch_exception
    def deselect(self):
        """Call clip's deselect actions"""
        for command in self._commands():
            if command == ClipCommandTypes.HOLD:
                if self.get_is_playing() or self.get_is_triggered():
                    active_section = self._module.get_active_section()
                    section_clip = (
                        active_section.get_clip_for_track(self._track)
                        if active_section
                        else None
                    )
                    if section_clip:
                        section_clip.fire(
                            force_legato=True,
                            quantization=self._clip.launch_quantization,
                        )

    @catch_exception
    def fire(self, force_legato=False, quantization=None, _q_reset=None):
        """
        Fires clip
        force_legato - sets clip as legato, returns to original value after clip is stopped or played
        quantization - set clip quantization and then delays firing until quantization takes effect
        _q-reset - internal parameter to change quantization back after firing
        """
        if quantization:
            old_value = self._clip.launch_quantization
            self._clip.launch_quantization = quantization
            self._midi_action(
                partial(self.fire, force_legato=force_legato, _q_reset=old_value)
            )
            return

        if force_legato and not self._clip.legato:
            self._clip.legato = True

            def reset_legato():
                self._clip.legato = False

            self._trigger_callbacks.append(partial(self._midi_action, reset_legato))

        self._clip.fire()

        if _q_reset is not None:
            self._clip.launch_quantization = _q_reset

    def stop(self):
        """"""
        self._clip.stop()

    @catch_exception
    def _run_trigger_callbacks(self):
        """Triggers list of callbacks once a clip is no longer triggered"""
        if not self._clip.is_triggered:
            for callback in self._trigger_callbacks:
                callback()
            self._trigger_callbacks = []

    def _add_listeners(self):
        """Broadcast state change on color or name update"""

        self._add_listener(
            self._clip.add_name_listener,
            self._clip.name_has_listener,
            self._clip.remove_name_listener,
            self._broadcast_update,
        )
        self._add_listener(
            self._clip.add_color_index_listener,
            self._clip.color_index_has_listener,
            self._clip.remove_color_index_listener,
            self._broadcast_update,
        )
        self._add_listener(
            self._clip.add_playing_status_listener,
            self._clip.playing_status_has_listener,
            self._clip.remove_playing_status_listener,
            self._broadcast_update,
        )
        self._add_listener(
            self._clip.add_playing_status_listener,
            self._clip.playing_status_has_listener,
            self._clip.remove_playing_status_listener,
            self._run_trigger_callbacks,
        )


class ClipCommandTypes:  # pylint: disable=too-few-public-methods
    """Clip Commands mappings to readable variables"""

    HOLD = "HOLD"
