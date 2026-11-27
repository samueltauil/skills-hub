/**
 * Aggregate skills from all source submodules
 * Reads SKILL.md files, extracts metadata, and collects all skill files
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import matter from 'gray-matter';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const SOURCES_DIR = path.join(ROOT, 'sources');
const OUTPUT_FILE = path.join(ROOT, 'site', 'src', 'data', 'skills.json');

// Licenses that prohibit redistribution — skills with these are excluded
const RESTRICTED_LICENSE_MARKERS = [
  'All rights reserved',
  'may not:',
  'Distribute, sublicense, or transfer',
  'Extract these materials from the Services'
];

const LICENSE_FILE_PATTERN = /^licen[cs]e(\.[a-z]+)?$/i;

// Source repositories configuration
const SOURCES = [
  {
    id: 'awesome-copilot',
    name: 'github/awesome-copilot',
    dir: 'awesome-copilot',
    paths: ['skills'],
    repo: 'https://github.com/github/awesome-copilot',
    author: 'github',
    defaultLicense: 'MIT',
    licenseNotice: 'MIT License\n\nCopyright GitHub, Inc.\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.'
  },
  {
    id: 'anthropics-skills',
    name: 'anthropics/skills',
    dir: 'anthropics-skills',
    paths: ['skills'],
    repo: 'https://github.com/anthropics/skills',
    author: 'anthropic',
    defaultLicense: 'Apache-2.0',
    licenseNotice: 'Licensed under the Apache License, Version 2.0. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0'
  },
  {
    id: 'mcp-ext-apps',
    name: 'modelcontextprotocol/ext-apps',
    dir: 'mcp-ext-apps',
    paths: ['plugins/mcp-apps/skills'],
    repo: 'https://github.com/modelcontextprotocol/ext-apps',
    author: 'modelcontextprotocol',
    defaultLicense: 'MIT',
    licenseNotice: 'Licensed under the Apache License, Version 2.0 (new contributions) / MIT License (prior contributions).'
  },
  {
    id: 'ui-ux-pro-max-skill',
    name: 'nextlevelbuilder/ui-ux-pro-max-skill',
    dir: 'ui-ux-pro-max-skill',
    paths: ['.claude/skills'],
    repo: 'https://github.com/nextlevelbuilder/ui-ux-pro-max-skill',
    author: 'nextlevelbuilder',
    defaultLicense: 'MIT',
    licenseNotice: 'MIT License\n\nCopyright (c) 2024 Next Level Builder\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.'
  },
  {
    id: 'azure-skills',
    name: 'microsoft/azure-skills',
    dir: 'azure-skills',
    paths: ['.github/plugins/azure-skills/skills'],
    repo: 'https://github.com/microsoft/azure-skills',
    author: 'microsoft',
    defaultLicense: 'MIT',
    licenseNotice: 'MIT License\n\nCopyright 2025 (c) Microsoft Corporation.\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.'
  },
  // Official vendor skill repositories. When licenseNotice is omitted, the
  // repository's root LICENSE file is used.
  {
    id: 'openai-skills',
    name: 'openai/skills',
    dir: 'openai-skills',
    // .system skills are Codex built-ins; only the curated catalog is published.
    paths: ['skills/.curated'],
    repo: 'https://github.com/openai/skills',
    author: 'openai',
    // No repository-wide license: each skill must ship its own LICENSE file.
    defaultLicense: null
  },
  {
    id: 'vercel-agent-skills',
    name: 'vercel-labs/agent-skills',
    dir: 'vercel-agent-skills',
    paths: ['skills'],
    repo: 'https://github.com/vercel-labs/agent-skills',
    author: 'vercel',
    defaultLicense: 'MIT',
    licenseNotice: 'MIT License (as declared in the vercel-labs/agent-skills README).'
  },
  {
    id: 'huggingface-skills',
    name: 'huggingface/skills',
    dir: 'huggingface-skills',
    paths: ['skills'],
    repo: 'https://github.com/huggingface/skills',
    author: 'huggingface',
    defaultLicense: 'Apache-2.0'
  },
  {
    id: 'cloudflare-skills',
    name: 'cloudflare/skills',
    dir: 'cloudflare-skills',
    paths: ['skills'],
    repo: 'https://github.com/cloudflare/skills',
    author: 'cloudflare',
    defaultLicense: 'Apache-2.0'
  },
  {
    id: 'sentry-skills',
    name: 'getsentry/skills',
    dir: 'sentry-skills',
    paths: ['skills'],
    repo: 'https://github.com/getsentry/skills',
    author: 'sentry',
    defaultLicense: 'Apache-2.0'
  },
  {
    id: 'expo-skills',
    name: 'expo/skills',
    dir: 'expo-skills',
    paths: ['plugins/expo/skills'],
    repo: 'https://github.com/expo/skills',
    author: 'expo',
    defaultLicense: 'MIT'
  },
  {
    id: 'dotnet-skills',
    name: 'dotnet/skills',
    dir: 'dotnet-skills',
    paths: ['plugins/*/skills'],
    exclude: ['plugins/dotnet-experimental/skills'],
    repo: 'https://github.com/dotnet/skills',
    author: 'dotnet',
    defaultLicense: 'MIT'
  },
  {
    id: 'firebase-agent-skills',
    name: 'firebase/agent-skills',
    dir: 'firebase-agent-skills',
    paths: ['skills'],
    repo: 'https://github.com/firebase/agent-skills',
    author: 'firebase',
    defaultLicense: 'Apache-2.0'
  },
  {
    id: 'docker-skills',
    name: 'docker/skills',
    dir: 'docker-skills',
    paths: ['skills'],
    repo: 'https://github.com/docker/skills',
    author: 'docker',
    defaultLicense: 'Apache-2.0'
  },
  {
    id: 'stripe-ai',
    name: 'stripe/ai',
    dir: 'stripe-ai',
    paths: ['skills'],
    repo: 'https://github.com/stripe/ai',
    author: 'stripe',
    defaultLicense: 'MIT'
  },
  {
    id: 'supabase-agent-skills',
    name: 'supabase/agent-skills',
    dir: 'supabase-agent-skills',
    paths: ['skills'],
    repo: 'https://github.com/supabase/agent-skills',
    author: 'supabase',
    defaultLicense: 'MIT'
  },
  {
    id: 'gemini-skills',
    name: 'google-gemini/gemini-skills',
    dir: 'gemini-skills',
    paths: ['skills'],
    repo: 'https://github.com/google-gemini/gemini-skills',
    author: 'google-gemini',
    defaultLicense: 'Apache-2.0'
  },
  {
    id: 'google-skills',
    name: 'google/skills',
    dir: 'google-skills',
    paths: ['skills/*'],
    repo: 'https://github.com/google/skills',
    author: 'google',
    defaultLicense: 'Apache-2.0'
  },
  {
    id: 'elastic-agent-skills',
    name: 'elastic/agent-skills',
    dir: 'elastic-agent-skills',
    paths: ['skills/*'],
    repo: 'https://github.com/elastic/agent-skills',
    author: 'elastic',
    defaultLicense: 'Apache-2.0'
  },
  {
    id: 'grafana-skills',
    name: 'grafana/skills',
    dir: 'grafana-skills',
    paths: ['skills/*'],
    repo: 'https://github.com/grafana/skills',
    author: 'grafana',
    defaultLicense: 'Apache-2.0'
  },
  {
    id: 'mongodb-agent-skills',
    name: 'mongodb/agent-skills',
    dir: 'mongodb-agent-skills',
    // plugins/* contain copies of the same skills
    paths: ['skills'],
    repo: 'https://github.com/mongodb/agent-skills',
    author: 'mongodb',
    defaultLicense: 'Apache-2.0'
  },
  {
    id: 'pulumi-agent-skills',
    name: 'pulumi/agent-skills',
    dir: 'pulumi-agent-skills',
    paths: ['pulumi/skills', 'migration/skills', 'package-maintenance/skills', 'delegation/skills'],
    repo: 'https://github.com/pulumi/agent-skills',
    author: 'pulumi',
    defaultLicense: 'Apache-2.0'
  },
  {
    id: 'neon-agent-skills',
    name: 'neondatabase/agent-skills',
    dir: 'neon-agent-skills',
    // plugins/* contain copies of the same skills
    paths: ['skills'],
    repo: 'https://github.com/neondatabase/agent-skills',
    author: 'neon',
    defaultLicense: 'Apache-2.0'
  },
  {
    id: 'callstack-agent-skills',
    name: 'callstackincubator/agent-skills',
    dir: 'callstack-agent-skills',
    paths: ['skills'],
    repo: 'https://github.com/callstackincubator/agent-skills',
    author: 'callstack',
    defaultLicense: 'MIT'
  }
];

