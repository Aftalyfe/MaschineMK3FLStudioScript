    # name=Maschine MK3

import arrangement
import channels
import chordsets as cs
import device
import general
import midi
import mixer
import patterns
import plugins
import transport
import ui

from midi import *

MIDI_PORT = 0 # used for selecting what MIDI IN PORT plugins should have for communicating with the script
MIDI_PORT_SERUM = 1 # used for selecting what MIDI IN PORT Serum should have in order to change presets
SERUM_PRESET_PREV_CC = 22 # look for serum.cfg file on your computer, in it you can specify
SERUM_PRESET_NEXT_CC = 23 # what midi cc controls change presets, set it to these numbers

# Maschine indexed colors from controller editor manual
Black0 = 0
Black1 = 1
Black2 = 2
Black3 = 3
Red0 = 4
Red1 = 5
Red2 = 6
Red3 = 7
Orange0 = 8
Orange1 = 9
Orange2 = 10
Orange3 = 11
LightOrange0 = 12
LightOrange1 = 13
LightOrange2 = 14
LightOrange3 = 15
WarmYellow0 = 16
WarmYellow1 = 17
WarmYellow2 = 18
WarmYellow3 = 19
Yellow0 = 20
Yellow1 = 21
Yellow2 = 22
Yellow3 = 23
Lime0 = 24
Lime1 = 25
Lime2 = 26
Lime3 = 27
Green0 = 28
Green1 = 29
Green2 = 30
Green3 = 31
Mint0 = 32
Mint1 = 33
Mint2 = 34
Mint3 = 35
Cyan0 = 36
Cyan1 = 37
Cyan2 = 38
Cyan3 = 39
Turquoise0 = 40
Turquoise1 = 41
Turquoise2 = 42
Turquoise3 = 43
Blue0 = 44
Blue1 = 45
Blue2 = 46
Blue3 = 47
Plum0 = 48
Plum1 = 49
Plum2 = 50
Plum3 = 51
Violet0 = 52
Violet1 = 53
Violet2 = 54
Violet3 = 55
Purple0 = 56
Purple1 = 57
Purple2 = 58
Purple3 = 59
Magenta0 = 60
Magenta1 = 61
Magenta2 = 62
Magenta3 = 63
Fuchsia0 = 64
Fuchsia1 = 65
Fuchsia2 = 66
Fuchsia3 = 67
White0 = 68
White1 = 69
White2 = 70
White3 = 71

# Plugin and channel color in OMNI/PAD mode, feel free to change these with any others from the list

PLUGIN_COLOR = Green1
PLUGIN_HIGHLIGHTED = Green3
CHANNEL_COLOR = White1
CHANNEL_HIGHLIGHTED = White3

# reverse engineered codes for channel rack colors
WHITE = -1
RED = -4892325
YELLOW = -4872871
GREEN = -4872871
ORANGE = -4872871
DEFAULT = -12037802
BLUE = -13619057

# modes for the pads
OMNI = 0
KEYBOARD = 1
CHORDS = 2
STEP = 3

# modes for 4D encoder
JOG = 0
VOLUME = 1
SWING = 2
TEMPO = 3



class Controller:
    def __init__(self):
        self.touch_strip = 0
        self.current_octave = 0
        self.current_offset = 0
        self.last_triggered = []
        self.encoder = 0
        self.active_chordset = 0
        self.current_group = cs.groups[0]
        self.scale = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]
        self.program = 0
        self.padmode = OMNI
        self.pattern = 0
        self.mute = 0
        self.channels = 0
        self.stepchannel = 0
        self.fixedvelocity = 0
        self.fixedvelocityvalue = 100
        self.safe_notes = []
        self.selected_track = 0
        self.mixer_snap = 0
        self.shifting = 0
        self.plugin_picker_active = 0

    def update_maschine_touch_strip(self, data1, state):  # toggles LEDs between pitch, mod, perform and notes buttons
        for button in range(49, 53):
            if data1 != button:
                device.midiOutMsg(176, 0, button, 0)
                # print("Turning off everything else" + str(button) + " The channel is:" + str(channel))
            else:
                device.midiOutMsg(176, 0, button, state)
                # print("Handling the pressed button" + str(button) + " The channel is:" + str(channel))

    def update_maschine_encoder(selfself, data1, state):  # toggles LEDs between volume, swing and tempo
        for button in range(44, 47):
            if data1 != button:
                device.midiOutMsg(176, 0, button, 0)
            else:
                device.midiOutMsg(176, 0, button, state)

    def note_off(self):
        if self.last_triggered != []:
            for note in range(0, 128):
                channels.midiNoteOn(channels.selectedChannel(), note, 0)
            for note in self.last_triggered:
                self.last_triggered.remove(note)
            return
        else:
            return


controller = Controller()

def update_led_state():
    if transport.isPlaying():
        device.midiOutMsg(176, 0, 57, 127)
    else:
        device.midiOutMsg(176, 0, 57, 0)
    if transport.isRecording():
        device.midiOutMsg(176, 0, 58, 127)
    else:
        device.midiOutMsg(176, 0, 58, 0)
    if ui.getVisible(midi.widBrowser):
        device.midiOutMsg(176, 0, 39, 127)
    else:
        device.midiOutMsg(176, 0, 39, 0)
    if ui.getVisible(midi.widMixer):
        device.midiOutMsg(176, 0, 37, 127)
    else:
        device.midiOutMsg(176, 0, 37, 0)
    if ui.getVisible(widPlaylist):
        device.midiOutMsg(176, 0, 36, 127)
    else:
        device.midiOutMsg(176, 0, 36, 0)
    if ui.getVisible(midi.widChannelRack):
        device.midiOutMsg(176, 0, 19, 127)
    else:
        device.midiOutMsg(176, 0, 19, 0)
    if ui.isMetronomeEnabled():
        device.midiOutMsg(176, 0, 56, 127)
    else:
        device.midiOutMsg(176, 0, 56, 0)
    if transport.isPlaying():
        device.midiOutMsg(176, 0, 59, 0)
    else:
        device.midiOutMsg(176, 0, 59, 127)
    if transport.getLoopMode():
        device.midiOutMsg(176, 0, 53, 127)
    else:
        device.midiOutMsg(176, 0, 53, 0)
    if ui.getSnapMode() == 3:
        device.midiOutMsg(176, 0, 48, 0)
    else:
        device.midiOutMsg(176, 0, 48, 127)

