# Modern Warfare Remastered – Runtime FOV

A portable field-of-view tool for the **Call of Duty: Modern Warfare Remastered single-player campaign**. The default FOV is **90**, with a supported input range of **65–110**.

## Requirements

- Windows and **64-bit Python 3.9 or newer**.
- Download Python from [python.org](https://www.python.org/downloads/windows/). Enable the Python launcher (`py`) or add Python to PATH during installation. Run the CMD launcher again after installing Python.
- No third-party Python packages or `pip install` commands are needed.
- Administrator permission: the tool requests UAC approval so it can access a game running as administrator.

**Portable paths do not mean universal game-version support.** Only the two verified version 1.3 executable variants listed below are supported. Other executables are rejected, even if their version number looks the same.

## Installation and usage

1. Download and extract the project. Keep `MWR FOV 90.cmd` and `MWR-FOV.py` together.
2. Place them beside `h1_sp64_ship.exe`, or in an immediate subfolder of the game directory, such as `fov`. In either location, the launcher can start the game if it is not already running.
3. You can also keep the tool anywhere else. In that case, start the campaign first, then run the tool. It detects the running game's location automatically.
4. Double-click `MWR FOV 90.cmd` and approve the administrator prompt.
5. Load a mission. The console displays the detected FOV values. **Keep the tool's window open while playing.**

The launcher locates its Python script relative to its own directory, so it also works when launched from a different working directory. No username, Python installation directory, or game drive is hardcoded. Each computer still needs Python installed.

## Choosing your own FOV

1. Right-click `MWR FOV 90.cmd` and open it in a text editor, such as Notepad.
2. Find this line:

   ```bat
   set "FOV=90"
   ```

3. Replace the number with your preferred value. For example:

   ```bat
   set "FOV=105"
   ```

4. Save the file. If the tool is running, close its window and launch it again. You do not need to restart the game.

Higher values give a wider field of view. Values outside **65–110** are rejected. Run only one instance at a time. The CMD filename does not control the FOV; you may rename it to `MWR FOV.cmd` if you prefer.

You can also set the value directly from a terminal:

```bat
py -3 "D:\Tools\fov\MWR-FOV.py" --fov 105
```

If the game is not running and the tool is stored elsewhere, specify the game directory:

```bat
py -3 "D:\Tools\fov\MWR-FOV.py" --fov 90 --game-dir "D:\Games\Call of Duty Modern Warfare Remastered"
```

The CMD launcher also accepts additional arguments:

```bat
"D:\Tools\fov\MWR FOV 90.cmd" --fov 95 --game-dir "D:\Games\Call of Duty Modern Warfare Remastered"
```

For a 60-second test, add `--test`. Use `--help` to display all options.

## How it works

The tool locates and validates the `cg_fov` setting in the running `h1_sp64_ship.exe` process. It sets the current, latched, and reset values to your chosen FOV. It checks approximately every 50 milliseconds, writes only when a value differs, and verifies each write by reading the value back.

**The runtime tool does not modify the executable or game configuration files on disk.** No separate DLL mod or static executable patch is required.

Closing the console or pressing **Ctrl+C** stops enforcing the value. It does not immediately restore the previous FOV. Fully restarting the game clears the memory changes. The tool exits when the game closes.

This tool is intended only for the verified **single-player campaign**. Multiplayer is unsupported. This project does not include game files, game executables, or DRM modifications.