/**
 * Expand a source's path patterns ("*" matches one non-hidden directory level)
 * into repo-relative directories that contain skill folders.
 */
function resolveSourcePaths(source) {
  const root = path.join(SOURCES_DIR, source.dir);
  const expand = (pattern) => {
    let current = [''];
    for (const segment of pattern.split('/')) {
      const next = [];
      for (const rel of current) {
        if (segment !== '*') {
          next.push(rel ? `${rel}/${segment}` : segment);
          continue;
        }
        const abs = path.join(root, rel);
        if (!fs.existsSync(abs)) continue;
        for (const d of fs.readdirSync(abs, { withFileTypes: true })) {
          if (d.isDirectory() && !d.name.startsWith('.')) {
            next.push(rel ? `${rel}/${d.name}` : d.name);
          }
        }
      }
      current = next;
    }
    return current;
  };
  return source.paths.flatMap(expand)
    .filter(rel => !(source.exclude || []).includes(rel))
    .filter(rel => fs.existsSync(path.join(root, rel)))
    .sort();
}

/**
 * Read a source repository's root LICENSE file, if present
 */
function readRepoLicense(source) {
  const root = path.join(SOURCES_DIR, source.dir);
  if (!fs.existsSync(root)) return null;
  const file = fs.readdirSync(root).find(n => LICENSE_FILE_PATTERN.test(n));
  if (!file) return null;
  const text = fs.readFileSync(path.join(root, file), 'utf-8');
  // The Apache-2.0 text is ~11KB; link to it rather than embedding it in every skill.
  if (detectLicense(text) === 'Apache-2.0') {
    return `Licensed under the Apache License, Version 2.0. See ${source.repo}/blob/${source.branch || 'main'}/${file}`;
  }
  return text;
}