def update_mixer_track():
    # update track num
    device.midiOutMsg(176, 0, 70, mixer.trackNumber())
    return

def update_mixer_values():
    # update volume
    converted_volume = round(mixer.getTrackVolume(mixer.trackNumber()) * 125)
    device.midiOutMsg(176, 0, 71, converted_volume)
    # update panning
    converted_pan = round((mixer.getTrackPan(mixer.trackNumber()) * 63) + 63)
    device.midiOutMsg(176, 0, 72, converted_pan)
    # update stereo separation
    ssindex = midi.REC_Mixer_SS + mixer.getTrackPluginId(mixer.trackNumber(), 0)
    ssvalue = general.processRECEvent(ssindex, 1, midi.REC_GetValue) + 63
    device.midiOutMsg(176, 0, 73, ssvalue)
    return

def refresh_channels():
    for channel in range(0, 17):
        device.midiOutMsg(144, 0, channel, 0)
    lower_channel = controller.channels * 16
    for channel in range(lower_channel, channels.channelCount()):
        index = channel - (controller.channels * 16)
        if plugins.isValid(channel):
            device.midiOutMsg(144, 0, index, PLUGIN_COLOR)
        else:
            device.midiOutMsg(144, 0, index, CHANNEL_COLOR)
        if index == 16:
            break
    if channels.selectedChannel() in range(lower_channel, channels.channelCount()):
        channel = channels.selectedChannel() - (controller.channels * 16)
        if plugins.isValid(channels.selectedChannel()):
            device.midiOutMsg(144, 0, channel, PLUGIN_HIGHLIGHTED)
        else:
            device.midiOutMsg(144, 0, channel, CHANNEL_HIGHLIGHTED)

def refresh_chan_screen():
    # refresh channel number
    device.midiOutMsg(176, 0, 74, channels.selectedChannel())
    # refresh offset volume
    id = midi.REC_Chan_OfsVol + channels.getRecEventId(channels.selectedChannel())
    value = channels.processRECEvent(id, 0, midi.REC_GetValue)
    device.midiOutMsg(176, 0, 75, round((value/25600) * 127) - 1)
    # refresh offset modx
    id = midi.REC_Chan_OfsFCut + channels.getRecEventId(channels.selectedChannel())
    value = general.processRECEvent(id, 0, midi.REC_GetValue)
    if -12 < value < 12:
        value = 0
    #print(value)
    device.midiOutMsg(176, 0, 76, round(((value + 256) / 512) * 127) - 1)
    return

def refresh_grid():
    lower_grid = controller.stepchannel * 16
    for gridbit in range(lower_grid, lower_grid + 16):
        index = gridbit - lower_grid
        device.midiOutMsg(144, 0, index, Black0)
    for gridbit in range(lower_grid, lower_grid + 16):
        index = gridbit - lower_grid
        if channels.getGridBit(channels.selectedChannel(), gridbit) == 1:
            device.midiOutMsg(144, 0, index, Purple3)
    return

def init_leds():
    for button in range(0, 127):
        device.midiOutMsg(176, 0, button, Black0)
    for note in range(0, 127):
        device.midiOutMsg(144, 0, note, Black0)
    device.midiOutMsg(176, 0, 3, int(transport.getSongPos() * 127))
    device.midiOutMsg(176, 0, 100, White1)
    device.midiOutMsg(176, 0, 30, Green0)
    device.midiOutMsg(176, 0, 31, Green0)
    device.midiOutMsg(176, 0, 33, Green0)
    device.midiOutMsg(176, 0, 34, Green0)
    device.midiOutMsg(176, 0, 35, 0)
    device.midiOutMsg(176, 0, 81, 127)
    device.midiOutMsg(176, 0, 77, 100)
    refresh_channels()
    refresh_chan_screen()
    return

def hex_it(data):
    if data:
        return data.hex()
    else:
        return "None"

def hex_string(string):
    s = string.encode('utf-8')
    hex_value = s.hex()
    return hex_value


def print_midi_info(event):  # quick code to see info about particular midi control (check format function in python)
    print("status: {}, channel: {}, note: {}, data1: {}, data2: {},, sysex: {}".format(event.status, event.midiChan,
                                                                                       event.note, event.data1,
                                                                                       event.data2,
                                                                                       hex_it(event.sysex)))

def OnInit():
    init_leds()
    update_led_state()
    update_mixer_values()
    refresh_chan_screen()
    refresh_channels()
    update_mixer_track()
    return

def OnDeInit():
    for button in range(0, 127):
        device.midiOutMsg(176, 0, button, Black0)
    for note in range(0, 127):
        device.midiOutMsg(144, 0, note, Black0)
    return

