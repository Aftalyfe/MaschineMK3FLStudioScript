MASCHINE MK3 SCRIPT for FL STUDIO MADE BY Aftalyfe

REQUIREMENTS:
- FL Studio 20.8.3 version or higher
- Controller Editor from Native Instruments installed on your machine (install it from Native Access)
- MASCHINE MK3 controller

Three files need to be downloaded to your machine to use this script: 
1) SCRIPT (device_MaschineMK3.py)
2) CHORDSETS (chordsets.py)
3) FL Studio.ncm3

HOW TO INSTALL
1) Open Controller Editor. If Maschine MK3 is not currently selected as a controller make sure to select it. Click on Edit > Open and open "FL Studio.ncm3" file. In the list of templates make sure that this one is currently selected. You can close the Controller Editor now.
2) Using the file browser in your Operating System of choice, browse to your FL Studio User data folder, usually '...Documents\Image-Line\FL Studio\Settings\Hardware\YourScriptSubFolder', where 'YourScriptSubFolder' is a sub folder you created for your script (you can name it however you want). Put BOTH of the other files (ending in .py) in this folder.
3) Open FL Studio, go to Options > MIDI Settings and find "Maschine MK3 Ctrl MIDI" in the list. Assign any input and output ports (just make sure it's the SAME NUMBER for both input and output). From the "Controller Type" dropdown list change "(generic controller)" into the new script that should appear on the right side of the dropdown menu. The name of the script is "Maschine MK3 (user)"
4) Make sure that "Enable" button is green.

Your Maschine controller is now ready for use. If nothing is lit up, hold "SHIFT" on your controller and press "CHANNEL(MIDI)". The controller should light up. If nothing happens try turning it off and on from the back of the controller.

PURPOSE:
To transfer the capability of using a Maschine controller inside Maschine software into FL Studio.

FEATURES (1.0.0)


MAIN SECTION

