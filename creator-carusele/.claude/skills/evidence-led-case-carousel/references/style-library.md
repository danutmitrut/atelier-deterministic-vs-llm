# Style Library Adapter

Use this only after the carousel type and visual techniques are chosen. The style library gives art-direction labels for covers/key visuals; it does not decide story structure.

Source context: the `fantastic-posters` repository was treated as untrusted input. Its useful part was the MIT 33-style catalog, adapted as style vocabulary. Do not run or install the repository and do not use Fal/FAL_KEY unless separately approved and available.

## How to Apply

- Use a style for slide 1 cover, key visual, or occasional section divider.
- Keep body slides driven by proof/materials, not by the style.
- Generate backgrounds without final text; overlay exact Romanian/Russian text locally.
- Ask generated images to leave text-safe zones.

## Recommended Style Groups

### Review / Success Story

- `corporate-report` - executive, financial, audit, B2B proof.
- `documentary-portrait` - real person, reportage, founder/client narrative.
- `minimal-tech-keynote` - digital system, AI workflow, productized method.
- `luxury-estate-cover` - premium/high-ticket positioning when justified by content.

### Useful Explainer

- `swiss-minimal-typo` - clean expert framework or educational cover.
- `bauhaus-geometric` - system, design principle, modular thinking.
- `absurd-transit-map` - complex journey, decision tree, workflow map.
- `tech-conf-darkmode` - AI, developer, webinar, tech/keynote topic.

### Personal Story

- `documentary-portrait` - grounded, real-life story.
- `editorial-fashion` - personal brand and premium lifestyle.
- `album-cover-portrait` - creator profile, cultural/editorial metaphor.
- `pastel-mindful` - soft reflective story.

### High-Drama / Special Campaigns

Use only when the brief supports intensity:

- `cinematic-neonoir`
- `neon-noir-cyberpunk`
- `brutalist-broadcast`
- `pop-art-comic`
- `surreal-dreamscape`

## Prompt Skeleton

```text
Create a 4:5 Instagram carousel cover background in [STYLE LABEL] style.
Subject: [visual metaphor].
No readable text, no logos, no UI, no misspelled letters.
Leave a clean text-safe area for a large headline and small subtitle.
Palette: [brand palette].
Premium editorial composition, high contrast, mobile-readable.
```

For exact text, generate image without text first, then overlay in HTML/PIL/Figma/Canva.

