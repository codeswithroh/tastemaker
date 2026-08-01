# Taste memory

Tastemaker memory has three layers. Read them in this order, and write to the smallest layer that fits the decision.

## The three layers

1. **Project style lock: `.tastemaker/style-lock.md`**
   - Holds the current project's palette, type, spacing, structure, assets, motion, and project-specific avoid list.
   - Wins over every other memory source. If the global profile prefers rounded buttons but this project lock says square controls, use the project lock.
   - Update it when a design choice becomes a rule for this project.

2. **Project decision log: `.tastemaker/decisions.log`**
   - Holds the actual keep, reject, and pending-review calls that shaped this project.
   - Append only. Do not rewrite history after the user changes their mind; append the newer decision.
   - Use it to explain why the lock says what it says.

3. **Personal taste profile: `~/.tastemaker/profile.md`**
   - Holds durable preferences that should influence future projects.
   - Promote only resolved decisions into this file. Pending-review entries stay local until the user responds.
   - Treat profile entries as priors, not commands. A project brief, brand system, or style lock can override them.

## Decision log format

Append one JSON object per line to `.tastemaker/decisions.log`.

Required fields:

```json
{"ts":"<ISO-8601 timestamp>","project":"<absolute or repo-root path>","surface":"<screen or component>","status":"kept|rejected|pending-review","axis":"<palette|type|density|structure|motion|assets|copy|interaction|other>","decision":"<specific choice>","reason":"<why this was chosen or rejected>","source":"user|agent-pending|migration","promote":false}
```

Examples:

```json
{"ts":"2026-08-01T12:40:00+05:30","project":"/Users/rohitpurkait/Documents/Tastemaker/tastemaker-site","surface":"homepage hero","status":"kept","axis":"structure","decision":"concise promise, one short explanation, two actions, one polished output preview","reason":"user preferred a clean first impression over a feature-dense compiler hero","source":"user","promote":true}
{"ts":"2026-08-01T12:46:00+05:30","project":"/Users/rohitpurkait/Documents/Tastemaker/tastemaker-site","surface":"dashboard empty state","status":"pending-review","axis":"assets","decision":"quiet line illustration matched to locked accent","reason":"chosen to keep the app shell calm while avoiding an asset-empty state","source":"agent-pending","promote":false}
```

If an existing project already has a plain-text decision log, keep appending in its current style for that project. New projects should use JSONL.

## Capture rules

- Ask one concrete keep/reject question after each meaningful design pass: "keep this hero density, or try a quieter variant?"
- When the user answers, log the verdict with `source: "user"`.
- When no user can answer, log `status: "pending-review"` and `source: "agent-pending"`. Include the reasoning, but do not claim approval.
- If the user later reviews a pending decision, append a new kept or rejected entry that references the earlier choice in `decision` or `reason`.
- Record choices at the level that helps a future build: "compact table rows at 36px" is useful; "looks nice" is not.

## Promotion rules

Promote a project decision into `~/.tastemaker/profile.md` only when it looks durable across projects.

Promote when:

- The user explicitly says a preference should carry forward.
- The same preference appears in two or more resolved decisions across surfaces or projects.
- The preference describes a reusable axis: density, motion feel, typography taste, asset style, shape language, hierarchy, or common rejects.

Do not promote:

- Pending-review decisions.
- One-off brand constraints.
- A decision forced by a client, sponsor, platform, or existing product identity.
- A fallback caused by missing assets, missing APIs, or time pressure.
- A decision the user accepted with hesitation.

## Profile format

Write `~/.tastemaker/profile.md` as a short, scannable Markdown file:

```markdown
# Tastemaker profile

Updated: <date>

## Strong priors
- Density: <preference> (evidence: <project>, <date>, <decision summary>)
- Motion: <preference> (evidence: <project>, <date>, <decision summary>)

## Things to avoid
- <pattern the user rejected> (evidence: <project>, <date>)

## Open questions
- <preference that needs one more resolved decision before promotion>
```

Keep entries specific enough to guide a build. Remove stale or contradicted entries only after a newer resolved decision supports the change.

## Reuse rules

- On a fresh project, read `~/.tastemaker/profile.md` before Step 2. State the 1-3 priors you are applying.
- On an existing project, read `.tastemaker/style-lock.md` first. Use the profile only where the project lock has no decision.
- When the profile and the user's current request conflict, follow the current request and log the new decision.
- When the profile and a project style lock conflict, follow the project style lock and mention the conflict if it matters.
- Do not let memory narrow creative range too early. Use it to avoid known rejects and start from known preferences, then still ground the project in its own brief and assets.

## Handoff

At the end of a design task, tell the user:

- Whether `.tastemaker/decisions.log` changed.
- Whether `.tastemaker/style-lock.md` changed.
- Whether `~/.tastemaker/profile.md` changed, and why.

This keeps the memory claim honest: Tastemaker stores local files on the user's machine. It does not learn through a hosted backend.
