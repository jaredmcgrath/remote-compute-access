# Ubuntu-app

This is a webserver that manages all functionality that needs to be located on Ubuntu.
This includes rebooting into a different OS.

## Installation

Install this app as a systemd service.

We assume this directory is located at `/home/jared/remote-compute-access/ubuntu-app`.

1. Copy the service file to systemd

```bash
sudo cp ./ubuntu-app.service /etc/systemd/system/
```

2. Make sure it is readable/writeable/executable by root

```bash
sudo chmod u+rwx /etc/systemd/system/ubuntu-app.service
```

3. Now enable the service with a systemd command:

```bash
sudo systemctl enable ubuntu-app
```

4. To stop the service:

```bash
sudo systemctl stop ubuntu-app
```
