import cx_Freeze
import sys
import os

# Dependencies
build_exe_options = {
    "packages": ["pandas", "numpy", "math", "time", "random"],
    "include_files": ["all_tanks.csv"]
}

# Base for Windows GUI application (no console window)
base = None
if sys.platform == "win32":
    base = "Console"  # Use "Win32GUI" to hide console window

cx_Freeze.setup(
    name="PandorasMetalBox",
    version="1.0",
    description="Pandora's Metal Box - Tank Gacha Game",
    options={"build_exe": build_exe_options},
    executables=[cx_Freeze.Executable("main.py", base=base, target_name="PandorasMetalBox.exe")]
)