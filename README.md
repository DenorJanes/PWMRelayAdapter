# sova_relay

Simple adapter that runs on a Raspberry Pi and controls a physical PWM relay
based on the state of a virtual Sokil relay pin.

## Project layout

```
/root/sova_relay/
├── pyproject.toml        # build configuration
├── requirements.txt      # quick install of dependencies
├── README.md             # this document
└── src/
    └── sova_relay/
        ├── __init__.py
        ├── __main__.py
        └── adapter.py    # main logic
```

## Getting started

1. **Create a virtual environment** (don't commit the venv itself):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   or build/install the package:
   ```bash
   pip install .
   ```

3. **Run the adapter**:
   ```bash
   python -m sova_relay
   ```

   The script will loop until you hit Ctrl‑C, listening on GPIO 17 and
   driving GPIO 18 with PWM.

## Packaging & Distribution

- Build a wheel:
  ```bash
  python -m build
  ```

- The resulting `.whl` file can be shipped along with a `requirements.txt` or
  used directly via `pip install sova_relay-0.1.0-py3-none-any.whl`.

> **Note:** It’s customary to add the virtual environment directory (e.g.
> `.venv/`) to `.gitignore` so it isn’t checked into source control.

## Testing

A placeholder `tests/` directory can be added and run with `pytest` if you
want to add unit tests later.

---

## Running as a systemd service

To install the adapter as a service on a systemd‑based Linux (e.g. Raspberry Pi
OS), copy the provided unit file and enable it:

```bash
sudo cp systemd/sova_relay_adapter.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sova_relay_adapter.service
sudo systemctl start sova_relay_adapter.service
```

The unit simply invokes the script inside the virtual environment created
in `/root/sova_relay`.  Adjust the paths or user if you install the project
somewhere else or run it as a non‑root account.

You can check its status with:

```bash
sudo systemctl status sova_relay_adapter.service
```

Logs are available via `journalctl -u sova_relay_adapter.service`.

## Quick install script

A helper script `install.sh` bundles the venv creation, dependency
installation and systemd setup. Ensure it is executable first (or invoke
it with `bash`):

```bash
cd /root/sova_relay
chmod +x install.sh       # only needed once if permissions were lost
./install.sh              # or `bash install.sh` if you prefer
```

It will:

1. Create/activate a `.venv` directory if needed
2. Install Python dependencies from `requirements.txt`
3. Copy the unit file, reload systemd, enable and start the service

Modify the script if you need different paths or want to run as a non‑root user.