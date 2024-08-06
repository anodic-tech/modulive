""" . """
from modulive.constants import Types
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

        self._build_tree()

    # Build

    @catch_exception
    def _build_tree(self):
        """Iterate through tracks and build virtual tree. Nonmutative."""
        for idx, clip_slot in enumerate(self._config_track.clip_slots):
            row_type = get_type(self._song.scenes[idx].name)
            config_clip = None
            if clip_slot.has_clip:
                config_clip = clip_slot.clip
                row_type = get_type(config_clip.name) or row_type
            if row_type == Types.SECTION:
                if config_clip:
                    clips = []
                    for child_track in self._child_tracks:
                        if child_track.clip_slots[idx].has_clip:
                            clips.append(
                                ClipWrapper(
                                    child_track.clip_slots[idx].clip, child_track
                                )
                            )
                    self._sections.append(Section(config_clip, clips))
                else:
                    self._sections.append(None)

        self._add_name_and_color_listeners()
        self._add_clip_listeners()

    @catch_exception
    def _rebuild(self):
        """Disconnect modules and rebuild virtual tree. Nonmutative"""
        for comp in self._macro_variations + self._sections + self._dynamic_clips:
            comp.disconnect()
        self._macro_variations = []
        self._sections = []
        self._dynamic_clips = []
        self._remove_name_and_color_listeners()
        self._remove_clip_listeners()

        self._build_tree()
        self._broadcast_update()

    # Get

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

    def get_state(self):
        return {"name": self.get_name(), "color_index": self.get_color_index()}

    def get_active_state(self):
        return {
            "name": self.get_name(),
            "color_index": self.get_color_index(),
            "sections": list(
                map(
                    lambda s: (s.get_state() if s else "None"),
                    self._sections,
                )
            ),
        }

    # Set

    @catch_exception
    def activate(self, ab):
        """Prepare module for performance"""
        self._log(self._track.mixer_device.crossfade_assign)
        self._log(ab)
        self._log(ab == "A")
        if ab == "A":
            self._track.mixer_device.crossfade_assign = 0
        elif ab == "B":
            self._track.mixer_device.crossfade_assign = 2
        self._log(f"Activating Module [{self.get_name()}]...")

    @catch_exception
    def deactivate(self):
        """Disable module"""
        self._track.mixer_device.crossfade_assign = 1
        self._log(f"Deactivating Module [{self.get_name()}]...")

    def stop(self):
        """Stop all clips in module"""
        self._track.stop_all_clips()

    def select_section(self, idx):
        """Select Section at index"""
        if self._sections[idx]:
            for section in self._sections:
                if section:
                    section.stop()
            self._sections[idx].select()

    def stop_section(self, idx):
        """Select Section at index"""
        if self._sections[idx]:
            self._sections[idx].stop()

    def _add_name_and_color_listeners(self):
        """Broadcast state change on color or name update to a track"""
        for track in [self._track] + self._child_tracks:
            track.add_name_listener(self._broadcast_update)
            track.add_color_index_listener(self._broadcast_update)

    def _add_clip_listeners(self):
        """Rebuild if a clip is added or removed"""
        for track in self._child_tracks:
            for clip_slot in track.clip_slots:
                clip_slot.add_has_clip_listener(self._rebuild)

    @catch_exception
    def _remove_name_and_color_listeners(self):
        """Remove track listeners"""
        for track in [self._track] + self._child_tracks:
            if track.name_has_listener(self._broadcast_update):
                track.remove_name_listener(self._broadcast_update)
            if track.color_index_has_listener(self._broadcast_update):
                track.remove_color_index_listener(self._broadcast_update)

    @catch_exception
    def _remove_clip_listeners(self):
        """Remove clip_slot listeners"""
        for track in self._child_tracks:
            for clip_slot in track.clip_slots:
                if clip_slot.has_clip_has_listener(self._rebuild):
                    clip_slot.remove_has_clip_listener(self._rebuild)

    @catch_exception
    def disconnect(self):
        """Remove all listeners and disconnect. Nonmutative."""
        self._remove_name_and_color_listeners()
        self._remove_clip_listeners()
        super().disconnect()
