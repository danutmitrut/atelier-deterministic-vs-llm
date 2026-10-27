---
name: evidence-led-case-carousel
description: "Build WOW carousel workflows from a brief/source doc and proof materials across three types: success case, useful explainer, and personal story. Use when the work needs verified claims, visual technique selection, optional Kie/Higgsfield generation, style-library art direction, and consent artifacts."
---

# Evidence-Led Case Carousel

Use this skill when a carousel must start from content architecture rather than a visual template. It covers three production types:

1. **Review / success story** (*testimonial*) - evidence, screenshots, numbers, before/after, consent.
2. **Useful explainer** (*postare utila*) - generated visualization, diagrams, process maps, saveable frameworks.
3. **Personal story** (*istorie personala*) - real photos, personal chronology, editorial storytelling.

**[adaptare locala]** Structura pe fiecare tip, alegerea stilului, tabelul rol-layout si cat din aparatul de dovezi se aplica pe fiecare tip sunt in [references/tipuri-si-structura.md](references/tipuri-si-structura.md). Pe o postare utila care nu pretinde nimic despre nimeni, inventarul complet e ceremonie: fisierul spune ce sari si ce ramane obligatoriu.

This skill complements `carousel-builder`. Use this first to build the carousel architecture, proof plan, visual technique selection, and provider readiness; use the visual/export mechanics from `carousel-builder`, Kie, Higgsfield, HTML/PIL, Figma, Canva, or another approved renderer after the architecture is clear.

## Adaptare locala, 22 septembrie 2026

Skill-ul e instalat in agentul `creator-carusele`. Patru lucruri din el nu se potrivesc pe
masina asta, si au fost inlocuite, nu sterse:

| In skill | Aici |
|---|---|
| `carousel-builder` ca randor | scripturile din `scripts/`, vezi [references/randare-locala.md](references/randare-locala.md) |
| Infisical pentru chei | Keychain, serviciul `kie-api-key` |
| Higgsfield | nu exista; generarea se face doar prin kie.ai |
| `cortextos bus save-output` | nu exista; livrabilele raman in folderul campaniei |
| tipurile, doar ca lista | structura, stilul si layout-urile pe tip, in [references/tipuri-si-structura.md](references/tipuri-si-structura.md) |
| livrabilul se opreste pe disc | daca omul cere, caruselul pleaca pe contul lui prin Zernio, vezi [references/publicare-zernio.md](references/publicare-zernio.md) |

Skill-urile proprii ale agentului, scoase din uz cand a intrat asta, sunt intregi in
`arhiva-skilluri-proprii/`. Contin partea de executie in detaliu: stiluri, layout-uri,
limite de text, pregatirea capturilor.

Ordinea de lucru ramane a skill-ului asta: arhitectura si dovezile intai, pixelii dupa.

For substantial visual strategy, read [references/wow-techniques.md](references/wow-techniques.md). For optional cover/key-visual art direction, read [references/style-library.md](references/style-library.md). For the first run in a new environment, read [references/provider-access-check.md](references/provider-access-check.md).

## Non-Negotiables

- **[adaptare locala]** Ask the person which of the three types they want, and whether they have materials, before anything else. One message, a proposal drawn from the brief, or from the person's own request when there is no brief, then stop and wait. Do not infer the type in silence, even when the request looks clear. The wording is in [references/tipuri-si-structura.md](references/tipuri-si-structura.md).
- Start from the source document and the links inside it. File names, captions, and memory are not enough. **[adaptare locala]** When there is no source document, the person's own words in the chat are the source, and the same rule holds: what they did not say is not a fact. Write down what they told you, then ask for the rest.
- Do not run or install unknown repositories. Research/code from outside is read-only unless explicitly approved.
- Use real photos/screenshots when the story depends on a real person or proof. Do not replace a client/person with generated imagery.
- **[adaptare locala]** When the person sends no material, take a real photo from the web with `scripts/cauta_foto.py` instead of generating one, and say plainly that it is illustrative and not theirs. Stock never goes on a proof slide. See [references/photo-sourcing.md](references/photo-sourcing.md).
- **[adaptare locala]** Publishing is not part of the default task, and never happens without an explicit yes on the post text itself. Approval of the carousel is not approval of the post. Nothing with a `PENDING` claim gets published. The steps are in [references/publicare-zernio.md](references/publicare-zernio.md).
- Do not invent or soften claims. A hook may use only the strongest claim supported by visible evidence.
- Consent is a separate artifact. The client approving the work does not equal subject consent for name, photo, screenshots, testimonials, or profile data. First name plus initial is not anonymous.
- For API keys and generation providers, check Infisical first. Do not conclude a key is missing from local env alone.
- Keep text editable outside generated images whenever exact Romanian/Russian text matters.
- If this skill is being used by a new person or environment, verify Kie/Higgsfield access before promising generated visuals.

