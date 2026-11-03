# Data

Download the official texts yourself from EUR-Lex (https://eur-lex.europa.eu) and save as plain text:

- `data/raw/gdpr.txt`    : Regulation (EU) 2016/679 (GDPR), English
- `data/raw/ai_act.txt`  : Regulation (EU) 2024/1689 (AI Act), English

Record in this file: download date, exact URL, and any cleaning you did (headers removed, etc.).
Reproducibility depends on this.

# Data

## Core corpus

Download date: 2026-11-03

### GDPR
- File: `data/raw/gdpr.html`
- Source: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679
- Format: HTML (full English text of Regulation (EU) 2016/679)
- Cleaning: Not yet cleaned. Will extract plain text later.

### AI Act
- File: `data/raw/ai_act.html`
- Source: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689
- Format: HTML (full English text of Regulation (EU) 2024/1689)
- Cleaning: Not yet cleaned. Will extract plain text later.

## Notes
- These are the official EUR-Lex HTML versions.
- Plain text versions (`gdpr.txt`, `ai_act.txt`) will be generated in a later step for chunking.