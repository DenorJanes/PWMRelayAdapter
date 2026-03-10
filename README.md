# sova_relay

Simple adapter that runs on a Raspberry Pi and controls a physical PWM relay
based on the state of a virtual Sokil relay pin.

## Quick install script

A helper script `install.sh` bundles the venv creation, dependency
installation and systemd setup. Ensure it is executable first (or invoke
it with `bash`):

```bash
chmod +x install.sh       # only needed once if permissions were lost
./install.sh              # or `bash install.sh` if you prefer
```

It will:

1. Create/activate a `.venv` directory if needed
2. Install Python dependencies from `requirements.txt`
3. Install the project package into the venv (so `python -m sova_relay` works)
4. Copy the unit file, reload systemd, enable and start the service

You can run the adapter manually with:

```bash
# after running install.sh or installing the package yourself
# (be sure to activate the virtual environment first)
source .venv/bin/activate    # or "venv" depending on your shell
python -m sova_relay
```

Modify the script if you need different paths or want to run as a non‑root user.