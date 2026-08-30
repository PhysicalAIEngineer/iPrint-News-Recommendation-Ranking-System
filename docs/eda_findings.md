# EDA Findings

## 1. User Behavior

- User activity is highly skewed.
- A subset of users generates significantly more interactions.
- Low-activity users require a cold-start strategy.

## 2. Article Popularity

- Article interactions exhibit a long-tail distribution.
- Popularity-only recommendation can create popularity bias.
- Personalized candidate generation is therefore required.

## 3. User-Item Matrix

- User-item interactions are highly sparse.
- Implicit collaborative filtering is appropriate.
- ALS will be evaluated as a collaborative candidate generator.

## 4. Content

- Content contains multiple languages.
- English-only filtering will be applied to content-based retrieval.
- Title + description will be used for semantic representation.

## 5. Content Lifecycle

- Pulled-out articles must be excluded before final ranking.

## 6. Sessions

- Session-level behavior will be used to capture short-term intent.

## 7. Temporal Behavior

- Time information will be preserved.
- Temporal train/validation/test splitting will be used to reduce
  future-information leakage.