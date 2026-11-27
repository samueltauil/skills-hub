#!/usr/bin/env node

/**
 * Validate the plugin marketplace and every plugin in it.
 *
 * Checks, without any network access or extra dependencies:
 *   - .github/plugin/marketplace.json structure (name, owner, metadata, plugins)
 *   - every marketplace entry: valid unique name, safe relative source that
 *     exists, description length, semver version, and that name/version/
 *     description match the plugin's own plugin.json
 *   - every plugin directory is listed in the marketplace (no orphans)
 *   - plugin.json against the closed Agent Plugins 1.0.0 manifest schema
 *   - skills/<dir>/SKILL.md against the Agent Skills spec (name matches dir,
 *     description 1-1024 characters)
 *   - no symlinks inside plugins, so nothing can point outside the plugin root
 *
 * Usage:
 *   node scripts/validate-plugins.js
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  MARKETPLACE_PATH,
  MAX_DESCRIPTION_LENGTH,
  PLUGINS_DIR,
  checkSkillMarkdown,
  isKebabName,
  isSafeRelativePath,
  isSemver,
  isValidPluginName,
  validatePluginManifest,
} from './plugin-spec.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

const MARKETPLACE_FIELDS = new Set(['$schema', 'name', 'owner', 'metadata', 'plugins']);
const ENTRY_FIELDS = new Set([
  'name', 'source', 'description', 'version', 'author', 'homepage', 'repository',
  'license', 'keywords', 'category', 'tags', 'strict',
]);

function readJson(file, errors, label) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (err) {
    errors.push(`${label}: ${err.code === 'ENOENT' ? 'file not found' : `invalid JSON (${err.message})`}`);
    return null;
  }
}

/** Walk a directory and report symlinks; returns relative file paths. */
function walk(dir, base, errors, label) {
  const files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    const rel = path.relative(base, full).split(path.sep).join('/');
    if (entry.isSymbolicLink()) {
      errors.push(`${label}/${rel}: symlinks are not allowed in plugins`);
    } else if (entry.isDirectory()) {
      files.push(...walk(full, base, errors, label));
    } else {
      files.push(rel);
    }
  }
  return files;
}

