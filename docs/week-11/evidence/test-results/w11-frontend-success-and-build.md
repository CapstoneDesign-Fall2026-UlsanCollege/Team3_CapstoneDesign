# Week 11 Frontend Test and Production Build Evidence

**Date:** November 13, 2026  
**Tester:** Lama Muskan (Sammygit15)  
**Environment:** Windows PowerShell; frontend working directory  
**Commit SHA:** Not captured for these local runs

## 1. Frontend Component Tests

**Command:** `npm.cmd test`  
**Runner:** Vitest 4.1.12  
**Run time shown:** 20:05:48 local machine time  
**Duration:** 1.14 seconds

| Test | Result |
|---|---|
| Loads inventory and menu from the API | Passed |
| Adds an ingredient using the correct API payload | Passed |
| Adds a menu item with its recipe | Passed |
| Does not delete a menu item when removal is cancelled | Passed |

**Summary:** 1 test file passed; 4 tests passed; 0 failed. The terminal screenshot supplied in the conversation shows all four passing assertions and the Vitest summary.

## 2. Frontend Production Build

**Command:** `npm.cmd run build`  
**Build script:** `tsc -b && vite build`  
**Vite version:** 8.3.0  
**Build time shown:** 20:06 (screenshot timestamp)  
**Build duration:** 424 ms

**Result:** TypeScript build step and Vite production build completed successfully. Vite reported 6 modules transformed and generated:
- `dist/index.html`: 0.16 kB (gzip 0.14 kB)
- `dist/assets/index-BuBFqgix.css`: 12.48 kB (gzip 3.26 kB)
- `dist/assets/index-jGTPvF1e.js`: 252.63 kB (gzip 77.21 kB)

## 3. Warning

Vite printed a configuration-loader warning: ESM syntax in `vite.config.ts` is being loaded as CommonJS under the current native config loader. The warning did not stop the test run or production build. It remains a configuration cleanup item and is not recorded as resolved.

## 4. Evidence Scope and Limitations

- These are local frontend test and build results, not GitHub Actions results.
- The test screenshot shows 4/4 tests passing.
- The build screenshot shows the production build completed in 424 ms.
- The exact source commit SHA was not captured at execution time.
- The initial failing Vitest run remains separately documented as diagnostic history: [w11-frontend-initial-run.md](w11-frontend-initial-run.md).
