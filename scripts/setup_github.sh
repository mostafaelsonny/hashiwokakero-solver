#!/usr/bin/env bash
# Creates the GitHub repo, pushes main + develop, and sets labels / milestones / rulesets.
#
# Usage:
#   ./scripts/setup_github.sh [repo-name] [public|private]        (default: public)
#   COLLABORATORS="monzer-user ebrahim-user rovan-user febronia-user" ./scripts/setup_github.sh hashiwokakero-solver public
#
# Needs: git, GitHub CLI (https://cli.github.com) logged in with `gh auth login`.
# Public repo => Rulesets are free. Collaborators get 'push' (= Write). The owner (Mostafa) is Admin and is the only
# one in the ruleset bypass list (Admin role, pull_request mode: he can merge his own PRs but cannot push directly).
set -euo pipefail

REPO_NAME="${1:-hashiwokakero-solver}"
VISIBILITY="${2:-public}"

command -v git >/dev/null || { echo "git is not installed"; exit 1; }
command -v gh  >/dev/null || { echo "Install GitHub CLI first: https://cli.github.com"; exit 1; }
gh auth status >/dev/null 2>&1 || gh auth login

cd "$(dirname "$0")/.."

if [ ! -d .git ]; then
  git init -b main
fi
git add -A
git commit -m "chore: initial project scaffold" || echo "(nothing new to commit)"

gh repo create "$REPO_NAME" "--$VISIBILITY" --source=. --remote=origin --push

# develop branch = where the team integrates daily
git checkout -B develop
git push -u origin develop
gh repo edit --default-branch develop

# labels
mk_label() { gh label create "$1" --color "$2" --description "$3" --force >/dev/null; }
mk_label sprint-1 1d76db "Sprint 1 - Understanding & Core Foundation"
mk_label sprint-2 0e8a16 "Sprint 2 - Backtracking"
mk_label sprint-3 fbca04 "Sprint 3 - GA & MA"
mk_label sprint-4 5319e7 "Sprint 4 - Integration & Testing"
mk_label task     ededed "Sprint task"
mk_label bug      d73a4a "Something is wrong"
mk_label blocked  b60205 "Blocked by a dependency or problem"
mk_label needs-fixes e99695 "Reviewed - needs fixes"
mk_label core     c5def5 "core/ rule engine"
mk_label algorithm bfd4f2 "algorithms/"
mk_label frontend  d4c5f9 "frontend/"
mk_label docs      0075ca "Documentation"

# milestones
for s in 1 2 3 4; do
  gh api "repos/{owner}/{repo}/milestones" -f title="Sprint $s" >/dev/null || true
done

# rulesets (see .github/rulesets/README.md). Pushed main + develop already exist at this point.
for b in main develop; do
  gh api -X POST "repos/{owner}/{repo}/rulesets" --input ".github/rulesets/protect-$b.json" >/dev/null \
    && echo "Ruleset applied: protect-$b" \
    || echo "WARN: could not apply the ruleset for '$b' (private repo on a free plan?). Import .github/rulesets/protect-$b.json manually, or make the repo public / use the Student Pack."
done

# collaborators
for u in ${COLLABORATORS:-}; do
  gh api -X PUT "repos/{owner}/{repo}/collaborators/$u" -f permission=push >/dev/null \
    && echo "Invited $u" || echo "WARN: could not invite $u"
done

echo
echo "Done. Repo: $(gh repo view --json url -q .url)"
echo "Next: share the link, enable .github/CODEOWNERS (needs usernames), tell everyone to read README.md + CONTRIBUTING.md."
