# RYLAY project identity separation — 2026-10-16

RYLAY is the original tenant-aware platform at `/Users/kaiyangchong/Project/RYLAY`, origin `Kaikaiyng/RYLAY`. The independent school-only product lives at `/Users/kaiyangchong/Project/Matahari`, origin `Kaikaiyng/Matahari`. Their databases, private configuration, application keys, dependency directories and session Cookie names are independent. Existing school branding and historical MIS identifiers are preserved.

Changed areas: repository/client documentation and project instructions, npm package/lockfile metadata, HTML fallback titles, environment defaults, deployment/CI database names, disposable PostgreSQL test names/guard, matching identity contracts and `tools/dev.py`. No student, finance, academic, permission or tenant business logic changed. Existing physical databases/clusters were not renamed; current dedicated MIS restrictions remain enforced.

Local verification: backend SQLite PHPUnit 419 passed / 13 skipped, 2,367 assertions; Pint, Composer validate and API routes passed. Admin Vitest 219 and App Vitest 59 passed; both clients independently passed lint and TypeScript/Vite builds. All 26 deployment contracts passed. PostgreSQL business behavior was not rerun for this identity-only change. No existing test was represented as PostgreSQL verification.

Commands: `php vendor/bin/phpunit`, `php vendor/bin/pint --test`, `composer validate --no-check-publish`, `php artisan route:list --path=api --except-vendor`, `npm test -- --maxWorkers=2`, `npm run lint`, `npm run build` in each client, root `node --test deploy/tests/*.test.mjs`. HTTP configuration and CSRF bootstrap return 200/204 and use `rylay_session`; Matahari uses `matahari_session`. Source secret-pattern, diff whitespace and canonical link checks passed.

Local launch: `python3 tools/dev.py start|stop|status`; it never initializes/resets data and stops only its own recorded process groups. Admin localhost:5173, App 127.0.0.1:5174, API loopback 8000.

Inherited Composer locks have five security advisories across four packages (Laravel Framework, CommonMark, Flysystem, Symfony HttpFoundation); security qualification is not passed. No production release, automatic merge or deployment is included. Existing lint/bundle warnings remain. GitHub full qualification, Windows runtime and production readiness are not claimed.

Review handoff: [RYLAY #14](https://github.com/Kaikaiyng/RYLAY/pull/14), with the standalone implementation in [Matahari #1](https://github.com/Kaikaiyng/Matahari/pull/1). Both remain draft/unmerged; local checkouts run the reviewed feature branches.
