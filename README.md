# Fast RideWithGPS route sync demo ⚡️

This Python script simulates downloading a user's routes from RideWithGPS.

It keeps an index of route IDs and the times they were last updated, so that it can run much
faster when there's nothing to do 🙂

Each time it runs, it rebuilds a new version of the index from the RWGPS route list endpoint and
compares it with the cached index.  Any outdated routes are re-downloaded, while orphans are purged.

When the index is up-to-date, no additional requests are made, and the script runs in just a few
seconds (as long as it takes to fetch the route list).

Currently, it doesn't save anything to disk, but just sleeps to simulate the download.

## Dependencies

* Python 3
* The Requests library for Python: `pip3 install requests`

## Running

To use the API's test user:

```
./main.py --user-id 1 --api-key testkey1 --auth-token ''
```

Try running it a second time to see that it runs much faster 🙂
