from github import Github
import sqlite3
import sys

#############################
# THESE ARE THE PARAMETERS
conn = sqlite3.connect(TRAC_FILENAME)
g = Github(AUTH_TOKEN)
repo = g.get_repo(REPO)
issue_from = 4
issue_to = 4
##############################


issues = []
c = conn.cursor()
sql = f'select id, milestone from ticket where CAST(id as decimal) >= {issue_from} and CAST(id as decimal)  <= {issue_to};'
for row in c.execute(sql):
    issues.append( (row[0], row[1]) )
print(f"Got {len(issues)} issues: {issues}")

milestones = {}
results1 = repo.get_milestones(state='open')
results2 = repo.get_milestones(state='closed')
results = [m for m in results1] + [m for m in results2]

for m in results:
    milestones[m.title] = m
print(f"Got {len(milestones)} milestones")

for issue_id, issue_milestone in issues:
    if milestones.get(issue_milestone, None) is None:
        print(f'Issue {issue_id} milestone "{issue_milestone}" not set/found')
        continue
    issue = repo.get_issue(number=issue_id)
    print(f'Editing issue {issue_id}, milestone={issue_milestone}')
    issue.edit(milestone = milestones[issue_milestone])
