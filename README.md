# restake_monitor
A python script to verify that ReStake completed properly, and alert when it fails on a network.

It checks the journal and extracts the information relative to each chain processed by restake. If it failed, it will send a Discord alert with the details if can find.

### Prerequisites

- ReStake must run as a service, so that it logs its activity in the journal.
- Python package `discord-webhook` must be installed. `python3 -m pip install discord-webhook` 
- A [Discord webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) must be provided: define the variable `webhook_url` at the top of the script.
- Discord user IDs can be provided for alerts to tag specific people, by defining the variable `recipients` at the top of the script.
  - Right-click on a user and click on Copy User ID, or click on a user and right-click on one of its roles then on Copy Role ID.
    - An ID looks like 972778865355272194
    - Add these IDs in the role_id item, following the syntax:
      - For a role: <@&972778865355272194>
      - For a user: <@972778865355272194>
  - You can add multiple roles and IDs by separating them with a space: `recipients = "<@&972778865355272194> <@951374414451187732>"`
  - Leave blank to tag no one.

### Usage

You can either run this script in `cron` after each run of ReStake -- the script will scan the journal for entries maximum **2 hours old**. Adjust this parameter if you need, the only requirements are that the script should run after ReStake has completed, and pick the journal entries from this run and not the previous one.
You can otherwise run it as a service, when ReStake has completed. [Here is an option to do it](https://unix.stackexchange.com/a/717744).
