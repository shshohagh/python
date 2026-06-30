# Custom Agent Rules

- When the user requests "push" (or similar phrasing) and there are uncommitted changes, do not ask for permission. Automatically stage all changes (`git add -A`), commit them with a descriptive auto-generated commit message based on the changed files, and push them to the remote repository.
