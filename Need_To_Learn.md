# Software Engineer Learning Roadmap — Entry-Level & Junior

> A complete, detailed skill map for an **Entry-Level** then a **Junior** software engineer
> (backend / Python / AI focus). Labels reflect **your own demonstrated work**, verified from
> `Learning/` (Design Patterns, Principles, Architecture, LLD Case studies, DSA, Proxy/LB),
> `LangChain/` (full LangChain Academy 0–6 + deep-agents-from-scratch), and `CP/` (LeetCode +
> CodeForces), plus production work (TraderBro, CWTAMC, RideBuddy, Volunteer Portal, Plastic Kothay).
>
> **Format:** `Topic — STATUS — short description (what it is / why it matters)`.
> The description tells a future chat thread what to teach when you say "help me learn X".

## Legend
- ✅ **Done** — demonstrated in your own project, practice code, or solved problems
- 🟡 **Partial / In Progress** — touched it; deepen or formalize
- ❌ **To Do** — no evidence yet in *your* work
- 🏭 = also **production-proven** (not just practice)

> **How to use with me later:** open a new thread, point me at this file, and say e.g.
> "teach me the ❌ items in Section 6 (Security)". I'll use the descriptions + your status to
> pick the right starting point and skip what you already know.

---
---

# PART 1 — ENTRY-LEVEL ENGINEER ROADMAP

*Goal: build and ship a working app; know the fundamentals; comfortable with one language + basic tools.* **→ Fully cleared.**

## 1. Computer Science Fundamentals

### 1.1 Programming Basics
- Variables, data types, operators — ✅ — storing values and the int/str/bool/float types + arithmetic/logical operators.
- Control flow (if/else, loops) — ✅ — branching and repeating logic with conditionals and for/while loops.
- Functions / parameters / return / scope — ✅ — reusable blocks, passing arguments, returning values, local vs global scope.
- Error & exception handling — ✅ — catching failures with try/except/finally instead of crashing.
- Input / output (files, stdin/stdout) — ✅ — reading/writing files and console I/O.
- Comments & code readability — ✅ — writing code humans can follow.

### 1.2 Data Structures (usage level)
- Arrays / lists — ✅ — ordered, indexable sequences; the workhorse container.
- Strings & manipulation — ✅ — text as immutable sequences; slicing, splitting, formatting.
- Hash maps / dictionaries — ✅ — O(1) key→value lookup; collision handling via chaining/open addressing.
- Sets — ✅ — unordered unique collections; fast membership tests and set algebra.
- Tuples — ✅ — immutable fixed-size records.
- Stacks — ✅ — LIFO; undo, parsing, DFS, expression evaluation.
- Queues / deque — ✅ — FIFO / double-ended; BFS, buffering, scheduling.
- Linked lists — ✅ — nodes linked by pointers; O(1) insert/delete, no random access.
- Trees / BST — ✅ — hierarchical nodes; BST gives ordered O(log n) search/insert.
- Heaps / priority queues — ✅ — partially-ordered tree; O(1) peek min/max, O(log n) push/pop.
- Graphs (representation) — ✅ — vertices + edges; adjacency list vs matrix.

### 1.3 Algorithms (basic)
- Big-O time & space complexity — ✅ — how runtime/memory grow with input size; the language of efficiency.
- Linear / binary search — ✅ — scan vs halve-the-search-space (needs sorted data).
- Sorting (built-in + manual) — ✅ — ordering data; know O(n²) simple sorts vs O(n log n) merge/quick.
- Recursion fundamentals — ✅ — a function calling itself; base case + recursive case.
- Two pointers — ✅ — two indices moving through data to avoid nested loops.
- Sliding window — ✅ — a moving sub-range for substring/subarray problems in O(n).
- Prefix sums — 🟡 — precomputed cumulative sums for O(1) range-sum queries.