export function validatePlugin(pluginDir, label = pluginDir) {
  const errors = [];
  const manifest = readJson(path.join(pluginDir, 'plugin.json'), errors, `${label}/plugin.json`);
  if (manifest) {
    for (const e of validatePluginManifest(manifest)) errors.push(`${label}/plugin.json: ${e}`);
    if (!isSemver(manifest.version)) errors.push(`${label}/plugin.json: "version" must be a semantic version`);
    if (typeof manifest.description !== 'string' || !manifest.description.trim()) {
      errors.push(`${label}/plugin.json: "description" is required`);
    } else if (manifest.description.length > MAX_DESCRIPTION_LENGTH) {
      errors.push(`${label}/plugin.json: "description" exceeds ${MAX_DESCRIPTION_LENGTH} characters`);
    }
    if (manifest.name !== path.basename(pluginDir)) {
      errors.push(`${label}/plugin.json: name "${manifest.name}" does not match directory "${path.basename(pluginDir)}"`);
    }
  }

  walk(pluginDir, pluginDir, errors, label);

  const skillsDir = path.join(pluginDir, 'skills');
  let skillCount = 0;
  if (!fs.existsSync(skillsDir) || !fs.lstatSync(skillsDir).isDirectory()) {
    errors.push(`${label}: missing skills/ directory`);
  } else {
    for (const entry of fs.readdirSync(skillsDir, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const skillMd = path.join(skillsDir, entry.name, 'SKILL.md');
      if (!fs.existsSync(skillMd)) {
        errors.push(`${label}/skills/${entry.name}: missing SKILL.md`);
        continue;
      }
      skillCount++;
      const { errors: skillErrors } = checkSkillMarkdown(fs.readFileSync(skillMd, 'utf8'), entry.name);
      for (const e of skillErrors) errors.push(`${label}/skills/${entry.name}: ${e}`);
    }
    if (skillCount === 0) errors.push(`${label}: skills/ contains no skills`);
  }
  if (!fs.existsSync(path.join(pluginDir, 'LICENSE'))) {
    errors.push(`${label}: missing LICENSE`);
  }
  return { errors, manifest, skillCount };
}

export function validateMarketplace(marketplace) {
  const errors = [];
  const label = MARKETPLACE_PATH;
  if (!marketplace || typeof marketplace !== 'object' || Array.isArray(marketplace)) {
    return [`${label}: must be a JSON object`];
  }
  for (const key of Object.keys(marketplace)) {
    if (!MARKETPLACE_FIELDS.has(key)) errors.push(`${label}: unknown property "${key}"`);
  }
  if (!isKebabName(marketplace.name)) errors.push(`${label}: "name" must be kebab-case and at most 64 characters`);
  if (!marketplace.owner || typeof marketplace.owner.name !== 'string' || !marketplace.owner.name.trim()) {
    errors.push(`${label}: "owner.name" is required`);
  }
  if (marketplace.metadata !== undefined) {
    const md = marketplace.metadata;
    if (!md || typeof md !== 'object') errors.push(`${label}: "metadata" must be an object`);
    else if (md.version !== undefined && !isSemver(md.version)) errors.push(`${label}: "metadata.version" must be a semantic version`);
  }
  if (!Array.isArray(marketplace.plugins) || marketplace.plugins.length === 0) {
    errors.push(`${label}: "plugins" must be a non-empty array`);
    return errors;
  }
  const names = new Set();
  marketplace.plugins.forEach((entry, i) => {
    const at = `${label}: plugins[${i}]${entry && entry.name ? ` (${entry.name})` : ''}`;
    if (!entry || typeof entry !== 'object') {
      errors.push(`${at}: must be an object`);
      return;
    }
    for (const key of Object.keys(entry)) {
      if (!ENTRY_FIELDS.has(key)) errors.push(`${at}: unknown property "${key}"`);
    }
    if (!isValidPluginName(entry.name)) errors.push(`${at}: invalid plugin name`);
    if (names.has(entry.name)) errors.push(`${at}: duplicate plugin name`);
    names.add(entry.name);
    if (typeof entry.source !== 'string' || !entry.source.startsWith('./') || !isSafeRelativePath(entry.source.slice(2))) {
      errors.push(`${at}: "source" must be a relative path starting with "./" that stays inside the repository`);
    }
    if (entry.description !== undefined &&
        (typeof entry.description !== 'string' || entry.description.length > MAX_DESCRIPTION_LENGTH)) {
      errors.push(`${at}: "description" must be a string of at most ${MAX_DESCRIPTION_LENGTH} characters`);
    }
    if (entry.version !== undefined && !isSemver(entry.version)) errors.push(`${at}: "version" must be a semantic version`);
    if (entry.author !== undefined && (typeof entry.author !== 'object' || typeof entry.author.name !== 'string')) {
      errors.push(`${at}: "author.name" must be a string`);
    }
    for (const list of ['keywords', 'tags']) {
      if (entry[list] !== undefined && (!Array.isArray(entry[list]) || entry[list].some(k => typeof k !== 'string'))) {
        errors.push(`${at}: "${list}" must be an array of strings`);
      }
    }
  });
  return errors;
}

export function validateRepository(root = ROOT) {
  const errors = [];
  const marketplace = readJson(path.join(root, MARKETPLACE_PATH), errors, MARKETPLACE_PATH);
  if (!marketplace) return { errors, pluginCount: 0, skillCount: 0 };
  errors.push(...validateMarketplace(marketplace));

  const pluginsRoot = path.join(root, PLUGINS_DIR);
  const listed = new Set();
  let pluginCount = 0;
  let skillCount = 0;

  for (const entry of Array.isArray(marketplace.plugins) ? marketplace.plugins : []) {
    if (!entry || typeof entry.source !== 'string' || !entry.source.startsWith('./')) continue;
    const rel = entry.source.slice(2);
    if (!isSafeRelativePath(rel)) continue;
    const dir = path.resolve(root, rel);
    if (!dir.startsWith(path.resolve(root) + path.sep)) continue;
    listed.add(dir);
    const label = rel;
    if (!fs.existsSync(dir) || !fs.lstatSync(dir).isDirectory()) {
      errors.push(`${MARKETPLACE_PATH}: source "${entry.source}" for "${entry.name}" does not exist`);
      continue;
    }
    pluginCount++;
    const result = validatePlugin(dir, label);
    errors.push(...result.errors);
    skillCount += result.skillCount;
    const m = result.manifest;
    if (m) {
      for (const field of ['name', 'version', 'description']) {
        if (entry[field] !== undefined && entry[field] !== m[field]) {
          errors.push(`${MARKETPLACE_PATH}: "${field}" for "${entry.name}" does not match ${label}/plugin.json`);
        }
      }
    }
  }

  if (fs.existsSync(pluginsRoot)) {
    for (const entry of fs.readdirSync(pluginsRoot, { withFileTypes: true })) {
      const dir = path.join(pluginsRoot, entry.name);
      if (!listed.has(dir)) errors.push(`${PLUGINS_DIR}/${entry.name}: not listed in ${MARKETPLACE_PATH}`);
    }
  }
  return { errors, pluginCount, skillCount };
}

function main() {
  const { errors, pluginCount, skillCount } = validateRepository();
  if (errors.length) {
    console.error(`❌ Plugin validation failed with ${errors.length} error(s):`);
    errors.slice(0, 100).forEach(e => console.error(`   - ${e}`));
    if (errors.length > 100) console.error(`   … and ${errors.length - 100} more`);
    process.exit(1);
  }
  console.log(`✅ Marketplace and ${pluginCount} plugins (${skillCount} skills) are valid.`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main();
}
