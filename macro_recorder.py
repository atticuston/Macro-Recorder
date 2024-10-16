#Copyright © 2024 Atticus

#This code is free to use, modify, and distribute by anyone. There are no restrictions on its usage, and you are welcome to do whatever you like with it. However, please acknowledge the original author, Atticus, when using or redistributing this code.

#No warranty is provided, and the author (me :D) is not liable for any damages that may arise from the use of this code, this is simply a project i did for fun and to automate some stuff the chances of me updating anything are really slim.

#I LOVE AI SO MUCH IF NOT IT THIS CODE WOULD LOOK LIKE A SEVERE DISORDER OF SHREKS HOUSE THANKS TO IT IT'S ACTUALLY READABLE (NOT LIKE MOST OF MY CODE) SO YEA ENJOY :D
import time
import pynput
from pynput.mouse import Listener as MouseListener, Button
from pynput.keyboard import Listener as KeyboardListener, Key
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pickle
import os
import threading

# FUCKING HATE CLASSES FUCK THEM
class ActionRecorder:
    def __init__(self):
        self.actions = []  # Store the recorded actions
        self.hidden_actions = set()  # Store the types of hidden actions
        self.start_time = None # Start time of recording
        self.recording = False # The variable that determines if it records or not (default is false)
        self.pressed_keys = {}  # Track the keys (now that i think about it this is pretty much a good version of a keylogger)
        self.record_delay = 0  # Delay before recording in ms (default 0 because fuck you)
        self.replay_delay = 0 # Same shit i ain't explaining it again

    def start_rec(self):
        self.actions = []
        self.start_time = time.time() + (self.record_delay / 1000)  # Apply the start delay of the recording transfers from mili seconds to seconds
        self.recording = True
        self.mouse_listener = MouseListener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll)
        self.keyboard_listener = KeyboardListener(on_press=self.on_key_press, on_release=self.on_key_release)
        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.display_delay_warning()

    def stop_rec(self):
        if self.recording:
            self.mouse_listener.stop()
            self.keyboard_listener.stop()
            self.recording = False

    def display_delay_warning(self):
        if self.record_delay > 0:
            messagebox.showinfo("Delay", f"Recording will start in {self.record_delay} milliseconds hurry up and close the window :D")
        if self.replay_delay > 0:
            messagebox.showinfo("Delay", f"Replay will start in {self.replay_delay} milliseconds hurry up and close the window :D")

    def on_click(self, x, y, button, pressed):
        try:
            action_time = time.time() - self.start_time
            if pressed:
                self.pressed_keys[str(button)] = action_time  # The actual tracker of the pressed key
            else:
                duration = (action_time - self.pressed_keys.pop(str(button), action_time)) * 1000 
                action = {
                    'type': 'mouse_click',
                    'button': str(button),
                    'position': (x, y),
                    'pressed': False,
                    'time': action_time,
                    'duration': duration
                }
                self.actions.append(action)
        except Exception as e:
            self.handle_error(e)

    def on_move(self, x, y):
        try:
            action_time = time.time() - self.start_time
            action = {
                'type': 'mouse_move',
                'position': (x, y),
                'time': action_time
            }
            self.actions.append(action)
        except Exception as e:
            self.handle_error(e)

    def on_scroll(self, x, y, dx, dy):
        try:
            action_time = time.time() - self.start_time
            action = {
                'type': 'mouse_scroll',
                'position': (x, y),
                'scroll': (dx, dy),
                'time': action_time
            }
            self.actions.append(action)
        except Exception as e:
            self.handle_error(e)

    def on_key_press(self, key):
        try:
            action_time = time.time() - self.start_time
            if key not in self.pressed_keys:
                self.pressed_keys[key] = action_time
            action = {
                'type': 'key_press',
                'key': str(key),
                'time': action_time
            }
            self.actions.append(action)
        except Exception as e:
            self.handle_error(e)

    def on_key_release(self, key):
        try:
            action_time = time.time() - self.start_time
            duration = (action_time - self.pressed_keys.pop(key, action_time)) * 1000
            action = {
                'type': 'key_release',
                'key': str(key),
                'time': action_time,
                'duration': duration
            }
            self.actions.append(action)
        except Exception as e:
            self.handle_error(e)

    def handle_error(self, error):
        print(f"Error detected: {error} you can fix it yourself or report it (prob ain't gonna do shit about it)")

