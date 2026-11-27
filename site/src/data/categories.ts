export interface CategoryInfo {
  name: string;
  icon: string;
  description: string;
}

export const categoryMeta: Record<string, CategoryInfo> = {
  'git-version-control': { name: 'Git & Version Control', icon: '🔀', description: 'Skills for Git operations, branching, merging, and version control workflows' },
  'code-quality': { name: 'Code Quality & Refactoring', icon: '✨', description: 'Skills for improving code quality, refactoring, and following best practices' },
  'documentation': { name: 'Documentation', icon: '📝', description: 'Skills for generating and maintaining documentation' },
  'diagrams': { name: 'Diagrams & Visualization', icon: '📊', description: 'Skills for creating diagrams, flowcharts, and visual representations' },
  'testing': { name: 'Testing', icon: '🧪', description: 'Skills for writing and managing tests' },
  'api-backend': { name: 'API & Backend', icon: '🔌', description: 'Skills for API development and backend services' },
  'frontend-ui': { name: 'Frontend & UI', icon: '🎨', description: 'Skills for frontend development and UI components' },
  'devops-cicd': { name: 'DevOps & CI/CD', icon: '🚀', description: 'Skills for deployment, CI/CD pipelines, and DevOps workflows' },
  'security': { name: 'Security', icon: '🔒', description: 'Skills for security analysis and best practices' },
  'data-analytics': { name: 'Data & Analytics', icon: '📈', description: 'Skills for data processing and analytics' },
  'office-documents': { name: 'Office Documents', icon: '📄', description: 'Skills for working with office documents and formats' },
  'mcp-development': { name: 'MCP Development', icon: '🔧', description: 'Skills for Model Context Protocol development' },
  'general': { name: 'General', icon: '📦', description: 'General-purpose development skills' },
};

export function getCategory(id: string | undefined): CategoryInfo & { id: string } {
  const key = id || 'general';
  return { id: key, ...(categoryMeta[key] || { name: key, icon: '📁', description: '' }) };
}
