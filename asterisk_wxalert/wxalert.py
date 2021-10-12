import os
import requests

def run(zone='WAZ039', device='WXAlert'):
    data = requests.get('https://api.weather.gov/alerts/active?zone={}'.format(zone)).json()

    severity = [ x['properties']['severity'] for x in data['features'] ]

    if 'Extreme' in severity:
        state = 'RINGING'
    elif 'Moderate' in severity:
        state = 'RINGING'
    elif 'Minor' in severity:
        state = 'INUSE'
    elif 'Unknown' in severity:
        state = 'INUSE'
    else:
        state = 'NOT_INUSE'

    os.system('/usr/sbin/asterisk -rx "devstate change Custom:{} {}"'.format(device, state))

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-z", "--zone", help="NOAA Weather Zone")
    parser.add_argument("-d", "--device", help="Custom device state to target")
    args = parser.parse_args()

    run(zone=args.zone, device=args.device)

if __name__ == "__main__":
    main()
