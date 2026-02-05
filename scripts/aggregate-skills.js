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

// Source repositories configuration
const SOURCES = [
  {
    id: 'awesome-copilot',
    name: 'github/awesome-copilot',
    path: path.join(SOURCES_DIR, 'awesome-copilot', 'skills'),
    repo: 'https://github.com/github/awesome-copilot',
    author: 'github',
    defaultLicense: 'MIT'
  },
  {
    id: 'anthropics-skills',
    name: 'anthropics/skills',
    path: path.join(SOURCES_DIR, 'anthropics-skills', 'skills'),
    repo: 'https://github.com/anthropics/skills',
    author: 'anthropic',
    defaultLicense: 'Proprietary'
  },
  {
    id: 'mcp-ext-apps',
    name: 'modelcontextprotocol/ext-apps',
    path: path.join(SOURCES_DIR, 'mcp-ext-apps', 'plugins', 'mcp-apps', 'skills'),
    repo: 'https://github.com/modelcontextprotocol/ext-apps',
    author: 'modelcontextprotocol',
    defaultLicense: 'MIT'
  }
];

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
    
    if (entry.isDirectory()) {
      // Skip __pycache__ and other common ignore patterns
      if (entry.name.startsWith('__') || entry.name.startsWith('.')) continue;
      files.push(...getFilesRecursive(fullPath, relativeTo));
    } else {
      // Skip hidden files
      if (entry.name.startsWith('.')) continue;
      
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
 * Process a single skill folder
 */
function processSkill(skillPath, skillName, source) {
  const skillMdPath = path.join(skillPath, 'SKILL.md');
  
  if (!fs.existsSync(skillMdPath)) {
    console.warn(`  Skipping ${skillName}: No SKILL.md found`);
    return null;
  }
  
  const { frontmatter, content, raw } = parseSkillFile(skillMdPath);
  
  // Get all files in the skill folder
  const files = getFilesRecursive(skillPath);
  
  // Check for LICENSE file
  const licenseFile = files.find(f => f.name.toLowerCase().includes('license'));
  const license = licenseFile ? 
    (licenseFile.content.includes('MIT') ? 'MIT' : source.defaultLicense) : 
    source.defaultLicense;
  
  // Build skill object
  const skill = {
    id: skillName,
    name: frontmatter.name || skillName,
    description: frontmatter.description || extractDescription(content),
    shortDescription: (frontmatter.description || extractDescription(content)).slice(0, 100),
    category: determineCategory(skillName, frontmatter.description || content),
    author: source.author,
    license,
    source: {
      repo: source.repo,
      repoName: source.name,
      path: `skills/${skillName}`,
      branch: 'main'
    },
    // Files for copy-to-clipboard
    files: files.map(f => ({
      path: f.path,
      name: f.name,
      content: f.content
    })),
    // Raw SKILL.md content for display
    skillMdContent: raw,
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
  
  for (const source of SOURCES) {
    console.log(`📦 Processing ${source.name}...`);
    
    if (!fs.existsSync(source.path)) {
      console.warn(`  ⚠️ Source path not found: ${source.path}`);
      continue;
    }
    
    const skillFolders = fs.readdirSync(source.path, { withFileTypes: true })
      .filter(d => d.isDirectory())
      .map(d => d.name);
    
    console.log(`  Found ${skillFolders.length} skill folders`);
    
    for (const skillName of skillFolders) {
      const skillPath = path.join(source.path, skillName);
      const skill = processSkill(skillPath, skillName, source);
      
      if (skill) {
        skills.push(skill);
        
        // Track category
        if (!categories.has(skill.category)) {
          categories.set(skill.category, 0);
        }
        categories.set(skill.category, categories.get(skill.category) + 1);
        
        console.log(`  ✅ ${skillName} (${skill.files.length} files)`);
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
