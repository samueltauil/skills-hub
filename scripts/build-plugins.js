#!/usr/bin/env node

/**
 * Build Agent Plugins from the aggregated skills catalog.
 *
 * Every conformant skill in site/src/data/skills.json becomes a standalone
 * plugin under plugins/<skill-id>/ following the Agent Plugins 1.0.0 spec
 * (https://agent-plugins.org):
 *
 *   plugins/<skill-id>/
 *   ├── plugin.json            # Agent Plugins manifest
 *   ├── README.md              # What it is and how to install it
 *   ├── LICENSE                # Upstream license notice
 *   └── skills/<skill-name>/   # The skill files, as scanned and published on the site
 *
 * It also writes the marketplace catalog at .github/plugin/marketplace.json so
 * the repository can be added as a marketplace in Copilot CLI and VS Code.
 *
 * Versions start at 1.0.0 and get a patch bump whenever a plugin's content
 * changes (tracked with a content hash stored in the manifest extensions).
 *
 * Usage:
 *   node scripts/build-plugins.js           # write plugins/ and marketplace.json
 *   node scripts/build-plugins.js --check   # fail if the generated output is out of date
 */

import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  EXTENSION_NAMESPACE,
  MARKETPLACE_NAME,
  MARKETPLACE_OWNER,
  MARKETPLACE_PATH,
  MARKETPLACE_REPO,
  PLUGINS_DIR,
  PLUGIN_SCHEMA_URL,
  SITE_URL,
  bumpPatch,
  checkSkillMarkdown,
  isSafeRelativePath,
  isValidPluginName,
  truncate,
} from './plugin-spec.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const SKILLS_JSON = path.join(ROOT, 'site', 'src', 'data', 'skills.json');

const MARKETPLACE_DESCRIPTION =
  'Curated catalog of Agent Skills for GitHub Copilot, packaged as Agent Plugins. Every skill is security scanned and installable on its own.';

function sha256(text) {
  return createHash('sha256').update(text).digest('hex');
}

function uniqueKeywords(skill) {
  const words = [skill.category, ...(skill.tags || [])]
    .filter(w => typeof w === 'string' && w.trim())
    .map(w => w.trim().toLowerCase());
  return [...new Set(words)];
}

function pluginReadme(skill, skillName) {
  const sourceUrl = `${skill.source.repo}/tree/${skill.source.branch || 'main'}/${skill.source.path}`;
  const vscodeLink = vscodeInstallLink(skill.id);
  return `# ${skill.id}

${truncate(skill.description)}

This plugin packages the [\`${skillName}\`](skills/${skillName}/SKILL.md) skill from
[${skill.source.repoName}](${sourceUrl}) so it can be installed on its own. It is generated
by [Skills Hub](${SITE_URL}/skills/${skill.id}/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

\`\`\`sh
copilot plugin marketplace add ${MARKETPLACE_REPO}
copilot plugin install ${skill.id}@${MARKETPLACE_NAME}
\`\`\`

VS Code (with \`chat.plugins.enabled\` turned on): [install with one click](${vscodeLink}),
or add the \`${MARKETPLACE_REPO}\` marketplace from the Agent Customizations editor and
search for \`${skill.id}\`.

## License

${skill.license}. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[${skill.source.repoName}](${skill.source.repo}).
`;
}

export function vscodeInstallLink(pluginName) {
  const inner = `vscode://chat-plugin/install?source=${encodeURIComponent(MARKETPLACE_REPO)}&plugin=${encodeURIComponent(pluginName)}`;
  return `https://vscode.dev/redirect?url=${encodeURIComponent(inner)}`;
}

/**
 * Work out what a skill's plugin should contain. Returns either
 * { plugin } or { skip: reason }.
 */
