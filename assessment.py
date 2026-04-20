from pydriller import Repository
import re

REPO_PATH = "/Users/mauli/Desktop/Camel/camel"

ISSUE_IDS = ["CAMEL-180", "CAMEL-321", "CAMEL-3214", "CAMEL-18065", "CAMEL-1818"]

ISSUE_IDS = [issue.upper() for issue in ISSUE_IDS]

pattern = re.compile(r'\b(' + '|'.join(ISSUE_IDS) + r')\b', re.IGNORECASE)

unique_commits = set()

total_files_changed = 0

total_dmm_size = 0
total_dmm_complexity = 0
total_dmm_interfacing = 0

valid_dmm_commits = 0

for commit in Repository(REPO_PATH).traverse_commits():

    if commit.msg and pattern.search(commit.msg):
        if commit.hash not in unique_commits:
            unique_commits.add(commit.hash)

            
            files_changed = [
                m for m in commit.modified_files
                if m.change_type.name in ['ADD', 'MODIFY', 'DELETE']
            ]
            total_files_changed += len(files_changed)

            
            if (commit.dmm_unit_size is not None and
                commit.dmm_unit_complexity is not None and
                commit.dmm_unit_interfacing is not None):

                total_dmm_size += commit.dmm_unit_size
                total_dmm_complexity += commit.dmm_unit_complexity
                total_dmm_interfacing += commit.dmm_unit_interfacing

                valid_dmm_commits += 1


total_commits = len(unique_commits)

avg_files_changed = (
    total_files_changed / total_commits if total_commits > 0 else 0
)

if valid_dmm_commits > 0:
    avg_dmm = (
        (total_dmm_size + total_dmm_complexity + total_dmm_interfacing)
        / valid_dmm_commits
    )
else:
    avg_dmm = 0

print("Total commits analyzed:", total_commits)
print("Average number of files changed:", round(avg_files_changed, 2))
print("Average DMM metrics:", round(avg_dmm, 4))