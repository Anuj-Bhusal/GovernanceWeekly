# Internship Daily Logbook — Governance Weekly

Project: Governance Weekly (Automated Governance News Intelligence System for Nepal)
Period: Nov 7, 2025 to Dec 27, 2025 (Weekends excluded)

Intern Roles (balanced across technical + reporting tasks)
- Person 1: scraping + automation, extraction/date parsing, DB + pipeline reliability, plus report QA and documentation support.
- Person 2: taxonomy + keyword systems, impact scoring + filtering, translation + extractor QA, PDF/report formatting, plus development support and testing.

---

## WEEK 1

**Nov 7, 2025 / Friday – Person 1**
- Set up Python 3.12 environment and verified dependency installation strategy (venv + requirements).
- Reviewed initial project scope and drafted the module breakdown (scrapers → extractor → translator → classifier → DB → reporting).
- Ran small connectivity checks and confirmed basic HTTP fetching works reliably.

**Nov 7, 2025 / Friday – Person 2**
- Drafted governance reporting expectations (weekly window, English-only briefing, clickable sources).
- Proposed initial category taxonomy and priority ordering for the report.
- Prepared a checklist for content quality (remove opinion/noise, avoid duplicates, keep summaries concise).

---

## WEEK 2

**Nov 10, 2025 / Monday – Person 1**
- Implemented the reusable scraping base with rate limiting and standardized headers.
- Built a consistent link extraction helper to normalize URLs and remove fragments.
- Recorded baseline performance metrics (links discovered per homepage, failures per request).

**Nov 10, 2025 / Monday – Person 2**
- Converted the taxonomy into an implementable keyword plan for 13 governance categories.
- Added initial exclusion categories (sports/entertainment/lifestyle) to reduce noise.
- Defined an early scoring idea to prioritize high-impact governance news.

**Nov 11, 2025 / Tuesday – Person 1**
- Integrated robots.txt compliance checks into fetch operations.
- Verified that disallowed URLs are safely skipped with clear logs.
- Tested rate limiting behavior under multiple requests to avoid server overload.

**Nov 11, 2025 / Tuesday – Person 2**
- Compiled “opinion/editorial/interview” exclusion indicators for URL and title patterns.
- Reviewed sample pages to identify recurring non-article elements that leak into text extraction.
- Documented formatting expectations for dates and sources in the final report.

**Nov 12, 2025 / Wednesday – Person 1**
- Added Selenium support for dynamic pages via a shared WebDriver manager.
- Verified headless browsing configuration for stable automated runs.
- Confirmed that Selenium fallback can retrieve content where plain requests fail.

**Nov 12, 2025 / Wednesday – Person 2**
- Designed the report structure: category headings, article metadata layout, and consistent summary block.
- Drafted category ordering rules to match governance priorities.
- Reviewed early Selenium output to ensure extracted text remains readable for summarization.

**Nov 13, 2025 / Thursday – Person 1**
- Implemented article extraction using readability with a BeautifulSoup fallback.
- Added cleaning steps to remove empty lines and normalize whitespace.
- Validated extraction quality on sample pages from different domains.

**Nov 13, 2025 / Thursday – Person 2**
- Defined summary expectations (multi-sentence, information dense; target length limits).
- Collected examples of common “junk strings” (read time, share prompts) to be removed.
- Prepared acceptance criteria for when an article should be excluded as non-news.

**Nov 14, 2025 / Friday – Person 1**
- Created the SQLite schema and DB initialization utilities.
- Ensured the schema supports original + translated text, summaries, categories, and metadata.
- Tested insert/commit/rollback paths for reliability.

**Nov 14, 2025 / Friday – Person 2**
- Reviewed stored sample records for missing fields and consistency.
- Proposed improvements to store category JSON reliably and keep URLs unique.
- Documented expected DB fields for presentation (what is stored and why).

---

## WEEK 3

**Nov 17, 2025 / Monday – Person 1**
- Implemented initial domain scraper classes and confirmed per-site URL discovery.
- Added simple site heuristics to keep only likely article links.
- Logged extraction success rates to identify weak sources early.

**Nov 17, 2025 / Monday – Person 2**
- Finalized category priority weights and minimum keyword match rules by priority.
- Added Nepali + English keywords where relevant to improve recall.
- Reviewed false positives and refined exclusion terms for better precision.

**Nov 18, 2025 / Tuesday – Person 1**
- Added publish-date extraction with multiple strategies (meta tags, time tags, JSON-LD).
- Integrated `dateparser` with conservative settings to avoid future-dated parsing.
- Tested date extraction on multiple sources and recorded failure patterns.

**Nov 18, 2025 / Tuesday – Person 2**
- QA’d date extraction results and documented common errors and missing date markers.
- Proposed a strict rule: skip undated articles to protect time-range accuracy.
- Prepared sample “bad date” cases for debugging and future improvements.

