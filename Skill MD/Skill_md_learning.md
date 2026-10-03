# Writing SKILL.md Files — A Beginner-to-Practical Guide

> A self-contained lesson on Agent Skills in Claude Code: what they are, why they
> work, how to write them, and what to focus on.
> Based on the official Claude Code skills documentation and the `skill-creator` guidance.

---

## Table of contents

1. [What a SKILL.md actually is](#1-what-a-skillmd-actually-is)
2. [Why it works — the economics](#2-why-it-works--the-economics)
3. [Mechanics in Claude Code](#3-mechanics-in-claude-code)
4. [Anatomy of the frontmatter](#4-anatomy-of-the-frontmatter)
5. [The description is 90% of the job](#5-the-description-is-90-of-the-job)
6. [Writing the body — the craft](#6-writing-the-body--the-craft)
7. [A worked example](#7-a-worked-example)
8. [Testing and iterating](#8-testing-and-iterating)
9. [Common mistakes](#9-common-mistakes)
10. [The checklist](#10-the-checklist)
11. [Quick reference card](#11-quick-reference-card)

---

## 1. What a SKILL.md actually is

A skill is **a folder with a `SKILL.md` file in it**. That's it.

```text
summarize-changes/
└── SKILL.md
```

The file has two parts: YAML frontmatter between `---` markers, and markdown
instructions below it.

````markdown
---
description: Summarizes uncommitted changes and flags anything risky. Use when the user asks what changed or wants a commit message.
---

Summarize the changes in two or three bullets, then list risks:
missing error handling, hardcoded values, tests that need updating.
````

### The mental model

**A skill is onboarding documentation for a new teammate who has amnesia.**

They're brilliant, but they've never seen your repo, your naming conventions, your
deployment dance, or your chart of accounts. You write it down once instead of
re-explaining it every session.

### When should you make one?

- You keep pasting the same instructions or checklist into chat.
- A section of your `CLAUDE.md` has grown from a *fact* into a *procedure*.
- You have a multi-step workflow with an order that matters.
- You have domain knowledge that Claude can't infer from the code.

### Skills vs. the other options

| Tool | What it is | When to use |
|---|---|---|
| `CLAUDE.md` | Always-loaded facts about the project | Short, universal context |
| **Skill** | On-demand expertise, loaded when relevant | Procedures, checklists, domain knowledge |
| Subagent | Isolated context for a sub-task | Keeping noisy work out of the main thread |
| Hook | Deterministic enforcement in the harness | Policy that must hold regardless of the model |
| MCP server | Connection to external systems/data | Tools and live data, not instructions |

---

## 2. Why it works — the economics

This is the part most people skip, and it's the whole reason skills exist.

> **CLAUDE.md is always loaded. A skill is loaded only when needed.**

A skill costs roughly **100 tokens** of context (just its name + description) until
Claude decides it's needed. Only then does the body get pulled in.

This is called **progressive disclosure**, and it has three levels:

| Level | What | Cost |
|---|---|---|
| 1 | `name` + `description` | Always in context (~100 tokens) |
| 2 | `SKILL.md` body | Loads only when the skill triggers |
| 3 | Bundled files (`references/`, `scripts/`, `assets/`) | Loads only when Claude reads them — scripts can **run** without being loaded at all |

That's why you can have 50 skills installed with no slowdown, but a 5,000-line
`CLAUDE.md` hurts on every single turn.

**Level 3 is the underrated one.** A 2,000-line Python script that does a data
transform costs *zero* context — Claude just executes it and reads the output.

> **Rule:** anything deterministic and repetitive should be a script, not prose
> instructions. Prose costs tokens and invites improvisation; a script is exact and free.

---

## 3. Mechanics in Claude Code

### Where skills live

The folder location decides the scope:

| Location | Path | Applies to |
|---|---|---|
| Enterprise | via managed settings | Everyone in the org |
| Personal | `~/.claude/skills/<name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<name>/SKILL.md` | That repo — commit it, the team gets it |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Wherever the plugin is enabled |

Precedence when names collide: **enterprise > personal > project**. A skill at any of
these levels also overrides a bundled skill of the same name.

**The directory name becomes the command you type.**
`.claude/skills/deploy-staging/SKILL.md` → `/deploy-staging`

### Creating one, start to finish

```bash
mkdir -p ~/.claude/skills/my-skill
# then write ~/.claude/skills/my-skill/SKILL.md
```

Verify it loaded by asking Claude: `What skills are available?`

### Two ways a skill fires

1. **Model-invoked** — Claude reads the descriptions of all available skills and
   decides "this one is relevant." Fully automatic.
2. **User-invoked** — you type `/skill-name`.

By default both are enabled. You can turn either off (see frontmatter below).

### Lifecycle — the detail people get wrong

Once a skill is invoked, its content enters the conversation as a message and
**stays there for the rest of the session**. Claude Code does **not** re-read the
file on later turns.

Consequences:

- Write **standing instructions** ("always format dates as `YYYY-MM-DD`"), not
  one-time steps that assume you'll be re-read later.
- Every line is a *recurring* token cost. Keep it lean.
- If a skill seems to "stop working" after the first response, the content is
  usually still there — the model is just choosing other approaches. Strengthen the
  instructions, or use a hook if you need hard enforcement.

### Live reload

Claude Code watches skill directories. Adding, editing, or removing a `SKILL.md`
under `~/.claude/skills/` or the project `.claude/skills/` takes effect **within the
current session**, no restart needed. This makes iteration very fast.

(Creating a *top-level* skills directory that didn't exist at session start does
require a restart, so the new directory can be watched.)

---

## 4. Anatomy of the frontmatter

All fields are optional. Only `description` is genuinely recommended.

```yaml
---
name: bank-categorizer          # display label; command still comes from folder name
description: What it does + when to use it   # ← the field that matters most
when_to_use: Extra trigger phrases           # appended to description in the listing
allowed-tools: Read Grep Bash(python3 *)     # pre-approve tools, skip permission prompts
disallowed-tools: WebSearch                  # remove tools while this skill is active
disable-model-invocation: true  # only YOU can run it — for anything with side effects
user-invocable: false           # only CLAUDE can run it — background knowledge
context: fork                   # run in an isolated subagent
agent: Explore                  # which subagent type, when context: fork
paths: "src/api/**"             # only auto-load when working on matching files
argument-hint: "[issue-number]" # autocomplete hint
model: inherit                  # model override while this skill is active
---
```

### The ones to learn first

**`description`** — covered in depth in section 5. This is the whole ballgame.

**`disable-model-invocation: true`** — put this on `/deploy`, `/commit`,
`/send-email`, `/release`. You do not want Claude deciding to deploy because your
code "looks ready." Anything with side effects should be manual-only.

**`user-invocable: false`** — the inverse. Use for background knowledge that isn't a
meaningful action. A `legacy-system-context` skill explains how an old system works;
Claude should know it when relevant, but `/legacy-system-context` isn't something a
human would ever want to "run."

| Frontmatter | You can invoke | Claude can invoke |
|---|---|---|
| *(default)* | Yes | Yes |
| `disable-model-invocation: true` | Yes | No |
| `user-invocable: false` | No | Yes |

**`allowed-tools`** — grants permission for the listed tools during the turn that
invokes the skill, so Claude doesn't stop to ask you. The grant clears when you send
your next message.

> ⚠️ **Security note:** a skill can grant itself broad tool access. Review project
> skills before trusting a repository.

### Useful string substitutions

| Variable | Meaning |
|---|---|
| `$ARGUMENTS` | Everything typed after the skill name |
| `$0`, `$1`, `$2` | Individual arguments by position |
| `${CLAUDE_SKILL_DIR}` | The skill's own folder — use this to reference bundled scripts |
| `${CLAUDE_PROJECT_DIR}` | The project root |
| `${CLAUDE_SESSION_ID}` | Current session ID, handy for logging |

`${CLAUDE_SKILL_DIR}` is the important one — it makes bundled scripts work no matter
where the skill is installed:

```yaml
---
name: render-chart
description: Render a chart from a CSV file
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/render.sh *)
---

Run `${CLAUDE_SKILL_DIR}/scripts/render.sh <csv-file>` to render the chart.
```

Because the same variable is used in both the body and `allowed-tools`, the command
matches the permission rule exactly and runs without prompting.

### Dynamic context injection

The `` !`command` `` syntax runs a shell command **before** Claude sees the skill,
and replaces the placeholder with the output. Claude receives real data, not the
command.

````markdown
---
name: pr-summary
description: Summarize changes in a pull request
allowed-tools: Bash(gh *)
---

## Pull request context
- Diff: !`gh pr diff`
- Comments: !`gh pr view --comments`

## Your task
Summarize this pull request...
````

For multi-line commands, use a fenced block opened with ```` ```! ````.

---

## 5. The description is 90% of the job

Internalize this: **a skill that never triggers is a skill that doesn't exist.**
The body can be perfect and it will never run if the description doesn't match how
you actually talk.

### Rule (a) — include both *what* and *when*

All the "when to use" information lives in the **description**, not the body. At
decision time the body hasn't been loaded yet, so Claude can't see it.

❌ `description: Bank statement helper`

✅ `description: Categorizes bank statement rows into expense accounts using our grant chart of accounts. Use whenever the user pastes bank transactions, mentions categorizing expenses, reconciling statements, or filling the Base sheet.`

### Rule (b) — be a little pushy

Claude's failure mode is **under-triggering**, not over-triggering. Add an explicit
nudge:

> "Make sure to use this skill whenever the user mentions dashboards, data
> visualization, or internal metrics — **even if they don't explicitly ask for a
> 'dashboard'.**"

### Rule (c) — use the words a real person would type

Not internal jargon. If your team says "recon," include both "reconcile" and "recon."
Include synonyms, abbreviations, and the sloppy phrasing you'd use at 11pm.

### Rule (d) — front-load the key use case

The combined `description` + `when_to_use` text is truncated at **1,536 characters**
in the skill listing. And if you have many skills, Claude Code shortens descriptions
to fit an overall budget (1% of the context window by default) — which can strip
exactly the keywords you needed.

- Run `/doctor` to see what your skill listing is costing and which skills are the
  biggest contributors.
- `/context` shows the size of the listing after the budget is applied.
- Raise the budget with the `skillListingBudgetFraction` setting if needed.

### Rule (e) — know what won't trigger

Claude only reaches for skills on tasks it can't trivially handle alone. A one-step
request like *"read this file"* won't trigger a skill no matter how good the
description is. Complex, multi-step, or specialized requests trigger reliably.

**This matters for testing too:** trivial prompts are bad test cases.

---

## 6. Writing the body — the craft

### Use imperative voice

✅ "Run the tests, then check the diff."
❌ "This skill will help you run tests and then you might want to check the diff."

### Be concise, because it's a recurring cost

Every line stays in context for the whole session. State **what to do**, not a
narrative essay about why the workflow exists. Apply the same conciseness test you'd
apply to `CLAUDE.md`.

### But give reasons where they matter

There's a real tension between "be concise" and "explain why." The resolution:

> **Give reasons instead of shouting rules.**

✅ `Use tabs — the build script parses column position.`
❌ `YOU MUST ALWAYS USE TABS!!!`

A reason generalizes to cases you didn't anticipate. A capitalized MUST only covers
the exact case you thought of, and heavy-handed rules tend to make the model rigid
and literal-minded.

### Pin down output formats with a literal template

````markdown
## Report structure
Always use this exact template:

# [Title]
## Summary
## Findings
## Recommendations
````

### Use input → output examples

Examples are worth more than three paragraphs of description.

````markdown
## Commit message format

**Example 1**
Input:  Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication

**Example 2**
Input:  Fixed crash when config file is missing
Output: fix(config): handle missing config file gracefully
````

### Stay under ~500 lines

Past that, split into supporting files and point at them from `SKILL.md` **with a
note on when to read each one**:

```markdown
## Additional resources
- Full account code list → [references/chart-of-accounts.md](references/chart-of-accounts.md)
- Ambiguous rows and edge cases → [references/edge-cases.md](references/edge-cases.md)

Read the chart of accounts only when a row doesn't match a rule above.
```

For reference files over ~300 lines, add a table of contents at the top.

### Organize by variant when a skill spans domains

```text
cloud-deploy/
├── SKILL.md           # workflow + "pick the right one" logic
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

Claude reads only the relevant reference file. One skill, three domains, minimal cost.

### Generalize — don't overfit

You'll be tempted to patch the skill every time it gets one case wrong. Resist adding
a rule per example. You'll end up with a brittle skill that only works on the five
cases you tested. If an issue is stubborn, try a *different framing or metaphor*
rather than piling on more constraints.

### Standard folder layout

```text
skill-name/
├── SKILL.md          # required — overview and navigation
├── references/       # docs loaded into context on demand
├── scripts/          # executable code — runs without consuming context
└── assets/           # templates, icons, fonts used in output
```

---

## 7. A worked example

A realistic skill using all the ideas above:

```text
~/.claude/skills/bank-categorizer/
├── SKILL.md
├── references/
│   └── chart-of-accounts.md
└── scripts/
    └── normalize.py
```

**`SKILL.md`:**

````markdown
---
name: bank-categorizer
description: Categorizes Bangladeshi bank statement rows into grant expense
  categories and sub-accounts. Use whenever the user pastes bank transaction
  rows, mentions categorizing expenses, reconciling a statement, filling the
  Base sheet, or asks which account a payment belongs to — even if they don't
  say "categorize" explicitly.
allowed-tools: Read Bash(python3 *)
---

# Bank statement categorizer

## Workflow
1. Normalize the pasted rows: `python3 ${CLAUDE_SKILL_DIR}/scripts/normalize.py`
2. Match each row against the rules below.
3. Output a markdown table: Date | Payee | Amount | Category | Sub-account
4. Leave Category blank when a row is ambiguous. Never guess — an incorrect
   category is worse than a blank one, because blanks get reviewed and wrong
   entries don't.

## Rules
- Payee "Shaheena Abedin" → Office Rent / Support Services
- Salary transfers to known staff accounts → Salaries / Personnel
- A-Chalan → Professional Services / Tax Return Filing - Annual
- SMS gateway purchases → Web Hosting and Domain Expenses

## Leave blank
Bare bKash transfers, ATM/POS withdrawals, bank charges, IBFT to unknown accounts.

## Reference
Full account codes → [references/chart-of-accounts.md](references/chart-of-accounts.md)
Read it only when a row doesn't match a rule above.
````

### What to notice in this example

| Technique | Where |
|---|---|
| Pushy description with real-world phrasing | `description` field, ending with "even if they don't say…" |
| Deterministic work pushed into a script | `normalize.py`, costs zero context |
| Short rule set in the body | Under 30 lines, cheap to keep in context |
| Long lookup table exiled to `references/` | Loads only when actually needed |
| A **reason** given for the blank rule | Generalizes to unseen cases |
| Explicit output format | The markdown table spec |
| `${CLAUDE_SKILL_DIR}` for the script path | Works at any install location |

---

## 8. Testing and iterating

**Seeing a skill trigger tells you Claude found it — not that it helped.**

Measure two things separately:

1. **Triggering** — does Claude invoke it on the prompts it should, and *not* on the
   ones it shouldn't?
2. **Output quality** — when it does fire, is the result better?

### The honest test: baseline comparison

Run the same prompt in a **fresh session** with the skill available, then again with
it disabled, and compare.

A fresh session matters. Leftover context from writing the skill will mask gaps in
the actual written instructions — you'll think the skill is working when really
*you* explained the missing part in chat.

### Write realistic test prompts

2–3 prompts of the kind a real user would actually type. Remember from section 5:
trivial one-step prompts won't trigger a skill regardless of description quality, so
they're useless as test cases.

### Automate it with `skill-creator`

```text
/plugin install skill-creator@claude-plugins-official
```

If the marketplace isn't found:

```text
/plugin marketplace add anthropics/claude-plugins-official
/plugin marketplace update claude-plugins-official
```

Then `/reload-plugins`, and ask Claude something like
*"evaluate my summarize-changes skill with skill-creator."*

It handles:

- **Test cases** stored in `evals/evals.json` inside the skill directory
- **Isolated runs** — one subagent per test case, clean context, records tokens + duration
- **Grading** — checks assertions against output, writes pass/fail with evidence
- **Benchmark** — with-skill vs without-skill pass rate, so you can weigh the
  improvement against the token and time overhead
- **Version comparison** — blind A/B between two versions of the skill
- **Description tuning** — generates should-trigger and should-not-trigger prompts,
  measures hit rate, proposes better descriptions
- **Review viewer** — an HTML report where you leave qualitative feedback that the
  next iteration reads

### The iteration loop

```text
draft → write test prompts → run with & without skill → review outputs
   ↑                                                          │
   └──────────────── revise based on feedback ────────────────┘
```

Repeat until satisfied, then expand the test set and try again at larger scale.

---

## 9. Common mistakes

| Mistake | Why it hurts | Fix |
|---|---|---|
| Vague description | Skill never triggers | Add what + when + real phrasing |
| "When to use" written in the body | Body isn't loaded at decision time | Move it to `description` |
| Everything in one giant SKILL.md | Recurring token cost every turn | Split into `references/` |
| Prose instructions for deterministic work | Slow, inconsistent, expensive | Write a script |
| Walls of capitalized MUSTs | Model becomes rigid and literal | Give reasons instead |
| Overfitting to test examples | Works on 5 cases, fails on the 6th | Generalize; try different framings |
| No `disable-model-invocation` on destructive skills | Claude may deploy on its own | Add the flag |
| Testing in the session where you wrote it | Your chat context hides the gaps | Test in a fresh session |
| Assuming the file is re-read each turn | Skill content is loaded once and persists | Write standing instructions |
| Too many skills with long descriptions | Listing gets truncated, keywords stripped | Trim, front-load, use `skillOverrides` |

---

## 10. The checklist

Before you consider a skill done:

- [ ] **Does the description contain the words I'd actually type?** *(biggest failure point by far)*
- [ ] Does the description say both **what it does** and **when to use it**?
- [ ] Is it a little pushy — does it name the trigger phrases explicitly?
- [ ] Is anything deterministic still written as prose? → move it to a script
- [ ] Is the body under 500 lines? → if not, split into `references/`
- [ ] Do my references have a note saying **when** to read them?
- [ ] Are my rules stated with **reasons**, or just capitalized demands?
- [ ] Would this work on a case I haven't tested, or did I overfit?
- [ ] Does anything here have side effects? → `disable-model-invocation: true`
- [ ] Is this background knowledge rather than an action? → `user-invocable: false`
- [ ] Personal or project scope? → team conventions go in `.claude/skills/` and get committed
- [ ] Did I test it in a **fresh session**, with and without the skill?

---

## 11. Quick reference card

### Minimal skill

```bash
mkdir -p ~/.claude/skills/my-skill
```

```markdown
---
description: Does X. Use when the user mentions A, B, or C.
---

Do the thing:
1. Step one
2. Step two
```

### Commands worth knowing

| Command | What it does |
|---|---|
| `/skill-name` | Invoke a skill directly |
| `What skills are available?` | Confirm your skill loaded |
| `/skills` | Menu; press Space to cycle visibility, Enter to save |
| `/doctor` | Estimate skill listing context cost and top contributors |
| `/context` | See the size of the skill listing |
| `claude --debug` | See YAML parse errors and budget warnings |

### Troubleshooting

**Skill not triggering:**
1. Check the description contains keywords you'd naturally say
2. Verify it appears in `What skills are available?`
3. Try rephrasing closer to the description
4. Invoke directly with `/skill-name` to confirm the body works
5. Run `--debug` — malformed YAML loads the body with **empty metadata**, so
   `/skill-name` still works but Claude has no description to match against

**Skill triggering too often:**
1. Make the description more specific
2. Add `disable-model-invocation: true`

### Sharing

| Scope | How |
|---|---|
| Project team | Commit `.claude/skills/` to version control |
| Broader | Package as a plugin with a `skills/` directory |
| Organization | Deploy via managed settings |

---

## Homework

Pick the one thing you've explained to Claude more than three times this month, and
write a 20-line `SKILL.md` for it.

Don't aim for perfect — the file live-reloads, so you'll iterate fast. Then run it
in a fresh session, once with and once without, and see if it actually helped.

---

## Further reading

- Claude Code skills reference — `https://code.claude.com/docs/en/skills`
- Skill authoring best practices — `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices`
- Agent Skills open standard — `https://agentskills.io`
- Evaluating skill output quality — `https://agentskills.io/skill-creation/evaluating-skills`