import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import test from 'node:test'

test('RYLAY platform identity and PostgreSQL identities preserve release compatibility', async () => {
  assert.equal(JSON.parse(await readFile('frontend/package.json', 'utf8')).name, 'rylay-admin')
  assert.equal(JSON.parse(await readFile('app/package.json', 'utf8')).name, 'rylay-school-app')
  assert.match(await readFile('backend/.env.example', 'utf8'), /^APP_NAME=RYLAY$/m)
  assert.match(await readFile('deploy/env/database.env.example', 'utf8'), /^PRODUCTION_DB_DATABASE=rylay_production$/m)
  // Internal image, network and release names are retained for existing tooling.
  assert.equal(JSON.parse(await readFile('backend/composer.json', 'utf8')).name, 'rylay/platform-api')
  assert.match(await readFile('deploy/scripts/package-release.sh', 'utf8'), /rylay-\$commit\.zip/)
  assert.match(await readFile('deploy/compose/application.yml', 'utf8'), /name: rylay_database/)
})
