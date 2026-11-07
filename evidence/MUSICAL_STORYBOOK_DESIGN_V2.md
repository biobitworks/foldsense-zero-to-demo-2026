# FoldSense: Musical Storybook v2 — review gate

## Scientific and artistic boundary

This is a **deterministic educational sonification of a hand-authored toy fixture**, **not** a model of folding free energy, solvent state, protein function, stability, disorder, or real molecular dynamics. All musical material is an original browser-synthesized composition rather than a recording or another composition. 0D–M are pedagogical lenses, not literal dimensions. The abstract toy sequence is not real ubiquitin BILN; real residue identity-to-pitch, contact, helix/sheet annotations and measured trajectories require a separately sourced/validated adapter.

## Immutable scientific input

Reuse exact FoldSense toy A=bead index 2, B=bead index 7, 12 frame IDs, and `distance = sqrt(dx²+dy²+dz²)` in demo units. Crossing: `old_distance >= 5 && new_distance < 5`, with an inverse when returning above 5. At frame 6 (zero-based frame 5), 5.226→4.630 toy units causes crossing. The music planner never changes scientific inputs.

## Educational music representation

| Lens | Voices | Plan | Concept |
|:---|---:|:---|:---|
| 0D | 1 | sustained C4 261.626 Hz | single amino acid focus |
| 1D | 1 | 8 sequential notes relative to C4 [0,2,4,7,5,9,7,4] semitones | illustrative sequence develops ordered melody |
| 2D | 2 | basic motif and a second line | schematic local secondary structures |
| 3D | 3 | [0,4,7] semitones and moving patterned figure | tertiary spatial context |
| 4D | 4 | open chord above threshold [0,4,7,12]; deliberately dissonant chord below [0,1,6,10] | **toy** contact-state change over time |
| M | 5 | multiscale conceptual ensemble | multi-chain context where applicable; not factual ubiquitin assembly |

For 4D tension metadata: `clamp(round((below ? 52 : 12) + min(20, abs(distance_now-distance_prev)*20) + (is_adjacent_crossing ? 25 : 0)),0,100)`. This number is an **artist-authored sonic tension control**. Neither the numeric value nor consonance/dissonance establishes protein folding thermodynamics, stability, function or misfolding. Source identity and musical mapping identity are separate. Voice count and interval arrays are deterministic for a chapter/frame.

## UI and sensory routing

The review prototype displays musical complexity next to the interactive molecule; prominent Play/Stop, voice bars, a tension meter with text, and expandable instrument/tempo. Soft bell/sine, warm strings/triangle and soft pulse/square; 2 tempos. Playback requires a user action and can optionally follow subsequent page/frame gestures only after explicit opt-in. Browser generated, no paid API. An optional audio channel is permitted **in every chosen accessibility profile when a user explicitly requests it**, but never required for hearing/combined profiles. Visual captions and haptics remain independent adapters. Watch vibration is NOT_CONNECTED. S Pen contact is NOT_TESTED in this review. Physical hearing and haptic perception are NOT_TESTED. The score is always available as text; color is not the sole encoding.

## Follow-up implementation with Lovable

Production Lovable has a two-note threshold chime, not this progressively polyphonic engine. Integrate into an isolated preview or a review branch; do not replace `audio.ts` or publish by default. A handoff was queued for Lovable with exact mapping and constraints, review status not a publication claim. Do not import the frozen private canonical FoldSense repository as if it were already merged.

## Test plan

- 4 sensory profiles × 3 learning paths = 12 headless Chromium paths, all PASS as of this review.
- 0D..M voice counts = `[1,1,2,3,4,5]`; eight notes in 1D; optional independent sound in every profile.
- 4D frame6 4.630 toy units; crossing-specific tension greater than above-threshold initial tension; chord changes.
- Stage page turn control still fits initial 384×688 viewport; no horizontal overflow.
- No browser console errors; playback API request only (not human hearing).
- Live Samsung, WebAudio physically heard, watch haptics, TalkBack, S Pen input, local VLM influence, protein fold prediction: NOT_TESTED / NOT_CONNECTED.

## Reference and custody

Parent review state: `FOLDSENSE-LIVING-STORYBOOK-REVIEW-20261107-T11`, exact parent artifact `/mnt/data/foldsense_review/TURN_BREAKPOINT_T11.json`. This review creates a successor. Hashes identify content; they do not establish biological truth. No signing or MMR inclusion claimed.