def OnRefresh(flag):
    try:
        print("Refresh Flag:" + str(flag))
        if flag == 256: # DIRTY LEDs
            update_led_state()
            return
        if flag == 263: # selecting mixer tracks
            update_mixer_track()
            return
        if flag == 4: # DIRTY MIXER CONTROLS
            if not controller.plugin_picker_active:
                update_mixer_values()
            return
        if flag == 260: # MAIN RECORDING FLAG
            if transport.isRecording():
                device.midiOutMsg(176, 0, 58, 127)
            else:
                device.midiOutMsg(176, 0, 58, 0)
            return
        if flag == 359 or flag == 375: # LOADING NEW CHANNELS (PLUGINS OR SAMPLES)
            if controller.padmode == OMNI:
                refresh_channels()
                if not controller.plugin_picker_active:
                    refresh_chan_screen()
                return
            elif controller.padmode == STEP: # LOADING NEW CHANNELS (PLUGINS OR SAMPLES)
                refresh_grid()
                if not controller.plugin_picker_active:
                    refresh_chan_screen()
                return
        if flag == 288: # CHANGING CHANNELS
            if controller.padmode == OMNI:
                refresh_channels()
            if controller.padmode == STEP:
                refresh_grid()
            if not controller.plugin_picker_active:
                refresh_chan_screen()
            update_led_state()
            return
        if flag == 311 and controller.padmode == OMNI: # DELETING CHANNELS
            refresh_channels()
            if not controller.plugin_picker_active:
                refresh_chan_screen()
            return
        if flag == 1024 or flag == 1056 or flag == 1280 and controller.padmode == STEP: # changing steps
            refresh_grid()
            return
        if flag == 295:
            if not controller.plugin_picker_active:
                refresh_chan_screen()
            update_led_state()
            return
        if flag == 32:
            if not controller.plugin_picker_active:
                refresh_chan_screen()
            update_led_state()
            return
    
        #print("Unhandled flag:" + str(flag))
    except TypeError as e:
        # Heavy-handed error handling of "Operation unsafe at current time" exceptions
        # we just discard all exceptions with that message - it's a bit of a yikes, and
        # ideally we'd prevent the issue from happening in the first place, but it'll do
        if e.args != ("Operation unsafe at current time",):
            # Raise errors without those args, or we could obscure some issues that probably should
            # be caught during development
            raise e

def OnMidiIn(event):
    # print_midi_info(event)
    return


def OnMidiMsg(event):  # same as above, but executes after OnMidiIn
    return

def OnProgramChange(event): # status = 192, event.data1 = value, data2 = 0, port is from midi options!
    return

def OnControlChange(event):
    # --------------------------------------------------------------------------------------------------------
    #   TOUCH STRIP
    # --------------------------------------------------------------------------------------------------------
    # letting touch strip handle pitch
    if event.data1 == 49:
        if controller.touch_strip != 1:
            controller.touch_strip = 1
            device.midiOutMsg(event.status, 0, 3, 64)
            controller.update_maschine_touch_strip(49, 127)
            event.handled = True
            return
        else:
            controller.touch_strip = 0
            device.midiOutMsg(event.status, 0, 3, int(transport.getSongPos() * 127))
            controller.update_maschine_touch_strip(49, 0)
            event.handled = True
            return
    # letting touch strip handle modwheel
    if event.data1 == 50:
        if controller.touch_strip != 2:
            controller.touch_strip = 2
            device.midiOutMsg(176, 0, 3, 0)
            controller.update_maschine_touch_strip(50, 127)
            event.handled = True
            return
        else:
            controller.touch_strip = 0
            device.midiOutMsg(event.status, 0, 3, int(transport.getSongPos() * 127))
            controller.update_maschine_touch_strip(50, 0)
            event.handled = True
            return
    # PERFORM FX
    if event.data1 == 51:
        mixer.linkTrackToChannel(0)
        ui.setHintMsg(channels.getChannelName(channels.selectedChannel()) + " linked to track " + str(mixer.trackNumber()))
        event.handled = True
        return
    # NOTES
    if event.data1 == 52:
        transport.globalTransport(FPT_F11, 1)
        event.handled = True
        return
    # touch strip coding
    if event.data1 == 3:
        if controller.touch_strip == 1:  # pitch
            channels.setChannelPitch(channels.selectedChannel(), float((event.data2 / 64) - 1))
            device.midiOutMsg(176, 0, 3, event.data2)
            event.handled = True
            return
        elif controller.touch_strip == 2:  # mod, the handled flag is false so its free to assign in FL
            device.midiOutMsg(176, 0, 3, event.data2)
            event.handled = False
            return
        else:
            song_length = transport.getSongLength(midi.SONGLENGTH_BARS)
            updated_position_in_bars = (int((event.data2 / 127) * song_length))
            updated_position = updated_position_in_bars / song_length
            transport.setSongPos(updated_position)
            device.midiOutMsg(176, 0, 3, int(transport.getSongPos() * 127))
            event.handled = True
            return
    if event.data1 == 2:
        if controller.touch_strip == 1:
            channels.setChannelPitch(channels.selectedChannel(), 0)
            device.midiOutMsg(176, 0, 3, 64)
        event.handled = True
        return
    # --------------------------------------------------------------------------------------------------------
    #   TRANSPORT CONTROLS
    # --------------------------------------------------------------------------------------------------------
    if event.data1 == 57:  # PLAY
        transport.start()
        if transport.isPlaying():
            device.midiOutMsg(176, 0, 57, 127)
        else:
            device.midiOutMsg(176, 0, 57, 0)
        event.handled = True
        return
    if event.data1 == 58 and controller.shifting == 1:
        if ui.isPrecountEnabled():
            transport.globalTransport(midi.FPT_CountDown, 1)
            ui.setHintMsg("Precount disabled")
            event.handled = True
            return
        transport.globalTransport(midi.FPT_CountDown, 1)
        ui.setHintMsg("Precount active")
        event.handled = True
        return
    if event.data1 == 58:  # RECORD
        transport.record()
        event.handled = True
        return
    if event.data1 == 59:  # STOP
        transport.stop()
        event.handled = True
        return
    if event.data1 == 53:  # RESTART
        transport.setLoopMode()
        event.handled = True
        return
    if event.data1 == 54:  # ERASE
        if event.data2 == 0:
            device.midiOutMsg(176, 0, 54, 0)
            event.handled = True
            return
        ui.delete()
        device.midiOutMsg(176, 0, 54, 127)
        event.handled = True
        return
    if event.data1 == 55:  # TAP TEMPO
        if event.data2 == 0:
            device.midiOutMsg(176, 0, 55, 0)
            event.handled = True
            return
        transport.globalTransport(106, 1)
        device.midiOutMsg(176, 0, 55, 127)
        event.handled = True
        return
    if event.data1 == 56: # FOLLOW (METRONOME)
        transport.globalTransport(midi.FPT_Metronome, 1)
        if ui.isMetronomeEnabled():
            device.midiOutMsg(176, 0, 56, 127)
            event.handled = True
            return
        device.midiOutMsg(176, 0, 56, 0)
        event.handled = True
        return

