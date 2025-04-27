""" . """
from modulive.constants import Types
from modulive.dynamic_clip import DynamicClip
from modulive.macro_variation import MacroVariation
from .utils import (
    activate_track,
    catch_exception,
    deactivate_track,
    get_children,
    get_main_device,
    get_name,
    get_param_path,
    get_type,
)
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

        self._macro_variations = []
        self._sections = []
        self._dynamic_clips = []

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
                                    child_track.clip_slots[idx].clip, child_track, self
                                )
                            )
                    self._sections.append(Section(config_clip, clips))
                else:
                    self._sections.append(None)
            elif row_type == Types.DYNAMIC_CLIP:
                if config_clip:
                    clips = []
                    for child_track in self._child_tracks:
                        if child_track.clip_slots[idx].has_clip:
                            clips.append(
                                ClipWrapper(
                                    child_track.clip_slots[idx].clip, child_track, self
                                )
                            )
                    self._dynamic_clips.append(DynamicClip(config_clip, clips))
            elif row_type == Types.MACRO_VARIATION:
                if config_clip:
                    track_clips = []
                    for child_track in self._child_tracks:
                        if child_track.clip_slots[idx].has_clip:
                            track_clips.append(
                                [child_track, child_track.clip_slots[idx].clip]
                            )
                    self._macro_variations.append(
                        MacroVariation(config_clip, track_clips)
                    )
                else:
                    self._macro_variations.append(None)

        self._add_name_and_color_listeners()
        self._add_clip_listeners()
        self._add_xfade_listener()

    @catch_exception
    def _rebuild(self):
        """Disconnect modules and rebuild virtual tree. Nonmutative"""
        for comp in self._macro_variations + self._sections + self._dynamic_clips:
            if comp:
                comp.disconnect()
        self._macro_variations = []
        self._sections = []
        self._dynamic_clips = []
        self._remove_name_and_color_listeners()
        self._remove_clip_listeners()
        self._remove_xfade_listener()

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

    def get_macro_variation(self, idx):
        """Get macro_variation with index"""
        mv = self.get_macro_variations()
        if len(mv) <= idx:
            return None
        return mv[idx]

    def get_macro_variation_by_name(self, name):
        """."""
        for mv in self._macro_variations:
            if mv and mv.get_name() == name:
                return mv
        return None

    def get_active_macro_variation(self):
        """."""
        for mv in self._macro_variations:
            if mv and mv.get_is_active():
                return mv
        return None

    def get_active_section(self):
        """
        Get currently playing section
        If no playing section get triggered section
        """
        for section in self._sections:
            if section and section.get_is_playing():
                return section
        for section in self._sections:
            if section and section.get_is_triggered():
                return section
        return None

    @catch_exception
    def _get_current_mapping(self):
        """Get the chain object correspding to the active mapping"""
        if self.get_active_section():
            mapping = self.get_active_section().get_mapping()
            if mapping is None:
                return None
            for device in self._config_track.devices:
                if device.name == "__MAPPINGS__":
                    for chain in device.chains:
                        if chain.name == mapping:
                            return chain
        return None

    # TODO: consolidate these GETs

    @catch_exception
    def get_dynamic_clips(self):
        """Get a list of dynamic clips for the active mapping"""
        dync = [None, None, None, None, None, None, None, None]

        mapping = self._get_current_mapping()
        if not mapping:
            return dync

        clips_device = None
        for device in mapping.devices:
            if device.name == "__DYNAMIC-CLIPS__":
                clips_device = device

        for i, chain in enumerate(clips_device.chains):
            if chain.name == "_":
                continue

            for dynamic_clip in self._dynamic_clips:
                if dynamic_clip.get_name() == chain.name:
                    dync[i] = dynamic_clip
        return dync

    @catch_exception
    def get_macro_variations(self):
        """Get a list of macro variations for the active mapping"""
        mv = [None, None, None, None]

        mapping = self._get_current_mapping()
        if not mapping:
            return mv

        clips_device = None
        for device in mapping.devices:
            if device.name == "__MACRO-VARIATIONS__":
                clips_device = device

        for i, chain in enumerate(clips_device.chains):
            if chain.name == "_":
                continue

            for macro_variation in self._macro_variations:
                if macro_variation.get_name() == chain.name:
                    mv[i] = macro_variation
        return mv

    @catch_exception
    def get_params(self):
        """Get a list of params for the active mapping"""
        params = [None, None, None, None, None, None, None]

        mapping = self._get_current_mapping()
        if not mapping:
            return params

        params_device = None
        for device in mapping.devices:
            if device.name == "__PARAMS__":
                params_device = device

        for i, chain in enumerate(params_device.chains):
            if chain.name == "_":
                continue
            track_name = get_param_path(chain.name)[0]
            param_name = get_param_path(chain.name)[1]

            for track in self._child_tracks:
                if track.name == track_name:
                    main_device = get_main_device(track)
                    for param in main_device.parameters:
                        if param.name == param_name:
                            params[i] = {
                                "param": param,
                                "track": track_name,
                                "color_index": chain.color_index
                                if not chain.is_auto_colored
                                else track.color_index,
                            }
        return params

    def get_state(self):
        """Get a dict representation of the state"""
        return {"name": self.get_name(), "color_index": self.get_color_index()}

    @catch_exception
    def get_active_state(self):
        """Get a more detailed state"""
        return {
            "name": self.get_name(),
            "color_index": self.get_color_index(),
            "sections": list(
                map(
                    lambda s: (s.get_state() if s else None),
                    self._sections,
                )
            ),
            "dynamic_clips": list(
                map(
                    lambda dc: (dc.get_state() if dc else None),
                    self.get_dynamic_clips(),
                )
            ),
            "macro_variations": list(
                map(
                    lambda mv: (mv.get_state() if mv else None),
                    self.get_macro_variations(),
                )
            ),
            "params": list(
                map(
                    lambda p: (
                        {
                            "name": p["param"].name,
                            "value": p["param"].value,
                            "min": p["param"].min,
                            "max": p["param"].max,
                            "track": p["track"],
                            "color_index": p["color_index"],
                        }
                        if p
                        else None
                    ),
                    self.get_params(),
                )
            ),
        }

    def get_integrated_tracks(self):
        """Return all tracks within integrated groups"""
        tracks = []
        for track in self._child_tracks:
            if track.is_grouped:
                if get_type(track.group_track.name) == Types.INTEGRATED:
                    tracks.append(track)
        return tracks

    # Set

    @catch_exception
    def activate(self, xy):
        """Prepare module for performance"""
        if xy == "X":
            self._track.mixer_device.crossfade_assign = 0
        elif xy == "Y":
            self._track.mixer_device.crossfade_assign = 2
        self._log(f"Activating Module [{self.get_name()}]...")
        for track in [self._track] + self._child_tracks:
            activate_track(track)
        self.toggle_integrated_tracks()
        # Set initial params
        if len(self._macro_variations) > 0:
            self._macro_variations[0].ramp(0)

    @catch_exception
    def deactivate(self):
        """Disable module"""
        self._track.mixer_device.crossfade_assign = 1
        self._log(f"Deactivating Module [{self.get_name()}]...")
        self.stop()
        for track in [self._track] + self._child_tracks:
            deactivate_track(track)

    @catch_exception
    def toggle_integrated_tracks(self):
        """Toggle integrated tracks depending on xfade position"""
        assign = self._track.mixer_device.crossfade_assign
        xfade = self._song.master_track.mixer_device.crossfader
        if assign == 0:
            if xfade.value <= 0:
                self._midi_action(self.activate_integrated_tracks)
            else:
                self._midi_action(self.deactivate_integrated_tracks)
        elif assign == 2:
            if xfade.value > 0:
                self._midi_action(self.activate_integrated_tracks)
            else:
                self._midi_action(self.deactivate_integrated_tracks)

    @catch_exception
    def activate_integrated_tracks(self):
        """Activate tracks in integration groups"""
        tracks = self.get_integrated_tracks()
        for track in tracks:
            activate_track(track)

    @catch_exception
    def deactivate_integrated_tracks(self):
        """Deactivate tracks in integration groups"""
        tracks = self.get_integrated_tracks()
        for track in tracks:
            deactivate_track(track)

    def stop(self):
        """Stop all clips in module"""
        self._track.stop_all_clips()

    def select_section(self, idx):
        """Select Section at index"""
        if self._sections[idx]:
            for section in self._sections:
                if section:
                    section.stop()
            for mv_name in self._sections[idx].get_macro_variation_names():
                mv = self.get_macro_variation_by_name(mv_name)
                mv.ramp(self._sections[idx].get_quantization())
            self._sections[idx].select()
            self.modulive.focus_track(None)

    def select_macro_variation(self, idx):
        """Select Macro Variation at index"""
        mvs = self.get_macro_variations()
        if mvs[idx]:
            mvs[idx].select()

    def stop_section(self, idx):
        """Select Section at index"""
        if self._sections[idx]:
            self._sections[idx].stop()

    def deselect_macro_variation(self, idx):
        """deSelect Macro Variation at index"""
        if self._macro_variations[idx]:
            self._macro_variations[idx].deselect()

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

    def _add_xfade_listener(self):
        """Toggle integration tracks on xfade movement"""
        self._song.master_track.mixer_device.crossfader.add_value_listener(
            self.toggle_integrated_tracks
        )

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
    def _remove_xfade_listener(self):
        """Remove xfade listener"""
        xfade = self._song.master_track.mixer_device.crossfader
        if xfade.value_has_listener(self.toggle_integrated_tracks):
            xfade.remove_value_listener(self.toggle_integrated_tracks)

    @catch_exception
    def disconnect(self):
        """Remove all listeners and disconnect. Nonmutative."""
        self._remove_name_and_color_listeners()
        self._remove_clip_listeners()
        super().disconnect()
