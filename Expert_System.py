import tkinter as tk
from tkinter import messagebox

def diagnose(symptoms):
    score = {
        "RAM/Hardware Failure": 0,
        "Bootloader/OS Corruption": 0,
        "Power Supply Issue": 0
    }

    if symptoms["restarts"]:
        score["RAM/Hardware Failure"] += 1
    if symptoms["new_update"]:
        score["RAM/Hardware Failure"] += 1
    if symptoms["hardware_change"]:
        score["RAM/Hardware Failure"] += 1
    if symptoms["blue_screen"]:
        score["RAM/Hardware Failure"] += 1

    if symptoms["no_boot_msg"]:
        score["Bootloader/OS Corruption"] += 1
    if symptoms["new_update"]:
        score["Bootloader/OS Corruption"] += 1

    if symptoms["beep_sounds"]:
        score["Power Supply Issue"] += 1

    sorted_issues = sorted(score.items(), key=lambda x: x[1], reverse=True)
    top_issue, top_score = sorted_issues[0]

    # Explanation
    explanation = f"Most probable issue: {top_issue} (confidence score: {top_score})\n\n"
    explanation += "All Issues Ranked:\n"
    for issue, s in sorted_issues:
        explanation += f" - {issue}: {s}\n"

    # Recommendation
    if top_issue == "RAM/Hardware Failure":
        recommendation = "Recommendation: Reseat RAM, disconnect added hardware, or check BIOS beep codes."
    elif top_issue == "Bootloader/OS Corruption":
        recommendation = "Recommendation: Try repairing bootloader via recovery tools or reinstall OS."
    else:
        recommendation = "Recommendation: Check power connections, power supply unit, or battery."

    return explanation + "\n" + recommendation


def get_diagnosis():
    symptoms = {
        "restarts": var1.get(),
        "no_boot_msg": var2.get(),
        "new_update": var3.get(),
        "hardware_change": var4.get(),
        "beep_sounds": var5.get(),
        "blue_screen": var6.get()
    }

    # Convert to boolean
    symptoms = {k: (v == "yes") for k, v in symptoms.items()}

    result = diagnose(symptoms)

    # Save to file
    try:
        with open("diagnosis_report.txt", "w", encoding="utf-8") as file:
            file.write("🛠️ Computer Boot Issue Diagnosis Report\n")
            file.write("="*45 + "\n\n")
            file.write(result)
        result += "\n\n📄 Report saved to 'diagnosis_report.txt'."
    except Exception as e:
        result += f"\n\n⚠️ Failed to save report: {str(e)}"

    messagebox.showinfo("Diagnosis Result", result)


# GUI Setup
root = tk.Tk()
root.title("Expert System - Computer Issue Diagnosis")
root.geometry("500x450")

title = tk.Label(root, text="Diagnose Computer Boot Issues", font=("Segoe UI", 16, "bold"))
title.pack(pady=10)

questions = [
    "Does it restart repeatedly after turning on?",
    "Do you see a 'No bootable device' message?",
    "Did you recently install a new OS or update drivers?",
    "Did you recently change any hardware (RAM, SSD, GPU)?",
    "Do you hear continuous beeps when turning on?",
    "Does the screen go blue or crash unexpectedly?"
]

vars = []
for q in questions:
    frame = tk.Frame(root)
    frame.pack(anchor="w", padx=20, pady=5)
    label = tk.Label(frame, text=q, anchor="w", width=60, justify="left")
    label.pack(side="left")
    var = tk.StringVar(value="no")
    tk.Radiobutton(frame, text="Yes", variable=var, value="yes").pack(side="left", padx=5)
    tk.Radiobutton(frame, text="No", variable=var, value="no").pack(side="left")
    vars.append(var)

var1, var2, var3, var4, var5, var6 = vars

btn = tk.Button(root, text="Diagnose", command=get_diagnosis, bg="#6200EA", fg="white", font=("Segoe UI", 12, "bold"))
btn.pack(pady=20)

root.mainloop()
