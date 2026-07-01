## Conventional Commits (worth adopting)
A widely-used standard that prefixes the type — and it feeds automation later (auto-changelogs, semantic versioning in CI, which ties to your CI/CD gap):

| Prefix    | For                                     |
| ---       | ---                                     |
| feat:     | a new feature                           |
| fix:      | a bug fix                               |
| docs:     | documentation only                      |
| refactor: | code change that isn't a fix or feature |
| test:     | adding/fixing tests                     |
| chore:    | tooling, deps, config                   |
| perf:     | performance improvement                 |

## Examples
1. Simple subject-only (fine for small, self-explanatory changes)

    ```
    solve: 155 Min Stack with O(1) getMin

    fix: handle empty list in heapify to avoid IndexError

    docs: add setup instructions to RideBuddy README

    test: add cases for cost-splitting with odd passenger count

    chore: bump langchain to 0.2.6
    ```

2. feat with a body (new feature — explain the why)
    ```
    feat: add Redis caching to TraderBro signal endpoint

    The /signals endpoint recomputed aggregation on every request,
    causing ~800ms responses under load. Cache results in Redis with
    a 60s TTL, cutting average response time to ~120ms.

    Refs #47
    ```

3. fix with a body + issue reference (the most valuable kind)
    ```
    fix: prevent driver from booking their own ride

    RideBuddy allowed a driver to appear as a passenger on their own
    posted ride, corrupting the seat count. Added a check that rejects
    bookings where passenger == ride.driver.

    Fixes #128
    ```

4. refactor (behavior unchanged — say what got cleaner)
    ```
    refactor: extract ride-matching into MatchStrategy class

    Matching logic was inlined in the view, making it untestable.
    Moved it behind a MatchStrategy interface so cost-splitting and
    gender-filter rules can be swapped and unit-tested independently.
    ```

5. perf (a measured improvement)
    ```
    perf: fix N+1 query in volunteer attendance list

    Listing volunteers issued one query per row for their role.
    Added select_related('role'), reducing 201 queries to 2.
    ```

## The pattern in one glance
```
<type>: <imperative summary, ~50 chars, no period>
        ↑ add / fix / refactor / solve / docs / test / perf / chore
<blank line>
<body — WHY, not what; wrap ~72 chars>
<blank line>
Fixes #<issue>
```
```
git commit -m "fix: prevent double booking" -m "Caused by a race condition in the payment task."
```