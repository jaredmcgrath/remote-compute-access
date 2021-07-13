# Remote Compute Access

## Commands

### Restart

Windows: `Restart-Computer`

This will cause the system to reboot, which will then boot into Ubuntu through GRUB

Ubuntu: `sudo reboot`

### Wake on LAN

Syntax: `wakeonlan -i <ip_addr> <mac_addr>`

Wake desktop: `wakeonlan -i 192.168.2.128 1c:1b:0d:95:58:e9`

### Shutdown (hibernate)

From SSH within desktop Ubuntu,

- Total shutdown: `systemctl hibernate`
- Sleep (wake into same OS): `systemctl suspend`

From within desktop powershell SSH:

- `C:\Windows\System32\rundll32.exe powrprof.dll,SetSuspendState Hibernate`

### Reboot to Windows

From Ubuntu,

```bash
cd ~
sudo ./remote-compute/reboot_os.sh --item 6
```

## GRUB Entries

0. Ubuntu
1. Advanced options for Ubuntu
2. Windows UEFI bootmgfw.efi
3. Windows Boot UEFI loader
4. Windows Boots UEFI fbx64.efi
5. EFI/ubuntu/mmx64.efi
6. Windows Boot Manager (on /dev/sdb1)
7. Linux Mint 19.1 Tessa (19.1) (on /dev/sdb5)
8. Advanced options for Linux Mint 19.1 Tessa (19.1) (on /dev/sdb5)
9. UEFI Firmware Settings
