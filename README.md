# batocera_notify

## Update

Started working on this, but really the best approach would be something in a container like some of the other projects adding onto Batocera. This does work, but isn't the best approach.

---

Built to display a window with an image and text for notifications sent from something like Home Assistant on your network.

The goal was to get something running with zero extra dependencies beyond what ships on a stock Batocera install.

- Listens for notifications over a plain TCP socket on **port 65432**.
- Expect messages in **UTF‑8** using the format `image_url;Title;Body` (see `client.py`).
- Renders the notification using **Pygame**.

---

## Security warning

These notifications are unencrypted and unauthenticated. **Anyone on your LAN can send anything to the box and whatever they send will be displayed.** Only run this if you are comfortable with that.

---

## Installation / Usage

### 1 – Quick manual test

If you just want to see it work once‑off:

```bash
# on the Batocera box
export DISPLAY=:0
scp notify.py display_script.py root@batocera:/userdata/system/
chmod +x /userdata/system/notify.py /userdata/system/display_script.py

# still on the Batocera box
cd /userdata/system
./notify.py &
```

Now fire up `client.py` (or the Home‑Assistant shell_command shown below) from another machine and you should get a pop‑up.

### 2 – Run automatically at boot (contribution from **@Selim042**)

Thanks to [@Selim042](https://github.com/daviddever/batocera_notify/issues/1) for working this out and writing it up.

1. **Create a tiny service script** at `/userdata/system/services/notifications`:

   ```bash
   #!/bin/bash
   export DISPLAY=:0
   /userdata/system/services/notify.py &
   ```

2. **Copy the project files** into that same folder:

   ```bash
   cp notify.py display_script.py /userdata/system/services/
   ```

3. **Mark everything executable** so Batocera will run it:

   ```bash
   chmod +x /userdata/system/services/{notifications,notify.py,display_script.py}
   ```

4. Reboot (or run `batocera-services restart`) and the notification service will be active from then on.

> **Heads‑up – quirks we noticed**\
> • The two Python files have to live in `/userdata/system/services/`; placing them in `/userdata/system` breaks their relative imports.\
> • Batocera complains about the “improperly named services” (because the files end in `.py`), but the service still works and the errors are not shown in the UI.

---

## Sending a notification

### Using Python

`client.py` shows a minimal example that connects to the socket and writes one message:

```python
# edit these first
BATOCERA_IP = "192.168.1.123"
PORT        = 65432

IMAGE_URL = "http://…/picture.png"
TITLE      = "Hello from Python"
BODY       = "It worked!"
```

Run the script and a pop‑up should appear on‑screen.

### From Home Assistant (shell_command)

1. Copy `ha_batocera_notify.py` somewhere HA can execute it (e.g. `/config/`).
2. In `configuration.yaml` add:

   ```yaml
   shell_command:
     batocera_notification: >-
       /config/ha_batocera_notify.py 192.168.1.123 65432 \
       'http://homeassistant.local:8123/local/example.png;Home Assistant;Hello World'
   ```

3. Restart HA, then call the `shell_command.batocera_notification` service from Developer Tools to test.
