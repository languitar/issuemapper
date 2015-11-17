# issuemapper

A script to collect issue tracking information from multiple sources (e.g. Redmine, Github).
Collected issues can be exported in multiple formats (e.g. iCal) with the aim to provide an overview about open or assigned issues.

## Installation

```sh
python3 setup.py install [--user]
```

## Usage

```sh
issuemapper <config file ini>
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

## License

This library is [free software](https://en.wikipedia.org/wiki/Free_software); you can redistribute it and/or modify it under the terms of the [GNU Lesser General Public License](https://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License) as published by the [Free Software Foundation](https://en.wikipedia.org/wiki/Free_Software_Foundation); either version 3 of the License, or any later version. This work is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU Lesser General Public License](https://www.gnu.org/copyleft/lgpl.html) for more details.
