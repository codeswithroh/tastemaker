# Prototype variants

Use this when the design direction is uncertain and the cost of guessing is high. A working picker teaches more than static explanation because you can feel density, hierarchy, and motion in context.

## When to prototype

Prototype before committing when the user asks for any of these and the direction is not obvious:

- Hero section
- Pricing card or plan comparison
- Dashboard summary card
- Onboarding step
- Empty state
- Toast or notification
- Command palette
- Data table interaction
- Motion-heavy feature explanation

Do not prototype routine wiring, backend work, or tiny visual fixes. Use the skill's normal workflow for those.

## Variant rules

- Build 2-3 variants by default. Use 4 only when the design space is wide.
- Each variant must differ on a named axis: layout, density, hierarchy, interaction model, or motion.
- Color swaps are not variants.
- Every variant uses the project's locked tokens and real content.
- Every variant must be shippable on its own. No dead controls, lorem ipsum, or placeholder states.
- The picker swaps variants instantly. Switching variants is a repeated action, so it gets no animation.

## Direction set

Before coding, write this small table in your working notes:

| Variant | Axis | Bet | Cost |
|---|---|---|---|
| Quiet | Lower density, minimal motion | Better for a daily-use tool | Less memorable |
| Editorial | Larger type, stronger visual rhythm | Better for a launch page | Uses more vertical space |
| Operational | Dense controls, faster motion | Better for repeated work | Less emotionally polished |

If two rows differ only by accent color, merge them and create a real alternative.

## Picker requirements

The prototype surface must render one variant at a time at real size, inside realistic surrounding context. Do not use side-by-side thumbnails for final judgment.

The picker chrome stays neutral and fixed:

- Floating pill, bottom center unless it covers the work.
- Number keys switch variants.
- Left and right arrows cycle.
- `R` replays entrance motion when a variant has motion worth replaying.
- URL parameter stores the current variant, for example `?v=2`.
- Exactly one variant has active state and `aria-current="true"`.

The picker may use its own dark glass style. It does not inherit product tokens because it is test harness chrome, not part of the product design.

## Promotion

When the user picks a variant, promote only that variant into production code. Delete the prototype surface unless the user asks to keep it. Record the decision in `.tastemaker/decisions.log` as kept or rejected evidence for future taste memory.

## Verification

Before showing the picker:

- Run the dev server or open the static file.
- Flip through every variant with mouse and keyboard.
- Replay motion.
- Check the console.
- Check 390px mobile and a desktop viewport.
- Confirm reduced motion drops movement while keeping clear state changes.
