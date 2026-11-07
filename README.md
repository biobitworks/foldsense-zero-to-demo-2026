# FoldSense — The Living Protein Storybook

**Zero to Demo 2026** · NemulAI × Hack District · November 7, 2026

**See, Hear, and Feel Protein Folding** — an interactive, accessible, musical learning experience about protein structure, sequence, and changing conformational relationships.

## Watch, play, inspect

- **Video walkthrough:** [Watch the musical storybook demonstration](submission.html) ([MP4](video/foldsense-zero-to-demo-2026.mp4)).
- **Interactive storybook:** [Open the local-first HTML storybook](storybook.html).
- **Published FoldSense Touch Lab:** https://foldsense-touch-lab.lovable.app/
- **Public GitHub submission:** https://github.com/biobitworks/foldsense-zero-to-demo-2026
- **Private upstream/canonical code:** `biobitworks/foldsense` (not public; not part of this submission).

### What is built

A six-chapter educational *metaphor* from 0D (one amino-acid focus), 1D (primary sequence), 2D (secondary motifs), 3D (tertiary shape), 4D (temporal conformational relationships), to M (multiscale/multimodal and possible quaternary context). This is not a literal dimensional classification of biochemistry.

The standalone HTML prototype implements three learning routes (sequence, shape, movement), four sensory-preference presets (all, less vision, less hearing, combined), SVG molecular illustrations, a deterministic 12-frame toy residue-distance trajectory, a 5.0 demo-unit threshold, original browser-synthesized educational music, optional narration, text/caption equivalents, vibration API requests, a simple question, and local JSON receipts.

Musical voices increase 1 → 1 → 2 → 3 → 4 → 5 from 0D to M. In 4D, the *synthetic* distance crosses the threshold at frame 6 (5.226 → 4.630 demo units), switching the illustrative consonant/dissonant chord. **Musical dissonance is an artistic mapping, not a measured protein energy, pathology, or stability score.** All diagrams and trajectories are illustrative; none are experimentally validated molecular dynamics.

### Technical stack and evidence

| Technology | Role | Evidence state |
|---|---|---|
| HTML5, CSS, vanilla JavaScript, SVG | Standalone educational story and interaction | **IMPLEMENTED**, browser-tested |
| Web Audio API oscillator synthesis | Original multivoice sound, instrument and tempo options | **IMPLEMENTED**, headless browser call tested; human audio **NOT_TESTED** |
| Web Speech API (speechSynthesis), ARIA text | Optional narration and screen-reader-readable status | **IMPLEMENTED**, physical spoken output **NOT_TESTED** |
| Browser Vibration API | Requested haptic event cues | **IMPLEMENTED**, S26 Chrome API accepted earlier in separate Touch Lab; this draft physical felt **NOT_TESTED** |
| Playwright / headless Chromium | 4 preferences × 3 learning paths, 12 test cases | **EXECUTED**, **12/12 PASS** on original review artifact |
| Lovable | Separate published FoldSense Touch Lab and accessibility routes | **PUBLISHED** separately; storybook prototype **NOT_IMPORTED** at this checkpoint |
| Firecrawl and SearchAPI | External source/scholarly-snippet retrieval in Touch Lab | Historical authenticated calls observed; **NOT** called by this static storybook |
| ExecuTorch 1.5.1 / XNNPACK | Separate S26 Android numerical canary | Real native device inference **OBSERVED**; trained storybook model **NOT_CONNECTED** |
| Ollama, Liquid LFM2.5 1.2B, Qwen2.5 1.5B | Separately executed source-bounded local candidate explanations on magicSTUDIObox | **EXECUTED**; **NOT** integrated into browser or phone storybook |
| Liquid Apollo / Samsung Qualcomm NPU (QNN) | Possible on-device multimodal engine | Apollo app package detected; model forward/QNN **NOT_TESTED** |
| Galaxy S26 Ultra / S Pen | Demonstration target | USB ADB/Chrome/pen driver **OBSERVED**; human pen interaction **NOT_TESTED** |
| Galaxy Watch Ultra2 | Planned complementary Wear OS haptic/story receiver | **NOT_CONNECTED**, native watch app **NOT_IMPLEMENTED** |
| Runway, Roblox, Minecraft | Exploratory visual/game references | **NOT_IMPLEMENTED**, no runtime dependence |

### Demo video provenance

The MP4 is a **screen-capture-derived, edited educational walkthrough** rendered from the actual offline storybook HTML in headless Chromium/Puppeteer, with an original algorithmically synthesized audio score matching the chapter mapping. It is **not** a live S26 recording, a demonstration of a watch connection, or a validated scientific folding trajectory. Source and script are in `scripts/`, and receipt under `evidence/`.

### Reproduce

Serve the repository statically (`python3 -m http.server 8000`) and open `http://localhost:8000/storybook.html`. Use `submission.html` for the video and judge-friendly overview. Test scripts under `tests/` may require Playwright/Chromium.

### Governance

This repository is a **public-safe educational submission**, separate from the private canonical FoldSense repository and its versioned FCO/FCG lineage. SHA-256 establishes byte identity only, not biological truth.

`SIGNATURE_STATE=NOT_SIGNED` · `MERKLE_MMR_STATE=NOT_COMMITTED`.

No production sponsor credentials, proprietary models, private conversation exports, experimental claims, or watch pairing data are included.
