#!/usr/bin/env python3
import os

print("=== Systemd Service Wizard ===")

# Събиране на данни от потребителя
name = input("Service name (без .service): ").strip()
description = input("Описание: ").strip()
exec_start = input("Команда за стартиране (ExecStart): ").strip()
user = input("User (празно = root): ").strip() or "root"
working_dir = input("Работна директория (празно = /): ").strip() or "/"
restart_policy = input("Restart policy (празно = always): ").strip() or "always"

# Генериране на съдържанието на .service файла
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

# Път до файла
service_path = f"/etc/systemd/system/{name}.service"

print("\nЩе се създаде файл:")
print(service_path)
print("\n--- Service file content ---")
print(unit_file)

confirm = input("\nДа се запише ли този файл? (y/n): ").lower()
if confirm == "y":
    try:
        # Писане на файла
        with open(service_path, "w") as f:
            f.write(unit_file)
        print(f"\nФайлът {service_path} е създаден успешно.")

        # Релоуд и enable
        os.system("systemctl daemon-reload")
        enable = input("Да се активира ли услугата (enable)? (y/n): ").lower()
        if enable == "y":
            os.system(f"systemctl enable {name}.service")
            print(f"Услугата {name} е активирана.")
        start = input("Да се стартира ли услугата (start)? (y/n): ").lower()
        if start == "y":
            os.system(f"systemctl start {name}.service")
            print(f"Услугата {name} е стартирана.")
    except PermissionError:
        print("\n⚠️ Нямаш права. Стартирай скрипта с sudo.")
else:
    print("\nОтказано.")