**Nov 19, 2025 / Wednesday – Person 1**
- Implemented translator module structure supporting multiple backends.
- Verified graceful fallback behavior when a preferred backend is unavailable.
- Added Nepali Unicode detection to decide when translation is required.

**Nov 19, 2025 / Wednesday – Person 2**
- Built translation QA checklist (no Nepali characters remain in English output).
- Reviewed sample translations for readability and meaning preservation.
- Identified the need for retry delays to handle rate limiting in free translation.

**Nov 20, 2025 / Thursday – Person 1**
- Integrated core collection pipeline: scrape → extract → translate → classify → store.
- Added structured logging to track per-article decisions (skipped/kept).
- Validated that failures in one scraper do not stop the entire pipeline.

**Nov 20, 2025 / Thursday – Person 2**
- Implemented the keyword-based classifier logic and tested category assignment.
- Verified that a single article can match multiple categories and remains sortable by priority.
- Reviewed classification errors and tuned keyword lists and match thresholds.

**Nov 21, 2025 / Friday – Person 1**
- Wrote initial tests for link extraction and a mocked scraper run.
- Verified the test suite catches broken parsing and URL normalization issues.
- Documented how to run tests during development.

**Nov 21, 2025 / Friday – Person 2**
- Reviewed end-to-end outputs from DB and identified duplicate clusters.
- Validated early summary structure and noted noise that reduces report quality.
- Proposed strict similarity thresholds for deduplication in reporting.

---

## WEEK 4

**Nov 24, 2025 / Monday – Person 1**
- Implemented weekly window logic (last Friday to run date) for collection scope.
- Added logging to display the computed date range during every run.
- Verified correct behavior for Friday morning edge case.

**Nov 24, 2025 / Monday – Person 2**
- Designed an impact scoring approach combining category priority and keyword relevance.
- Defined minimum impact threshold to keep the PDF short and meaningful.
- Reviewed sample scoring outputs for fairness across categories.

**Nov 25, 2025 / Tuesday – Person 1**
- Added deduplication in collection: URL uniqueness check and title similarity skipping.
- Validated that duplicates across sources are reduced before DB insertion.
- Recorded skipped reasons for traceability.

**Nov 25, 2025 / Tuesday – Person 2**
- Tuned similarity thresholds and validated that near-duplicate headlines are caught.
- Reviewed deduplication false positives and adjusted for safe governance reporting.
- Added notes for slide explanation: why deduplication matters in weekly briefs.

**Nov 26, 2025 / Wednesday – Person 1**
- Implemented reporting data preparation: load weekly items, convert to report-friendly dicts.
- Ensured categories are parsed correctly from JSON strings in DB.
- Added “summary missing → generate on the fly” logic for robustness.

**Nov 26, 2025 / Wednesday – Person 2**
- Implemented PDF generator layout decisions: compact spacing, readable headings, consistent metadata.
- Validated clickable URL format in ReportLab paragraphs.
- Proposed category ordering to match governance priority narrative.

**Nov 27, 2025 / Thursday – Person 1**
- Integrated PDF generation into the pipeline and verified consistent output naming.
- Ensured the report groups items by category and sorts by impact.
- Tested PDF generation failure handling and confirmed errors are logged clearly.

**Nov 27, 2025 / Thursday – Person 2**
- QA’d PDF readability, margins, and summary legibility across pages.
- Refined the “article meta” line to include full clickable URL and impact score.
- Documented PDF formatting rules for internship presentation.

**Nov 28, 2025 / Friday – Person 1**
- Implemented one-command runner flow to automate setup + execution.
- Verified it clears old DB records and previous PDFs before a fresh run.
- Confirmed the generated PDF auto-opens on Windows for easy review.

**Nov 28, 2025 / Friday – Person 2**
- Produced a weekly QA checklist covering date range, duplicates, opinion filtering, and translation quality.
- Ran a review of the first “weekly-style” PDF and compiled improvement requests.
- Prepared a short explanation of the pipeline for viva narration.

---

## WEEK 5

**Dec 1, 2025 / Monday – Person 1**
- Extended extractor cleaning with regex patterns for tags, ads, and share prompts.
- Validated that cleaned text improves summary quality and reduces noise.
- Logged before/after examples to confirm cleaning effectiveness.

**Dec 1, 2025 / Monday – Person 2**
- Expanded category keywords and ensured balanced Nepali/English coverage.
- Reviewed “uncategorized” cases and added missing governance-related terms.
- Updated exclusions to reduce non-governance stories entering the report.

**Dec 2, 2025 / Tuesday – Person 1**
- Improved translation stability: Nepali detection, fallback behavior, and failure markers.
- Added retry logic and re-initialization steps for the free translator backend.
- Tested translation with short and long Nepali samples.

