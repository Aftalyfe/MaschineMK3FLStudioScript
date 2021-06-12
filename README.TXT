MASCHINE MK3 SCRIPT for FL STUDIO MADE BY Aftalyfe

PURPOSE:
To transfer the capability of using a Maschine controller inside Maschine software into FL Studio.

FEATURES (1.0.0)

MAIN SECTION

- "CHANNEL(MIDI)" button opens and closes Channel Rack, the button LED shows if Channel Rack is currently visible
- "PLUG-IN Instance" button opens and closes the editor window of the currently selected channel
- "ARRANGER" button opens and closes Playlist window, the button LED shows if Playlist is currently visible
- "MIXER" button opens and closes Mixer window, the button LED shows if Mixer is currently visible
- "BROWSER" button opens and closes Plugin Picker window, the button LED shows if Plugin Picker window is currently visible
- "SAMPLING" button opens and closes Browser window, the button LED shows if Browser window is currently visible (The reason that BROWSER button is not opening Browser window is that I didn't know what to do with the SAMPLING buttton, might change this later if FL Studio API gets updated with something useful)
- LEFT and RIGHT buttons toggle between 2 knob pages, first knob page is preassigned, the second one is there so you could still assign it to other things
- "FILE(Save)" button opens the menu of the currently active window. If nothing is active opens the main file menu. If "VARIATION" button is being held while pressing this it will save the project.
- "SETTINGS" button opens and closes MIDI settings
- "AUTO" is currently inactive
- "MACRO(Set)" button is a "right click" button used primarily for opening context menus in Browser for handling samples

4D ENCODER

- Rotating encoder will do different things depending on what mode is currently active. "VOLUME", "SWING" and "TEMPO" buttons toggle between different modes. If no mode is selected the encoder is in a "free" mode that most of the time just scrolls through whatever is active.
- VOLUME mode controls channel volume of a selected channel on the channel rack (this is not the same volume that you can control from the KNOB WHEEL section)
