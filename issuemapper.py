#!/usr/bin/env python3

import abc
import urllib.parse

import icalendar

from github import Github
from redmine import Redmine


class Issue(object):

    def __init__(self, uid, title, description, project, url, created, updated,
                 author=None, percent_done=None, start=None, due=None):
        if uid is None:
            raise ValueError('uid must not be None')
        if title is None:
            raise ValueError('title must not be None')
        if description is None:
            raise ValueError('description must not be None')
        if project is None:
            raise ValueError('project must not be None')
        if url is None:
            raise ValueError('url must not be None')
        if created is None:
            raise ValueError('created must not be None')
        if updated is None:
            raise ValueError('updated must not be None')
        self.uid = uid
        self.title = title
        self.description = description
        self.project = project
        self.url = url
        self.created = created
        self.updated = updated
        self.author = author
        self.percent_done = percent_done
        self.start = due
        self.due = due

    def __str__(self):
        return '{clazz}[uid={uid}, title={title}, ' \
           'project={project}, due={due}]'.format(
               clazz=self.__class__.__name__,
               uid=self.uid,
               title=self.title,
               project=self.project,
               due=self.due)


class IssueSource(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def issues(self):
        pass


class RedmineIssueSource(IssueSource):

    def __init__(self, redmine):
        self.redmine = redmine
        self.parsed_url = urllib.parse.urlparse(redmine.url)

    def _make_id(self, issue_id):
        return '{}-{}@{}'.format(
            issue_id, self.parsed_url.path, self.parsed_url.netloc)

    def issues(self):
        issues = self.redmine.issue.filter(assigned_to_id='me',
                                           status_id='open')

        source_issues = []
        for issue in issues:
            uid = self._make_id(issue.id)
            author = self.redmine.user.get(issue.author.id)
            source_issues.append(Issue(
                uid,
                issue.subject,
                issue.description,
                issue.project.name,
                issue.url,
                issue.created_on,
                issue.updated_on,
                author=(issue.author.name, author.url),
                percent_done=issue.done_ratio,
                start=issue.start_date if hasattr(issue, 'start_date') else None,
                due=issue.due_date if hasattr(issue, 'due_date') else None))
        return source_issues


class GithubIssueSource(IssueSource):

    def __init__(self, github):
        self.github = github

    def _make_id(self, issue_id):
        return '{}@{}'.format(
            issue_id, 'github.com')

    def issues(self):
        issues = self.github.get_user().get_issues()

        source_issues = []
        for issue in issues:
            due = None
            if issue.milestone:
                due = issue.milestone.due_on
            source_issues.append(Issue(
                self._make_id(issue.id),
                issue.title,
                issue.body,
                issue.repository.name,
                issue.html_url,
                issue.created_at,
                issue.updated_at,
                author=(issue.user.login, issue.user.html_url),
                due=due))

        return source_issues


class IssueSink(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def generate(self, issues):
        pass


class ICalIssueSink(IssueSink):

    def generate(self, issues):

        calendar = icalendar.Calendar()
        calendar.add('prodid', '-//languitar//issuemapper//')
        calendar.add('version', '2.0')

        for issue in issues:
            todo = icalendar.Todo()
            todo.add('UID', issue.uid)
            todo.add('CREATED', issue.created)
            todo.add('DTSTAMP', issue.updated)
            todo.add('LAST-MODIFIED', issue.updated)
            todo.add('SUMMARY', issue.title)
            todo.add('DESCRIPTION', issue.description)
            todo.add('CATEGORIES', issue.project)
            todo.add('URL', issue.url)
            if issue.author:
                organizer = icalendar.vCalAddress(issue.author[1])
                organizer.params['CN'] = icalendar.vText(issue.author[0])
                todo.add('ORGANIZER', organizer)
            if issue.percent_done:
                todo.add('PERCENT-COMPLETE', issue.percent_done)
            if issue.start:
                todo.add('START', issue.start)
            if issue.due:
                todo.add('DUE', issue.due)
            todo.add('CLASS', 'PUBLIC')
            calendar.add_component(todo)

        return calendar.to_ical()