#----------------------------------------------------------------------------------------------------------------------
#   MODE PICKER
#----------------------------------------------------------------------------------------------------------------------

    if event.data1 == 84:  # CHORDS
        for chordset in range(100, 108):
            device.midiOutMsg(176, 0, chordset, 0)
        for mode in range(81, 85):
            device.midiOutMsg(176, 0, mode, 0)
        for note in range(0, 16):
            device.midiOutMsg(144, 0, note, 0)
        controller.padmode = CHORDS
        controller.note_off()
        device.midiOutMsg(176, 0, 84, 127)
        device.midiOutMsg(176, 0, controller.active_chordset + 100, 44)
        event.handled = True
        return
    if event.data1 == 81:  # PAD MODE/OMNI MODE
        for channel in range(100, 108):
            device.midiOutMsg(176, 0, channel, 0)
        for mode in range(81, 85):
            device.midiOutMsg(176, 0, mode, 0)
        for note in range(0, 16):
            device.midiOutMsg(144, 0, note, 0)
        device.midiOutMsg(176, 0, 81, 127)
        controller.padmode = OMNI
        controller.note_off()
        refresh_channels()
        device.midiOutMsg(176, 0, controller.channels + 100, White3)
        event.handled = True
        return
    if event.data1 == 82:  # KEYBOARD
        for group in range(100, 108):
            device.midiOutMsg(176, 0, group, 0)
        for mode in range(81, 85):
            device.midiOutMsg(176, 0, mode, 0)
        for note in range(0, 16):
            device.midiOutMsg(144, 0, note, 0)
        device.midiOutMsg(176, 0, 82, 127)
        controller.padmode = KEYBOARD
        controller.note_off()
        device.midiOutMsg(176, 0, cs.groups.index(controller.current_group) + 100, 4)
        event.handled = True
        return
    if event.data1 == 83:  # STEP SEQUENCING
        for stepchannel in range(100, 108):
            device.midiOutMsg(176, 0, stepchannel, 0)
        for mode in range(81, 85):
            device.midiOutMsg(176, 0, mode, 0)
        for note in range(0, 16):
            device.midiOutMsg(144, 0, note, 0)
        device.midiOutMsg(176, 0, 83, 127)
        controller.padmode = STEP
        controller.note_off()
        device.midiOutMsg(176, 0, controller.stepchannel + 100, Purple1)
        refresh_grid()
        event.handled = True
        return
    # --------------------------------------------------------------------------------------------------------
    #   OTHER CONTROLS
    # --------------------------------------------------------------------------------------------------------
    if event.data1 == 80:
        if controller.fixedvelocity == 0:
            controller.fixedvelocity = 1
            device.midiOutMsg(176, 0, 80, 127)
            event.handled = True
            return
        controller.fixedvelocity = 0
        device.midiOutMsg(176, 0, 80, 0)
        event.handled = True
        return
    if event.data1 == 85 and controller.shifting == 1 and event.data2 != 0:
        arrangement.addAutoTimeMarker(arrangement.currentTime(True), "TRANSITION")
        ui.setHintMsg("Marker Added")
        event.handled = True
        return
    if event.data1 == 85: # SELECT NEXT SCENE IN THE SONG
        if event.data2 == 0:
            device.midiOutMsg(176, 0, 85, 0)
            event.handled = True
            return
        arrangement.jumpToMarker(1, 1)
        device.midiOutMsg(176, 0, 85, 127)
        event.handled = True
        return
    if event.data1 == 86: # ACTIVATE PATTERN SELECTION WHEN "PATTERN" BUTTON IS PRESSED
        if event.data2 == 0:                     # DEACTIVATE PATTERN SELECTION WHEN RELEASED
            for pattern in range(0, 16):
                device.midiOutMsg(144, 0, pattern, 0)
            controller.pattern = 0
            device.midiOutMsg(176, 0, 86, 0)
            if controller.padmode == OMNI:
                refresh_channels()
            event.handled = True
            return
        for pattern in range(0, 16):
            device.midiOutMsg(144, 0, pattern, 0)
        controller.pattern = 1
        device.midiOutMsg(176, 0, 86, 127)
        for pattern in range(0, patterns.patternCount()):
            device.midiOutMsg(144, 0, pattern, Lime1)
        event.handled = True
        return
    if event.data1 == 87: # OPEN EVENT (PIANO ROLL)
        if event.data2 == 0:
            ui.hideWindow(midi.widPianoRoll)
            event.handled = True
            return
        ui.showWindow(midi.widPianoRoll)
        event.handled = True
        return
    if event.data1 == 88: # HOLDING DOWN SHIFT ("VARIATION" BUTTON)
        if event.data2 == 0:
            controller.shifting = 0
            event.handled = True
            return
        controller.shifting = 1
        event.handled = True
        return
    if event.data1 == 89: # DUPLICATE
        if event.data2 == 0:
            ui.paste()
            device.midiOutMsg(176, 0, 89, 0)
            event.handled = True
            return
        ui.copy()
        device.midiOutMsg(176, 0, 89, 127)
        event.handled = True
        return
    if event.data1 == 90: # SELECT
        if event.data2 == 0:
            arrangement.liveSelection(arrangement.currentTime(1), 1)
            device.midiOutMsg(176, 0, 90, 0)
            event.handled = True
            return
        arrangement.liveSelection(arrangement.currentTime(1), 0)
        device.midiOutMsg(176, 0, 90, 127)
        event.handled = True
        return
    if event.data1 == 91 and controller.shifting == 1:
        if event.data2 == 0:
            device.midiOutMsg(176, 0, 91, 0)
            event.handled = True
            return
        mixer.soloTrack(mixer.trackNumber(), -1, fxSoloModeWithSourceTracks)
        device.midiOutMsg(176, 0, 91, 0)
        event.handled = True
        return
    if event.data1 == 91:
        if event.data2 == 0:
            device.midiOutMsg(176, 0, 91, 0)
            event.handled = True
            return
        mixer.soloTrack(mixer.trackNumber(), -1, fxSoloModeWithDestTracks)
        device.midiOutMsg(176, 0, 91, 0)
        event.handled = True
        return
    if event.data1 == 92 and controller.shifting == 1: # SIMULATED CHOKE FUNCTION
        for channel in range(0, channels.channelCount()):
            for note in range(0, 128):
                channels.midiNoteOn(channel, note, 0)
        event.handled = True
        return
    if event.data1 == 92: # MUTE MIXER TRACK
        if event.data2 == 0:
            device.midiOutMsg(176, 0, 92, 0)
            event.handled = True
            return
        mixer.muteTrack(mixer.trackNumber())
        device.midiOutMsg(176, 0, 92, 127)
        event.handled = True
        return
    if event.data1 == 39 and event.data2 != 0: # SAMPLING
        if not ui.getVisible(widBrowser):
            ui.showWindow(widBrowser)
            event.handled = True
            return
        if ui.getFocused(widBrowser):
            ui.hideWindow(widBrowser)
            event.handled = True
            return
        ui.setFocused(widBrowser)
        event.handled = True
        return
    if event.data1 == 40 and controller.shifting == 1:  # FILE Save button
        if event.data2 == 0:
            device.midiOutMsg(176, 0, event.data1, 0)
            event.handled = True
            return
        transport.globalTransport(midi.FPT_Save, 1)
        device.midiOutMsg(176, 0, event.data1, 127)
        event.handled = True
        return
    if event.data1 == 40:  # FILE Save button
        if event.data2 == 0:
            device.midiOutMsg(176, 0, event.data1, 0)
            event.handled = True
            return
        transport.globalTransport(midi.FPT_Menu, 1)
        device.midiOutMsg(176, 0, event.data1, 127)
        event.handled = True
        return
    if event.data1 == 22: # PREVIOUS FL PRESET
        if event.data2 != 0:
            channels.showEditor(channels.selectedChannel(), 1)
            device.midiOutMsg(176, 0, event.data1, 127)
            if plugins.isValid(channels.selectedChannel()):
                if ui.getFocusedPluginName() == "Serum":
                    message1 = 176 + (SERUM_PRESET_PREV_CC << 8) + (0 << 16) + (MIDI_PORT_SERUM << 24)
                    message2 = 176 + (SERUM_PRESET_PREV_CC << 8) + (127 << 16) + (MIDI_PORT_SERUM << 24)
                    device.forwardMIDICC(message1)
                    device.forwardMIDICC(message2)
                    event.handled = True
                    return
                else:
                    plugins.prevPreset(channels.selectedChannel())
                    event.handled = True
                    return
        device.midiOutMsg(176, 0, event.data1, 0)
        event.handled = True
        return
    if event.data1 == 23:
        if event.data2 != 0: # NEXT FL PRESET
            channels.showEditor(channels.selectedChannel(), 1)
            device.midiOutMsg(176, 0, event.data1, 127)
            if plugins.isValid(channels.selectedChannel()):
                if ui.getFocusedPluginName() == "Serum":
                    message1 = 176 + (SERUM_PRESET_NEXT_CC << 8) + (0 << 16) + (MIDI_PORT_SERUM << 24)
                    message2 = 176 + (SERUM_PRESET_NEXT_CC << 8) + (127 << 16) + (MIDI_PORT_SERUM << 24)
                    device.forwardMIDICC(message1)
                    device.forwardMIDICC(message2)
                    event.handled = True
                    return
                else:
                    plugins.nextPreset(channels.selectedChannel())
                    event.handled = True
                    return
        device.midiOutMsg(176, 0, event.data1, 0)
        event.handled = True
        return
    if event.data1 == 24 or event.data1 == 25:
        if event.data2 != 0:
            device.midiOutMsg(176, 0, event.data1, 127)
            if event.data1 == 25 and controller.program <= 126:
                controller.program += 1
                ui.setHintMsg("PROGRAM = " + str(controller.program))
            elif event.data1 == 24 and controller.program != 0:
                controller.program -= 1
                ui.setHintMsg("PROGRAM = " + str(controller.program))
            message = 192 + (controller.program << 8) + (0 << 16) + (MIDI_PORT << 24)
            device.forwardMIDICC(message)
            event.handled = True
            return
        device.midiOutMsg(176, 0, event.data1, 0)
        event.handled = True
        return
    if event.data1 == 36: #PLAYLIST
        if ui.getVisible(widPlaylist):
            ui.hideWindow(midi.widPlaylist)
            event.handled = True
            return
        ui.showWindow(midi.widPlaylist)
        event.handled = True
        return
    if event.data1 == 35: # SHOW/HIDE PLUGIN/SAMPLE FORM CURRENTLY SELECTED
        if event.data2 == 0:
            device.midiOutMsg(176, 0, 35, 0)
            event.handled = True
            return
        device.midiOutMsg(176, 0, 35, 127)
        channels.showCSForm(channels.selectedChannel(), -1)
        event.handled = True
        return
    if event.data1 == 38:# PLUGIN PICKER
        if event.data2 == 0:
            event.handled = True
            return
        if controller.plugin_picker_active == 0:
            transport.globalTransport(midi.FPT_F8, 1)
            controller.plugin_picker_active = 1
            device.midiOutMsg(176, 0, 38, 127)
        else:
            transport.globalTransport(midi.FPT_F8, 1)
            controller.plugin_picker_active = 0
            device.midiOutMsg(176, 0, 38, 0)
        #print(controller.plugin_picker_active)
        event.handled = True
        return
    if event.data1 == 37: # MIXER
        if ui.getVisible(midi.widMixer):
            ui.hideWindow(midi.widMixer)
            device.midiOutMsg(176, 0, event.data1, 0)
            event.handled = True
            return
        ui.showWindow(midi.widMixer)
        device.midiOutMsg(176, 0, event.data1, 127)
        event.handled = True
        return
    if event.data1 == 19: # CHANNEL RACK
        if ui.getVisible(1):
            ui.hideWindow(1)
            device.midiOutMsg(176, 0, 19, 0)
            event.handled = True
            return
        ui.showWindow(midi.widChannelRack)
        device.midiOutMsg(176, 0, 19, 127)
        event.handled = True
        return
    if event.data1 == 41: # MIDI SETTINGS
        transport.globalTransport(midi.FPT_F10, 1)
        event.handled = True
        return
    if event.data1 == 43: # RIGHT CLICK
        if not ui.isInPopupMenu():
            transport.globalTransport(midi.FPT_ItemMenu, 1)
            event.handled = True
            return
        else:
            ui.closeActivePopupMenu()
            event.handled = True
            return
    if event.data1 == 48:
        if event.data2 != 0:
            ui.snapOnOff()
            if ui.getSnapMode() == 3:
                device.midiOutMsg(176, 0, 48, 0)
            else:
                device.midiOutMsg(176, 0, 48, 127)
        #print(ui.getSnapMode())
        event.handled = True
        return

    # --------------------------------------------------------------------------------------------------------
    #   4-D ENCODER
    # --------------------------------------------------------------------------------------------------------
    if event.data1 == 44:
        if controller.encoder == VOLUME:
            controller.encoder = JOG
            event.handled = True
            controller.update_maschine_encoder(44, 0)
            return
        else:
            controller.encoder = VOLUME
            event.handled = True
            controller.update_maschine_encoder(44, 127)
            return
    if event.data1 == 45:
        if controller.encoder == SWING:
            controller.encoder = JOG
            event.handled = True
            controller.update_maschine_encoder(45, 0)
            return
        else:
            controller.encoder = SWING
            event.handled = True
            controller.update_maschine_encoder(45, 127)
            return
    if event.data1 == 46:
        if controller.encoder == TEMPO:
            controller.encoder = JOG
            event.handled = True
            controller.update_maschine_encoder(46, 0)
            return
        else:
            controller.encoder = TEMPO
            event.handled = True
            controller.update_maschine_encoder(46, 127)
            return
    if event.data1 == 7:  # PRESS
        ui.enter()
        event.handled = True
        return
    if event.data1 == 8:  # ROTATION
        if event.data2 == 65:
            if controller.encoder == JOG:
                if ui.getFocused(midi.widMixer):
                    ui.right()
                    event.handled = True
                    return
                ui.down()
                event.handled = True
                return
            elif controller.encoder == VOLUME:
                volume = channels.getChannelVolume(channels.selectedChannel()) + 0.01
                channels.setChannelVolume(channels.selectedChannel(), volume)
                event.handled = True
                return
            elif controller.encoder == SWING:
                ui.setFocused(midi.widPlaylist)
                ui.jog(1)
                event.handled = True
                return
            elif controller.encoder == TEMPO:
                transport.globalTransport(midi.FPT_TempoJog, 10)
                event.handled = True
                return
        if event.data2 == 63:
            if controller.encoder == JOG:
                if ui.getFocused(midi.widMixer):
                    ui.left()
                    event.handled = True
                    return
                ui.up()
                event.handled = True
                return
            elif controller.encoder == VOLUME:
                volume = channels.getChannelVolume(channels.selectedChannel()) - 0.01
                channels.setChannelVolume(channels.selectedChannel(), volume)
                event.handled = True
                return
            elif controller.encoder == SWING:
                ui.setFocused(midi.widPlaylist)
                ui.jog(-1)
                event.handled = True
                return
            elif controller.encoder == TEMPO:
                transport.globalTransport(midi.FPT_TempoJog, -10)
                event.handled = True
                return
    if event.data1 == 30:
        if event.data2 == 0:
            device.midiOutMsg(176, 0, event.data1, Green1)
            event.handled = True
            return
        device.midiOutMsg(176, 0, event.data1, Green3)
        ui.up()
        event.handled = True
        return
    if event.data1 == 31:
        if event.data2 == 0:
            device.midiOutMsg(176, 0, event.data1, Green1)
            event.handled = True
            return
        ui.right()
        device.midiOutMsg(176, 0, event.data1, Green3)
        event.handled = True
        return
    if event.data1 == 33:
        if event.data2 == 0:
            device.midiOutMsg(176, 0, event.data1, Green1)
            event.handled = True
            return
        ui.down()
        device.midiOutMsg(176, 0, event.data1, Green3)
        event.handled = True
        return
    if event.data1 == 34:
        if event.data2 == 0:
            device.midiOutMsg(176, 0, event.data1, Green1)
            event.handled = True
            return
        ui.left()
        device.midiOutMsg(176, 0, event.data1, Green3)
        event.handled = True
        return
    # -----------------------------------------------------------------------------------------------------
    #   GROUPS
    # --------------------------------------------------------------------------------------------------------
    if 100 <= event.data1 <= 107:
        for group in range(100, 108):
            device.midiOutMsg(176, 0, group, 0)
        for channel in range(0, 16):
            device.midiOutMsg(144, 0, channel, 0)
        if controller.padmode == OMNI:
            controller.channels = event.data1 - 100
            device.midiOutMsg(176, 0, event.data1, White1)
            controller.note_off()
            refresh_channels()
            event.handled = True
            return
        elif controller.padmode == KEYBOARD:
            controller.current_group = cs.groups[event.data1 - 100]
            device.midiOutMsg(176, 0, event.data1, 4)
            controller.note_off()
            event.handled = True
            return
        elif controller.padmode == CHORDS:
            controller.active_chordset = event.data1 - 100
            controller.note_off()
            device.midiOutMsg(176, 0, event.data1, 44)
            event.handled = True
            return
        elif controller.padmode == STEP:
            controller.stepchannel = event.data1 - 100
            refresh_grid()
            device.midiOutMsg(176, 0, event.data1, Purple1)
            event.handled = True
            return

    # --------------------------------------------------------------------------------------------------------
    #   OCTAVE SHIFTING
    # --------------------------------------------------------------------------------------------------------
    if event.data1 == 26 and controller.current_octave >= -2:
        if event.data2 != 0:
            device.midiOutMsg(176, 0, event.data1, 127)
            controller.current_octave -= 1
            event.handled = True
            controller.note_off()
            ui.setHintMsg("Current octave: " + str(controller.current_octave))
            return
        device.midiOutMsg(176, 0, event.data1, 0)
        event.handled = True
        return
    if event.data1 == 27 and controller.current_octave <= 2:
        if event.data2 != 0:
            device.midiOutMsg(176, 0, event.data1, 127)
            controller.current_octave += 1
            event.handled = True
            controller.note_off()
            ui.setHintMsg("Current octave: " + str(controller.current_octave))
            return
        device.midiOutMsg(176, 0, event.data1, 0)
        event.handled = True
        return
    if event.data1 == 28 and controller.current_offset != -11:
        if event.data2 != 0:
            device.midiOutMsg(176, 0, event.data1, 127)
            controller.current_offset -= 1
            event.handled = True
            controller.note_off()
            ui.setHintMsg("Root note: " + controller.scale[controller.current_offset])
            return
        device.midiOutMsg(176, 0, event.data1, 0)
        event.handled = True
        return
    elif event.data1 == 28 and controller.current_octave >= -2:
        if event.data2 != 0:
            device.midiOutMsg(176, 0, event.data1, 127)
            controller.current_offset = 0
            controller.current_octave -= 1
            event.handled = True
            controller.note_off()
            ui.setHintMsg("Current octave: " + str(controller.current_octave))
            return
        device.midiOutMsg(176, 0, event.data1, 0)
        event.handled = True
        return
    if event.data1 == 29 and controller.current_offset != 11:
        if event.data2 != 0:
            device.midiOutMsg(176, 0, event.data1, 127)
            controller.current_offset += 1
            event.handled = True
            controller.note_off()
            ui.setHintMsg("Root note: " + controller.scale[controller.current_offset])
            return
        device.midiOutMsg(176, 0, event.data1, 0)
        event.handled = True
        return
    elif event.data1 == 29 and controller.current_octave <= 2:
        if event.data2 != 0:
            device.midiOutMsg(176, 0, event.data1, 127)
            controller.current_offset = 0
            controller.current_octave += 1
            event.handled = True
            controller.note_off()
            ui.setHintMsg("Current octave: " + str(controller.current_octave))
            return
        device.midiOutMsg(176, 0, event.data1, 0)
        event.handled = True
        return