### 1.4 Object-Oriented Programming
- Classes & objects — ✅ — blueprints and their instances bundling data + behavior.
- Encapsulation — ✅ — hiding internal state behind a controlled interface.
- Inheritance — ✅ — a subclass reusing/extending a parent class.
- Polymorphism — ✅ — same interface, different behavior; avoid isinstance/type-switching.
- Abstraction / interfaces — ✅ — programming to a contract, not an implementation.
- Composition over inheritance — ✅ — building behavior by combining objects rather than deep class trees.
- SOLID principles — ✅ — five OOP design rules (see Junior §1.2) for maintainable code.

### 1.5 Programming Paradigms
- Procedural — ✅ — step-by-step instructions and procedures.
- Object-oriented — ✅ — organizing code around objects.
- Functional basics — ✅ — pure functions, immutability, map/filter/reduce; fewer side effects.

## 2. A Language in Depth — Python

### 2.1 Core Language
- Idiomatic syntax & PEP 8 — ✅ — writing "Pythonic" code to the style guide.
- Comprehensions (list/dict/set) — ✅ — concise one-line collection building.
- Slicing & unpacking — ✅ — `seq[a:b:c]` and `a, *rest = iterable`.
- f-strings & formatting — ✅ — inline string interpolation.
- Mutability & references — ✅ — which types can change in place + how names point to objects.

### 2.2 Intermediate Python
- Decorators — ✅ — wrap a function to add behavior (logging, timing, auth) without editing it.
- Generators & iterators (`yield`) — ✅ — lazy, memory-efficient streams of values.
- Context managers (`with`) — ✅ — guaranteed setup/teardown (files, locks, DB sessions) via `__enter__/__exit__`.
- `*args` / `**kwargs` — ✅ — variable positional/keyword arguments.
- Type hints / `typing` — ✅ — optional static type annotations for tooling and clarity.
- Dataclasses / Pydantic — ✅ — declarative data models with validation (Pydantic powers FastAPI).
- Custom exceptions / chaining — ✅ — defining your own error types and preserving causes.

### 2.3 Standard Library & Tooling
- `collections`, `itertools`, `json`, `datetime`, `os/sys` — ✅ — batteries-included utilities you'll use daily.
- `logging` module — ✅ 🏭 — structured, level-based logging instead of print.
- `threading` / concurrency primitives — ✅ — locks, semaphores, threads for concurrent code.
- venv / pip / requirements.txt — ✅ — isolated environments and dependency pinning.
- `uv` / lockfiles — ✅ — fast modern dependency resolver with reproducible lockfiles.
- Poetry — ✅ — alternative dependency/packaging manager.

## 3. Version Control — Git & GitHub  *(strong)*
- init / clone / status / add / commit — ✅ — the core local Git loop.
- `.gitignore` — ✅ — excluding files (secrets, build artifacts) from version control.
- History (log, diff, blame) — 🟡 — inspecting what changed, when, and by whom.
- Undo (reset, revert, restore) — 🟡 — safely rolling back changes at different levels.
- Feature/task branches — ✅ 🏭 — isolating work per feature before merging.
- Merging — ✅ — combining branches.
- Rebasing — 🟡 — replaying commits for a linear history (vs merge commits).
- Merge-conflict resolution — ✅ — reconciling competing edits to the same lines.
- Pull requests — ✅ — proposing + reviewing changes before merge.
- Issues (create/link/close) — ✅ — tracking work and bugs.
- Project boards / kanban — ✅ — visual task management on GitHub Projects.
- Tags & releases — 🟡 — marking versioned snapshots for distribution.

## 4. Command Line & Linux
- Navigation / file ops / viewing — ✅ — cd/ls/cp/mv/rm/cat/grep etc.
- Pipes & redirection — ✅ — chaining commands (`|`) and routing output (`>`, `2>&1`).
- Env vars / `.env` — ✅ — configuration via the environment, kept out of code.
- File permissions — 🟡 — chmod/chown; read/write/execute and ownership.
- Processes (ps/top/kill) — 🟡 — listing, monitoring, and terminating running programs.
- SSH & remote access — ✅ — secure shell into remote servers; key-based auth.
- Bash scripting — 🟡 — automating tasks with shell scripts.

