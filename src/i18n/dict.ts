import type { Locale } from '../content.config';
import { defaultLocale } from '../content.config';

export type { Locale };
export { defaultLocale };
export type TranslationKey = keyof typeof dict.zh;

export const dict = {
  zh: {
    // Navigation
    'nav.notes': '笔记',
    'nav.blog': '博客',
    'nav.docs': '文档',
    'nav.search': '搜索',

    // Header
    'header.theme_toggle': '切换暗色模式',

    // Footer
    'footer.built_with': '由',

    // Search
    'search.label': '搜索站点',
    'search.placeholder': '搜索...',
    'search.title': '搜索',
    'search.no_results': '未找到结果。',
    'search.unavailable': '搜索不可用。',

    // Docs
    'docs.title': '文档',
    'docs.no_posts': '暂无文档',

    // Blog
    'blog.title': '博客',
    'blog.no_posts': '暂无文章',

    // Notes
    'notes.title': '笔记',
    'notes.no_notes': '暂无笔记',
    'notes.count': '{count} 条笔记',
    'notes.graph': '知识图谱 →',
    'notes.no_index': '此文件夹没有 index.md。',
    'notes.breadcrumb': '笔记',
    'notes.backlinks': '引用链接',
    'notes.backlinks_count': '{count} 篇笔记引用了此页面',
    'notes.no_description': '暂无描述',

    // Homepage
    'home.recent_writing': '近期文章',
    'home.all_posts': '所有文章 →',
    'home.note_vaults': '笔记库',
    'home.all_notes': '所有笔记 →',
    'home.no_posts': '暂无文章。',

    // Post
    'post.toc': '目录',
    'post.updated': '更新于',
    'post.previous': '上一篇',
    'post.next': '下一篇',

    // Graph
    'graph.title': '知识图谱',
    'graph.description':
      '每个文件夹是一个独立的知识领域。节点 = 笔记，连线 = wiki 链接。拖动重排，滚轮缩放，点击跳转。',
    'graph.no_connections': '此文件夹暂无连接。添加 [[wiki 链接]] 来关联笔记。',
    'graph.folder_stats': '{folder}/ · {nodes} 条笔记 · {links} 条连接',
  },

  en: {
    'nav.notes': 'Notes',
    'nav.blog': 'Blog',
    'nav.docs': 'Docs',
    'nav.search': 'Search',

    'header.theme_toggle': 'Toggle dark mode',

    'footer.built_with': 'Built with',

    'search.label': 'Search the site',
    'search.placeholder': 'Search...',
    'search.title': 'Search',
    'search.no_results': 'No results found.',
    'search.unavailable': 'Search unavailable.',

    // Docs
    'docs.title': 'Docs',
    'docs.no_posts': 'No docs yet',

    'blog.title': 'Blog',
    'blog.no_posts': 'No posts yet',

    'notes.title': 'Notes',
    'notes.no_notes': 'No notes published yet',
    'notes.count': '{count} notes',
    'notes.graph': 'Graph →',
    'notes.no_index': 'No index.md in this folder.',
    'notes.backlinks': 'Linked References',
    'notes.backlinks_count': '{count} notes link here',
    'notes.no_description': 'No description',
    'notes.breadcrumb': 'Notes',

    'home.recent_writing': 'Recent Writing',
    'home.all_posts': 'All posts →',
    'home.note_vaults': 'Note Vaults',
    'home.all_notes': 'All notes →',
    'home.no_posts': 'No posts yet.',

    'post.toc': 'On this page',
    'post.updated': 'Updated',
    'post.previous': 'Previous',
    'post.next': 'Next',

    'graph.title': 'Knowledge Graph',
    'graph.description':
      'Each folder is a self-contained knowledge domain. Nodes = notes, lines = wiki-links within the folder. Drag to rearrange, scroll to zoom, click to navigate.',
    'graph.no_connections':
      'No connections in this folder yet. Add [[wiki-links]] between notes.',
    'graph.folder_stats': '{folder}/ · {nodes} notes · {links} connections',
  },
} as const;