export function planPlugin(skill) {
  if (!isValidPluginName(skill.id)) {
    return { skip: `"${skill.id}" is not a valid plugin name` };
  }
  const files = Array.isArray(skill.files) ? skill.files : [];
  const skillMd = files.find(f => f.path === 'SKILL.md');
  if (!skillMd) return { skip: 'no SKILL.md at the skill root' };

  const { errors, data } = checkSkillMarkdown(skillMd.content);
  if (errors.length) return { skip: errors.join('; ') };
  const skillName = data.name;

  const unsafe = files.filter(f => !isSafeRelativePath(f.path));
  if (unsafe.length) return { skip: `unsafe file path(s): ${unsafe.map(f => f.path).join(', ')}` };
  if (!skill.source || !skill.source.repo) return { skip: 'missing source repository' };

  const contents = new Map();
  for (const f of [...files].sort((a, b) => a.path.localeCompare(b.path))) {
    contents.set(`skills/${skillName}/${f.path}`, f.content);
  }
  contents.set('LICENSE', `${(skill.licenseNotice || skill.license || '').trim()}\n`);
  contents.set('README.md', pluginReadme(skill, skillName));

  const manifest = {
    $schema: PLUGIN_SCHEMA_URL,
    name: skill.id,
    version: '1.0.0',
    description: truncate(skill.description),
    author: { name: skill.author, url: `https://github.com/${skill.source.repoName.split('/')[0]}` },
    homepage: `${SITE_URL}/skills/${skill.id}/`,
    repository: skill.source.repo,
    license: skill.license,
    keywords: uniqueKeywords(skill),
    extensions: {
      [EXTENSION_NAMESPACE]: {
        category: skill.category,
        source: {
          repo: skill.source.repo,
          path: skill.source.path,
          branch: skill.source.branch || 'main',
        },
        contentHash: '',
      },
    },
  };

  const hashInput = JSON.stringify({
    manifest: { ...manifest, version: undefined },
    files: [...contents.entries()],
  });
  manifest.extensions[EXTENSION_NAMESPACE].contentHash = `sha256:${sha256(hashInput)}`;

  return { plugin: { name: skill.id, skillName, manifest, contents, category: skill.category } };
}

/** Keep the previous version when content is unchanged, otherwise bump the patch. */
export function resolveVersion(manifest, previous) {
  if (!previous || typeof previous.version !== 'string') return '1.0.0';
  const prevHash = previous.extensions?.[EXTENSION_NAMESPACE]?.contentHash;
  const nextHash = manifest.extensions[EXTENSION_NAMESPACE].contentHash;
  return prevHash === nextHash ? previous.version : bumpPatch(previous.version);
}

export function marketplaceEntry(plugin) {
  const m = plugin.manifest;
  return {
    name: m.name,
    source: `./${PLUGINS_DIR}/${m.name}`,
    description: m.description,
    version: m.version,
    author: { name: m.author.name },
    homepage: m.homepage,
    repository: m.repository,
    license: m.license,
    category: plugin.category,
    keywords: m.keywords,
  };
}

export function buildMarketplace(plugins, previous) {
  const entries = plugins.map(marketplaceEntry).sort((a, b) => a.name.localeCompare(b.name));
  const prevVersion = previous?.metadata?.version;
  const changed = !previous || JSON.stringify(previous.plugins) !== JSON.stringify(entries);
  return {
    name: MARKETPLACE_NAME,
    owner: { name: MARKETPLACE_OWNER.name },
    metadata: {
      description: MARKETPLACE_DESCRIPTION,
      version: prevVersion ? (changed ? bumpPatch(prevVersion) : prevVersion) : '1.0.0',
    },
    plugins: entries,
  };
}

function readJson(file) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch {
    return null;
  }
}

function listFiles(dir, base = dir) {
  if (!fs.existsSync(dir)) return [];
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...listFiles(full, base));
    else out.push(path.relative(base, full).split(path.sep).join('/'));
  }
  return out;
}

const json = obj => `${JSON.stringify(obj, null, 2)}\n`;

/**
 * Generate everything in memory. `root` is the repository root used to look
 * up previously published versions.
 */
export function generate(catalog, root = ROOT) {
  const plugins = [];
  const skipped = [];
  const seen = new Set();
  const skills = [...(catalog.skills || [])].sort((a, b) => a.id.localeCompare(b.id));

  for (const skill of skills) {
    if (seen.has(skill.id)) {
      skipped.push({ id: skill.id, reason: 'duplicate skill id' });
      continue;
    }
    seen.add(skill.id);
    const result = planPlugin(skill);
    if (result.skip) {
      skipped.push({ id: skill.id, reason: result.skip });
      continue;
    }
    const plugin = result.plugin;
    const previous = readJson(path.join(root, PLUGINS_DIR, plugin.name, 'plugin.json'));
    plugin.manifest.version = resolveVersion(plugin.manifest, previous);
    plugin.contents.set('plugin.json', json(plugin.manifest));
    plugins.push(plugin);
  }

  const marketplace = buildMarketplace(plugins, readJson(path.join(root, MARKETPLACE_PATH)));
  return { plugins, skipped, marketplace };
}

