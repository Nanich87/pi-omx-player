# Raspberry Pi OMXPlayer

[Български](README.md) | **English**

A web remote for playing videos on a TV through a Raspberry Pi.

The Raspberry Pi is connected to the TV over HDMI and plays the videos with `omxplayer`. You control it from the browser on a phone, tablet or computer on the same network, with no keyboard or mouse attached to the Pi.

## What it is for

A home media center: you keep a folder of TV series or movies on the Raspberry Pi and want to watch them on the TV, choosing and controlling them from your phone.

## Features

- List of the videos in a configured folder, sorted alphabetically, with search.
- Start a video with a single tap. The current video is shown at the top and highlighted in the list.
- Stop playback.
- Turn the volume up and down.
- Switch the audio track (for example, another language).
- Switch, show and hide subtitles.
- Dark, phone-friendly interface in Bulgarian. The controls stay visible while you scroll, and commands are sent without reloading the page.

## Technologies

- **Python 3** and **[Flask](https://flask.palletsprojects.com/)** for the web server.
- **[omxplayer](https://github.com/popcornmix/omxplayer)** for hardware-accelerated playback over HDMI. The app controls it by sending its keyboard shortcuts (`+`, `-`, `j`, `k`, `m`, `q`, etc.) to its standard input.
- A **Jinja2** template, **[Bootstrap 5](https://getbootstrap.com/)** and **[Bootstrap Icons](https://icons.getbootstrap.com/)** for the interface (loaded from a CDN).
- A little plain JavaScript for search and for sending commands in the background.

## Requirements

- A Raspberry Pi connected to a TV or monitor over HDMI.
- Raspberry Pi OS with a working `omxplayer`.
- Python 3 and Flask.

> **Important:** `omxplayer` is no longer maintained. It works on Raspberry Pi OS Buster and on 32-bit Bullseye with the legacy graphics driver enabled. It does not work on 64-bit Raspberry Pi OS, on Bookworm or on the Raspberry Pi 5.

## Installation

```bash
sudo apt install omxplayer python3-flask
git clone https://github.com/Nanich87/pi-omx-player.git
cd pi-omx-player
```

## Configuration

In `app.py`, set the folder that contains your videos:

```python
TV_PATH = '/home/pi/videos'
```

You can also change `HOST` and `PORT` if needed (default `0.0.0.0:5000`).

## Running

```bash
python3 app.py
```

Then open this address in the browser on your phone or computer:

```
http://<Pi-IP-address>:5000
```

You can find the Pi's IP address with `hostname -I`.

## Security

The app has no login or password. Anyone on the network who opens the address can start and stop videos. Use it only on a trusted home network and do not expose it to the internet.

## License

[MIT](LICENSE)