## 5. How the Web Works
- HTTP model, methods, status codes — ✅ — request/response; GET/POST/etc.; 2xx/4xx/5xx meanings.
- Headers — ✅ — metadata on requests/responses (content-type, auth, caching).
- Cookies & sessions — ✅ — how servers remember a logged-in user across requests (cookie = opaque session ID; real identity lives server-side; HttpOnly/SameSite; sessions vs JWT).
- HTML / CSS — ✅  — page structure and styling (box model, flexbox, grid).
- Responsive design — ✅ — layouts that adapt to screen size.
- JavaScript fundamentals — ✅ — the browser's scripting language.
- DOM & events — ✅ — manipulating the page tree and reacting to user input.
- Client–server model — ✅ — who requests vs who serves.
- DNS resolution — ✅ — turning domain names into IP addresses.
- Browser rendering — ✅ — how HTML/CSS/JS become pixels (parse → layout → paint).

## 6. Databases (Basics)
- Relational model — ✅ — data as tables of rows/columns with relationships.
- SQL CRUD + WHERE/ORDER BY/GROUP BY — ✅ — create/read/update/delete + filter/sort/aggregate.
- Joins — ✅ — combining rows across tables (inner/left/right).
- Keys & relationships — ✅ — primary/foreign keys; one-to-many, many-to-many.
- Normalization — ✅ — structuring tables (1NF–3NF) to remove redundancy.
- ORM (Django ORM, MongoEngine) — ✅ 🏭 — querying the DB through Python objects.
- NoSQL basics — ✅ 🏭 — document/key-value stores; schema-flexible (MongoDB).
- Migrations — ✅ — versioned, repeatable schema changes.

## 7. Building a Backend (Basics)
- Framework project setup — ✅ 🏭 — bootstrapping Django/FastAPI/Flask apps.
- Routing / URL patterns — ✅ — mapping URLs to handler functions.
- Request handling & responses — ✅ — parsing input, returning JSON/HTML.
- Build a REST API — ✅ 🏭 — resource endpoints over HTTP.
- Templates / serving HTML — ✅ — server-rendered pages.
- Config & env separation — ✅🏭 — per-environment settings (dev/staging/prod).
- Basic auth (login/logout) — ✅ — authenticating users.

## 8. Testing (Basics)
- Why we test — ✅ — catching regressions and documenting behavior.
- Writing a unit test — ✅ — verifying one function/unit in isolation.
- Assertions — ✅ — stating expected outcomes.
- Running a test suite — ✅ — executing all tests and reading results.
- Read a failing test & fix — ✅ — using a red test to locate a bug.

## 9. Dev Tooling
- IDE proficiency (VS Code) — ✅ — editor features, extensions, shortcuts.
- Debugger (breakpoints, step) — 🟡 — pausing execution to inspect state (beyond print).
- Linters / formatters (flake8, black, isort) — 🟡 — auto-enforcing style and catching smells.
- Reading docs — ✅ — learning APIs from official documentation.

## 10. Soft Skills
- Problem decomposition — ✅ — breaking a big task into small solvable pieces.
- Searching docs / SO — ✅ — finding answers efficiently.
- Asking good questions — ✅ — giving context so others can help.
- Commit messages / READMEs — ✅ — communicating intent and onboarding others.
- Time management — ✅ — prioritizing and scoping work.

### ✅ Entry-Level Verdict
Fully cleared — only cosmetic 🟡s remain (rebase, debugger, linters, functional basics).

---
---

# PART 2 — JUNIOR ENGINEER ROADMAP

*Goal: production-quality code; ship safely with tests + CI; working security + system design; operate what you deploy.* **→ Knowledge strong; gaps in safety/ops.**

## 1. Advanced Language & Code Quality