// Category keywords for auto-categorization
const CATEGORY_KEYWORDS = {
  'git-version-control': ['git', 'commit', 'branch', 'github', 'version control', 'gh-cli', 'contribution'],
  'code-quality': ['refactor', 'lint', 'quality', 'review', 'clean code', 'vscode-ext'],
  'documentation': ['doc', 'readme', 'prd', 'requirements', 'markdown', 'meeting', 'internal-comms', 'microsoft-docs', 'microsoft-code-reference'],
  'diagrams': ['diagram', 'excalidraw', 'plantuml', 'mermaid', 'visualization', 'circuit', 'azure-resource-visualizer'],
  'testing': ['test', 'e2e', 'unit test', 'qa', 'playwright', 'scoutqa', 'chrome-devtools', 'webapp-testing'],
  'api-backend': ['api', 'rest', 'graphql', 'backend', 'sdk', 'nuget'],
  'frontend-ui': ['frontend', 'ui', 'react', 'css', 'design', 'canvas', 'image', 'penpot', 'brand', 'theme', 'slack-gif', 'web-artifacts', 'algorithmic-art'],
  'devops-cicd': ['deploy', 'ci', 'cd', 'docker', 'kubernetes', 'terraform', 'azure', 'appinsights', 'winapp'],
  'security': ['security', 'auth', 'rbac', 'role', 'permission'],
  'data-analytics': ['data', 'analytics', 'sql', 'powerbi', 'snowflake', 'workiq'],
  'office-documents': ['docx', 'xlsx', 'pptx', 'pdf', 'word', 'excel', 'powerpoint'],
  'mcp-development': ['mcp', 'model context protocol', 'skill-creator', 'make-skill']
};

/**
 * Determine category based on skill name and description
 */
function determineCategory(skillName, description = '') {
  const text = `${skillName} ${description}`.toLowerCase();
  
  for (const [category, keywords] of Object.entries(CATEGORY_KEYWORDS)) {
    for (const keyword of keywords) {
      if (text.includes(keyword.toLowerCase())) {
        return category;
      }
    }
  }
  return 'code-quality'; // default
}

// Binary extensions to skip when collecting skill files
const BINARY_EXTENSIONS = new Set([
  '.ttf', '.otf', '.woff', '.woff2', '.eot',
  '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.webp',
  '.zip', '.tar', '.gz', '.bz2',
  '.pdf', '.doc', '.docx',
  '.exe', '.dll', '.so', '.dylib',
  '.pyc', '.pyo', '.class',
  '.db', '.sqlite', '.coverage',
]);

/**
 * Recursively get all files in a directory
 */
