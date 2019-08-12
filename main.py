#!/usr/bin/env python3

import argparse
import requests

from datetime import datetime
from pathlib import Path

BASE_URI = 'https://ridewithgps.com'
INDEX_FILE = Path('index.txt')


def read_index():
    if not INDEX_FILE.exists():
        return {}

    index = {}
    with INDEX_FILE.open('r') as f:
        for line in f:
            route_id, update_time = line.split()
            index[int(route_id)] = datetime.fromisoformat(update_time)
    return index


def write_index(index):
    with INDEX_FILE.open('w') as f:
        for route_id, update_time in index.items():
            print(route_id, update_time.isoformat(), file=f)


def download_route(route_id, auth_params):
    # Download the route to disk.
    pass


def delete_route(route_id):
    # Delete the route from disk.
    pass


def fetch_route_list(user_id, auth_params):
    # Fetch 100 routes at a time until we have them all.
    offset = 0
    limit = 100

    results = []
    while True:
        r = requests.get(
            f'{BASE_URI}/users/{user_id}/routes.json',
            params={'offset': offset, 'limit': limit, **auth_params}
        )

        j = r.json()
        results.extend(j['results'])
        if len(results) >= j['results_count']:
            break
        else:
            offset += limit

    return results


def sync(user_id, auth_params):
    current_index = read_index()
    route_list = fetch_route_list(user_id, auth_params)
    print(f'found {len(route_list)} routes')

    # Build the new index and a set of outdated route IDs.
    new_index = {
        r['id']: datetime.fromisoformat(r['updated_at'].replace('Z', '+00:00'))
        for r in route_list
    }
    outdated = {
        route_id
        for route_id, update_time in new_index.items()
        if route_id not in current_index or current_index[route_id] < update_time
    }

    # Re-download any missing or outdated routes.
    if outdated:
        print(f'updating {len(outdated)} routes')
        for i, route_id in enumerate(outdated, 1):
            print(f'{i} / {len(outdated)}: {route_id}')
            download_route(route_id, auth_params)

    # Purge routes in the index that weren't in the returned list.
    orphans = current_index.keys() - new_index.keys()
    if orphans:
        print(f'purging {len(orphans)} orphan routes')
        for route_id in orphans:
            delete_route(route_id)

    if not orphans and not outdated:
        print('up-to-date!')

    # Finally, write the new index file.
    write_index(new_index)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--api-key', required=True)
    parser.add_argument('-t', '--auth-token', required=True)
    parser.add_argument('-u', '--user-id', required=True)
    args = parser.parse_args()
    auth_params = {'apikey': args.api_key, 'auth_token': args.auth_token}
    sync(args.user_id, auth_params)
