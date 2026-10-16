# GitHub development baseline — 2026-10-16

The project separation PR is being prepared for merge to the repository default branch. This is a development baseline update, not a production deployment.

## Security updates

Compatible Composer updates: Laravel Framework 13.36.0, Laravel Prompts 0.3.26, CommonMark 2.10.3, Flysystem 3.36.0 and Symfony HttpFoundation 8.1.9. npm locks update Vitest/Mocker to 4.1.12 and vulnerable transitive dependencies including source-map-js 1.2.2 and Undici 7.30.1. Package manifests and application business logic are unchanged.

`composer audit --locked` reports no advisories. `npm audit --audit-level=moderate` passes independently in Admin and School App; complete npm audit reports zero vulnerabilities. The earlier separation evidence's dependency security blockers are resolved by this update.

## Continuous integration

`.github/workflows/pull-request.yml` invokes full qualification for the exact PR head SHA with `contents: read`, no inherited secrets, and no deployment action. The existing default-branch release candidate workflow remains in place. New regression contracts pin safe dependency ranges and PR workflow inputs. All 31 deployment contracts pass locally.

## Local verification

RYLAY backend: SQLite 419 passed / 13 skipped (2,367 assertions), PostgreSQL 18.6 411 passed / 21 skipped (2,353 assertions). PostgreSQL qualification uses a newly initialized independent local test cluster on loopback 55435 and disposable `rylay_test`; the application SQLite demo was not reset or migrated.

Admin 219 tests and School App 59 tests passed. Each client passed Oxlint and TypeScript/Vite build. Backend Pint, Composer validation, API routes and all 31 deployment contracts passed. Live Matahari CSRF/login/session/scoped-read/logout smoke and separate project session Cookies still pass after the framework update. Fresh read-only review reports no Critical or Important findings.

Commands: backend `php vendor/bin/phpunit`, `php vendor/bin/pint --test`, `composer validate --no-check-publish`, `composer audit --locked`, API route loading; per client `npm test -- --maxWorkers=2`, `npm run lint`, `npm run build`, `npm audit --audit-level=moderate`; root `node --test deploy/tests/*.test.mjs`. PostgreSQL tests require the project's explicit reset opt-in and disposable database guard.

GitHub-hosted execution and merge results must be verified separately; local passes do not claim remote CI or production readiness. Existing lint/bundle advisories remain warnings, not errors. No production hosting or automatic deployment is configured by this change.
