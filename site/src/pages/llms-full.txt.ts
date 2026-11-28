import type { APIRoute } from 'astro';
import skillsData from '../data/skills.json';
import { categoryMeta } from '../data/categories';
import { renderLlms } from '../data/seo-discovery.js';

export const prerender = true;

export const GET: APIRoute = ({ site }) => new Response(renderLlms(site, skillsData.skills, categoryMeta, true), {
  headers: { 'Content-Type': 'text/plain; charset=utf-8' },
});
