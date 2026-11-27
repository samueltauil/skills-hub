import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  PLUGIN_FIELDS,
  PLUGIN_SCHEMA_URL,
  bumpPatch,
  checkSkillMarkdown,
  isSafeRelativePath,
  isValidPluginName,
  isValidSkillName,
  truncate,
  validatePluginManifest,
} from './plugin-spec.js';
import { diffOutput, generate, planPlugin, resolveVersion, vscodeInstallLink, writeOutput } from './build-plugins.js';
import { validateMarketplace, validateRepository } from './validate-plugins.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function skillMd(name, description = 'Does a useful thing.') {
  return `---\nname: ${name}\ndescription: ${description}\n---\n\n# ${name}\n\nInstructions.\n`;
}

function makeSkill(overrides = {}) {
  const id = overrides.id || 'demo-skill';
  return {
    id,
    name: id,
    description: 'Does a useful thing.',
    category: 'testing',
    author: 'example',
    license: 'MIT',
    licenseNotice: 'MIT License\n\nCopyright Example',
    tags: ['demo', 'Testing'],
    source: { repo: 'https://github.com/example/skills', repoName: 'example/skills', path: `skills/${id}`, branch: 'main' },
    files: [
      { path: 'SKILL.md', name: 'SKILL.md', content: skillMd(overrides.skillName || id) },
      { path: 'references/guide.md', name: 'guide.md', content: '# Guide\n' },
    ],
    ...overrides,
  };
}

function tempRoot() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'skills-hub-plugins-'));
}

test('plugin and skill names follow the specs', () => {
  assert.ok(isValidPluginName('my-plugin'));
  assert.ok(isValidPluginName('my.plugin2'));
  assert.ok(!isValidPluginName('My-Plugin'));
  assert.ok(!isValidPluginName('-leading'));
  assert.ok(!isValidPluginName('double--hyphen'));
  assert.ok(!isValidPluginName('a'.repeat(65)));
  assert.ok(isValidSkillName('pdf-tools'));
  assert.ok(!isValidSkillName('pdf.tools'));
  assert.ok(!isValidSkillName('trailing-'));
});

test('relative paths must stay inside the plugin', () => {
  assert.ok(isSafeRelativePath('skills/x/SKILL.md'));
  assert.ok(!isSafeRelativePath('../escape'));
  assert.ok(!isSafeRelativePath('a/../../b'));
  assert.ok(!isSafeRelativePath('/etc/passwd'));
  assert.ok(!isSafeRelativePath('C:/windows'));
  assert.ok(!isSafeRelativePath('a\\b'));
  assert.ok(!isSafeRelativePath('a//b'));
});

test('truncate and bumpPatch', () => {
  assert.equal(truncate('short'), 'short');
  const long = truncate('word '.repeat(400), 100);
  assert.ok(long.length <= 100);
  assert.ok(long.endsWith('…'));
  assert.equal(bumpPatch('1.0.0'), '1.0.1');
  assert.equal(bumpPatch('2.3.9'), '2.3.10');
  assert.equal(bumpPatch('nope'), '1.0.0');
});

test('manifest validation mirrors the closed Agent Plugins schema', () => {
  const schema = JSON.parse(fs.readFileSync(path.join(__dirname, 'schemas', 'agent-plugins-1.0.0.plugin.schema.json'), 'utf8'));
  assert.deepEqual([...PLUGIN_FIELDS].sort(), Object.keys(schema.properties).sort());
  assert.equal(schema.properties.$schema.const, PLUGIN_SCHEMA_URL);

  assert.deepEqual(validatePluginManifest({ $schema: PLUGIN_SCHEMA_URL, name: 'ok' }), []);
  assert.ok(validatePluginManifest({ name: 'ok' }).some(e => e.includes('$schema')));
  assert.ok(validatePluginManifest({ $schema: PLUGIN_SCHEMA_URL, name: 'ok', skills: [] }).some(e => e.includes('"skills"')));
  assert.ok(validatePluginManifest({ $schema: PLUGIN_SCHEMA_URL, name: 'ok', author: { name: 'x', team: 'y' } }).length > 0);
  assert.ok(validatePluginManifest({ $schema: PLUGIN_SCHEMA_URL, name: 'ok', keywords: [1] }).length > 0);
  assert.ok(validatePluginManifest({ $schema: PLUGIN_SCHEMA_URL, name: 'ok', extensions: { bad: {} } }).length > 0);
});

test('SKILL.md checks name, directory and description length', () => {
  assert.deepEqual(checkSkillMarkdown(skillMd('demo'), 'demo').errors, []);
  assert.ok(checkSkillMarkdown(skillMd('demo'), 'other').errors[0].includes('does not match'));
  assert.ok(checkSkillMarkdown(skillMd('demo', 'x'.repeat(1025)), 'demo').errors[0].includes('1025'));
  assert.ok(checkSkillMarkdown('# no frontmatter', 'demo').errors[0].includes('frontmatter'));
});

test('planPlugin lays out a spec-compliant plugin', () => {
  const { plugin } = planPlugin(makeSkill({ id: 'demo-skill', skillName: 'demo' }));
  assert.equal(plugin.name, 'demo-skill');
  assert.equal(plugin.skillName, 'demo');
  assert.ok(plugin.contents.has('skills/demo/SKILL.md'));
  assert.ok(plugin.contents.has('skills/demo/references/guide.md'));
  assert.ok(plugin.contents.has('LICENSE'));
  assert.ok(plugin.contents.get('README.md').includes('copilot plugin install demo-skill@skills-hub'));
  assert.deepEqual(validatePluginManifest(plugin.manifest), []);
  assert.deepEqual(plugin.manifest.keywords, ['testing', 'demo']);
});