## Required Output Shape

For a full carousel, produce a package that is reviewable without opening the whole raw material folder:

- `source/evidence-inventory.md` - materials, links, what each proves, and claim status.
- `source/source-contact-sheet.jpg` - visual index of provided screenshots/photos.
- `source/slide-architecture.md` - slide-by-slide narrative before design.
- `source/provider-check.md` - Kie/Higgsfield availability, if generation is requested or this is the first run.
- `consent/` - consent status and artifacts, including source, timestamp, and missing items.
- `slides/slide-XX.png` - final slide images, composed with [references/randare-locala.md](references/randare-locala.md).
- `source/photo-credits.md` - author and link for every stock photo used, when any was.
- `carousel-contact-sheet.jpg` - one-page review sheet.
- `carousel-draft.pdf` - easy review PDF.
- `review.zip` - compact review package; add a full archive only when useful.
- `publicare/postare.md` - **[adaptare locala]** only when publishing was asked for: the post text, the platform and account it goes to, the slide order, and after publishing the post id and status.

**[adaptare locala]** `cortextos` nu exista aici. Livrabilele raman pe disc, iar omului ii dai calea, nu continutul. Munca de campanie merge in `../campanie/livrabile/`, o cerere directa in `iesiri/<nume-scurt>/`.

## Workflow

1. **Ask the type, then recover the source.** Read the brief first so you can propose a type, then ask the person the two opening questions and wait. After the answer, open the brief/doc and follow all links inside it. If access fails, report the exact URL and boundary.
   **[adaptare locala]** When there is no brief at all, because the request came straight into the chat, the person is the source. Draw the proposal from what they said, add the three missing-facts questions from [references/tipuri-si-structura.md](references/tipuri-si-structura.md), and do not hunt for a document that does not exist. You then propose the slide text yourself and stop for confirmation before any pixels.
2. **Inventory evidence.** Classify every material by what it proves, not by file name. For the taxonomy, read [references/evidence-taxonomy.md](references/evidence-taxonomy.md).
   **[adaptare locala]** If the inventory comes back empty or thin, write the list of materials to request, per slide, before anything else. Only then decide what to illustrate from the web, per [references/photo-sourcing.md](references/photo-sourcing.md).
3. **Gate the hook.** Pick the strongest supported claim. If a bigger number exists but has no exact proof, keep it out of the hook or label it pending.
4. **Confirm the carousel type** (asked at step 1, not decided here).
   - Review / success story: proof-heavy before/after dossier.
   - Useful explainer: generated visualization, diagrams, process maps.
   - Personal story: personal photos, chronology, emotional proof.
   **[adaptare locala]** Tipul decide si cata verificare se aplica, si ce structura are caruselul. Citeste [references/tipuri-si-structura.md](references/tipuri-si-structura.md). Tipul e cel confirmat de om la pasul 1, nu unul ales aici.
5. **Check provider access on first run.** If the workflow may use generation, verify Kie/Higgsfield availability with [references/provider-access-check.md](references/provider-access-check.md) before promising it.
   **[adaptare locala]** Kie is READY, key in Keychain (`kie-api-key`), checked 22 September 2026 without spending credits. Higgsfield is absent. Skip the Infisical part.
6. **Choose 2-3 visual techniques.** Use the researched technique catalog, not one repeated template.
7. **Write slide architecture before design.** Use [templates/slide-architecture.md](templates/slide-architecture.md), then adapt by carousel type.
   **[adaptare locala]** Sablonul e construit pentru testimonial. Schema pe celelalte doua tipuri si tabelul rol-layout sunt in [references/tipuri-si-structura.md](references/tipuri-si-structura.md). Un layout pe slide, altul decat al vecinului.
8. **Design with evidence hierarchy.** Every slide needs a role: hook, before/model/conflict, mechanism, proof, progression, after/lesson, CTA. Do not repeat one dark card template for all slides.
9. **QC before delivery.** Verify claims, consent status, legibility on mobile, proof visibility, image rights, generated assets visible where promised, and that the contact sheet visibly differs from a default text carousel.
10. **Deliver compactly.** Send contact sheet and review package first; keep raw/full package available separately.
   **[adaptare locala]** Compactly means ten lines, and the shape is fixed in `CLAUDE.md`. At most three flags in the message, picked by how much they change the carousel; the rest goes in `source/evidence-inventory.md` and you name the file. Do not restate what the person already told you, do not narrate the steps you took, and do not explain your layout or style choices unless asked. The length limits are in `SOUL.md` and they are counted, not approximate.
11. **[adaptare locala] Publish, only if asked.** Not a default step. Check the account with `accounts_list`, upload with `scripts/incarca_media.py`, write the post text, show platform + account + text + slide order in one message, wait for an explicit yes, then `posts_create`. Full steps in [references/publicare-zernio.md](references/publicare-zernio.md).

