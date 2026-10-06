# Step-by-step setup and use

## 1. Build and upload

Complete [BUILD.md](BUILD.md). This firmware runs on the ESP32-S3, not as a desktop app.

## 2. Prepare Gemini access

Create your own Gemini API key in [Google AI Studio](https://aistudio.google.com/). Use a 2.4 GHz Wi-Fi network. The saved firmware defaults to `gemini-3.8-live`; choose a supported Live model for your account if needed. See Google's [Live API guide](https://ai.google.dev/gemini-api/docs/live-api/capabilities).

## 3. Configure without saving credentials in source

The included helper asks for credentials interactively with hidden secret input. It sends newline-delimited JSON over USB serial and does not save credentials to a file. Close other serial monitors first.

```sh
python3 -m venv .venv
```

Activate it: `source .venv/bin/activate` on macOS/Linux, or `.venv\Scripts\activate` on Windows. Then:

```sh
python -m pip install -r requirements.txt
python tools/configure.py --port PORT --mode gemini
```

Enter Wi-Fi name, Wi-Fi password, API key, and model when prompted. Expect `CONFIG_SAVED`. The device stores credentials in its local Preferences/NVS. Wait for Wi-Fi connection; press RESET if needed. Never put real credentials in a committed file or shell command.

## 4. Optional: enable Hermes task execution

Use your own agent backend. Hermes is the original integration name; any other agent can replace it through a compatible API or adapter. See [agent backend interface](AGENT_BACKEND.md). Set its URL in ignored `Gemini_Live/local_config.h` before rebuilding. The client expects Cloudflare Access service-token authentication plus a bearer API key:

```sh
python tools/configure.py --port PORT --mode hermes
```

Enter Cloudflare client ID, client secret, and Hermes API key. Expect `HERMES_CONFIG_SAVED`; reset the board so the worker reloads credentials. The client uses `GET /v1/models`, `POST /v1/runs` with an `input` and an `Idempotency-Key`, and `GET /v1/runs/{run_id}`. Submission must return HTTP 202 with `run_id`; polling expects status plus output/error. Inspect `hermes_bridge.h` for the complete protocol.

The included TLS trust root is ISRG Root X1. Your backend certificate must chain to a trusted root in `hermes_roots.h`; update the public CA root if your service uses another CA. Keep TLS verification enabled. Backend tools, permissions and local-computer integrations must already exist; this repository does not install them.

## 5. Start a conversation

- Short BOOT press: start/stop Gemini Live; press BOOT to wake from idle light sleep.
- Speak after the display shows Listening. Ask an ordinary question first.
- With Hermes configured, ask for an action supported by your backend. Routing is model-driven.
- Bell: a Hermes completion/approval event arrived; result remains queued for a Live session.
- Volume button: short press increases volume; long press decreases volume.

The firmware sleeps after about two idle minutes when no session/task is active. Serial diagnostics include spoken response text and task information; keep logs private.

## 6. Optional: save backup Wi-Fi

```sh
python tools/configure.py --port PORT --mode backup-wifi
```

Hold BOOT for about three seconds to switch between primary and backup Wi-Fi. Use a 2.4 GHz compatible hotspot. To return explicitly to primary Wi-Fi, send `{"command":"select_primary_wifi"}` over a 115200-baud serial monitor with newline enabled.

## 7. Troubleshoot

- Missing `local_config.h`: copy the example as described in the build guide.
- Upload fails: check the USB data cable, board port and BOOT/RESET sequence; close serial monitors.
- `CONFIG_INVALID`: Wi-Fi name cannot be empty; Gemini key must have at least 20 characters.
- Gemini connection fails: check network, API access/quota and supported model ID.
- Hermes unavailable: check local URL, CA root, Cloudflare token, bearer key, backend protocol, then reboot after configuration.
- Audio/display errors: confirm original hardware, pins and OPI PSRAM settings.

Microphone recognition needs a physical test on your board; successful compilation does not prove audio behavior.
