/**
 * Shared constants and checks for the Agent Plugins spec (https://agent-plugins.org)
 * and the Agent Skills spec (https://agentskills.io/specification).
 *
 * Used by build-plugins.js (generation) and validate-plugins.js (validation).
 */

import matter from 'gray-matter';

export const PLUGIN_SCHEMA_URL = 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json';
export const MARKETPLACE_NAME = 'skills-hub';
export const MARKETPLACE_OWNER = { name: 'samueltauil' };
export const MARKETPLACE_REPO = 'samueltauil/skills-hub';
export const SITE_URL = 'https://skillshub.space';
export const PLUGINS_DIR = 'plugins';
export const MARKETPLACE_PATH = '.github/plugin/marketplace.json';
export const EXTENSION_NAMESPACE = 'space.skillshub';

export const MAX_NAME_LENGTH = 64;
export const MAX_DESCRIPTION_LENGTH = 1024;
export const MAX_COMPATIBILITY_LENGTH = 500;

// plugin.json `name` pattern from the Agent Plugins 1.0.0 schema
const PLUGIN_NAME_RE = /^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$/;
// SKILL.md `name` rules from the Agent Skills spec
const SKILL_NAME_RE = /^(?!.*--)[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
// Marketplace and plugin entry names are kebab-case
const KEBAB_RE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const SEMVER_RE = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/;
const NAMESPACE_RE = /^[a-z0-9-]+(?:\.[a-z0-9-]+)+$/;

// Closed set of top-level plugin.json properties allowed by the 1.0.0 schema
export const PLUGIN_FIELDS = new Set([
  '$schema', 'name', 'version', 'description', 'author', 'homepage',
  'repository', 'license', 'keywords', 'extensions',
]);
const AUTHOR_FIELDS = new Set(['name', 'email', 'url']);
const PLUGIN_STRING_FIELDS = ['version', 'description', 'homepage', 'repository', 'license'];

export function isValidPluginName(name) {
  return typeof name === 'string' && name.length >= 1 && name.length <= MAX_NAME_LENGTH && PLUGIN_NAME_RE.test(name);
}

export function isValidSkillName(name) {
  return typeof name === 'string' && name.length >= 1 && name.length <= MAX_NAME_LENGTH && SKILL_NAME_RE.test(name);
}

export function isKebabName(name) {
  return typeof name === 'string' && name.length >= 1 && name.length <= MAX_NAME_LENGTH && KEBAB_RE.test(name);
}

export function isSemver(version) {
  return typeof version === 'string' && SEMVER_RE.test(version);
}

export function bumpPatch(version) {
  const m = SEMVER_RE.exec(version || '');
  if (!m) return '1.0.0';
  return `${m[1]}.${m[2]}.${Number(m[3]) + 1}`;
}

/**
 * A relative path is safe when it stays inside its root: no absolute paths,
 * no drive letters, no backslashes and no `..` segments.
 */
export function isSafeRelativePath(p) {
  if (typeof p !== 'string' || p.length === 0) return false;
  if (p.startsWith('/') || p.includes('\\') || /^[a-zA-Z]:/.test(p) || p.includes('\0')) return false;
  return !p.split('/').some(seg => seg === '..' || seg === '');
}

/**
 * Validate a plugin.json object against the Agent Plugins 1.0.0 manifest schema.
 * Returns a list of error strings (empty when valid).
 */
export function validatePluginManifest(manifest) {
  const errors = [];
  if (!manifest || typeof manifest !== 'object' || Array.isArray(manifest)) {
    return ['plugin.json must be a JSON object'];
  }
  for (const key of Object.keys(manifest)) {
    if (!PLUGIN_FIELDS.has(key)) errors.push(`unknown property "${key}" (schema does not allow additional properties)`);
  }
  if (manifest.$schema !== PLUGIN_SCHEMA_URL) {
    errors.push(`"$schema" must be "${PLUGIN_SCHEMA_URL}"`);
  }
  if (!isValidPluginName(manifest.name)) {
    errors.push(`"name" ${JSON.stringify(manifest.name)} is not a valid plugin name`);
  }
  for (const field of PLUGIN_STRING_FIELDS) {
    if (field in manifest && typeof manifest[field] !== 'string') errors.push(`"${field}" must be a string`);
  }
  if ('author' in manifest) {
    const a = manifest.author;
    if (!a || typeof a !== 'object' || Array.isArray(a)) {
      errors.push('"author" must be an object');
    } else {
      for (const [k, v] of Object.entries(a)) {
        if (!AUTHOR_FIELDS.has(k)) errors.push(`unknown author property "${k}"`);
        else if (typeof v !== 'string') errors.push(`"author.${k}" must be a string`);
      }
    }
  }
  if ('keywords' in manifest) {
    if (!Array.isArray(manifest.keywords) || manifest.keywords.some(k => typeof k !== 'string')) {
      errors.push('"keywords" must be an array of strings');
    }
  }
  if ('extensions' in manifest) {
    const ext = manifest.extensions;
    if (!ext || typeof ext !== 'object' || Array.isArray(ext)) {
      errors.push('"extensions" must be an object');
    } else {
      for (const [ns, v] of Object.entries(ext)) {
        if (!NAMESPACE_RE.test(ns)) errors.push(`extension namespace "${ns}" must be reverse-domain (e.g. "com.example")`);
        if (!v || typeof v !== 'object' || Array.isArray(v)) errors.push(`extension "${ns}" must be an object`);
      }
    }
  }
  return errors;
}

/**
 * Parse SKILL.md content and check it against the Agent Skills spec.
 * `dirName` is the skill's parent directory name, which must equal `name`.
 */
export function checkSkillMarkdown(content, dirName) {
  const errors = [];
  let data;
  try {
    data = matter(content).data;
  } catch (err) {
    return { errors: [`SKILL.md frontmatter could not be parsed: ${err.message}`], data: {} };
  }
  if (!data || typeof data !== 'object' || Object.keys(data).length === 0) {
    return { errors: ['SKILL.md is missing YAML frontmatter'], data: {} };
  }
  if (!isValidSkillName(data.name)) {
    errors.push(`SKILL.md name ${JSON.stringify(data.name)} is not a valid skill name`);
  } else if (dirName !== undefined && data.name !== dirName) {
    errors.push(`SKILL.md name "${data.name}" does not match its directory "${dirName}"`);
  }
  if (typeof data.description !== 'string' || data.description.trim().length === 0) {
    errors.push('SKILL.md description is required');
  } else if (data.description.length > MAX_DESCRIPTION_LENGTH) {
    errors.push(`SKILL.md description is ${data.description.length} characters (max ${MAX_DESCRIPTION_LENGTH})`);
  }
  if (data.compatibility !== undefined &&
      (typeof data.compatibility !== 'string' || data.compatibility.length > MAX_COMPATIBILITY_LENGTH)) {
    errors.push(`SKILL.md compatibility must be a string of at most ${MAX_COMPATIBILITY_LENGTH} characters`);
  }
  return { errors, data };
}

/** Trim text to `max` characters on a word boundary, adding an ellipsis if cut. */
export function truncate(text, max = MAX_DESCRIPTION_LENGTH) {
  const clean = String(text || '').replace(/\s+/g, ' ').trim();
  if (clean.length <= max) return clean;
  const cut = clean.slice(0, max - 1);
  const lastSpace = cut.lastIndexOf(' ');
  return `${(lastSpace > max * 0.6 ? cut.slice(0, lastSpace) : cut).replace(/[\s.,;:]+$/, '')}…`;
}
