# vim-hubfix 

:GitHubFix https://github.com/user/project/pull/123

Retrieve comments on a Github pull request and show them in a vim quickfix window.

Given a GitHub pull request URL, this plugin pulls all the line comments, resolves
them to actual line numbers from the local copy and populates the quickfix window
with the comments.

For authentification, create a GitHub token and export it in your shell environnment `GITHUB_TOKEN`.

## TODO

- Auto detect the url from Github open PRs -> remote branch names -> current local branch
- Trust GitHub output less
- Use a multiline error format (newer GCC, clang?) to handle multiline comments in vim by default
- Add support for filtering out resolved conversations once GH adds it to their API
