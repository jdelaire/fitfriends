---
name: fitfriend-workout-generator
description: Generate the next weekly FitFriends outdoor fitness workout in /Users/jdelaire/Projects/fitfriends. Use when the user asks to generate, create, prepare, or add the next FitFriends session/workout, especially requests that previously used generate-next-session.sh or must follow AGENTS.md, history/session-YYYY-MM-DD.md, videos.md, and index.html session-array rules.
---

# FitFriend Workout Generator

## Workflow

1. Work from `/Users/jdelaire/Projects/fitfriends` unless the user gives another FitFriends repo path.
2. Run the context helper:

   ```bash
   python3 ~/.codex/skills/fitfriend-workout-generator/scripts/session_context.py --repo /Users/jdelaire/Projects/fitfriends
   ```

3. Read `AGENTS.md` fully and treat it as the source of truth.
4. Read the two most recent `history/session-YYYY-MM-DD.md` files reported by the helper.
5. Read `videos.md` before selecting demo links, and inspect `index.html` around the static `const sessions = [...]` array.
6. Compute the upcoming Wednesday strictly after the request date. Create exactly one new file named `history/session-YYYY-MM-DD.md`.
7. Update `index.html` so the new `YYYY-MM-DD` appears in the static `sessions` array.
8. Update `videos.md` for every selected exercise link, using one line per mapping:

   ```text
   Exercise Name – https://www.youtube.com/...
   ```

9. Return only the generated filename and the Markdown file contents when the user asked to generate a session.

`generate-next-session.sh` is only a thin wrapper around `codex exec "generate the next workout"`. This skill should perform the same repo task directly while applying the current `AGENTS.md` contract.

## Session Contract

Start the workout file directly with the warm-up. Do not include an introduction, cooldown, conclusion, or unrelated commentary.

Use this exact section order:

1. `1️⃣ Warm-Up (~10 minutes)`
   - 5 movements.
   - 30s each.
   - Repeat 2 rounds.

2. `2️⃣ TABATA Core (~12 minutes)`
   - Generate two versions.
   - Each version has 4 movements.
   - 20s work / 10s rest.
   - Pure bodyweight core only.
   - No crawling movements and no rotational patterns.
   - Put a YouTube URL next to every movement.

3. `3️⃣ EMOM Strength (10 minutes)`
   - Generate two different EMOM options.
   - Each option has exactly 2 movements.
   - Minute 1 is movement A; minute 2 is movement B.
   - Repeat for 10 minutes.
   - Bodyweight only.
   - Put a YouTube URL next to every movement.

4. `4️⃣ High-Intensity Finisher (~15 minutes)`
   - Generate three versions: AMRAP, For Time, and Ladder.
   - AMRAP has 2 or 3 bodyweight movements.
   - For Time has 3 to 5 bodyweight movements.
   - Ladder has 2 to 4 movements and is descending, ascending, or up-down.
   - Put a YouTube URL next to every movement.

Allowed tools and surfaces: bodyweight, jump rope, fixed benches, and stable steps around 50 cm for support/platform work. Bench dips, step-ups, and box jumps are allowed. Bear plank holds are allowed; bear crawls are not.

Inspire yourself from classic CrossFit worout Scheme.

Do not use bear crawl, crab walk, rotational movements, or equipment other than jump rope and fixed benches/steps.

## Anti-Repetition Rules

Before drafting, compare against each of the two most recent sessions:

- Warm-up: at least 3 of 5 movements must differ from each recent warm-up.
- TABATA: each new option must have at least 3 of 4 movements different from each recent TABATA option, and must not reuse an exact 4-movement set.
- EMOM: do not reuse an exact 2-movement pairing from either recent session.
- Finishers: do not reuse an exact finisher movement list, and each new finisher may share no more than 1 movement with any single recent finisher.
- If a staple such as burpees, push-ups, or air squats appeared prominently in finishers in both recent sessions, avoid it in all finishers for the new session.

Vary movement patterns across the whole workout. Reuse a cached video URL when the exercise name is an exact match in `videos.md`.

## Video Selection

Use real YouTube URLs only.

Priority:

1. Exact exercise-name match in `videos.md`.
2. Search these playlists, in order:
   - `https://www.youtube.com/playlist?list=PLdWvFCOAvyr0q99QIkLBq4tfYhTVbsBIs`
   - `https://www.youtube.com/playlist?list=PLdWvFCOAvyr3EWQhtfcEMd3DVM5sJdPL4`
3. Search YouTube more broadly only when no suitable playlist video is found.

When a new video is selected, add or update the exact exercise mapping in `videos.md`. Keep URLs plain in the workout Markdown, not Markdown links.

## Validation

Before final response, verify:

- The target `history/session-YYYY-MM-DD.md` exists and no extra session file was created.
- `index.html` includes the new `YYYY-MM-DD` in the static `sessions` array.
- `videos.md` includes every selected exercise mapping.
- The workout has two TABATA options, two EMOM options, and AMRAP, For Time, and Ladder finishers.
- Every exercise line has a real YouTube URL.
- No cooldown, introduction, conclusion, bear crawl, crab walk, or rotational exercise appears.
- The anti-repetition rules hold against the two most recent previous sessions.