### 1.1 Deeper Python
- Async / `asyncio` — 🟡 — non-blocking concurrency with async/await for I/O-bound work.
- Concurrency: threads, mutex, semaphore, GIL — ✅ — running work in parallel safely; the GIL limits CPU-bound threading.
- Profiling & performance (cProfile/timeit) — 🟡 — measuring where time goes before optimizing.
- Memory model & GC — 🟡 — reference counting + garbage collection; avoiding leaks.
- Strict typing + mypy — ❌ — enforcing type hints at check-time to catch bugs early.
- Packaging / publishing — 🟡 — `src` layout, `pyproject.toml`, building installable packages.

### 1.2 Software Design  *(strong)*
- SOLID applied — ✅ — SRP (one reason to change), OCP (open/closed), LSP (substitutability), ISP (small interfaces), DIP (depend on abstractions).
- Design heuristics: DRY, KISS, YAGNI, LoD, SoC, Fail-Fast — ✅ — don't-repeat, keep-simple, don't-over-build, least-knowledge, separate-concerns, error-early.
- GoF Design Patterns — ✅ — reusable solutions to recurring design problems:
  - Creational (Singleton, Factory, Abstract Factory, Builder, Prototype) — ✅ — controlling how objects are created.
  - Structural (Adapter, Bridge, Composite, Decorator, Facade, Proxy) — ✅ — composing objects into larger structures.
  - Behavioral (Strategy, Observer, Command, State, Template, Iterator, Memento, Chain of Responsibility, Visitor, Interpreter) — ✅ — how objects communicate and share responsibility.
- Clean code & naming — ✅ — readable, intention-revealing code.
- Refactoring (legacy → improved) — ✅ — restructuring code without changing behavior.
- LLD / OOD case studies — ✅ — designing real systems (vending machine, parking lot, elevator, booking) class-by-class; state machines + transition matrices.

### 1.3 Architecture Styles  *(strong)*
- Layered / N-tier (MVT) — ✅ 🏭 — presentation → business → data separation.
- Clean / Onion — ✅ — dependencies point inward toward domain core.
- Hexagonal (ports & adapters) — ✅ — isolate business logic from external tech via interfaces.
- CQRS — ✅ — separate read and write models/paths.
- Event-Driven Architecture (pub/sub) — ✅ — components react to events instead of calling each other directly.
- Microservices — ✅ — independently deployable services with their own data, talking over the network.
- Coupling & dependency management — ✅ — minimizing how tightly modules depend on each other.
- Monolith vs microservices trade-offs — ✅ — when to split vs stay unified.

## 2. Testing (Depth)  *(true gap — partial)*
- Test pyramid — 🟡 — many fast unit tests, fewer integration, fewest slow e2e.
- pytest + pytest-django — 🟡 — the standard Python test runner + Django integration.
- Fixtures — ❌ — reusable, composable test setup/teardown.
- Mocking & patching (`unittest.mock`) — ❌ — replacing real dependencies (APIs, DB, time) with fakes.
- Test data factories (factory_boy / faker) — ❌ — generating realistic test objects on demand.
- Coverage measurement (coverage.py) — ❌ — measuring which lines tests exercise.
- DRF `APITestCase` — 🟡 — testing REST endpoints end-to-end.
- Integration tests — 🟡 — testing components together (with real DB/services).
- TDD workflow — ❌ — write the failing test first, then code to pass it.
- Property-based (Hypothesis) — ❌ — generate many random inputs to find edge cases.
- Load testing (Locust) — ❌ — simulating many concurrent users to find bottlenecks.
- Time control (freezegun) — ❌ — freezing/mocking the clock in tests.
- LLM testing — ❌ — eval datasets, mocking LLM calls for determinism, LLM-as-judge. *(rare differentiator)*

## 3. CI/CD  *(true gap — biggest, on YOUR repos)*
- What CI/CD is & why — 🟡 — automatically build/test/deploy on every change.
- GitHub Actions syntax (jobs/steps/triggers) — ❌ — YAML workflows triggered by push/PR.
- Pipeline: lint → test → build → deploy — ❌ — the standard automated quality gate.
- Secrets in CI — ❌ — injecting credentials securely into pipelines.
- Dependency & build caching — ❌ — speeding pipelines by caching deps/layers.
- Matrix builds — ❌ — testing across multiple versions/OSes in parallel.
- Build & push Docker image in CI — ❌ — producing deployable images automatically.
- Automated deploy from CI — ❌ — shipping to a host when checks pass.
- Status badges — ❌ — README badge showing build/test status.
- Branch protection (require checks) — ❌ — blocking merges until CI passes.

