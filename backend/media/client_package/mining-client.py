import argparse
import os
import requests
import hashlib
import configparser
import time
import logging


def mine(block_number, previous_hash, nonce_range):
    for nonce in range(*nonce_range):
        text = str(block_number) + previous_hash + str(nonce)
        new_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        if new_hash.startswith('0000'):
            return nonce, new_hash
    return None, None


def communicate_with_server(server_url, hardware_id):
    response = requests.get(f"{server_url}/get-task/", params={'hardware_id': hardware_id})
    if response.status_code == 200:
        task = response.json()
        block_number, previous_hash, nonce_range = task['block_number'], task['previous_hash'], tuple(
            task['nonce_range'])

        nonce, hash_solution = mine(block_number, previous_hash, nonce_range)

        if nonce is not None:
            # Submit result back to the server
            result_data = {
                'block_id': task['block_id'],
                'nonce': nonce,
                'hash': hash_solution
            }
            response = requests.post(f"{server_url}/submit-result/", json=result_data)
            logging.info(f"Submitted: {response.text}")
        else:
            logging.info("No valid nonce found.")
    else:
        logging.error(f"No task available or server error. Code: {response.status_code}, Text: {response.text}")


def write_config(field, value):
    config.clear()
    config.read(f'{dir_path}/config.ini')
    config['DEFAULT'][field] = value
    with open(f'{dir_path}/config.ini', 'w') as configfile:
        config.write(configfile)


def parse_config_arguments(config_string):
    pairs = config_string.split(',')
    for pair in pairs:
        if '=' in pair:
            field, value = pair.split('=', 1)
            write_config(field, value)
        else:
            logging.error(f"Error: Invalid format for {pair}. Correct format is field=value.")


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--write-config', type=str)
        args = parser.parse_args()
        if args.write_config:
            parse_config_arguments(args.write_config)
        else:
            config.read(f'{dir_path}/config.ini')
            hardware_id = config.getint('DEFAULT', 'hardware_id')
            server_url = config.get('DEFAULT', 'server_url')
            write_config('client_pid', str(os.getpid()))

            while True:
                try:
                    communicate_with_server(server_url, hardware_id)
                except Exception as e:
                    logging.error(f"Communication error occurred: {e}")
                time.sleep(5)
    except Exception as e:
        logging.error(f"Fatal error occurred: {e}")


if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(script_path)
    config = configparser.ConfigParser()
    logging.basicConfig(level=logging.INFO, filename=f'{dir_path}/logs.log')
    main()

