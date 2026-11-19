# Prediabetes explainer video: GitHub build kit

## Setup (5 minutes)
1. Copy these into your repo root, keeping the folders:
   - `.github/workflows/build-video.yml`
   - `video-src/` (build_video.py, script.json, voiceover/)
2. On GitHub: **Settings > Actions > General > Workflow permissions > Read and write permissions** > Save.
3. **Actions tab > "Build explainer video" > Run workflow.** It takes about 8-15 minutes.
4. The finished `prediabetes-explainer.mp4` is committed to your repo root (and attached as a downloadable artifact). Your GitHub Pages site picks it up automatically.
5. Open `page-snippet.html`, paste the `<video>` tag and the ranges/references section into your `index.html`.

## Customising
- **Words:** edit `video-src/script.json`. The first sentence starts with "If you have a risk score of 5 or higher...". Scene timing adjusts to the voice automatically.
- **Screen text / ranges:** edit `TESTS` and `REFS` in `video-src/build_video.py`.
- **Voice:** set env `TTS_VOICE` in the workflow (e.g. `en-GB-SoniaNeural`, `en-US-AndrewNeural`). If the voice annoys you, the most natural option is your own: record one file per scene and save as `video-src/voiceover/hook.mp3`, `what.mp3`, `silent.mp3`, `tests.mp3`, `calc.mp3`, `dpp.mp3`, `steps.mp3`, `outro.mp3`. Any file present replaces the generated voice.
- **Music:** original, royalty-free, generated in code (soft C-G-Am-F piano-pluck and pad, ducked under the voice).

## Local test
`pip install pillow numpy edge-tts` (plus ffmpeg), then `PREVIEW=1 python video-src/build_video.py` for a fast low-res render.
