if exists('g:loaded_hubfix')
  finish
endif

let s:path = expand('<sfile>:p:h')

function! s:HubFixDo(inurl)
  let l:cmd = s:path . "/hubfix-get.py " .  a:inurl
  cgetexpr system(l:cmd)
  cope
  let w:quickfix_title = l:cmd
endfunction

command -nargs=1 -complete=history HubFix call s:HubFixDo(<q-args>)
