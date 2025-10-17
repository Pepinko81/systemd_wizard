#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import messagebox

def generate_service():
    name = entry_name.get().strip()
    description = entry_description.get().strip()
    exec_start = entry_exec.get().strip()
    user = entry_user.get().strip() or "root"
    working_dir = entry_workdir.get().strip() or "/"
    restart_policy = entry_restart.get().strip() or "always"

    if not name or not exec_start:
        messagebox.showerror("Грешка", "Името на услугата и командата ExecStart са задължителни.")
        return

    unit_file = f"""[Unit]
Description={description}
After=network.target

[Service]
ExecStart={exec_start}
WorkingDirectory={working_dir}
User={user}
Restart={restart_policy}

[Install]
WantedBy=multi-user.target
"""
    service_path = f"/etc/systemd/system/{name}.service"

    # Потвърждение
    if messagebox.askyesno("Потвърждение",
                           f"Ще се създаде:\n{service_path}\n\nДа се продължи ли?"):
        try:
            with open(service_path, "w") as f:
                f.write(unit_file)
            os.system("systemctl daemon-reload")
            messagebox.showinfo("Готово", f"Създаден е {service_path}")

            if messagebox.askyesno("Enable", "Да се активира ли услугата (enable)?"):
                os.system(f"systemctl enable {name}.service")

            if messagebox.askyesno("Start", "Да се стартира ли услугата (start)?"):
                os.system(f"systemctl start {name}.service")

        except PermissionError:
            messagebox.showerror("Грешка", "Нямаш права. Стартирай скрипта с sudo.")
        except Exception as e:
            messagebox.showerror("Грешка", f"Възникна проблем: {e}")

# --- Tkinter GUI ---
root = tk.Tk()
root.title("Systemd Service Creator")

tk.Label(root, text="Име на услугата (без .service):").grid(row=0, column=0, sticky="w")
entry_name = tk.Entry(root, width=40)
entry_name.grid(row=0, column=1)

tk.Label(root, text="Описание:").grid(row=1, column=0, sticky="w")
entry_description = tk.Entry(root, width=40)
entry_description.grid(row=1, column=1)

tk.Label(root, text="ExecStart команда:").grid(row=2, column=0, sticky="w")
entry_exec = tk.Entry(root, width=40)
entry_exec.grid(row=2, column=1)

tk.Label(root, text="User (празно = root):").grid(row=3, column=0, sticky="w")
entry_user = tk.Entry(root, width=40)
entry_user.grid(row=3, column=1)

tk.Label(root, text="Работна директория (празно = /):").grid(row=4, column=0, sticky="w")
entry_workdir = tk.Entry(root, width=40)
entry_workdir.grid(row=4, column=1)

tk.Label(root, text="Restart policy (празно = always):").grid(row=5, column=0, sticky="w")
entry_restart = tk.Entry(root, width=40)
entry_restart.grid(row=5, column=1)

btn_generate = tk.Button(root, text="Създай услугата", command=generate_service)
btn_generate.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
