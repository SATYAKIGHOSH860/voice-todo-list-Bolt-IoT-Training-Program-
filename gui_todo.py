import tkinter as tk
from tkinter import messagebox
import json
import os
import pyttsx3
import speech_recognition as sr

# ========== Setup ==========

engine = pyttsx3.init()
engine.setProperty('rate', 175)

def speak(text):
    engine.say(text)
    engine.runAndWait()

recognizer = sr.Recognizer()
mic = sr.Microphone()

# ========== Data File Setup ==========
if not os.path.exists("todo_data.json"):
    with open("todo_data.json", "w") as f:
        json.dump({}, f)

with open("todo_data.json", "r") as f:
    tasks = json.load(f)

categories = ["Personal", "Work", "Shopping", "Others"]

# ========== Voice Input ==========
def take_voice_input():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        speech = recognizer.recognize_google(audio)
        return speech
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""

# ========== Task Functions ==========

def add_task():
    category = category_var.get()
    task = task_entry.get()

    if not task:
        speak("Please enter a task.")
        return

    if category not in tasks:
        tasks[category] = []

    tasks[category].append(task)
    save_tasks()
    speak(f"Task added in {category}")
    task_entry.delete(0, tk.END)
    list_tasks()

def delete_task():
    category = category_var.get()
    task = task_entry.get()

    if category in tasks and task in tasks[category]:
        tasks[category].remove(task)
        save_tasks()
        speak(f"Task removed from {category}")
    else:
        speak("Task not found.")
    task_entry.delete(0, tk.END)
    list_tasks()

def list_tasks():
    output_box.delete('1.0', tk.END)
    for category, task_list in tasks.items():
        output_box.insert(tk.END, f"{category}:\n")
        for task in task_list:
            output_box.insert(tk.END, f" - {task}\n")
        output_box.insert(tk.END, "\n")

def save_tasks():
    with open("todo_data.json", "w") as f:
        json.dump(tasks, f, indent=4)

def add_task_voice():
    speak("Say the task.")
    task = take_voice_input()
    task_entry.delete(0, tk.END)
    task_entry.insert(0, task)
    add_task()


def list_tasks_voice():
    if not tasks:
        speak("You have no tasks.")
        return

    for category, task_list in tasks.items():
        if task_list:
            speak(f"In {category} category, you have:")
            for task in task_list:
                speak(task)
        else:
            speak(f"No tasks in {category} category.")

def delete_task_voice():
    speak("Say the task you want to delete.")
    task = take_voice_input()

    found = False
    for category, task_list in tasks.items():
        if task in task_list:
            task_list.remove(task)
            found = True
            speak(f"Deleted {task} from {category}")
            break

    if not found:
        speak("Task not found.")
   
    save_tasks()
    list_tasks()


# ========== GUI Setup ==========

root = tk.Tk()
root.title("Voice-Controlled To-Do List")

# Dropdown for categories
category_var = tk.StringVar(value=categories[0])
tk.Label(root, text="Category").grid(row=0, column=0, padx=5, pady=5)
tk.OptionMenu(root, category_var, *categories).grid(row=0, column=1, padx=5, pady=5)

# Entry for task
tk.Label(root, text="Task").grid(row=1, column=0, padx=5, pady=5)
task_entry = tk.Entry(root, width=30)
task_entry.grid(row=1, column=1, padx=5, pady=5)

# Buttons
tk.Button(root, text="Add Task", command=add_task).grid(row=2, column=0, padx=5, pady=5)
tk.Button(root, text="Add via Voice", command=add_task_voice).grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Delete Task", command=delete_task).grid(row=3, column=0, padx=5, pady=5)
tk.Button(root, text="List Tasks", command=list_tasks).grid(row=3, column=1, padx=5, pady=5)
tk.Button(root, text="List Tasks via Voice", command=list_tasks_voice).grid(row=5, column=0, padx=5, pady=5)
tk.Button(root, text="Delete Task via Voice", command=delete_task_voice).grid(row=5, column=1, padx=5, pady=5)

# Output display
output_box = tk.Text(root, height=10, width=50)
output_box.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

list_tasks()
root.mainloop()
