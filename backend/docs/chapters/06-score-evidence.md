# Prompt: Chapter 6 — Role score and evidence

Continue the frozen Chapters 1–5 backend. Add deterministic `role_score` and human-readable `evidence` for every classified node. Do not implement clustering, priority ranking, persistence, or API endpoints.

Define role-specific score formulas using normalized feature values relevant to the assigned role. Every result must be finite and clipped to 0..1. State clearly that role_score measures strength of rule match, not criminal probability or guilt. Avoid hardcoded gids and randomness.

Generate evidence from the same concrete inputs used by the rule. Include real counts, amounts, ratios, depth, or reach values as appropriate. Keep it nonempty, deterministic, at most 200 characters, understandable without ML knowledge, and cautious in wording. Handle isolated nodes, zero amounts, missing pass-through, seeds, and truncated depth-four nodes explicitly.

Tests must cover every role's formula and evidence template, score boundaries, evidence length, embedded real values, deterministic output, no nulls, invalid input, and non-mutation. Real-data smoke checks require all 2248 scores in 0..1 and all evidence valid. Manually inspect ten varied gids and verify evidence against their features.

Update methodology documentation with formulas and examples. Report formulas, sample evidence, real-data validation, pytest, all earlier regressions, and checklist.
