import subprocess
import shlex

# Android-App-Pakete, die du starten kannst
APPS = {
    "vlc": "org.videolan.vlc",
    "chrome": "com.android.chrome",
    "firefox": "org.mozilla.firefox",
    "termux": "com.termux",
    "whatsapp": "com.whatsapp",
    "telegram": "org.telegram.messenger",
}

def command_exists(cmd: str) -> bool:
    result = subprocess.run(
        ["bash", "-lc", f"command -v {shlex.quote(cmd)} >/dev/null 2>&1"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

def open_android_app(package: str):
    subprocess.run(
        ["am", "start", "-a", "android.intent.action.MAIN",
         "-c", "android.intent.category.LAUNCHER", package],
        check=False
    )

def open_program(name: str):
    name = name.strip().lower()

    # 1) Wenn es ein Termux-Befehl ist (z.B. nmap, python, bash)
    if command_exists(name):
        subprocess.Popen([name])
        return True

    # 2) Wenn es eine bekannte App ist
    if name in APPS:
        open_android_app(APPS[name])
        return True

    # 3) Wenn du eine App per Paketname öffnen willst
    if "." in name:
        open_android_app(name)
        return True

    return False

def clean_command(command: str) -> str:
    c = command.strip().lower()
    for prefix in ["öffne ", "open ", "start ", "starte ", "run "]:
        if c.startswith(prefix):
            return c[len(prefix):].strip()
    return c

print("Termux Programm-Öffner")
print("Beispiele: 'öffne vlc', 'öffne nmap', 'öffne chrome'")
print("Beenden mit: 'beenden'")

while True:
    cmd = input("\nBefehl: ").strip()

    if not cmd:
        continue

    if cmd.lower() in ["beenden", "exit", "quit"]:
        print("Programm beendet.")
        break

    target = clean_command(cmd)

    if open_program(target):
        print(f"Öffne: {target}")
    else:
        print(f"Programm oder App nicht gefunden: {target}")
        print("Versuche: öffne vlc, öffne chrome, öffne nmap")
