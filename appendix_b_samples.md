markdown
# Appendix B: Qualitative Analysis & Human Evaluation Samples
‌
This document provides sample outputs comparing **DIINA** with the **AfriBERTa** baseline, as evaluated by native Yoruba linguists.
‌
## 1. Qualitative Comparison (Text Generation)
‌
**Prompt:** *"Write a short paragraph about the importance of Yoruba proverbs."*
‌
### 🟢 DIINA Output (Proposed Model)
> "Àlọ́ Yorùbá kò ṣeé fiṣẹ́ kankan. Wọ́n jẹ́ àmì ọgbọ́n àti ìjìnlẹ̀ ìmọ̀ tí àwọn tí ó kọjá lọ ti fi sílẹ̀ fún wa. Nípasẹ̀ àlọ́, a lè fi ojú ọgbọ́n wòye ohun gbogbo tí ó ṣẹlẹ̀ ní ayé..."
>
> **English Translation:** "Yoruba proverbs are invaluable. They are signs of wisdom and deep knowledge left for us by those who have gone before. Through proverbs, we can view everything that happens in the world with the eyes of wisdom..."
>
> **Linguist Note:** Demonstrates high poetic depth and authentic use of "kò ṣeé fiṣẹ́ kankan" (invaluable).
‌
### 🔴 AfriBERTa Output (Baseline)
> "Àlọ́ Yorùbá jẹ́ ohun pàtàkì nínú ẹ̀kọ́ àti ìmọ̀ Yorùbá. Wọ́n máań ṣàlàyé ohun tí wọ́n rí nínú ayé ní ọ̀nà tí ó kún fún ọgbọ́n..."
>
> **English Translation:** "Yoruba proverbs are important in Yoruba learning and knowledge. They explain what they see in the world in a way full of wisdom..."
>
> **Linguist Note:** Grammatically correct but lacks the cultural nuance and lexical richness of DIINA.
‌
## 2. Sample Entries from the "Treasure Corpus"
The following are examples of manually annotated data used for fine-tuning:
‌
| Source | Text (Yoruba) | Annotation (NER/POS) |
| :--- | :--- | :--- |
| Folk Tale | Èènìyàn lè máa gbójú kọ́ ọ̀tọ̀ ṣùgbón òun kò lè... | [Noun, Verb, Pronoun, ...] |
| News | Gómìnà ìpínlẹ̀ Èkó, Babajide Sanwo-Olu, ti kéde... | [Person: Babajide Sanwo-Olu, Loc: Èkó] |
‌
