# Fast RideWithGPS route sync demo ⚡️

This Python script simulates downloading a user's routes from the [RideWithGPS web
API](https://ridewithgps.com/api).

It keeps an index of route IDs and the times they were last updated, so that it can run much faster
when there's nothing to do 🙂

Each time it runs, it rebuilds a new version of the index from the RWGPS route list endpoint and
compares it with the cached index.  Any outdated routes are re-downloaded, while orphan routes (that
no longer exist in the RWGPS account) are purged.

When the index is up-to-date, no additional requests are made, and the script runs in just a few
seconds (as long as it takes to fetch the route list).

Currently, it doesn't save the routes to disk, but just sleeps to simulate the download.

## Dependencies

* [Python 3](https://www.python.org/)
* [uv](https://github.com/astral-sh/uv)

Run `uv sync` in the root directory.

## Running

To use the API's test user:

```shell
uv run main.py --user-id 1 --api-key testkey1 --auth-token ''
```

Try running it a second time to see that it runs much faster 🙂
