# Comeback — career meme

`Comeback` + spinner → years **2022 → 2026** (slide + fade, 0.7s hold each) → cut to black → **404 / Not Found**.
Warm sepia + film-grain vintage look.

## 1. Preview it (no install)

Just open the file in a browser:

```bash
open index.html        # macOS
```

Click anywhere (or press **R**) to replay. **This alone is enough to screen-record** with QuickTime / OBS.

## 2. Export a clean MP4 (frame-perfect)

Needs Node (have it) + ffmpeg:

```bash
brew install ffmpeg        # one time
npm install                # installs puppeteer (downloads a Chrome ~once)
npm run render             # -> out.mp4  (1080x1920 vertical, 60fps)
```

Other sizes:

```bash
npm run render:square      # 1080x1080
npm run render:wide        # 1920x1080
OUT=comeback.mp4 FPS=30 node render.js
```

## Tweaks

- **Timing** (fade-in, the 0.7s hold, slide speed): the `:root` CSS vars at the top of `index.html`.
- **Years**: the `YEARS` array in the `<script>`.
- **Colors / fonts**: CSS — `#comeback`, `#year`, `#err-code` (the red `#e23b3b`).

Everything is driven by a single `seek(t)` function, so the preview and the MP4 are identical frame-for-frame.
