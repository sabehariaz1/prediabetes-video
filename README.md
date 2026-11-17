# Prediabetes Community Explainer Video (2 Minutes)

An educational, community-focused 1080p animated explainer video built with Remotion and rendered automatically via GitHub Actions.

## Folder Structure
- `src/index.ts` — Remotion entry point
- `src/Root.tsx` — Video composition registration (1920x1080, 30fps, 3,600 frames = 2:00)
- `src/theme.ts` — Shared color palette, typography, and timing constants
- `src/components/SlideShell.tsx` — Reusable slide wrapper, background watermarks, and bottom caption bar
- `src/components/Icons.tsx` — Reusable vector medical illustrations (person silhouette, blood drop, glucose meter, sugar cup, heart)
- `src/scenes/Scene1Hook.tsx` — Global prevalence & silent symptoms (0:00 – 0:16)
- `src/scenes/Scene2WhatIsIt.tsx` — Animated A1C semicircular gauge (0:16 – 0:32)
- `src/scenes/Scene3InsideBody.tsx` — Healthy insulin key vs. insulin resistance (0:32 – 0:48)
- `src/scenes/Scene4RiskFactors.tsx` — Combined 3-column risk factors overview (0:48 – 1:10)
- `src/scenes/Scene5HowToFindOut.tsx` — 3 diagnostic tests with Normal & Prediabetes ranges (1:10 – 1:30)
- `src/scenes/Scene6GoodNews.tsx` — 58% risk reduction & lifestyle pillars (1:30 – 1:45)
- `src/scenes/Scene7Closing.tsx` — Action steps, community awareness purpose & ADA/CDC references (1:45 – 2:00)
- `.github/workflows/render-video.yml` — Automated GitHub Actions MP4 renderer

## How to Render on GitHub
1. Upload all files and folders (including `src/` and `.github/`) to your GitHub repository.
2. Open the **Actions** tab and wait for **Render 2-Minute Prediabetes Explainer** to complete.
3. Download **`prediabetes-explainer-2min`** under **Artifacts**.