## 4. Databases (Engineering)
- Indexes (B-tree, composite, when) — ❌ — data structures that make lookups fast; know when to add one.
- Query plans (`EXPLAIN ANALYZE`) — ❌ — reading how the DB executes a query to find slowness.
- N+1 problem (select_related/prefetch_related) — ❌ — accidental per-row queries in ORMs; the classic Django interview bug.
- Query optimization & profiling — ❌ — rewriting slow queries; spotting full scans.
- Transactions: ACID, isolation, deadlocks — 🟡 — all-or-nothing units; isolation levels; deadlock avoidance.
- Safe / zero-downtime migrations — 🟡 — schema changes without breaking a live app.
- Connection pooling — 🟡 — reusing DB connections under load.
- Caching strategies (cache-aside, TTL, eviction LRU/LFU) — ✅ — serving hot data from memory; expiry + eviction policies.
- Replication / read replicas — 🟡 — copies of the DB to scale reads / for failover.
- Sharding / partitioning — ❌ — splitting data across nodes for horizontal scale.
- Backups & restore — ❌ — disaster recovery; tested restores.
- SQL vs NoSQL trade-offs — ✅ 🏭 — choosing the right store per access pattern.

## 5. API Engineering
- REST best practices — ✅ 🏭 — resource-oriented, stateless HTTP APIs.
- Resource naming & status-code discipline — 🟡 — nouns for URLs, correct codes for outcomes.
- Versioning — ❌ — evolving an API without breaking clients (/v1, headers).
- Pagination — 🟡 — returning large result sets in pages (offset/cursor).
- Filtering / sorting / search — 🟡 — query params to shape responses.
- Rate limiting / throttling — 🟡 — capping request rates to protect the service.
- Auth: API keys ✅ / Session 🟡 / JWT 🟡 / OAuth2 ❌ — proving who the caller is; stateless tokens vs delegated auth.
- Authorization / RBAC — ✅ 🏭 — what an authenticated user is allowed to do (role-based).
- API docs (OpenAPI/Swagger/drf-spectacular) — 🟡 — machine-readable, browsable API contracts.
- Standardized error responses — 🟡 — consistent error shape across endpoints.
- Idempotency & safe retries — 🟡 — making repeated calls safe (no double charge).
- Webhooks — 🟡 🏭 — server-to-server event callbacks.
- GraphQL — ❌ — query language letting clients request exactly the fields they need. *(optional)*

## 6. Security  *(true gap — missing)*
- OWASP Top 10 — ❌ — the canonical list of the most critical web vulnerabilities:
  - Injection (SQL/command) — ❌ — untrusted input executed as code/queries; fix with parameterization.
  - Broken authentication — ❌ — weak login/session handling letting attackers impersonate users.
  - Sensitive data exposure — ❌ — leaking secrets/PII via logs, transit, or storage.
  - Broken access control — 🟡 — users accessing things they shouldn't (you do RBAC).
  - Security misconfiguration — ❌ — insecure defaults, open ports, verbose errors.
  - XSS — ❌ — injecting scripts into pages viewed by other users.
  - CSRF — 🟡 — tricking a logged-in browser into unwanted actions (Django guards this).
  - SSRF — ❌ — tricking the server into making attacker-chosen requests.
  - Vulnerable dependencies — ❌ — known-CVE libraries in your tree.
