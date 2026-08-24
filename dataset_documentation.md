# Dataset Documentation

## Domain

The domain is retail loan rejection letters sent by a European consumer bank to
applicants whose credit application was declined. The evaluation task is
structured extraction: given the full text of a rejection letter, the model must
identify the primary reason for the decline and state whether the letter offers
the applicant a manual review of the decision by a human. This mirrors a real
compliance use case, where a bank needs to audit outgoing letters at scale for
consistency and for the presence of required disclosures.

## Sources

All 15 letters in this dataset are synthetic and were authored for this lab.

Real rejection letters cannot be used. They contain personal data (name,
address, financial circumstances, credit assessment) and processing them for a
training exercise has no lawful basis under GDPR Article 6, so no real letters
were collected, anonymised, or uploaded. The synthetic letters were written to
reflect the structure and phrasing typical of German consumer credit
correspondence, including the wording patterns required by the EU Consumer
Credit Directive around notifying an applicant of a database consultation.

This is a genuine limitation of the dataset and is carried through to
`evaluation_summary.md`: results measure model behaviour on letters I wrote, not
on production correspondence, and my own authoring style is a confound.

## What makes a good example

**Input** is a single field, `letter`, containing the complete letter body as
plain text. Letters run roughly 120 to 250 words and include the elements a real
one would: a reference to the application, the decision, a stated ground for the
decision, and closing information about next steps.

**Expected output** has two fields:

| Field | Type | Values |
|---|---|---|
| `reason_code` | closed set | `credit_score`, `debt_to_income`, `insufficient_income`, `employment_history`, `incomplete_application`, `collateral_value` |
| `manual_review_offered` | closed set | `yes`, `no` |

A closed taxonomy was chosen deliberately. If the expected output were free text
(for example a summary of the letter), a correctness judge would be scoring
style as much as accuracy and the resulting numbers would be close to
meaningless. With fixed labels there is a defensible right answer per example,
so disagreement between model and reference is a real error rather than a
difference in phrasing.

**Metadata** per example:

- `reason_code`: repeated as metadata so results can be grouped by reason
- `difficulty`: `clear` or `ambiguous`
- `source`: `synthetic` for all examples

**Diversity.** The set covers all six reason codes, mixes letters that offer
manual review with letters that do not, and includes deliberately harder cases:
letters that mention a secondary factor alongside the primary one, letters that
use indirect phrasing rather than naming the reason outright, and letters that
mention a complaints procedure without actually offering a review of the credit
decision. Those ambiguous cases are the point of the dataset. A model that
scores well on the clear letters and fails on the indirect ones tells me
something useful about where this would break in production.

8 of the 15 examples are labelled `clear` and 7 are labelled `ambiguous`.