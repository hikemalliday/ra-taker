# RA TAKER

- Take discord members of channel and `POST` to RoZRaidTracker

## Screenshot uploads

`/screenshot` accepts an image attachment and an optional caption. Only members
with the `Officers`, `Leader`, or `Pker` role can use it. Configure
`SCREENSHOT_REST_URI` with the tracker screenshot endpoint, for example
`https://tracker.example.com/api/screenshots/`. The existing `API_KEY` is sent
as the API-key authorization credential.