- Password hashing (bcrypt/argon2) — 🟡 — one-way salted hashing, never plaintext.
- Secrets management (never commit; vaults) — 🟡 — keeping keys out of code and history.
- Input validation & sanitization — 🟡 — rejecting/cleaning untrusted input (Pydantic helps).
- HTTPS / TLS termination — ✅ 🏭 — encrypting traffic; ending TLS at the proxy.
- CORS — 🟡 — controlling which origins may call your API from a browser.
- Security headers (CSP, HSTS, X-Frame-Options) — 🟡 — browser-enforced hardening.
- Dependency scanning (pip-audit/Dependabot) — ❌ — automated alerts for vulnerable packages.

## 7. System Design (Junior level)  *(strong)*
- Reverse proxy — ✅ 🏭 — a front server routing/protecting/terminating TLS for backends (nginx).
- Load balancing — ✅ — spreading traffic across many backends:
  - L4 vs L7 — ✅ — balance by IP/port vs by HTTP content.
  - Algorithms (round-robin ✅, least-conn / ip-hash 🟡) — how requests are distributed.
  - Active health checks — ✅ — auto-evicting unhealthy backends (rise/fall/interval).
- Horizontal vs vertical scaling — ✅ — add more machines vs a bigger machine.
- Caching layers (app / CDN / DB) — ✅ — storing results closer to the user/app.
- CDN & object storage — ✅ 🏭 — edge-cached static assets; S3-style blob storage (R2).
- Statelessness & session storage — 🟡 — keep app servers stateless; store sessions externally.
- Message queues / async workers — ✅ 🏭 — offloading slow work from the request cycle (Celery).
- Event-driven / pub-sub at scale — ✅ — decoupling producers and consumers of events.
- DB replication & read replicas — 🟡 — scaling reads / failover.
- Sharding / partitioning — ❌ — splitting data for write/scale.
- CAP theorem & consistency models — ❌ — the consistency/availability/partition trade-off.
- Service discovery / overlay networks — 🟡 — services finding each other across hosts.
- Practice "design X" problems — 🟡 — interview-style whiteboard designs (URL shortener, rate limiter, feed).

## 8. Networking (Deeper)  *(strong)*
- OSI (L4 vs L7) — ✅ — the layered network model; transport vs application.
- TCP vs UDP, 3-way handshake — ✅ — reliable connection setup vs fire-and-forget.
- TLS/SSL handshake & SNI — ✅ — how encryption is negotiated; routing TLS by hostname.
- DNS (A, CNAME, round-robin) — ✅ — name resolution + basic DNS load distribution.
- HTTP/1.1 keep-alive — 🟡 — reusing connections for multiple requests.
- HTTP/2 & HTTP/3 — 🟡 — multiplexed / QUIC-based modern HTTP.
- WebSockets — 🟡 — persistent two-way connections for real-time.
- Proxy headers (`X-Forwarded-For`, `X-Real-IP`) — ✅ — preserving the client IP through proxies.
- Firewalls / ports / security groups — 🟡 — controlling network access.

## 9. DevOps & Infrastructure
- Docker (images, containers, volumes, networks) — ✅ 🏭 — packaging apps into portable containers.
- docker-compose multi-service — ✅ 🏭 — defining multi-container stacks declaratively.
- Dockerfile best practices (layer cache, slim) — 🟡 — small, fast, reproducible images.
- Multi-stage builds — 🟡 — separate build vs runtime stages for lean images.
- Container registry — 🟡 — storing/distributing images (push/pull).
- Cloud (Azure ✅ 🏭, AWS 🟡) — managed compute/storage/networking.
- PaaS deploys (Render, Vercel) — ✅ 🏭 — push-to-deploy hosting.
- Container management (Portainer) — ✅ 🏭 — a UI to run/monitor containers.
- Kubernetes (pod/deploy/service) — ❌ — orchestrating containers at scale (self-healing, scaling).
- IaC (Terraform) — ❌ — declaring infrastructure as version-controlled code.
- Reverse proxy / nginx config — ✅ 🏭 — writing nginx server/location/proxy_pass blocks.

