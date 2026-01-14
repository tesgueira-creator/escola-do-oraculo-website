#!/bin/bash
cd "c:\Users\XKELU27\Downloads\escola-do-oraculo-website"
git add backend_server/main.py run_server_debug.py FIX_REPORT_PASSWORD_BCRYPT.md SESSION_SUMMARY.py
git commit -m "Fix: Handle passwords longer than 72 bytes in bcrypt

- Added hashlib import for SHA256 hashing
- Modified get_password_hash() to hash long passwords with SHA256 first
- Modified verify_password() with same pattern
- Fixed dotenv loading in run_server_debug.py
- Resolves error: 'password cannot be longer than 72 bytes'
- All tests pass locally
- Ready for production deployment"
git push
