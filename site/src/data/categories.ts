export interface CategoryInfo {
  name: string;
  description: string;
}

export const categoryMeta: Record<string, CategoryInfo> = {
  'git-version-control': { name: 'Git & Version Control', description: 'Skills for Git operations, branching, merging, and version control workflows' },
  'code-quality': { name: 'Code Quality & Refactoring', description: 'Skills for improving code quality, refactoring, and following best practices' },
  'documentation': { name: 'Documentation', description: 'Skills for generating and maintaining documentation' },
  'diagrams': { name: 'Diagrams & Visualization', description: 'Skills for creating diagrams, flowcharts, and visual representations' },
  'testing': { name: 'Testing', description: 'Skills for writing and managing tests' },
  'api-backend': { name: 'API & Backend', description: 'Skills for API development and backend services' },
  'frontend-ui': { name: 'Frontend & UI', description: 'Skills for frontend development and UI components' },
  'devops-cicd': { name: 'DevOps & CI/CD', description: 'Skills for deployment, CI/CD pipelines, and DevOps workflows' },
  'security': { name: 'Security', description: 'Skills for security analysis and best practices' },
  'data-analytics': { name: 'Data & Analytics', description: 'Skills for data processing and analytics' },
  'office-documents': { name: 'Office Documents', description: 'Skills for working with office documents and formats' },
  'mcp-development': { name: 'MCP Development', description: 'Skills for Model Context Protocol development' },
  'general': { name: 'General', description: 'General-purpose development skills' },
};

export function getCategory(id: string | undefined): CategoryInfo & { id: string } {
  const key = id || 'general';
  return { id: key, ...(categoryMeta[key] || { name: key, description: '' }) };
}