## 10. Observability  *(true gap — partial)*
- Log levels — ✅ — DEBUG/INFO/WARN/ERROR severity.
- File-based logging — ✅ 🏭 — writing logs to files for diagnosis.
- Structured / JSON logging (structlog) — ❌ — machine-parseable logs for aggregation.
- Correlation / request IDs — ❌ — tracing one request across services/logs.
- Error tracking (Sentry) — ❌ — automatic capture + alerting on exceptions.
- Metrics (Prometheus + Grafana) — ❌ — counters/gauges/histograms + dashboards (RED/USE).
- Tracing (OpenTelemetry + Jaeger/Tempo) — ❌ — following a request's path/timing across services.
- Health checks (`/healthz`, `/readyz`) — ❌ — liveness (alive?) vs readiness (ready to serve?) endpoints.
- Alerting & SLI/SLO/error budgets — ❌ — getting paged on problems; reliability targets.
- Uptime monitoring (UptimeRobot/Healthchecks.io) — ❌ — external "is it up?" pings.
- Resource monitoring (docker stats) — ✅ 🏭 — watching CPU/memory/storage of containers.

## 11. Async & Background Processing
- Task queues (Celery) — ✅ 🏭 — running jobs outside the web request.
- Broker / result backend (Redis) — ✅ 🏭 — the queue transport + result store.
- Scheduled tasks (Celery beat / cron) — 🟡 — running jobs on a timetable.
- Retries, backoff, idempotency — 🟡 — surviving transient failures without duplicating effects.
- Message durability (Redis vs RabbitMQ/Kafka) — 🟡 — in-memory speed vs persistent log-based brokers.
- Dead-letter / failure handling — ❌ — quarantining messages that keep failing.

## 12. AI / LLM & Agent Engineering  *(specialty / standout)*
- LLM API integration (GPT, Gemini, xAI) — ✅ 🏭 — calling model providers from code.
- LangChain (chains, routers) — ✅ 🏭 — composing LLM calls + routing logic.
- LangGraph graphs (nodes/edges/state) — ✅ 🏭 — modeling agent control flow as a state graph.
- State management (schemas, reducers, multi-schema) — ✅ — how graph state is shaped and updated.
- Short-term memory / summarization / trimming — ✅ — managing conversation context within token limits.
- Long-term memory (store, profile & collection) — ✅ — persisting facts across sessions.
- Human-in-the-loop (breakpoints, edit-state, time-travel) — ✅ — pausing an agent for human approval/edits.
- Streaming responses / interruption — ✅ — token-by-token output you can cancel.
- Map-reduce / parallelization / sub-graphs — ✅ — fanning out work and composing sub-agents.
- Multi-agent / subagents — ✅ — coordinating specialized agents on subtasks.
- Building agents from scratch (file/task/todo/research tools) — ✅ — custom tool-using agents.
- Tool calling / function calling — ✅ 🏭 — letting the model invoke your functions.
- Research assistant / agentic retrieval — ✅ — agents that search + synthesize.
- RAG — ✅ 🏭 — grounding answers in retrieved documents (vector search).
- Vector databases (Qdrant) — ✅ 🏭 — storing/searching embeddings by similarity.
- Prompt engineering & templates — ✅ — designing reliable, reusable prompts.
- Agent deployment (LangGraph platform, assistants, double-texting) — ✅ — serving agents in production.
- Token / cost management — 🟡 — controlling spend and context size.
- Guardrails & output validation — ❌ — constraining/validating model output (schemas, filters, safety).
- LLM evaluation — ❌ — eval datasets + LLM-as-judge to measure quality. *(rare, high-value)*
- LLM observability (Langfuse-style tracing) — 🟡 — tracing prompts/costs/latency of LLM calls.

