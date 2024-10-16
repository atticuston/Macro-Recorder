# Macro-Recorder
Uhh free project to record and then replay key strokes (yes that includes mouse movement and clicks) in an open source python script (report issues if you want i might fix them probably not as i made this as a time saver)
**Steps to use this:**
1. Install python (if already installed you're good):
```https://www.python.org/```
2. Install Required Libraries:
```pip install pynput```
pickle and tkinter are pre installed in python (i think)
3. Run the project
```python macro_recorder.py```

**How to use each button (no way in fucking hell i'm adding gui dyi job for you to do :D)**
Start Recording

    What it does: Begins recording your mouse movements and keyboard presses after a short wait time (if you set one).

Stop Recording

    What it does: Stops the recording process.

Replay Actions

    What it does: Plays back the actions you recorded. You can choose how many times to repeat the recording witht eh loop count below.

Set Loop Count

    What it does: Lets you decide how many times to repeat the recorded actions. A box will pop up asking for a number.

Set Start Delay (ms)

    What it does: Allows you to set a wait time before starting the recording. You enter this time in milliseconds.

Set Replay Delay (ms)

    What it does: Lets you set a pause before the recorded actions play back. Enter the delay in milliseconds.

Save Actions

    What it does: Saves your recorded actions to a file named actions.pkl, so you can use them later.

Load Actions

    What it does: Opens previously saved actions from the actions.pkl file. If there are no saved actions, you'll see an error message.

Edit Action

    What it does: Allows you to change a specific recorded action (this feature needs to be added based on what you need).

Delete Action

    What it does: Removes a selected action from the list of recorded actions (this feature needs to be added based on what you need).

Duplicate Action

    What it does: Creates a copy of a selected action.

Add Custom Action

    What it does: Lets you add a new action manually (probably the most buggy feature in the entire code and NO i'm not gonna fix it).

Hide Actions

    What it does: Hides specific actions from view based on the rules you set.

Unhide Actions

    What it does: Shows hidden actions again so you can see them duh.

**Thanks to Chatgpt for making my code not look like it came straight out of shreks insides it made it actually readable and probably fixed some errors and changed names of my lazy variables so it's easy to understand.**
