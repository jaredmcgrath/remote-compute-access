# Raspi-app

This is a webserver that manages the critical functionality for the remote-compute-access system. All functionality that requires a device with a LAN connection happens here.

## Installation

Install this app as a systemd service.

We assume this directory is located at `/home/jared/remote-compute-access/raspi-app`.

1. Copy the service file to systemd

```bash
sudo cp ./raspi-app.service /etc/systemd/system/
```

2. Make sure it is readable/writeable/executable by root

```bash
sudo chmod u+rwx /etc/systemd/system/raspi-app.service
```

3. Now enable the service with a systemd command:

```bash
sudo systemctl enable raspi-app
```

4. To stop the service:

```bash
sudo systemctl stop raspi-app
```