test('planPlugin skips non-conformant skills', () => {
  assert.ok(planPlugin(makeSkill({ id: 'Bad_Name' })).skip);
  const longDesc = makeSkill();
  longDesc.files[0].content = skillMd('demo-skill', 'x'.repeat(1100));
  assert.match(planPlugin(longDesc).skip, /1100/);
  const unsafe = makeSkill();
  unsafe.files.push({ path: '../evil.md', name: 'evil.md', content: 'x' });
  assert.match(planPlugin(unsafe).skip, /unsafe/);
});

test('versions only change when content changes', () => {
  const { plugin } = planPlugin(makeSkill());
  const previous = { version: '1.0.4', extensions: plugin.manifest.extensions };
  assert.equal(resolveVersion(plugin.manifest, previous), '1.0.4');
  assert.equal(resolveVersion(plugin.manifest, { version: '1.0.4', extensions: {} }), '1.0.5');
  assert.equal(resolveVersion(plugin.manifest, null), '1.0.0');
});

test('generated output validates, stays in sync and cleans up stale plugins', () => {
  const root = tempRoot();
  try {
    const catalog = { skills: [makeSkill({ id: 'alpha' }), makeSkill({ id: 'beta' })] };
    writeOutput(generate(catalog, root), root);
    assert.deepEqual(validateRepository(root).errors, []);
    assert.deepEqual(diffOutput(generate(catalog, root), root), []);

    // Rebuilding unchanged content keeps versions stable
    const mp = JSON.parse(fs.readFileSync(path.join(root, '.github/plugin/marketplace.json'), 'utf8'));
    assert.equal(mp.metadata.version, '1.0.0');
    assert.deepEqual(mp.plugins.map(p => [p.name, p.version, p.source]), [
      ['alpha', '1.0.0', './plugins/alpha'],
      ['beta', '1.0.0', './plugins/beta'],
    ]);

    // Editing generated files is detected
    fs.appendFileSync(path.join(root, 'plugins/alpha/skills/alpha/SKILL.md'), 'tampered');
    assert.ok(diffOutput(generate(catalog, root), root).some(p => p.includes('out of date')));

    // Changing a skill bumps its plugin and the marketplace; removed skills are deleted
    const changed = { skills: [makeSkill({ id: 'alpha', description: 'Now does more.' })] };
    writeOutput(generate(changed, root), root);
    const after = JSON.parse(fs.readFileSync(path.join(root, '.github/plugin/marketplace.json'), 'utf8'));
    assert.deepEqual(after.plugins.map(p => [p.name, p.version]), [['alpha', '1.0.1']]);
    assert.equal(after.metadata.version, '1.0.1');
    assert.ok(!fs.existsSync(path.join(root, 'plugins/beta')));
    assert.deepEqual(validateRepository(root).errors, []);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('validator catches marketplace and plugin problems', () => {
  const root = tempRoot();
  try {
    writeOutput(generate({ skills: [makeSkill({ id: 'alpha' })] }, root), root);
    const mpFile = path.join(root, '.github/plugin/marketplace.json');
    const mp = JSON.parse(fs.readFileSync(mpFile, 'utf8'));

    // Orphan plugin directory
    fs.mkdirSync(path.join(root, 'plugins/orphan'));
    assert.ok(validateRepository(root).errors.some(e => e.includes('plugins/orphan: not listed')));
    fs.rmSync(path.join(root, 'plugins/orphan'), { recursive: true });

    // Version drift between marketplace and plugin.json
    fs.writeFileSync(mpFile, JSON.stringify({ ...mp, plugins: [{ ...mp.plugins[0], version: '9.9.9' }] }));
    assert.ok(validateRepository(root).errors.some(e => e.includes('"version" for "alpha" does not match')));

    // Missing source
    fs.writeFileSync(mpFile, JSON.stringify({ ...mp, plugins: [{ ...mp.plugins[0], source: './plugins/missing' }] }));
    assert.ok(validateRepository(root).errors.some(e => e.includes('does not exist')));
    fs.writeFileSync(mpFile, JSON.stringify(mp));

    // Skill directory that does not match its SKILL.md name
    fs.renameSync(path.join(root, 'plugins/alpha/skills/alpha'), path.join(root, 'plugins/alpha/skills/renamed'));
    assert.ok(validateRepository(root).errors.some(e => e.includes('does not match its directory')));
    fs.renameSync(path.join(root, 'plugins/alpha/skills/renamed'), path.join(root, 'plugins/alpha/skills/alpha'));

    // Symlinks are rejected
    fs.symlinkSync('/etc/hostname', path.join(root, 'plugins/alpha/skills/alpha/link'));
    assert.ok(validateRepository(root).errors.some(e => e.includes('symlinks are not allowed')));
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('marketplace structure checks', () => {
  assert.ok(validateMarketplace({ name: 'Bad Name', owner: { name: 'x' }, plugins: [{}] }).some(e => e.includes('kebab-case')));
  assert.ok(validateMarketplace({ name: 'ok', plugins: [{ name: 'a', source: './a' }] }).some(e => e.includes('owner.name')));
  const dupes = validateMarketplace({
    name: 'ok',
    owner: { name: 'x' },
    plugins: [{ name: 'a', source: './plugins/a' }, { name: 'a', source: '../a' }],
  });
  assert.ok(dupes.some(e => e.includes('duplicate')));
  assert.ok(dupes.some(e => e.includes('"source"')));
});

test('VS Code deep link is double encoded for the redirect wrapper', () => {
  assert.equal(
    vscodeInstallLink('pdf'),
    'https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpdf',
  );
});
