# Data Cleaning Report

## Objective

Document every data cleaning operation performed on the raw Olist datasets.

---

## Cleaning Log

| Step | Dataset | Action | Status |
|------|---------|--------|--------|
| 1 | All | Loaded raw datasets | ✅ |
| 2 | All | Created working copies | ✅ |
| 3 | Orders | Pending datetime conversion | ⏳ |
| 4 | Products | Pending missing value treatment | ⏳ |
| 5 | Reviews | Pending missing value treatment | ⏳ |
| 6 | Final | Save cleaned datasets | ⏳ |

---

## Notes

- Raw datasets remain unchanged.
- All cleaning operations are performed on copied datasets.
- Cleaned datasets will be saved in `data/processed/`.