function getFilesRecursive(dir, relativeTo = dir) {
  const files = [];
  
  if (!fs.existsSync(dir)) return files;
  
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    const relativePath = path.relative(relativeTo, fullPath).replace(/\\/g, '/');
    
    // Resolve symlinks to determine actual type
    const stat = fs.statSync(fullPath, { throwIfNoEntry: false });
    if (!stat) continue;
    
    if (stat.isDirectory()) {
      // Skip __pycache__ and other common ignore patterns
      if (entry.name.startsWith('__') || entry.name.startsWith('.')) continue;
      files.push(...getFilesRecursive(fullPath, relativeTo));
    } else {
      // Skip hidden files
      if (entry.name.startsWith('.')) continue;
      // Skip binary files
      if (BINARY_EXTENSIONS.has(path.extname(entry.name).toLowerCase())) continue;
      
      const content = fs.readFileSync(fullPath, 'utf-8');
      files.push({
        path: relativePath,
        name: entry.name,
        content: content
      });
    }
  }
  
  return files;
}

/**
 * Parse SKILL.md frontmatter and content
 */
function parseSkillFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter(content);
  
  return {
    frontmatter,
    content: body.trim(),
    raw: content
  };
}

/**
 * Extract description from markdown content
 */
function extractDescription(content) {
  // Remove frontmatter block if present (in case gray-matter missed it)
  const withoutFrontmatter = content.replace(/^---[\s\S]*?---\n*/m, '');
  
  // Get first paragraph
  const lines = withoutFrontmatter.split('\n');
  const descLines = [];
  
  for (const line of lines) {
    // Skip headers
    if (line.startsWith('#')) continue;
    // Skip empty lines at start
    if (descLines.length === 0 && line.trim() === '') continue;
    // Stop at next empty line or header after we have content
    if (descLines.length > 0 && (line.trim() === '' || line.startsWith('#'))) break;
    descLines.push(line.trim());
  }
  
  return descLines.join(' ').slice(0, 300);
}

/**
 * Detect actual license from a LICENSE file's content
 */
function detectLicense(licenseContent) {
  if (!licenseContent) return null;
  
  // Check for restrictive/proprietary licenses first
  const isRestricted = RESTRICTED_LICENSE_MARKERS.some(marker => 
    licenseContent.includes(marker)
  );
  if (isRestricted) return 'Proprietary';
  
  // Detect known open source licenses
  if (/Apache License,?\s+(Version\s+)?2\.0/i.test(licenseContent)) return 'Apache-2.0';
  if (licenseContent.includes('MIT License') || licenseContent.includes('Permission is hereby granted, free of charge')) return 'MIT';
  if (licenseContent.includes('BSD')) return 'BSD';
  
  return null;
}

/**
 * Check if a license permits redistribution
 */
function isRedistributable(license) {
  const allowed = ['MIT', 'Apache-2.0', 'BSD', 'ISC', 'CC-BY-4.0'];
  return allowed.includes(license);
}

/**
 * Process a single skill folder
 */
function processSkill(skillPath, skillName, source, repoPath) {
  const skillMdPath = path.join(skillPath, 'SKILL.md');
  
  if (!fs.existsSync(skillMdPath)) {
    console.warn(`  Skipping ${skillName}: No SKILL.md found`);
    return null;
  }
  
  const { frontmatter, content } = parseSkillFile(skillMdPath);
  
  // Get all files in the skill folder
  const files = getFilesRecursive(skillPath);
  
  // Detect license from a LICENSE file in the skill folder. A license file
  // with unrecognized terms overrides the source default and is excluded.
  const licenseFile = files.find(f => !f.path.includes('/') && LICENSE_FILE_PATTERN.test(f.name))
    || files.find(f => LICENSE_FILE_PATTERN.test(f.name));
  const detectedLicense = licenseFile ? (detectLicense(licenseFile.content) || 'Unknown') : null;
  const license = detectedLicense || source.defaultLicense || 'Unknown';
  
  // Skip skills with non-redistributable licenses
  if (!isRedistributable(license)) {
    console.warn(`  ⛔ Skipping ${skillName}: License "${license}" does not permit redistribution`);
    return null;
  }
  
  // Build license notice from the skill's LICENSE file or fall back to source default
  const licenseNotice = licenseFile ? licenseFile.content : (source.licenseNotice || source.repoLicense || '');
  
  // Build skill object
  const skill = {
    id: skillName,
    name: frontmatter.name || skillName,
    description: frontmatter.description || extractDescription(content),
    shortDescription: (frontmatter.description || extractDescription(content)).slice(0, 100),
    category: determineCategory(skillName, frontmatter.description || content),
    author: source.author,
    license,
    licenseNotice,
    source: {
      repo: source.repo,
      repoName: source.name,
      path: repoPath,
      branch: source.branch || 'main'
    },
    // Files for copy-to-clipboard
    files: files.map(f => ({
      path: f.path,
      name: f.name,
      content: f.content
    })),
    // Tags from frontmatter or auto-generated
    tags: frontmatter.tags || generateTags(skillName, frontmatter.description || content),
    // Metadata
    featured: frontmatter.featured || false,
    complexity: frontmatter.complexity || 'intermediate',
    platforms: frontmatter.platforms || ['windows', 'macos', 'linux']
  };
  
  return skill;
}

