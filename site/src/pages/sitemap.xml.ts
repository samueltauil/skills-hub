import type { APIRoute } from 'astro';
import skillsData from '../data/skills.json';
import { renderSitemap } from '../data/seo-discovery.js';

export const prerender = true;

export const GET: APIRoute = ({ site }) => new Response(renderSitemap(site, skillsData.skills), {
  headers: { 'Content-Type': 'application/xml; charset=utf-8' },
});