# ANOTHER CLASS FUCKING HATE THEM
class ActionReplayer:
    def __init__(self, actions, hidden_actions=set(), loop_count=1):
        self.actions = actions
        self.hidden_actions = hidden_actions
        self.loop_count = loop_count
        self.mouse = MouseController()
        self.keyboard = KeyboardController()

    def replay_actions(self):
        for _ in range(self.loop_count):
            previous_time = 0
            for action in self.actions:
                try:
                    if action['type'] in self.hidden_actions:
                        continue
                    delay = max(action['time'] - previous_time, 0) # Makes it so the delay cannot be - (i think)
                    time.sleep(delay)
                    previous_time = action['time']

                    if action['type'] == 'mouse_click':
                        x, y = action['position']
                        self.mouse.position = (x, y)
                        if action['pressed']:
                            self.mouse.press(getattr(Button, action['button'].split('.')[-1]))
                        else:
                            self.mouse.release(getattr(Button, action['button'].split('.')[-1]))
                            time.sleep(action.get('duration', 0) / 1000)

                    elif action['type'] == 'mouse_move':
                        x, y = action['position']
                        self.mouse.position = (x, y)

                    elif action['type'] == 'mouse_scroll':
                        dx, dy = action['scroll']
                        self.mouse.scroll(dx, dy)

                    elif action['type'] == 'key_press':
                        key = self._get_key(action['key'])
                        self.keyboard.press(key)

                    elif action['type'] == 'key_release':
                        key = self._get_key(action['key'])
                        self.keyboard.release(key)
                        time.sleep(action.get('duration', 0) / 1000)  # key hold duration nothing much

                except Exception as e:
                    print(f"Error during replay: {e}")

    def _get_key(self, key_string):
        try:
            if 'Key.' in key_string:
                return getattr(Key, key_string.split('.')[1])
            else:
                return key_string.strip("'")
        except AttributeError:
            return key_string

