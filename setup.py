from cx_Freeze import setup, Executable
import os
import sys

# 현재 스크립트의 디렉터리 얻기
base_path = os.path.dirname(os.path.abspath(__file__))

include_files = [
    os.path.join(base_path, "config.ini"),
    os.path.join(base_path, "meteor_dodger.ico"),
    (os.path.join(base_path, "img/"), "img"),
    (os.path.join(base_path, "font/"), "font"),
    (os.path.join(base_path, "sound/"), "sound")
]

options = {
    "build_exe": {
        "packages": ['os', 'sys', 'pygame', 'random', 'math', 'time'],
        "include_files": include_files,
        "includes": [],
    }
    
}
base = "Win32GUI" if sys.platform == "win32" else None
executables = [
    Executable(
        "main.py",
        base="Win32GUI",
        icon="meteor_dodger.ico",
    )
]

setup(
    name="meteor_dodger",
    version="1.0",
    description="A game where a spaceship shoots missiles at asteroids and dodges them.",
    options=options,
    executables=executables,
)
