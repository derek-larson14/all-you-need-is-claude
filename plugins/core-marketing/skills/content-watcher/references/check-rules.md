# Check rules — how to apply the brand book

Walk these categories in order. Skip a category only if the brand book doesn't define rules in it.

## 1. Banned words and phrases (highest priority)

Scan the content for any exact-string match against the brand book's banned list. Case-insensitive. Watch for variants:
- "best in class" → also catch "best-in-class", "world-class"
- "revolutionary" → also catch "revolutionizing", "a revolution in"
- "guaranteed" → also catch "guarantee", "we guarantee"

Severity: usually **Fix**. Escalate to **Block** if the banned word is part of a category the brand has explicitly called legal/compliance (e.g. "no superlatives — substantiation rule" rather than "we just don't say 'awesome'").

## 2. Compliance / legal claims

Look for claims in any sensitive category the brand book flags:
- **Medical/health**: "cures", "treats", "heals", "prevents [condition]", "speeds recovery", "boosts immunity" — these are FDA-regulated for any product the FDA touches.
- **Sustainability**: "100% recycled", "carbon neutral", "sustainable", "eco-friendly" — these typically need third-party certification or clear sourcing.
- **Performance/results**: "lose X pounds", "results in X days", "X% improvement" — needs cited study or substantiation.
- **Comparative/competitive**: "best", "leading", "#1", "no other" — needs substantiation or is outright banned.

Severity: **Block** if the claim is unsubstantiated *and* in a regulated category. **Fix** if it's substantiated elsewhere but the citation isn't in the copy itself (the marketer can add the disclosure).

## 3. Voice and tone

Compare the writing against the brand book's voice principles. Each principle usually comes with do/don't pairs — use those as direct calibration. Common drift patterns:
- Jargon when the brand says "plain language"
- Corporate-speak when the brand says "conversational"
- Overpromising when the brand says "honest"
- Hedging ("perhaps", "might", "could") when the brand says "direct"
- Em dashes when the brand bans em dashes
- Adverbs when the brand discourages adverbs

Severity: **Fix** for clear drift. **Note** for borderline cases.

## 4. Persona alignment

Does the copy speak to the brand's stated audience? If the brand book describes the persona as "29-year-old time-pressed parent who lifts 3x a week," and the copy reads like it's for "elite endurance athletes," that's a mismatch.

Look for:
- Vocabulary level (technical jargon for a non-technical audience or vice versa)
- Cultural references the persona wouldn't catch
- Pain points or aspirations that don't match the persona's stated goals

Severity: usually **Fix** unless the mismatch is so severe the copy is for the wrong audience entirely (then **Block**).

See `references/persona-alignment.md` for the full rubric.

## 5. Messaging pillar invocation

The brand has 3-4 messaging pillars (e.g. "sustainability transparency", "performance for real life", "designed in collaboration with athletes"). A piece doesn't need to hit all of them, but it should invoke at least one *clearly*. If the copy is generic enough that you couldn't tell which brand it came from, that's a pillar gap.

Severity: **Note** in most cases. **Fix** if the piece is meant to be a pillar piece (the brief said so) but doesn't deliver.

## 6. Format-specific rules

If the brand book has channel-specific rules (e.g. "Instagram captions: lead with a question", "email subject lines: under 50 characters"), apply them to the matching format only.

Severity: matches what the brand book says. If silent, treat as **Note**.

## What NOT to flag

- Things the brand book doesn't address. If the brand book is silent on Oxford commas, you don't have an opinion on Oxford commas.
- Personal preference. You are not the writer's editor; you are the brand's enforcement layer.
- Generic SEO concerns (that's the brief generator's job, or a separate audit).
- Punctuation, unless the brand explicitly bans (em dashes, exclamation points, etc.) or requires (Oxford comma, sentence case in headlines, etc.).