# --------------------------------------------------------------------------------------------------------
#   ROTARY WHEELS
# --------------------------------------------------------------------------------------------------------
    # LEFT SECTION
    if event.data1 == 20:
        if event.data2 == 0:
            controller.mixer_snap = 0
            event.handled = True
            return
        controller.mixer_snap = 1
        event.handled = True
        return
    if event.data1 == 70: # MIXER SELECT
        controller.selected_track = event.data2
        mixer.setTrackNumber(controller.selected_track)
        event.handled = True
        return
    if event.data1 == 71: # MIXER VOLUME
        if controller.mixer_snap == 1:
            mixer.setTrackVolume(mixer.trackNumber(), 0.8)
            event.handled = True
            return
        converted_volume = event.data2 / 125
        if 0.78 < converted_volume < 0.82:
            converted_volume = 0.8
        mixer.setTrackVolume(mixer.trackNumber(), converted_volume)
        event.handled = True
        return
    if event.data1 == 72: # MIXER PAN
        if controller.mixer_snap == 1:
            mixer.setTrackPan(mixer.trackNumber(), 0)
            event.handled = True
            return
        converted_pan = (event.data2 / 63) - 1
        if -0.05 < converted_pan < 0.05:
            converted_pan = 0
        mixer.setTrackPan(mixer.trackNumber(), converted_pan)
        event.handled = True
        return
    if event.data1 == 73: # MIXER STEREO SEPARATION
        if controller.mixer_snap == 1:
            ssindex = midi.REC_Mixer_SS + mixer.getTrackPluginId(mixer.trackNumber(), 0)
            general.processRECEvent(ssindex, 0, midi.REC_UpdateValue | midi.REC_UpdateControl | midi.REC_ShowHint)
            event.handled = True
            return
        converted_ss = event.data2 - 63
        if -2 < converted_ss < 2:
            converted_ss = 0
        ssindex = midi.REC_Mixer_SS + mixer.getTrackPluginId(mixer.trackNumber(), 0)
        general.processRECEvent(ssindex, converted_ss, midi.REC_UpdateValue | midi.REC_UpdateControl | midi.REC_ShowHint)
        event.handled = True
        return
    # RIGHT SECTION
    if event.data1 == 74:
        if event.data2 < channels.channelCount():
            channels.selectOneChannel(event.data2)
            ui.setHintMsg("Channel selected: " + str(channels.getChannelName(channels.selectedChannel())))
        else:
            device.midiOutMsg(176, 0, 74, channels.selectedChannel())
        event.handled = True
        return
    if event.data1 == 75:
        id = midi.REC_Chan_OfsVol + channels.getRecEventId(channels.selectedChannel())
        value = (event.data2 / 127) * 25600
        if 12200 < value < 13300:
            value = 12800
        general.processRECEvent(id, round(value), midi.REC_UpdateValue | midi.REC_UpdateControl | midi.REC_ShowHint)
        # value is between 0 and 25600
        event.handled = True
        return
    if event.data1 == 76:
        id = midi.REC_Chan_OfsFCut + channels.getRecEventId(channels.selectedChannel())
        value = ((event.data2 / 127) * 512) - 256
        #value2 = general.processRECEvent(id, round(value), midi.REC_GetValue)
        #print(value)
        if -12 < value < 12:
            value = 0
        general.processRECEvent(id, round(value), midi.REC_UpdateValue | midi.REC_UpdateControl | midi.REC_ShowHint)
        # value is between -256 and 256
        event.handled = True
        return
    if event.data1 == 77:
        controller.fixedvelocityvalue = event.data2
        event.handled = True
        return

