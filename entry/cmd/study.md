The whole model in one idea: 3 streams
Every program has three default channels, each with a number:

Stream	Number	Default	Purpose
stdin	0	keyboard	input into the program
stdout	1	terminal	normal output
stderr	2	terminal	error/diagnostic output
The key insight beginners miss: stdout and stderr are separate channels. Both print to your screen by default, so they look identical — but you can route them independently. That separation is the entire point of redirection.

Redirection and pipes just re-plug these channels somewhere other than the keyboard/terminal.

Redirection — send a stream to a file

command > file        # stdout → file  (OVERWRITE — truncates existing!)
command >> file       # stdout → file  (APPEND)
command < file        # file → stdin   (feed input from a file)

command 2> errors.log # stderr → file  (the "2" = stderr)
command 1> out.log    # stdout → file  (the "1" is the default, usually omitted)
Examples:


ls > files.txt              # save listing
echo "line" >> log.txt      # append a line
python script.py 2> err.txt # capture only errors, let normal output show
Combining stdout + stderr (the 2>&1 you asked about)
This is the one everyone fumbles. 2>&1 means "send stream 2 (stderr) to wherever stream 1 (stdout) is currently going." The &1 means "the destination of 1", not "a file named 1".


command > all.log 2>&1     # stdout → all.log, THEN stderr → same place ✅
command &> all.log         # shorthand for the same thing (bash/zsh)
⚠️ Order matters — this is the classic gotcha:


command > all.log 2>&1     # ✅ both go to all.log
command 2>&1 > all.log     # ❌ stderr goes to the TERMINAL, only stdout → all.log
Why: redirections are processed left to right. In the wrong version, 2>&1 copies "where stdout points right now" (still the terminal) to stderr before stdout gets pointed at the file. So put 2>&1 last.

Discarding output: /dev/null
/dev/null is the "black hole" — anything written there vanishes.


command > /dev/null            # discard normal output, still see errors
command 2> /dev/null           # discard errors, still see output  (silence warnings)
command > /dev/null 2>&1       # discard EVERYTHING (run silently)
Pipes — connect programs together
| connects the stdout of the left command to the stdin of the right command. No temp files needed:


cat access.log | grep ERROR | wc -l    # count error lines
Read it left to right: read file → keep ERROR lines → count them.

Pipes only carry stdout by default. To pipe errors too:


command 2>&1 | grep something    # merge stderr into the pipe first
command |& grep something        # shorthand (bash/zsh) for the same
This is why docker logs c 2>&1 | grep ERROR works — Docker writes some output to stderr, so you merge it in before grepping.

The toolkit that makes pipes powerful
These are the "filters" you chain. Each reads stdin, transforms, writes stdout:

Tool	Does
grep PATTERN	keep matching lines (-v = invert, -i = ignore case, -c = count)
sort	sort lines (-n numeric, -r reverse)
uniq	collapse adjacent duplicates (-c = count each) — usually after sort
wc -l	count lines
head -n / tail -n	first / last n lines (tail -f = follow live)
cut -d, -f1	extract column 1, comma-delimited
awk '{print $2}'	extract/process fields (whitespace-split)
sed 's/a/b/'	find-and-replace
xargs CMD	turn stdin lines into arguments for CMD
tee file	split: write to file and pass through to screen
tee is the special one — it forks the stream so you can save and keep piping:


make 2>&1 | tee build.log | grep -i error   # full log to file, errors to screen
Real one-liners you'll actually use

# Top 5 IPs hitting an access log
cat access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -5

# Find your biggest files
du -ah . | sort -rh | head -10

# Is the server process running?
ps aux | grep gunicorn | grep -v grep

# Live-tail Docker logs, only errors
docker logs -f mycontainer 2>&1 | grep -i error

# Count Python files in a repo
find . -name '*.py' | wc -l
That sort | uniq -c | sort -rn is the canonical "count and rank" idiom — memorize it.

Two gotchas worth knowing
> truncates instantly — cmd > file empties file before cmd even runs. Never do sort file > file (you'll wipe it). Use a temp file or sponge.
Each pipe stage runs in a subshell — variables set inside ... | while read x; do VAR=... done don't survive outside the loop in bash. (Edge case, but it bites people.)

2  >  &1
│  │  │
│  │  └── "&1" = the place where stream 1 (stdout) is currently pointing
│  └───── ">" = redirect
└──────── "2" = stream 2 (stderr)