# FUCK CLASSES MAN TOO MUCH
class ActionGUI(tk.Tk):
    def __init__(self, recorder):
        super().__init__()
        self.recorder = recorder
        self.loop_count = 1  # Default loop count is 1 cuz u wanna be able to control your shit (i think)
        self.hidden_actions = set()
        self.title("Action Recorder")
        self.geometry("1575x500")
        self.create_widgets()

    def create_widgets(self):
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=('Type', 'Details', 'Time', 'Duration'))
        self.tree.heading('#0', text='ID')
        self.tree.heading('Type', text='Action Type')
        self.tree.heading('Details', text='Details')
        self.tree.heading('Time', text='Time')
        self.tree.heading('Duration', text='Duration (ms)')
        self.tree.column('#0', width=50)
        self.tree.column('Type', width=100)
        self.tree.column('Details', width=400)
        self.tree.column('Time', width=100)
        self.tree.column('Duration', width=100)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the Treeview
        self.scrollbar = tk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Control buttons
        self.record_button = tk.Button(self, text="Start Recording", command=self.start_rec)
        self.stop_button = tk.Button(self, text="Stop Recording", command=self.stop_rec)
        self.replay_button = tk.Button(self, text="Replay Actions", command=self.replay_actions)
        self.save_button = tk.Button(self, text="Save Actions", command=self.save_actions)
        self.load_button = tk.Button(self, text="Load Actions", command=self.load_actions)
        self.loop_button = tk.Button(self, text="Set Loop Count", command=self.set_loop_count)
        self.start_delay_button = tk.Button(self, text="Set Start Delay (ms)", command=self.set_start_delay)
        self.record_delay_button = tk.Button(self, text="Set Replay Delay (ms)", command=self.set_replay_delay)

        self.record_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.replay_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.load_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.loop_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.start_delay_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.record_delay_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.edit_button = tk.Button(self, text="Edit Action", command=self.edit_action)
        self.delete_button = tk.Button(self, text="Delete Action", command=self.delete_action)
        self.duplicate_button = tk.Button(self, text="Duplicate Action", command=self.duplicate_action)
        self.add_button = tk.Button(self, text="Add Custom Action", command=self.add_custom_action)

        self.edit_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.delete_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.duplicate_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.hide_button = tk.Button(self, text="Hide Actions", command=self.hide_actions)
        self.unhide_button = tk.Button(self, text="Unhide Actions", command=self.unhide_actions)

        self.hide_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.unhide_button.pack(side=tk.LEFT, padx=10, pady=10)


    def start_rec(self):
        self.recorder.start_rec()
        self.update_action_list()

    def stop_rec(self):
        self.recorder.stop_rec()
        self.update_action_list()

    def replay_actions(self):
        if self.recorder.actions:
            replayer = ActionReplayer(self.recorder.actions, hidden_actions=self.hidden_actions, loop_count=self.loop_count)
            threading.Thread(target=replayer.replay_actions).start()

    def save_actions(self):
        with open('actions.pkl', 'wb') as f:
            pickle.dump(self.recorder.actions, f)
        with open('hidden_actions.pkl', 'wb') as f:
            pickle.dump(self.hidden_actions, f)

    def load_actions(self):
        if os.path.exists("actions.pkl"):
            with open("actions.pkl", "rb") as f:
                self.recorder.actions = pickle.load(f)
            self.update_action_list()
        else:
            messagebox.showerror("Error", "No saved actions found!")

    def set_loop_count(self):
        loop_count_str = tk.simpledialog.askstring("Input", "Enter loop count:", parent=self)
        if loop_count_str and loop_count_str.isdigit():
            self.loop_count = int(loop_count_str)

    def set_start_delay(self):
        delay_str = tk.simpledialog.askstring("Input", "Enter delay before recording (ms):", parent=self)
        if delay_str and delay_str.isdigit():
            self.recorder.record_delay = int(delay_str)

    def set_replay_delay(self):
        delay_str = tk.simpledialog.askstring("Input", "Enter delay before replaying (ms):", parent=self)
        if delay_str and delay_str.isdigit():
            self.recorder.replay_delay = int(delay_str)

    def update_action_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for idx, action in enumerate(self.recorder.actions):
            if action['type'] not in self.hidden_actions:
                details = action.get('position', '') if action['type'] in ['mouse_click', 'mouse_move'] else action.get('key', '')
                duration = action.get('duration', '')
                self.tree.insert('', 'end', text=str(idx), values=(action['type'], details, round(action['time'], 3), duration))

    def hide_actions(self):
        action_type = self.ask_for_input("Hide Actions", "Action Type to Hide:")
        self.hidden_actions.add(action_type)
        self.update_action_list()


    def edit_action(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = int(self.tree.item(selected_item, 'text'))
            action = self.recorder.actions[item_id]
            new_time = float(self.ask_for_input("Edit Action", f"New time for {action['type']} (current: {action['time']}):"))
            action['time'] = new_time
            self.update_action_list()
        if not selected_item:
            messagebox.showerror("Error", "No action selected for editing.")
            return

        selected_idx = int(selected_item[0])
        action = self.recorder.actions[selected_idx]

        action_type = action['type']
        if action_type == 'mouse_click':
            button = action['button']
            position = action['position']
            duration = action.get('duration', 0)

            new_button = tk.simpledialog.askstring("Edit Action", "Enter new button:", initialvalue=button, parent=self)
            new_position = tk.simpledialog.askstring("Edit Action", "Enter new position (x,y):", initialvalue=f"{position[0]},{position[1]}", parent=self)
            new_duration = tk.simpledialog.askstring("Edit Action", "Enter new duration (ms):", initialvalue=str(duration), parent=self)

            if new_button and new_position and new_duration:
                try:
                    x, y = map(int, new_position.split(','))
                    action['button'] = new_button
                    action['position'] = (x, y)
                    action['duration'] = int(new_duration)
                    self.update_action_list()
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please try again.")

        elif action_type == 'mouse_move':
            position = action['position']
            new_position = tk.simpledialog.askstring("Edit Action", "Enter new position (x,y):", initialvalue=f"{position[0]},{position[1]}", parent=self)
            if new_position:
                try:
                    x, y = map(int, new_position.split(','))
                    action['position'] = (x, y)
                    self.update_action_list()
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please try again.")

        elif action_type == 'key_press' or action_type == 'key_release':
            key = action['key']
            new_key = tk.simpledialog.askstring("Edit Action", "Enter new key:", initialvalue=key, parent=self)
            if new_key:
                action['key'] = new_key
                self.update_action_list()

    def delete_action(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = int(self.tree.item(selected_item, 'text'))
            del self.recorder.actions[item_id]
            self.update_action_list()

    def duplicate_action(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = int(self.tree.item(selected_item, 'text'))
            action = self.recorder.actions[item_id].copy()
            self.recorder.actions.append(action)
            self.update_action_list()

    def unhide_actions(self):
        self.hidden_actions.clear()
        self.update_action_list()

    def add_custom_action(self):
        action_type = tk.simpledialog.askstring("Add Custom Action", "Enter action type (mouse_click, mouse_move, key_press, key_release):", parent=self)
        if action_type not in ['mouse_click', 'mouse_move', 'key_press', 'key_release']:
            messagebox.showerror("Error", "Invalid action type. Please enter one of the following: mouse_click, mouse_move, key_press, key_release.")
            return

        if action_type == 'mouse_click':
            button = tk.simpledialog.askstring("Add Custom Action", "Enter mouse button (left, right, middle):", parent=self)
            position = tk.simpledialog.askstring("Add Custom Action", "Enter position (x,y):", parent=self)
            duration = tk.simpledialog.askstring("Add Custom Action", "Enter duration (ms):", parent=self)

            if button and position and duration:
                try:
                    x, y = map(int, position.split(','))
                    action = {
                        'type': 'mouse_click',
                        'button': button,
                        'position': (x, y),
                        'pressed': False,
                        'time': 0, 
                        'duration': int(duration)
                    }
                    self.recorder.actions.append(action)
                    self.update_action_list()
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please try again.")

        elif action_type == 'mouse_move':
            position = tk.simpledialog.askstring("Add Custom Action", "Enter position (x,y):", parent=self)
            if position:
                try:
                    x, y = map(int, position.split(','))
                    action = {
                        'type': 'mouse_move',
                        'position': (x, y),
                        'time': 0,
                    }
                    self.recorder.actions.append(action)
                    self.update_action_list()
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please try again.")

        elif action_type == 'key_press':
            key = tk.simpledialog.askstring("Add Custom Action", "Enter key:", parent=self)
            action = {
                'type': 'key_press',
                'key': key,
                'time': 0,
            }
            self.recorder.actions.append(action)
            self.update_action_list()

        elif action_type == 'key_release':
            key = tk.simpledialog.askstring("Add Custom Action", "Enter key:", parent=self)
            duration = tk.simpledialog.askstring("Add Custom Action", "Enter duration (ms):", parent=self)
            if duration:
                action = {
                    'type': 'key_release',
                    'key': key,
                    'time': 0,
                    'duration': int(duration)
                }
                self.recorder.actions.append(action)
                self.update_action_list()

    def toggle_hidden(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No action selected.")
            return

        selected_idx = int(selected_item[0])
        action = self.recorder.actions[selected_idx]
        action_type = action['type']

        if action_type in self.hidden_actions:
            self.hidden_actions.remove(action_type)
            messagebox.showinfo("Unhide", f"{action_type} action unhidden.")
        else:
            self.hidden_actions.add(action_type)
            messagebox.showinfo("Hide", f"{action_type} action hidden.")
        
        self.update_action_list()  # UHH reloads the list after hiding/unhiding

    def ask_for_input(self, title, prompt):
        input_window = tk.Toplevel(self)
        input_window.title(title)
        input_window.geometry("300x100")
        label = tk.Label(input_window, text=prompt)
        label.pack(pady=5)
        entry = tk.Entry(input_window)
        entry.pack(pady=5)
        input_value = tk.StringVar()

        def submit_input():
            input_value.set(entry.get())
            input_window.destroy()

        submit_button = tk.Button(input_window, text="Submit", command=submit_input)
        submit_button.pack(pady=5)
        input_window.wait_window()
        return input_value.get()

# Maybe the thing that makes the whole project work
if __name__ == "__main__":
    recorder = ActionRecorder()
    gui = ActionGUI(recorder)
    gui.mainloop()