- "CHANNEL(MIDI)" button opens and closes Channel Rack, the button LED shows if Channel Rack is currently visible
- "PLUG-IN Instance" button opens and closes the editor window of the currently selected channel
- "ARRANGER" button opens and closes Playlist window, the button LED shows if Playlist is currently visible
- "MIXER" button opens and closes Mixer window, the button LED shows if Mixer is currently visible
- "BROWSER" button opens and closes Plugin Picker window, the button LED shows if Plugin Picker window is currently visible
- "SAMPLING" button opens and closes Browser window, the button LED shows if Browser window is currently visible (The reason that BROWSER button is not opening Browser window is that I didn't know what to do with the SAMPLING buttton, might change this later based on feedback if FL Studio API gets updated with something useful)
- LEFT and RIGHT buttons toggle between 2 knob pages, first knob page is preassigned, the second one is there so you could still assign it to other things
- "FILE(Save)" button opens the menu of the currently active window. If nothing is active opens the main file menu. If "VARIATION" button is being held while pressing this it will save the project.
- "SETTINGS" button opens and closes MIDI settings
- "AUTO" is currently inactive
- "MACRO(Set)" button is a "right click" button used primarily for opening context menus in Browser for handling samples


4D ENCODER

- Rotating encoder will do different things depending on what mode is currently active. "VOLUME", "SWING" and "TEMPO" buttons toggle between different modes. If no mode is selected the encoder is in a "free" mode that most of the time just scrolls through whatever is active.
- VOLUME mode controls channel volume of a selected channel on the channel rack (this is not the same volume that you can control from the KNOB WHEEL section)
- SWING(Position) mode controls position in the Playlist, by selecting this mode you can scroll through your song from the controller.
- TEMPO(Tune) mode will increase or decrease your BPM in values of 1 BPM

- LEFT, RIGHT, DOWN, UP will behave exactly like pressing arrow keys on your keyboard.
- Clicking the encoder will behave like pressing Enter on your keyboard
- When in Browser window you can use the encoder together with MACRO button to load samples etc.


TRANSPORT SECTION

- "RESTART(Loop)" button will switch between PATTERN and SONG mode. In future updates it will toggle the loop mode on/off while VARIATION is being held.
- "ERASE" button is behaving like pressing "Delete" on your keyboard
- "TAP" button will make it possible to "tap" define tempo.
- "FOLLOW" button is currently assigned to activating and deactivating metronome function. This might change when I find another use for it. The button LED shows if Metronome is currently active.
- "PLAY" button is starting and pausing your song. The button LED shows if FL Studio is playing something.
- "REC" button is turning the big REC button on and off. The button LED shows if recording is currently active. If VARIATION is held, this button turns precount on and off.
- "STOP" button stops the playing and brings the play arrowhead to the beginning
- "SHIFT" button unfortunately does not send any MIDI message and therefore can't be used for anything other than what it can do natively. Instead, VARIATION button is used as a shift command.


PAD MODE/KEYBOARD/CHORDS/STEP SECTION

This section will toggle between 4 different functions for the PADS.

- PAD mode is like an OMNI MODE. When PAD MODE is selected the PADS will light up according to how many channels currently exist in the project. You can select and trigger different channels by hitting the appropriate pad. Everything that is a PLUGIN by default will light up green. Everything else will light up white. If there is more than 16 channels in the project you can press any of the GROUP buttons on the left to "scroll" through different channel sets.

- KEYBOARD mode turns your PADS into notes/keys of a particular scale. They will play whatever channel is currently selected. The active scale is selected by pressing any of the 8 groups on the left. The right display will show you what scale is currently selected. Keep in mind it is possible to Octave shift and Semitone shift any scale or chord (check TOP BUTTON SECTION). There are also FPC and BATTERY scales available which although not being scales per se are premapped for use with FPC and BATTERY plugins. The last two groups are left as chromatic scales for customization purposes. It is possible to relatively easy make custom scales and chordsets by editing chordsets.py file. More on that later.

- CHORDS mode turns your PADS into predefined CHORDS. They will play whatever channel is currently selected. The active chordset is selected by pressing any of the 8 groups on the left. Keep in mind it is possible to Octave shift and Semitone shift any scale or chord (check TOP BUTTON SECTION). Since chord preferences are highly individual, lower 4 chordsets are left unchanged. It is possible to relatively easy make custom scales and chordsets by editing chordsets.py file. There will be a video tutorial on how to customize these to your own preferences.

- STEP mode turns your PADS into a Step Sequencer. Each group holds a set of 16 gridbits that can be turned on and off. The gridbits will trigger the currently selected channel. Unlike keys and chords, gridbits cannot be shifted in pitch from the controller (yet!).


TOUCHSTRIP

Touchstrip by default controls the position of the play arrowhead in the song. There are 2 more modes that are activated by pressing buttons PITCH and MOD.

- PITCH mode controls the pitch of the currently selected channel and behaves exactly like a pitch wheel (snaps back to zero when released)

- MOD mode (lol) is not handled by default because there is nothing in FL studio API to connect it directly to MOD WHEEL functionality, and besides, FL Studio does not pass MIDI CC to plugins by default, so there is no point in setting it to CC#1 anyway. Instead, what you should do to set-it-and-forget-it is you need to go into your Browser, open "Current project", open "Remote control", click on the "Omni - Mod wheel" and touch your touchstrip while MOD mode is currently ACTIVE. This will link your touchstrip in MOD mode to MOD WHEEL functionality and all you need to do now is save that project as a template and set that template to open by default whenever you load a new project.

- PERFORM(FX Select) button will link whatever channel is currently selected to whatever mixer track is currently selected. You can select both of them quickly with the 1st and 5th rotary knobs under the screens.

- NOTES button will open your Project Info settings page to quickly type in notes (see what I did there?) about the project

- LOCK button will activate and deactivate the snap-to-grid function. The button LED shows if snap-to-grid is currently active.


TOP BUTTONS SECTION

LEFT SECTION

- PRESET- will select the previous preset in a list of FL Studio presets (.fst files) for the selected channel if that channel is a plugin. It works with any native plugin and it can also work with Serum. This will be explained in a video tutorial.

- PRESET+ will select the next preset in a list of FL Studio presets (.fst files) for the selected channel if that channel is a plugin. It works with any native plugin and it can also work with Serum. This will be explained in a video tutorial.

- PROG- will send a PC (Program Control) message on the midi port 0 by default. The currently active program will be displayed in the hint bar. To make a plugin receive this message you need to set its midi in port to 0. Keep in mind that native FL Studio plugins cannot receive this message and since you can control their presets with the PRESET- and PRESET+ knobs there is no need for them to do so.

- PROG+ will send a PC (Program Control) message on the midi port 0 by default. The currently active program will be displayed in the hint bar. To make a plugin receive this message you need to set its midi in port to 0. Keep in mind that native FL Studio plugins cannot receive this message and since you can control their presets with the PRESET- and PRESET+ knobs there is no need for them to do so.

RIGHT SECTION

- OCTAVE- and OCTAVE+ will shift the notes triggered from this controller by one octave. This is limited to -3 and +3 octaves respectfully.

- SEMI- and SEMI+ will shift the notes triggered from this controller by one semitone. This is limited to -11 and +11 semitones respectfully. If they cross this limit they will reset and OCTAVE will be shifted instead.


ENCODER SECTION

- MIX. TRACK will select a mixer track and display the number of the currently selected mixer track on the screen. This will also happen when selecting the track with a mouse.

- VOLUME will set the selected mixer track volume. It will also snap to default value. It will also display the volume of the selected track with 100 being the default loudness.

- PAN will select the pan of the currently selected mixer track. It will also snap to default value. It will also display the pan of the selected track with 0 being the center value and vary between -63 and +63.

- STEREO controls the stereo separation of the currently selected mixer track. It will also snap to default value. It will also display the stereo separation of the selected track with 0 being the center value and vary between -63 and +63.

- CHAN. SEL. will select a channel from the currently available channels and display what channel is currently selected.

- CHAN. VOL. controls the volume offset of the currently selected channel. This is not the volume that is located on the Channel Rack. This is a volume that is located inside the Editor of the currently selected channel.

- CHAN.MODX is a control that makes it possible to quickly control cutoff and filtering of a channel without loading a filter anywhere. In some cases its not working as intended, this is subject to change based on the feedback.

- FIX.VEL. controls the velocity of notes when FIXED VELOCITY mode is turned on via FIXED VEL button. This applies to both KEYBOARD and CHORDS mode.


OTHER CONTROLS

- FIXED VEL button turns the fixed velocity mode on and off. The button LED shows if the mode is currently active or not.

- SCENE button selects a part of the song based on song markers. While VARIATION is being held, this button will place a "TRANSITION" marker on the current spot in the song. This is useful to quickly mark the spots in the song where there is a transition happening (e.g. going from a verse into a hook) and also to loop a particular section of the song when working on a hook part for example.

- PATTERN button turns your pads into patterns (whatever current pad mode is). By holding this button your pads will light up in a lime green color and each lit up pad will represent a pattern from your pattern list. By pressing an empty pad (a pad that is not lit) FL Studio will open an empty pattern for you to record something on it. This enables a quick workflow by laying down different patterns uninterrupted. This mode might be expanded in the future based on feedback and API changes.

- EVENTS button will open Piano Roll for the currently selected channel. Unfortunately, FL Studio API does not support things like quantization and basic Piano Roll editing. As soon as this is implemented I will update this script with new functionality.

- VARIATION(Navigate) button is essentialy a "shift" button. While holding down this button another button will change what it does. Refer to a particular button to see what it's alternative function is. The pads will also get a "shift treatment" as soon as FL Studio API gets updated.

- DUPLICATE button will copy and paste whatever is currently selected. The idea was that it works the same way like pressing Ctrl+B (that it pastes whatever is selected after the selection) but unfortunately it just drops it at the start of the song. Not sure if this is possible, subject to change.

- SELECT button will create a selection based on when it's pressed and released. For example, you could put the 4D encoder into SWING(Position) mode, press select and while it's being held scroll through the song until you reached a point where you want to stop the selection. Then you can release the button and the selection will be made. To deselect something just press this button once (for example a selection made with the SCENE button).

- SOLO button will solo the currently selected mixer track (you can use the first encoder to select what it is). It will also keep active all the tracks that the currently selected track is routed into. For example if you solo track 1 it will also keep the master track active because it is routed into it. By holding VARIATION button you can bypass this behaviour and have a "true solo" mode. Not sure if this is useful, might change this later.

- MUTE button will mute the currently selected track. While holding down VARIATION this button should work like pressing Ctrl+H. Unfortunately, this behaviour is still not supported by the API, so I tried a workaround that just sends a message to all the channels to stop all notes from being played, but it doesn't work properly. Will probably change this later.




 



