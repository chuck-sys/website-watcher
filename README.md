# Website Watcher

A heavily automated solution to checking certain simple academic websites
regularly.

## Requirements

- Python
- Pipenv

For your environmental variables, make sure the following are set:

- `SENDGRID_KEY`: API key you got from sendgrid
- `CACHE_DIR`: Directory (relative to this one) you want to place cached HTML
  files (that have changed) for comparing later. This directory will be changed
  as frequently as you run the program.

## Running

You are meant to place the commands to run it in a cron file and have it run
regularly. For testing purposes you can also run it manually.

```bash
pipenv run watch
```
