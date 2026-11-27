import fs from 'node:fs';
import path from 'node:path';

export const MARKETPLACE_NAME = 'skills-hub';
export const MARKETPLACE_REPO = 'samueltauil/skills-hub';

interface MarketplaceEntry {
  name: string;
  version?: string;
  source: string;
}

let cache: Map<string, MarketplaceEntry> | null = null;

/**
 * Plugins published in the repository marketplace (.github/plugin/marketplace.json),
 * keyed by plugin name. Read at build time from the repository root.
 */
export function getMarketplacePlugins(): Map<string, MarketplaceEntry> {
  if (cache) return cache;
  cache = new Map();
  const candidates = [
    path.resolve(process.cwd(), '../.github/plugin/marketplace.json'),
    path.resolve(process.cwd(), '.github/plugin/marketplace.json'),
  ];
  for (const file of candidates) {
    if (!fs.existsSync(file)) continue;
    try {
      const marketplace = JSON.parse(fs.readFileSync(file, 'utf8'));
      for (const entry of marketplace.plugins || []) cache.set(entry.name, entry);
    } catch (err) {
      console.warn(`Could not read ${file}: ${(err as Error).message}`);
    }
    break;
  }
  return cache;
}

export function vscodeInstallLink(pluginName: string): string {
  const inner = `vscode://chat-plugin/install?source=${encodeURIComponent(MARKETPLACE_REPO)}&plugin=${encodeURIComponent(pluginName)}`;
  return `https://vscode.dev/redirect?url=${encodeURIComponent(inner)}`;
}