# --------------------------------------------------------------------------------------------------------
#   NOTES
# --------------------------------------------------------------------------------------------------------
def OnNoteOn(event):
    if controller.shifting == 1 and event.data2 != 0:
        if event.data1 == 0:
            general.undoUp()
            event.handled = True
            return
        if event.data1 == 1:
            general.undoDown()
            event.handled = True
            return
    if controller.pattern == 1 and event.data2 != 0:
        compare_pattern = patterns.patternCount() - 1
        if event.data1 > compare_pattern:
            patterns.selectPattern(1)
            patterns.findFirstNextEmptyPat(midi.FFNEP_DontPromptName)
            device.midiOutMsg(144, 0, event.data1, 25)
            event.handled = True
            return
        patterns.jumpToPattern(event.data1 + 1)
        device.midiOutMsg(144, 0, event.data1, 25)
        event.handled = True
        return
    if controller.pattern == 1 and event.data2 == 0:
        compare_pattern = patterns.patternCount() - 1
        if event.data1 > compare_pattern:
            device.midiOutMsg(144, 0, event.data1, 0)
            event.handled = True
            return
        device.midiOutMsg(144, 0, event.data1, Lime1)
        event.handled = True
        return
    if controller.padmode == OMNI:
        realnote = cs.C5 + (controller.current_octave * 12) + controller.current_offset + 12
        index = event.data1 + (controller.channels * 16)
        if index < channels.channelCount():
            if event.data2 != 0:
                if controller.fixedvelocity == 0:
                    channels.midiNoteOn(index, realnote, event.data2)
                else:
                    channels.midiNoteOn(index, realnote, controller.fixedvelocityvalue)
                channels.selectOneChannel(index)
                channel = channels.selectedChannel()
                if plugins.isValid(channel):
                    device.midiOutMsg(144, 0, event.data1, PLUGIN_HIGHLIGHTED)
                else:
                    device.midiOutMsg(144, 0, event.data1, CHANNEL_HIGHLIGHTED)
            else:
                channels.midiNoteOn(index, realnote, 0)
        event.handled = True
        return
    elif controller.padmode == KEYBOARD:
        realnote = controller.current_group[event.data1] + (controller.current_octave * 12) + controller.current_offset + 12
        if event.data2 != 0:
            controller.last_triggered.append(realnote)
            if controller.fixedvelocity == 0:
                channels.midiNoteOn(channels.selectedChannel(), realnote, event.data2)
            else:
                channels.midiNoteOn(channels.selectedChannel(), realnote, controller.fixedvelocityvalue)
            device.midiOutMsg(144, 0, event.data1, Red1)
            event.handled = True
            return
        else:
            if realnote in controller.last_triggered:
                controller.last_triggered.remove(realnote)
            channels.midiNoteOn(channels.selectedChannel(), realnote, 0)
            device.midiOutMsg(144, 0, event.data1, 0)
            event.handled = True
            return
    elif controller.padmode == CHORDS:
        if event.data2 != 0:
            for note in cs.chdSet[controller.active_chordset][event.data1]:
                realnote = note + (controller.current_octave * 12) + controller.current_offset + 12
                if realnote not in controller.last_triggered:
                    if controller.fixedvelocity == 0:
                        channels.midiNoteOn(channels.selectedChannel(), realnote, event.data2)
                    else:
                        channels.midiNoteOn(channels.selectedChannel(), realnote, controller.fixedvelocityvalue)
                    controller.last_triggered.append(realnote)
                else:
                    controller.last_triggered.append(realnote)
            device.midiOutMsg(144, 0, event.data1, Blue1)
            event.handled = True
            return
        else:
            for note in cs.chdSet[controller.active_chordset][event.data1]:
                realnote = note + (controller.current_octave * 12) + controller.current_offset + 12
                if realnote in controller.last_triggered:
                    controller.last_triggered.remove(realnote)
                if realnote not in controller.last_triggered:
                    channels.midiNoteOn(channels.selectedChannel(), realnote, 0)
            device.midiOutMsg(144, 0, event.data1, 0)
            event.handled = True
            return
    elif controller.padmode == STEP and event.data2 != 0:
        index = event.data1 + (controller.stepchannel * 16)
        if channels.getGridBit(channels.selectedChannel(), index) == 0:
            channels.setGridBit(channels.selectedChannel(), index, 1)
            event.handled = True
            return
        channels.setGridBit(channels.selectedChannel(), index, 0)
        event.handled = True
        return

# FOR THIS CONTROLLER NOTE OFF STATUS NEVER APPEARS, INSTEAD DATA2 WITH 0 VALUE TURNS NOTES OFF
def OnNoteOff(event):
    event.handled = True
    return

def OnKeyPressure(event):
    return


def OnChannelPressure(event):
    return
