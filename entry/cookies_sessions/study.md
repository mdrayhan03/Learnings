The problem: HTTP is stateless
Every HTTP request is independent — the server has no built-in memory that request #2 came from the same person as request #1. So after you log in, how does the next request prove "it's still me"?

Answer: the client sends a little piece of identifying data with every request. That piece is a cookie.

Cookies — the browser's automatic memory
A cookie is a small key=value pair that:

The server sets via a response header (Set-Cookie).
The browser stores.
The browser automatically sends back on every subsequent request to that domain (Cookie header).
The actual HTTP looks like this:


# Response — server tells browser to store a cookie
HTTP/1.1 200 OK
Set-Cookie: sessionid=abc123xyz; HttpOnly; Secure; SameSite=Lax

# Every later request — browser sends it back automatically
GET /dashboard HTTP/1.1
Cookie: sessionid=abc123xyz
That automatic re-sending is the whole trick. You don't write code to attach it — the browser does it for you for that domain.

Cookie attributes (this is where security lives)
When setting a cookie, the attributes matter enormously:

Attribute	Meaning	Why it matters
Expires / Max-Age	when it dies	no expiry = "session cookie" (gone when browser closes)
Domain / Path	where it's sent	scope the cookie tightly
Secure	only sent over HTTPS	stops sniffing on plain HTTP
HttpOnly	JavaScript can't read it	blocks XSS from stealing the session
SameSite	Strict/Lax/None — sent on cross-site requests?	primary CSRF defense
Two of these are critical for your security gap:

HttpOnly → even if an attacker injects JS (XSS), document.cookie can't read the session cookie. Always set it on auth cookies.
SameSite=Lax (or Strict) → the browser won't send the cookie on cross-site form posts, which neuters most CSRF attacks.
Sessions — where the real data lives
Here's the key distinction people miss:

A cookie is just the transport. A session is server-side state that the cookie points to.

You almost never store real user data in the cookie itself. Instead:

On login, the server creates a session record (server-side — in a DB table or Redis) holding {user_id: 42, role: "admin", ...}.
It gives that record a random session ID and sends only that ID to the browser in a cookie.
On each request, the browser sends the session ID; the server looks up the record to know who you are.

Browser cookie:   sessionid = abc123xyz          ← just an opaque pointer
Server store:     abc123xyz → {user_id: 42, role: "admin", cart: [...]}   ← the real data
Why only the ID? Because the browser can't be trusted — if you stored role=admin in the cookie, a user could edit it. Storing it server-side and handing out a random ID means tampering is useless (they'd have to guess a valid session ID).

The full login flow

1. POST /login  (username + password)
2. Server verifies credentials
3. Server creates session {user_id: 42} in Redis/DB, gets id "abc123"
4. Response: Set-Cookie: sessionid=abc123; HttpOnly; Secure; SameSite=Lax
5. Browser stores it
6. GET /dashboard  →  Cookie: sessionid=abc123  (automatic)
7. Server looks up "abc123" → user 42 → "this is Rayhan" → serves page
8. Logout → server deletes the session record + clears the cookie
How Django does exactly this
You've used this without seeing the mechanism:


from django.contrib.auth import login

def my_login(request):
    user = authenticate(username=u, password=p)
    login(request, user)      # creates session, sets the 'sessionid' cookie
    # Django stored {_auth_user_id: user.pk} server-side

def dashboard(request):
    request.user            # Django read 'sessionid', looked up the session, gave you the user
    request.session['x']    # you can store arbitrary per-user data here
The cookie is named sessionid by default.
The session data lives in the django_session table (default) — or Redis/cache if you set SESSION_ENGINE to a cache backend (much faster; relevant to your Redis experience).
Django's CSRF protection uses a separate csrftoken cookie + form token — the mechanism you've seen as "Django gives CSRF for free."
Sessions vs tokens (JWT) — connects your other 🟡
This is the big architectural fork, and a common interview question:

Session (cookie + server store)	JWT (token)
Where's the state?	server-side (DB/Redis)	inside the token itself (signed)
Server memory	needs a session store	stateless — nothing to store
Revoke/logout	easy — delete the record	hard — token valid until it expires
Scaling across servers	needs shared store (Redis)	trivial — any server can verify the signature
Typical use	traditional web apps (browser)	APIs, mobile, microservices
Rule of thumb: browser web app → sessions; stateless API / mobile / service-to-service → JWT. Sessions are easy to revoke; JWTs are easy to scale. Knowing why you'd pick each is what interviewers want.

Security threats to name (your OWASP prep)
Session hijacking — attacker steals the session ID (via sniffing or XSS) → use Secure + HttpOnly.
Session fixation — attacker plants a known session ID before login → fix by rotating the session ID on login (Django does this).
CSRF — attacker makes your browser send its cookie on a forged request → SameSite + CSRF tokens.
XSS stealing cookies — mitigated by HttpOnly.
---
Exercises
1. Why is it a bad idea to store is_admin=true directly in a cookie, and what should you store instead?
ans: if we store is_admin = true in the cookie then if cookie stole then can use that as admin and that's very risky. instead we should use normal cookie and we will check in the code logic is this session for admin or not.

2. Which cookie attribute stops a successful XSS attack from reading the session cookie? Which one is the main CSRF defense?
ans: use HttpOnly for make it more secure, CSRF tokens help to defense CSRF

3. You're building a mobile app + REST API backend. Session cookies or JWT — which, and give the main reason.
ans: we should use JWT here because our client is device not a brower so we can't store session like cookie so we need to use JWT

4. Trace it: a user logs in, closes the browser tab (not the browser), reopens it, and is still logged in. What kind of cookie (attribute-wise) made that possible, and where was the actual user identity stored the whole time?
ans: session exprie time attribute helps to store the session in the browser cookie under the domain or url

5. Judgment: your app runs on 3 load-balanced servers. With cookie-sessions, a user logs into server A but their next request hits server B and they're logged out. What's the fix — and how does JWT sidestep this problem entirely?
ans: for this we need a sticky session in the load balancer and session create from the backend server and need to store but JWT don't need to store or create from server side that's why we need to use JWT