**Dec 2, 2025 / Tuesday – Person 2**
- Conducted translation QA and identified patterns that still produce Nepali remnants.
- Proposed stricter post-translation checks to avoid unreadable PDF blocks.
- Verified that English sources bypass translation to save time and reduce failures.

**Dec 3, 2025 / Wednesday – Person 1**
- Implemented heuristic summarizer to produce multi-sentence summaries within length bounds.
- Ensured summary generation uses translated text when available.
- Verified summaries are stored in DB for reuse during reporting.

**Dec 3, 2025 / Wednesday – Person 2**
- Reviewed summaries for completeness and reduced overly short/fragmented outputs.
- Suggested thresholds (min/max characters) to consistently achieve 5–6 lines in PDF.
- Documented summarization logic in slide-friendly language.

**Dec 4, 2025 / Thursday – Person 1**
- Implemented smart filtering: impact scoring, strict deduplication, and top-N selection.
- Verified deterministic ordering by impact score for reproducible reports.
- Tested filtering on a larger collection to ensure the PDF remains compact.

**Dec 4, 2025 / Thursday – Person 2**
- Validated impact scoring against governance priorities and adjusted category bonuses.
- Verified that cross-cutting articles (multi-category) get appropriate extra weight.
- Performed QA on filtered results to ensure coverage is balanced across categories.

**Dec 5, 2025 / Friday – Person 1**
- Improved error handling: scraper isolation, DB rollback, and robust continuation.
- Added clearer logs for skip reasons (duplicate/out-of-range/excluded/undated).
- Ran a full pipeline regression test after refactors.

**Dec 5, 2025 / Friday – Person 2**
- Performed weekly report QA and identified site-specific junk text that still appears.
- Drafted additional junk-removal patterns for later implementation.
- Prepared mid-internship progress notes for documentation.

---

## WEEK 6

**Dec 8, 2025 / Monday – Person 1**
- Added URL/title pattern filtering to exclude opinion/editorial/interview content early.
- Verified the filter triggers before translation to save compute time.
- Reviewed logs to ensure only factual news proceeds to classification.

**Dec 8, 2025 / Monday – Person 2**
- Updated exclusion strategy to be safer: title-focused opinion detection to avoid false positives.
- Expanded exclude keyword list to include common editorial labels.
- Verified that factual articles mentioning “opinion” in body are not incorrectly removed.

**Dec 9, 2025 / Tuesday – Person 1**
- Improved publish-date extraction reliability by adding more candidate selectors.
- Tested date parsing on problematic sources and documented remaining gaps.
- Ensured date comparisons are consistent when timezone info exists.

**Dec 9, 2025 / Tuesday – Person 2**
- Reviewed out-of-range items and traced them back to missing/incorrect publish dates.
- Proposed strict policy: skip articles without publish dates.
- Prepared QA evidence to confirm improvements after changes.

**Dec 10, 2025 / Wednesday – Person 1**
- Enforced “dated-only inclusion”: skip undated articles during collection.
- Verified that pinned old stories no longer leak into weekly PDFs.
- Re-ran the pipeline to confirm fewer out-of-range records in DB.

**Dec 10, 2025 / Wednesday – Person 2**
- QA’d the weekly output to ensure time-range accuracy improved.
- Monitored article volume to ensure skipping undated items does not reduce coverage too much.
- Updated documentation notes: trade-off between strictness and recall.

**Dec 11, 2025 / Thursday – Person 1**
- Added delays between translation attempts and chunk translations to reduce rate limiting.
- Verified stable runs under larger article volumes.
- Confirmed that translation failures are handled without breaking the pipeline.

**Dec 11, 2025 / Thursday – Person 2**
- Performed translation QA on the PDF for English-only readability.
- Verified that summaries no longer contain unreadable Nepali blocks.
- Updated report QA checklist to include “no Nepali characters” check.

**Dec 12, 2025 / Friday – Person 1**
- Standardized current-year URL filtering across scrapers to reduce old URL discovery.
- Verified consistent link filtering rules across all 10 sources.
- Ran a cross-source regression test for collection stability.

**Dec 12, 2025 / Friday – Person 2**
- Added junk text patterns for site-specific artifacts (read-time, Nepali calendar strings).
- Validated that cleaned content improves classification and summarization accuracy.
- Documented cleaning rules for slides (what is removed and why).

---

## WEEK 7

**Dec 15, 2025 / Monday – Person 1**
- Verified opinion URL exclusions across all scrapers and validated skip logs.
- Checked that excluded items are not inserted into DB.
- Confirmed that factual governance news continues to pass through.