/**
 * Generate tags from skill name and description
 */
function generateTags(name, description) {
  const tags = new Set();
  const text = `${name} ${description}`.toLowerCase();
  
  const tagKeywords = [
    'git', 'azure', 'api', 'cli', 'test', 'deploy', 'doc', 'diagram',
    'mcp', 'python', 'typescript', 'react', 'design', 'security',
    'data', 'analytics', 'office', 'pdf', 'excel', 'word', 'powerpoint'
  ];
  
  for (const keyword of tagKeywords) {
    if (text.includes(keyword)) {
      tags.add(keyword);
    }
  }
  
  // Add name parts as tags
  const nameParts = name.split('-').filter(p => p.length > 2);
  nameParts.forEach(p => tags.add(p));
  
  return Array.from(tags).slice(0, 5);
}

/**
 * Main aggregation function
 */
async function aggregate() {
  console.log('🔍 Aggregating skills from source repositories...\n');
  
  const skills = [];
  const categories = new Map();
  
  const usedIds = new Set();
  
  for (const source of SOURCES) {
    console.log(`📦 Processing ${source.name}...`);
    
    const sourcePaths = resolveSourcePaths(source);
    if (sourcePaths.length === 0) {
      console.warn(`  ⚠️ No skill paths found in sources/${source.dir} (${source.paths.join(', ')})`);
      continue;
    }
    source.repoLicense = readRepoLicense(source);
    
    const skillFolders = sourcePaths.flatMap(rel =>
      fs.readdirSync(path.join(SOURCES_DIR, source.dir, rel), { withFileTypes: true })
        .filter(d => d.isDirectory() && !d.name.startsWith('.'))
        .map(d => ({ name: d.name, repoPath: `${rel}/${d.name}` }))
    );
    
    console.log(`  Found ${skillFolders.length} skill folders`);
    
    for (const { name: skillName, repoPath } of skillFolders) {
      const skillPath = path.join(SOURCES_DIR, source.dir, repoPath);
      try {
        const skill = processSkill(skillPath, skillName, source, repoPath);
      
        if (skill) {
          // Skill IDs drive page URLs and CLI installs, so they must be unique.
          // Earlier sources keep the bare name; later ones get a prefix.
          if (usedIds.has(skill.id)) {
            const prefixed = `${source.author}-${skill.id}`;
            skill.id = usedIds.has(prefixed) ? `${source.id}-${skill.id}` : prefixed;
          }
          if (usedIds.has(skill.id)) {
            console.warn(`  ⚠️ Skipping ${repoPath}: duplicate skill id "${skill.id}"`);
            continue;
          }
          usedIds.add(skill.id);
          skills.push(skill);
        
          // Track category
          if (!categories.has(skill.category)) {
            categories.set(skill.category, 0);
          }
          categories.set(skill.category, categories.get(skill.category) + 1);
        
          console.log(`  ✅ ${skillName} (${skill.files.length} files)`);
        }
      } catch (err) {
        console.warn(`  ⚠️ Skipping ${skillName}: ${err.message}`);
      }
    }
    
    console.log('');
  }
  
  // Build output
  const output = {
    version: '2.0.0',
    lastUpdated: new Date().toISOString(),
    totalSkills: skills.length,
    categories: Array.from(categories.entries()).map(([id, count]) => ({
      id,
      count
    })),
    skills
  };
  
  // Ensure output directory exists
  const outputDir = path.dirname(OUTPUT_FILE);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  // Write output
  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(output, null, 2));
  
  console.log('📊 Summary:');
  console.log(`  Total skills: ${skills.length}`);
  console.log(`  Categories: ${categories.size}`);
  console.log(`  Output: ${OUTPUT_FILE}`);
  console.log('\n✅ Aggregation complete!');
}

aggregate().catch(console.error);
