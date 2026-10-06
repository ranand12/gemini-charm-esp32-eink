# Build guide

## 1. Hardware

Use the original compatible ESP32-S3 board: 8 MB flash, 8 MB OPI PSRAM, ES8311 speaker codec, ES7210 microphone codec and 200×200 e-paper panel. A generic ESP32-S3 without these peripherals needs driver/pin adaptations.

Display pins: CS 11, DC 10, RESET 9, BUSY 8, MOSI 13, clock 12, power control 6. BOOT button: GPIO 0. Volume button: GPIO 18. Audio wiring is defined in the sketch's `setup()` and bundled codec configuration. Check wiring against your actual board before powering it.

## 2. Install tools

Install [Arduino CLI](https://docs.arduino.cc/arduino-cli/installation/), Git, and Python 3. On macOS with Homebrew:

```sh
brew install arduino-cli git python
```

Clone this private repository using your authenticated GitHub account, then enter its folder:

```sh
git clone https://github.com/ranand12/gemini-live-agent.git
cd gemini-live-agent
```

## 3. Install the tested dependencies

```sh
arduino-cli core update-index --additional-urls https://espressif.github.io/arduino-esp32/package_esp32_index.json
arduino-cli core install esp32:esp32@3.3.0 --additional-urls https://espressif.github.io/arduino-esp32/package_esp32_index.json
arduino-cli lib install "ArduinoJson@7.4.3" "Adafruit GFX Library@1.12.6" "Adafruit BusIO@1.17.4"
```

WebSockets, codec board and ESP codec sources are bundled. The ESP32 core supplies ESP-SR/AEC. Do not install a different WebSockets implementation in place of the bundled code.

## 4. Set the local endpoint

```sh
cp Gemini_Live/local_config.example.h Gemini_Live/local_config.h
```

Edit `local_config.h`: replace the example HTTPS URL with your Hermes service URL, without a trailing slash. This local file is ignored by Git. For Gemini-only operation, leave the example URL and skip Hermes credential configuration. Hermes requires a compatible separate backend; see [setup](SETUP.md).

## 5. Compile

```sh
arduino-cli compile --fqbn esp32:esp32:esp32s3:CDCOnBoot=cdc,PSRAM=opi,FlashMode=qio,FlashSize=8M,PartitionScheme=huge_app --build-path build Gemini_Live
```

The same board settings are in `Gemini_Live/sketch.yaml`. Build output stays in ignored `build/` and must not be committed.

Arduino IDE alternative: install ESP32 core 3.3.0 and the library versions above; open `Gemini_Live/Gemini_Live.ino`; select ESP32S3 Dev Module, USB CDC enabled, OPI PSRAM, QIO, 8 MB flash and Huge APP partition, then Verify.

## 6. Flash

Connect with a USB data cable. Identify the actual board port:

```sh
arduino-cli board list
```

Replace `PORT` below with the detected port (`/dev/cu.usbmodem…` on macOS, `COM…` on Windows, `/dev/ttyACM…` on Linux):

```sh
arduino-cli upload --port PORT --fqbn esp32:esp32:esp32s3:CDCOnBoot=cdc,PSRAM=opi,FlashMode=qio,FlashSize=8M,PartitionScheme=huge_app --input-dir build Gemini_Live
```

Close serial monitors before uploading. Do not select `/dev/cu.debug-console`. If connecting fails, hold BOOT, press/release RESET, release BOOT, then retry. Upload replaces firmware; keep any existing full-device backup outside this repository. Existing NVS credentials can remain after a normal upload, so setup may already be present.

Next: [configure and run](SETUP.md).

Reference: [Arduino CLI getting started](https://docs.arduino.cc/arduino-cli/getting-started/).

## Export validation

The sanitized source compiled successfully using the versions above: 1,383,043 bytes of program storage (43% of the Huge APP partition), 48,676 bytes of global RAM (14%). The placeholder backend cannot execute tasks until configured. No device was flashed or physically tested during export.
