from setuptools import setup

setup(
    name='issuemapper',
    version='0.1-dev',

    install_requires=['icalendar', 'PyGithub', 'python-redmine'],

    scripts=['issuemapper'],

    author='Johannes Wienke',
    author_email='languitar@semipol.de',
    url='https://github.com/languitar/issuemapper',
    description='A tool to collect issues from multiple sources '
                '(e.g. Redmine or Github) and export them in formats to '
                'have a quick overview of all issues (e.g. iCal).',

    license='LGPLv3+',
    keywords=['issues', 'redmine', 'github', 'ical', 'ticket'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)'
    ])
