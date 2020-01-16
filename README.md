# Delete Google Play Music Duplicates

Delete duplicate songs on Google Play Music. Requires *Python 3.x* and `gmusicapi`.

**License:** MIT

## Run
Simple!

Install `gmusicapi` via `pip`, if you haven't got it yet: `pip install gmusicapi`

Then...

1. Open a console window in this directory
2. Run `python DeleteDupes.py`
3. Confirm deletion with `y` at the prompt

Alternatively...

1. Double-click `Run.cmd` and let it do the magic
2. Confirm deletion with `y` at the prompt

The tool itself will loop through three times, but you may want to run it again after a few minutes to make sure.

**Do NOT use the `split-methods` branch, unless you're willing to risk your entire collection. It has not been tested.**
***The `master` branch is the only known-working branch and will only be updated after testing.***

## Still to do

* Error handling
* Nicer/clearer messages