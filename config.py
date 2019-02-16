config = dict(
    DEBUG=False,
    SECRET_KEY='1d94e52c-1c89-4515-b87a-f48cf3cb7f0b',
    PONY={
        'provider': 'postgres',
        'user': 'distripp',
        'password': 'bananas2323',
        'database': 'distripp',
        'host': 'db',
        'port': 5432,
        'create_tables': False
    },
    JIRA={
        'base_url': 'http://www.mocky.io/v2/',
        'rest_sprints': '5c6868213800007b1fb101a8',
        'rest_sprint_overview': '5c6868cd380000021fb101a9?sprintId=',
        'rest_issue': '5c6869113800002a20b101ac/',
        'user': 'user',
        'password': 'password'
    },
    JIRA_DOCKER_MOCKOON={
        'base_url': 'http://host.docker.internal:3535',
        'rest_sprints': '/jira/rest/greenhopper/latest/sprintquery/3111?includeHistoricSprints=true&includeFutureSprints=true',
        'rest_sprint_overview': '/jira/rest/greenhopper/latest/rapid/charts/sprintreport?rapidViewId=3111&sprintId=',
        'rest_issue': '/jira/rest/api/latest/issue/',
        'user': 'user',
        'password': 'password'
    }
)
