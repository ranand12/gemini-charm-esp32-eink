"""Send configuration over USB without writing secrets to disk."""
import argparse
import getpass
import json
import time

import serial


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', required=True)
    parser.add_argument('--mode', choices=['gemini', 'hermes', 'backup-wifi'], default='gemini')
    args = parser.parse_args()
    if args.mode == 'gemini':
        payload = {'command': 'configure', 'ssid': input('Wi-Fi name: '),
                   'password': getpass.getpass('Wi-Fi password: '),
                   'key': getpass.getpass('Gemini API key: '),
                   'model': input('Live model [gemini-3.8-live]: ') or 'gemini-3.8-live'}
        expected = 'CONFIG_SAVED'
    elif args.mode == 'hermes':
        payload = {'command': 'configure_hermes',
                   'cf_id': getpass.getpass('Cloudflare client ID: '),
                   'cf_secret': getpass.getpass('Cloudflare client secret: '),
                   'hermes_key': getpass.getpass('Hermes API key: ')}
        expected = 'HERMES_CONFIG_SAVED'
    else:
        payload = {'command': 'configure_backup_wifi', 'ssid': input('Backup Wi-Fi name: '),
                   'password': getpass.getpass('Backup Wi-Fi password: ')}
        expected = 'BACKUP_WIFI_SAVED'
    encoded = (json.dumps(payload, ensure_ascii=False) + '\n').encode('utf-8')
    if len(encoded) > 2048:
        raise SystemExit('Configuration too long for the device serial buffer.')
    try:
        with serial.Serial(args.port, 115200, timeout=1, write_timeout=5) as device:
            time.sleep(2)
            device.reset_input_buffer()
            device.write(encoded)
            device.flush()
            deadline = time.monotonic() + 15
            while time.monotonic() < deadline:
                line = device.readline().decode('utf-8', errors='replace').strip()
                # Print only known acknowledgements; never echo arbitrary device data.
                if line == expected:
                    print(expected)
                    return
                if line in {'CONFIG_INVALID', 'BACKUP_WIFI_INVALID'}:
                    raise SystemExit('Device rejected configuration. Check inputs and retry.')
    except serial.SerialException:
        raise SystemExit('Could not use serial port. Check port, cable and other serial monitors.')
    raise SystemExit('No acknowledgement. Check board/port; configuration may need retrying.')


if __name__ == '__main__':
    main()
