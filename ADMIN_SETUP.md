# Administrator first: senatemovement

Only the initial administrator is configured during first setup. There is no public signup, default password, or automatic creation of coordinators, viewers, or PU agents.

## Private local setup

From `/workspace/senatemovement`, stop the development server, then run:

```sh
.venv/bin/python app.py --setup-admin
.venv/bin/python app.py
```

Enter your chosen username and a password of 12–1024 characters at the terminal prompts. Password entry is hidden. Keep it private; do not send credentials in chat. This configures only this local database, not the future hosted database. Rerunning the setup command can recover/reset an administrator and invalidates existing sessions.

## Hosted setup

Follow DEPLOYMENT.md to create a separate PostgreSQL database and Render service for this portal. Privately run `.venv/bin/python manage.py hash-password` and put its output in the hosting provider's `ADMIN_PASSWORD_HASH` setting. Set `ADMIN_NAME` there too. Treat the hash as sensitive. Startup creates that administrator only if no active administrator exists; it does not overwrite an existing administrator. Remove the bootstrap hash from hosting settings after verifying access.

No hosting or database resources have been created by this setup. The prepared source must be available in the hosting provider's selected repository before deployment; local files are not automatically pushed by environment publication.

## Create other logins

Sign in as administrator and open **Accounts**. Choose a unique username, a temporary password of at least 12 characters, the role, and **Account enabled**, then save. Share account credentials through a private channel outside this chat. Give each person their own account.

| Role | Configuration | Access |
| --- | --- | --- |
| Administrator | No area assignment | All records and account management |
| Viewer | No area assignment | Read and export Benue South records; no edits |
| Coordinator | Choose one LGA; optionally enter exact ward names, one per line | Manage operational records and submit results inside the assigned scope |
| PU Agent | Choose LGA → ward → one polling unit | View that PU and submit/correct its results; no account or contact-directory management |

The PU Agent login is separate from an agent's contact/assignment record. Create an additional administrator only when that person should manage all records and accounts.

## Verify before sharing access

Create disposable sample logins, then check each role's permitted page and a denied action outside its role or area. Verify that viewers cannot edit, coordinators cannot access another area, and PU agents cannot access another PU's results or photos. Disable/delete sample logins afterwards. Do not enter real result sheets or personal contact records during this check.

Administrators can reset passwords or disable accounts in Accounts. Changing credentials, enabled status or scope invalidates existing sessions. The portal prevents disabling/demoting your own administrator or the last active administrator. Non-administrator accounts can be deleted with explicit confirmation; historical results and reviews are preserved.

The portal has no self-service password recovery or forced password change on first login. Administrator resets are the supported recovery route. Sessions are held in memory and end on service restart.