/** Compare generated output with what is on disk. Returns a list of differences. */
export function diffOutput({ plugins, marketplace }, root = ROOT) {
  const problems = [];
  const pluginsRoot = path.join(root, PLUGINS_DIR);
  const expected = new Set(plugins.map(p => p.name));

  if (fs.existsSync(pluginsRoot)) {
    for (const dir of fs.readdirSync(pluginsRoot)) {
      if (!expected.has(dir)) problems.push(`${PLUGINS_DIR}/${dir} is stale (no matching skill)`);
    }
  }
  for (const plugin of plugins) {
    const dir = path.join(pluginsRoot, plugin.name);
    const onDisk = new Set(listFiles(dir));
    for (const [rel, content] of plugin.contents) {
      const file = path.join(dir, rel);
      if (!onDisk.has(rel)) problems.push(`${PLUGINS_DIR}/${plugin.name}/${rel} is missing`);
      else if (fs.readFileSync(file, 'utf8') !== content) problems.push(`${PLUGINS_DIR}/${plugin.name}/${rel} is out of date`);
      onDisk.delete(rel);
    }
    for (const rel of onDisk) problems.push(`${PLUGINS_DIR}/${plugin.name}/${rel} is not generated from the catalog`);
  }
  const mpFile = path.join(root, MARKETPLACE_PATH);
  if (!fs.existsSync(mpFile) || fs.readFileSync(mpFile, 'utf8') !== json(marketplace)) {
    problems.push(`${MARKETPLACE_PATH} is out of date`);
  }
  return problems;
}

/** Write generated output to disk, removing stale plugins and files. */
export function writeOutput({ plugins, marketplace }, root = ROOT) {
  const pluginsRoot = path.join(root, PLUGINS_DIR);
  fs.mkdirSync(pluginsRoot, { recursive: true });
  const expected = new Set(plugins.map(p => p.name));
  for (const dir of fs.readdirSync(pluginsRoot)) {
    if (!expected.has(dir)) fs.rmSync(path.join(pluginsRoot, dir), { recursive: true, force: true });
  }
  let written = 0;
  for (const plugin of plugins) {
    const dir = path.join(pluginsRoot, plugin.name);
    const stale = new Set(listFiles(dir));
    for (const [rel, content] of plugin.contents) {
      stale.delete(rel);
      const file = path.join(dir, rel);
      if (fs.existsSync(file) && fs.readFileSync(file, 'utf8') === content) continue;
      fs.mkdirSync(path.dirname(file), { recursive: true });
      fs.writeFileSync(file, content);
      written++;
    }
    for (const rel of stale) fs.rmSync(path.join(dir, rel), { force: true });
    removeEmptyDirs(dir);
  }
  const mpFile = path.join(root, MARKETPLACE_PATH);
  fs.mkdirSync(path.dirname(mpFile), { recursive: true });
  fs.writeFileSync(mpFile, json(marketplace));
  return written;
}

function removeEmptyDirs(dir) {
  if (!fs.existsSync(dir)) return;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) removeEmptyDirs(path.join(dir, entry.name));
  }
  if (fs.readdirSync(dir).length === 0) fs.rmdirSync(dir);
}

function main() {
  const check = process.argv.includes('--check');
  const catalog = JSON.parse(fs.readFileSync(SKILLS_JSON, 'utf8'));
  const output = generate(catalog);

  for (const s of output.skipped) {
    console.warn(`⚠️  Skipping ${s.id}: ${s.reason}`);
  }

  if (check) {
    const problems = diffOutput(output);
    if (problems.length) {
      console.error(`❌ Plugins are out of date with the skills catalog (${problems.length} difference(s)):`);
      problems.slice(0, 50).forEach(p => console.error(`   - ${p}`));
      if (problems.length > 50) console.error(`   … and ${problems.length - 50} more`);
      console.error('Run "npm run build:plugins" and commit the result.');
      process.exit(1);
    }
    console.log(`✅ ${output.plugins.length} plugins and ${MARKETPLACE_PATH} are up to date.`);
    return;
  }

  const written = writeOutput(output);
  console.log(`✅ Built ${output.plugins.length} plugins (${written} file(s) written, ${output.skipped.length} skipped).`);
  console.log(`📦 Marketplace "${output.marketplace.name}" v${output.marketplace.metadata.version} → ${MARKETPLACE_PATH}`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main();
}
