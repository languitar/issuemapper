# issuemapper

A script to collect issue tracking information from multiple sources (e.g. Redmine, Github).
Collected issues can be exported in multiple formats (e.g. iCal) with the aim to provide an overview about open or assigned issues.

## Installation

```sh
python3 setup.py install [--user]
```

## Usage

```sh
issuemapper <config file ini> > /target/file.ics
```

This command could be placed in a cron job to have e.g. a constantly up-to-date iCal file with VTODO entries for every issue.

## Configuration

The issue trackers to use as sources for open issues as well as the way collected issues shall be exported are configured in an INI-style configuration file.
This file lists multiple "sources" and one "sink".
The format is as follows:

```ini
[source:redmine_assigned_example]
class=RedmineAssignedIssueSource
host=https://redmine.example.com
key=abcdefghAPIkey

[source:this_part_is_user_defined_and_unique]
class=RedmineAssignedIssueSource
host=https://insecureredmine.example.com
key=anotherAPIkey
verify_ssl=false

[source:github_assigned]
class=GithubIssueSource
token=gihubAPItokenabcdef

[sink]
class=ICalIssueSink
```

## Sinks

### ICalIssueSink

Creates a single iCal export via stdout with all open issues being VTODO components.

Options:

### CsvIssueSink

Creates a CSV file via stdout with all issues.

Options:

### TaskWarriorIssueSink

Exports issues to [Taskwarrior](https://taskwarrior.org/).
Issues directly end up in the Taskwarrior directory.
There is no stdout output.
Issues are only added to Taskwarrior.
You need to manually purge issues before.
It is advisable to use a custom `taskrc` file specifying a custom storage directory which can be deleted before every sync.

Options:
* `taskrc` (optional): custom `taskrc` file to use when interacting with Taskwarrior

## Client Applications

For iCal export:
* [Thunderbird Lightning](https://www.mozilla.org/en-US/projects/calendar/): add the generated ics file as a new remote calendar using a `file://` URL.

## License

This library is [free software](https://en.wikipedia.org/wiki/Free_software); you can redistribute it and/or modify it under the terms of the [GNU Lesser General Public License](https://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License) as published by the [Free Software Foundation](https://en.wikipedia.org/wiki/Free_Software_Foundation); either version 3 of the License, or any later version. This work is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU Lesser General Public License](https://www.gnu.org/copyleft/lgpl.html) for more details.
