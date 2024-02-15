# batocera_notify

Built to display a window with an image and text for notifications sent from
something like Home Assistant on your network.

There are probabally better ways to do this but was built to work without
needing anything not availible on default Batocera install.

Uses python socket to listen for notifications on port 65432

Notifactions are expected in utf-8 in url;Title;Text format (see client.py example)

Notifications are displayed using Pygame

## Security Warning

The notifcations are sent in clear text and there is no authentication for
accepting connections

- Don't run this unless you are comfortable with any device on your network
  having access
- Don't run this unless you are comfortable with any device on your network
  potentially seeing the notifcation information

## Instructions

This can all be done with a shell script called by Batocera's startup script

Set the Display environmental variable `export DISPLAY=:0`

Copy `notify.py` and `display_script.py` to `/userdata/system` on the Batocera box
Example using scp

```bash
scp notify.py root@your-batocera:notify.py
scp display_script.py root@your-batocera:display_script.py
```

Set the permissions on both scripts to allow exectution

```bash
chmod +x notify.py
chmod +x display_script.py
```

Start the script

`./notify.py &`

## Sending a notifications

### Using Python

Once the script is running the `client.py` script shows an example of how to
send a notification from a remote computer. The notifcation consists of a url to
an image that the Batocera box has access to download with a web request, a
Title heading and a text line.

Edit the `client.py` script and add your Batocera boxes address and the url, Title
and text for your notfication and run the script.

### Simple Home Assistant Example

This is the simplest way to test that things are working.

First copy the `ha_batocera_notify.py` script to somewhere Home Assistant can access
it and make sure it has execute permissions.

Then add a `shell_command` entry to the Home Assistant `configuration.yaml` adding
your Batocera and Home Assistant address information.

```yaml
shell_command:
  batocera_notification: "/config/ha_batocera_notify.py <BATOCERA ADDRESS> 65432 'http://<HOME ASSISTANT ADDRESS:8123/local/<YOUR PNG IMAGE";Home Assistant;Hello World'"
```

Restart Home Assistant (reloading the YAML config files option does not appear
to work for changes to `configuration.yaml`)

Go to Developer Tools --> Services and find the "Shell Command:
batocera_notification" service

Click the Call Service button

Assuming everything is setup correctly and the `notify.py` script is running on
your Batocera box the notifcation should go through.

See the [Home Assistant Shell Command integration documentation](https://www.home-assistant.io/integrations/shell_command/#examples)
for more advanced automation examples