**Dec 15, 2025 / Monday – Person 2**
- Strengthened classifier exclusion keywords for opinion/blog/interview indicators.
- Ensured exclusions remain title-first to avoid harming factual coverage.
- Reviewed category distribution changes after exclusion updates.

**Dec 16, 2025 / Tuesday – Person 1**
- Tuned report-stage deduplication logic using strict similarity thresholds.
- Verified that near-duplicate summaries are eliminated even if titles differ slightly.
- Confirmed final report length stays within the target (top N).

**Dec 16, 2025 / Tuesday – Person 2**
- QA’d final PDF to ensure duplicates are reduced and categories remain balanced.
- Adjusted impact score expectations and verified star rating thresholds.
- Prepared examples for viva: how deduplication reduces repetition.

**Dec 17, 2025 / Wednesday – Person 1**
- Added additional extractor junk rules for recurring banners across sources.
- Verified improved summary quality after cleaner text input.
- Ran regression checks to ensure extraction still captures meaningful paragraphs.

**Dec 17, 2025 / Wednesday – Person 2**
- Reviewed PDF layout consistency and readability of the meta line.
- Verified clickable URLs are preserved after HTML escaping.
- Updated documentation draft with final “workflow overview” section.

**Dec 18, 2025 / Thursday – Person 1**
- Verified pipeline automation end-to-end (setup → collect → summarize → open PDF).
- Checked error handling under partial scraper failures.
- Confirmed reproducible results with configured thresholds and date range.

**Dec 18, 2025 / Thursday – Person 2**
- Wrote viva-ready explanation notes describing each module’s role in the pipeline.
- Prepared reporting narrative: why categories, impact scoring, and deduplication are used.
- Reviewed the final report for factual tone and removed remaining opinion-like entries.

**Dec 19, 2025 / Friday – Person 1**
- Performed multi-source integration testing and addressed inconsistent link filtering.
- Verified that undated articles are skipped consistently across scrapers.
- Confirmed DB entries are complete (title, date, translation, summary, categories).

**Dec 19, 2025 / Friday – Person 2**
- Conducted final weekly quality review and updated the acceptance checklist.
- Verified category ordering matches the intended governance priority narrative.
- Prepared “final demo flow” instructions for presentation.

---

## WEEK 8

**Dec 22, 2025 / Monday – Person 1**
- Finalized module separation for maintainability and readability.
- Verified configuration via `.env` controls rate limits, report size, and scoring thresholds.
- Documented execution steps for a clean handover.

**Dec 22, 2025 / Monday – Person 2**
- Aligned taxonomy, keyword lists, and PDF category ordering for consistency.
- Verified that high-priority topics (corruption/irregularity) appear first in the report.
- Reviewed example outputs to confirm category assignment logic is explainable in slides.

**Dec 23, 2025 / Tuesday – Person 1**
- Improved logging clarity with consistent skip-reason messages.
- Verified that exclusion reasons (opinion/excluded/duplicate/out-of-range) are traceable.
- Performed a final pipeline run to validate stable behavior.

**Dec 23, 2025 / Tuesday – Person 2**
- QA’d OnlineKhabar-specific artifacts and confirmed removal of “OK AI” disclaimer text.
- Reviewed summaries and ensured the report maintains a factual tone.
- Prepared final documentation edits and slide bullet points.

**Dec 24, 2025 / Wednesday – Person 1**
- Verified database schema supports full lifecycle fields (original, translated, summary, categories, scoring).
- Confirmed date storage and retrieval behavior is consistent across runs.
- Prepared codebase packaging notes for submission.

**Dec 24, 2025 / Wednesday – Person 2**
- Finalized internship documentation package: workflow explanation, tech stack, and module roles.
- Prepared a concise “system architecture” section for academic submission.
- Created a final QA checklist to be used before weekly publication.

**Dec 25, 2025 / Thursday – Person 1**
- Conducted final demonstration dry run and validated report naming and date-range labeling.
- Verified that the report remains within target size and is readable end-to-end.
- Checked that automation works without manual intervention on Windows.

**Dec 25, 2025 / Thursday – Person 2**
- Reviewed final PDF for formatting consistency, link correctness, and clarity of summaries.
- Prepared viva speaking points: problem statement, workflow, and key technical decisions.
- Documented lessons learned and possible future enhancements.

**Dec 26, 2025 / Friday – Person 1**
- Finalized the codebase for submission: confirmed reproducible run steps and stable pipeline behavior.
- Coordinated final review with Person 2 and addressed any last-minute report issues.
- Prepared repository hygiene notes (what to include/exclude, how to run).

**Dec 26, 2025 / Friday – Person 2**
- Finalized presentation and documentation: demo plan, architecture explanation, and module overview.
- Prepared final internship wrap-up summary highlighting both technical and governance relevance.
- Verified that the final PDF output meets academic and professional reporting standards.

---

End of Logbook.
