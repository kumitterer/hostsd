# hostsd - A simple hosts file manager

[![Support Private.coffee!](https://shields.private.coffee/badge/private.coffee-support%20us!-pink?logo=coffeescript)](https://private.coffee)
[![PyPI](https://shields.private.coffee/pypi/v/hostsd)](https://pypi.org/project/hostsd/)
[![PyPI - Python Version](https://shields.private.coffee/pypi/pyversions/hostsd)](https://pypi.org/project/hostsd/)
[![PyPI - License](https://shields.private.coffee/pypi/l/hostsd)](https://pypi.org/project/hostsd/)
[![Latest Git Commit](https://shields.private.coffee/gitea/last-commit/kumi/hostsd?gitea_url=https://git.private.coffee)](https://git.private.coffee/kumi/hostsd)

`hostsd` is a simple hosts file manager that allows you to separate your hosts file into multiple files and directories and easily enable or disable them. It's useful for development environments where you need to manage lots of hosts entries, or for managing ad-blocking hosts files.

## Dependencies

- Python 3.8 or later (earlier versions may work but are untested)
- Linux or macOS (should work on Windows too but is untested)

## Installation

### From PyPI

Just install the package using pip, ideally in a virtual environment:

```bash
pip install hostsd
```

See the [hostsd PyPI page](https://pypi.org/project/hostsd/) for more information.

### From AUR

If you're using Arch Linux, you can install the package from the AUR:

```bash
yay -S hostsd
```

After that, the `hostsd` command will be available globally.

See the [hostsd AUR page](https://aur.archlinux.org/packages/hostsd/) for more information.

### From source

You can also install `hostsd` from source, again ideally in a virtual environment:

```bash
git clone https://git.private.coffee/kumi/hostsd.git
cd hostsd
pip install .
```

The short version of that is:

```bash
pip install git+https://git.private.coffee/kumi/hostsd.git
```

## Configuration

Usually, you don't really need to configure anything. By default, `hostsd` reads files from `/etc/hosts.d` and writes the output to `/etc/hosts` (or `C:\Windows\System32\drivers\etc\hosts[.d]` on Windows).

To get started, simply run `hostsd --init` to move your existing hosts file to `/etc/hosts.d/00-hosts` and create a new `/etc/hosts` file that includes all files in `/etc/hosts.d`.

If you need to change the input or output paths, you can use the `-d` and `-o` options:

```bash
hostsd -d /etc/my-hosts/ -o /etc/my-hostfile
```

This will read files from `/etc/my-hosts/` and write the output to `/etc/my-hostfile`.

## Usage

To write the contents of `/etc/hosts.d/*` to `/etc/hosts`:

```bash
sudo hostsd
```

You can also specify the input and output paths:

```bash
hostsd -i /etc/hosts.d -o /etc/hosts
```

### Excluding files

There are several ways to exclude files and directories from being included in the output:

1. You can disable a file or directory by adding a `.disabled` extension:

```bash
mv /etc/hosts.d/10-my-file /etc/hosts.d/10-my-file.disabled
```

2. Hidden files and directories are ignored as well:

```bash
mv /etc/hosts.d/regular-file /etc/hosts.d/.hidden-file
```

3. You can include the magic string `HOSTSD_IGNORE` within a file to exclude it from the output, for example as a comment:

```bash
echo "# HOSTSD_IGNORE" >> /etc/hosts.d/10-my-file
```

4. Any binary files are automatically ignored.

Note that files are not currently checked for validity, so your `hosts.d` directory should only contain valid hosts file entries or files that are excluded using one of the methods above.

## Running hostsd automatically

You can run `hostsd` automatically using a cron job or a systemd timer. Here's an example of a systemd timer (assuming you have installed `hostsd` globally, for simplicity):

```ini
# /etc/systemd/system/hostsd.timer
[Unit]
Description=Update hosts file every minute

[Timer]
OnBootSec=1min
OnUnitActiveSec=1min

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/hostsd.service
[Unit]
Description=Update hosts file

[Service]
Type=oneshot
ExecStart=/usr/bin/hostsd
```

```bash
sudo systemctl enable hostsd.timer
sudo systemctl start hostsd.timer
```

This will run `hostsd` every minute. So you can just drop a new file in `/etc/hosts.d` and it will be picked up automatically.

You could even combine this with a git repository and you have a simple way to manage your hosts files across multiple machines or share them with others, without needing to set up and manage a full DNS server.

## License

hostsd is licensed under the MIT license. See [LICENSE](LICENSE) for the full license text.
