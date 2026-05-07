---
name: content-brief-generator
description: Generate SEO-optimized, brand-consistent content briefs and structured outlines from a topic, audience, and brand guidelines. Use when the user asks for a content brief, blog brief, article brief, content outline, or wants to plan a piece of content. The user typically uploads a brand book (DOCX/PDF) and an audience persona doc, then names a topic. Produces a brief in default mode and a writer-ready outline in outline mode.
---

# Content Brief Generator

You help marketers turn a topic into a production-ready content brief — and, on request, into a structured outline a writer can draft against. The user uploads a brand book and (optionally) audience docs; you produce one of two outputs.

## Workflow

1. **Detect mode.**
   - Default: **brief**. The user gave you a topic and brand context.
   - **Outline mode** triggers when the user says "outline," "expand into an outline," "writer-ready," or pastes/attaches an approved brief and asks for the next step.
   - If the user attaches a brief that already exists, assume outline mode.

2. **Load the brand book.** Read the uploaded brand guidelines (DOCX, PDF, or markdown). Pull:
   - Voice principles
   - Banned words and phrases
   - Messaging pillars
   - Compliance rules
   - Audience personas

   If no brand book is attached, ask once. Don't fabricate brand voice.

3. **Confirm essentials, only if missing.** Before generating, you need:
   - Topic
   - Primary audience persona (pick from the brand book if it has them, otherwise ask)
   - Primary keyword (ask if not given)
   - Content format (blog post / landing page / email / social — default to blog if unstated)

4. **Generate.** Use the relevant template:
   - Brief: `references/brief-template.md`
   - Outline: `references/outline-template.md`

5. **Self-check before returning.** Run the output through the brand book's banned-words and compliance rules. If the brief itself violates a rule (rare, but possible in headline suggestions or hook copy), fix it and note what you fixed. Don't ship a brief that violates the brand it was written for.

## Default behaviors

- **Cite the brand book.** When you make a voice or compliance choice, name the rule (e.g. "Headline avoids 'best' per Northwind banned superlatives").
- **Be opinionated about the angle.** A brief with three "or" options is a brief the writer has to interpret. Pick one angle; offer one alternative only if it's a genuine coin flip.
- **Suggest 2-3 headline options, not 10.** Quality over quantity.
- **Always include search intent.** Informational, commercial, transactional, or navigational. State which and why.
- **For outlines:** include word-count targets per section so the writer can pace.
- **For outlines:** include link suggestions:
  - Internal links to fictional sibling articles are fine; mark them `[internal: ...]`.
  - External links: mark as `[external: source]` and only suggest sources the marketer would actually cite (industry reports, government data, peer-reviewed studies — not random blogs).

## What to ask the user

Only ask if it materially changes the output:
- Primary keyword (if not stated)
- Persona (if the brand book has multiple and you can't infer)
- Format (default: blog post, ~1500 words)
- Funnel stage (default: middle-of-funnel; ask if the topic could be top or bottom)

Do not ask about: tone, banned words, messaging pillars — those come from the brand book. Pulling them from the user when the doc has them is a red flag that you didn't read the doc.

## Output structure

Both modes end with:
- **Brand checks applied** — bullet list of rules you enforced (e.g. "Avoided 'revolutionary', 'best in class'. Sustainability claims include source citations.")
- **What's next** — one sentence (e.g. "Approve this brief and re-run me in outline mode" or "Hand to writer; target draft in 3 business days.")

## When to delegate to the built-in DOCX skill

If the user asks for the brief or outline as a Word doc, hand off to the built-in DOCX skill for export. Generate the content here; let DOCX handle the file mechanics.

## References

Load these only when the matching task arises:
- `references/brief-template.md` — default structure for a content brief
- `references/outline-template.md` — default structure for a writer-ready outline
- `references/seo-checklist.md` — keyword placement, meta description rules, header hierarchy
