""" . """
from .utils import catch_exception, get_children, get_name, get_type
from .modulive_component import ModuliveComponent
from .section import Section
from .clip_wrapper import ClipWrapper


class Module(ModuliveComponent):
    """Module component"""

    @catch_exception
    def __init__(self, track):
        super().__init__()

        self._track = track
        self._log(f"Creating Module [{self.get_name()}]...")

        self._child_tracks = get_children(track, self._song.tracks)
        self._log(f"Tracks: {list(map(lambda t: t.name, self._child_tracks))}")

        # Get config track
        for child_track in self._child_tracks:
            if child_track.name == "__CONFIG__":
                self._config_track = child_track
        if self._config_track is None:
            raise Exception("__CONFIG__ track not found")

        self._macro_variations = []
        self._sections = []
        self._dynamic_clips = []

        for idx, clip_slot in enumerate(self._config_track.clip_slots):
            if clip_slot.has_clip:
                config_clip = clip_slot.clip
                row_type = get_type(config_clip.name) or get_type(
                    self._song.scenes[idx].name
                )
                if row_type == "SECTION":
                    clips = []
                    for child_track in self._child_tracks:
                        if child_track.clip_slots[idx].has_clip:
                            ClipWrapper(child_track.clip_slots[idx].clip, child_track)
                    self._sections.append(Section(config_clip, clips))

        self._add_name_and_color_listeners()

    def get_name(self):
        """Get main track name"""
        return get_name(self._track.name)

    def get_color_index(self):
        """Get track color index"""
        return self._track.color_index

    def get_section(self, idx):
        """Get section with index"""
        if len(self._sections) <= idx:
            return None
        return self._sections[idx]

    def activate(self):
        """Prepare module for performance"""
        self._log(f"Activating Module [{self.get_name()}]...")

    def deactivate(self):
        """Disable module"""
        self._log(f"Dectivating Module [{self.get_name()}]...")

    def _add_name_and_color_listeners(self):
        """Broadcast state change on color or name update"""
        for track in [self._track] + self._child_tracks:
            track.add_name_listener(self._broadcast_update)
            track.add_color_index_listener(self._broadcast_update)

    @catch_exception
    def disconnect(self):
        """Remove all listeners and disconnect"""
        for track in [self._track] + self._child_tracks:
            if track.name_has_listener(self._broadcast_update):
                track.remove_name_listener(self._broadcast_update)
            if track.color_index_has_listener(self._broadcast_update):
                track.remove_color_index_listener(self._broadcast_update)
        super().disconnect()
