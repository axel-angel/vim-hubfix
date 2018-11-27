# vim-hubfix 

Pull request comments in the vim quickfix window

Given a GitHub pull request URL, this plugin pulls all the line comments, resolves
them to actual line numbers from the local copy and populates the quickfix window
with the comments.

:HubFix https://github.com/user/project/pull/123

## TODO

* Actually handle reply comments
* Clean up Python / hunk matching scheme
* Support authentication
* Trust GitHub output less
* Use a multiline error format (newer GCC, clang?) to handle multiline comments in vim by default
* Add support for filtering out resolved conversations once GH adds it to their API
