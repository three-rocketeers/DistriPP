# database
db_host = "127.0.0.1"
db_port = 3306
db_user = "root"
db_password = "root"
db_name = "distripp"


# JIRA
jira_base_url = "http://localhost:3535"
jira_board = 3111
jira_rest_sprints = "/jira/rest/greenhopper/latest/sprintquery/" + str(jira_board) +"?includeHistoricSprints=true&includeFutureSprints=true"
jira_rest_sprint_overview = "/jira/rest/greenhopper/latest/rapid/charts/sprintreport?rapidViewId=" + str(jira_board) + "&sprintId="
jira_rest_issue = "/jira/rest/api/latest/issue/"
jira_user = "user"
jira_pass = "password"