## 13. Data Structures & Algorithms (Interview Filter)  *(strong)*
- Complexity analysis (Big-O, amortized) — ✅ — reasoning about scaling cost.
- Arrays & strings — ✅ — in-place tricks, scanning, hashing.
- Hash maps / sets — ✅ — O(1) lookup patterns (dedup, counting, grouping).
- Two pointers / sliding window — ✅ — linear-time subarray/substring techniques.
- Stacks & queues — ✅ — monotonic stacks, BFS queues, parsing.
- Linked lists — ✅ — pointer manipulation (reverse, cycle, merge, LRU).
- Trees & BST (traversals) — ✅ — DFS/BFS, in/pre/post-order, BST properties.
- Heaps / priority queues — ✅ — top-k, scheduling, merge-k.
- Recursion — ✅ — divide-and-conquer thinking.
- Dynamic programming — ✅ — memoization/tabulation for overlapping subproblems.
- Greedy — ✅ — locally-optimal choices that prove globally optimal.
- Bit manipulation — ✅ — bitwise tricks (masks, counting bits, base conversion).
- Math / number theory — ✅ — primes, gcd, digit/number problems.
- Intervals — ✅ — merging/inserting overlapping ranges.
- Graphs — traversal (BFS/DFS/Dijkstra) — 🟡 — shortest paths, connectivity (representation done; traversal next).
- Backtracking — 🟡 — explore-and-undo search (N-Queens, permutations, subsets, Sudoku).
- Tries (prefix trees) — ❌ — fast prefix/autocomplete lookups.
- Disjoint Set Union (Union-Find) — ❌ — tracking merged groups (Kruskal, connectivity).
- Competitive programming (CodeForces) — ✅ — timed contest problem-solving practice.

## 14. Professional Practices
- Agile / Scrum — ✅ — iterative delivery, sprints, standups.
- Code review (give/receive) — 🟡 — constructive feedback + responding to it.
- Technical writing & study notes — ✅ — clear docs/specs (you write strong `.md` roadmaps).
- README / architecture docs — 🟡 — explaining how to run + how it's built.
- Debugging methodology — 🟡 — reproduce → isolate → fix → verify.
- Task estimation — 🟡 — predicting effort realistically.
- Onboarding into a large codebase — 🟡 — navigating unfamiliar code efficiently.
- Pair programming — 🟡 — collaborative real-time coding.

## 15. Deployment & Release Engineering
- Deploy to PaaS / cloud — ✅ 🏭 — getting an app live.
- Env separation (dev/staging/prod) — 🟡 — isolated environments per stage.
- Zero-downtime deploys — 🟡 — releasing without dropping requests.
- Rollbacks — ❌ — reverting to a previous good release fast.
- Blue-green / canary — ❌ — shifting traffic gradually/safely to a new version.
- Feature flags — ❌ — toggling features without redeploying.
- Graceful shutdown / circuit breakers / retry-with-backoff — 🟡 — resilient handling of failure/restart.

---
---

# Junior-Level Priority Summary

Your knowledge gaps are largely closed (design, architecture, concurrency, DSA, agentic AI are ✅).
Remaining true gaps are in **operations, safety, and a few interview-tail topics**:

### 🔴 Close these (highest impact)
1. **CI/CD on your own repos** — GitHub Actions (lint+test) on RideBuddy/Volunteer Portal. ~1 day.
2. **Security / OWASP Top 10** — most invisible gap; nothing in your work shows it. ~1 weekend.
3. **Testing depth** — fixtures, mocking, coverage, factory_boy, Locust (already in your RoadMap).
4. **Database engineering** — indexing, `EXPLAIN`, the N+1 problem.
5. **Observability** — Sentry + structured logging + `/healthz`.

### 🟡 Finish the tail
6. **DSA tail** — graph traversal (BFS/DFS/Dijkstra), backtracking, tries, Union-Find.
7. **AI tail** — LLM evaluation + guardrails.

### ✅ Already strong — lean into these
GoF patterns, SOLID/principles, architecture styles, LLD/concurrency, system design (proxy/LB/
caching/queues), networking, agentic AI (full LangChain Academy + agents-from-scratch), DSA core,
Docker, multi-DB.

> **Resume caveat:** practice labs and course work are real *knowledge* but go on the resume only
> as a "Skills/Study" line or a public documented project — not as production bullets unless deployed.
>
> **For future threads:** point me here and name a section/status (e.g. "teach me §6 ❌ items").
> I'll start from your current level using these descriptions and skip what you already know.
