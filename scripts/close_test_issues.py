#!/usr/bin/env python3
"""
Close test GitHub issues
"""
import requests

REPO = "ynizan/permitindex-site"
# Close test issues #1, #3, #4, #5
TEST_ISSUES = [1, 3, 4, 5]

for issue_num in TEST_ISSUES:
    url = f"https://api.github.com/repos/{REPO}/issues/{issue_num}"

    # First, get the issue to see its current state
    response = requests.get(url)
    if response.status_code == 200:
        issue = response.json()
        print(f"\nIssue #{issue_num}: {issue['title']}")
        print(f"  Current state: {issue['state']}")

        if issue['state'] == 'open':
            # Add a comment explaining closure
            comment_url = f"{url}/comments"
            comment_data = {
                "body": "🧹 Closing test issue - part of feedback system testing and validation."
            }
            comment_response = requests.post(comment_url, json=comment_data)

            # Close the issue
            close_data = {"state": "closed"}
            close_response = requests.patch(url, json=close_data)

            if close_response.status_code == 200:
                print(f"  ✅ Closed issue #{issue_num}")
            else:
                print(f"  ❌ Failed to close: {close_response.status_code}")
                print(f"     {close_response.text}")
        else:
            print(f"  ℹ️  Already closed")
    else:
        print(f"\n❌ Could not fetch issue #{issue_num}: {response.status_code}")

print("\n✅ Done!")
