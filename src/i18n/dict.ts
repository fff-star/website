export type Locale = 'zh' | 'en';

export const defaultLocale: Locale = 'zh';

export type TranslationKey = keyof typeof dict.zh;

export const dict = {
  zh: {
    // Navigation
    'nav.notes': '笔记',
    'nav.blog': '博客',
    'nav.tags': '标签',
    'nav.search': '搜索',

    // Header
    'header.theme_toggle': '切换暗色模式',

    // Footer
    'footer.built_with': '由',
    'footer.rss': 'RSS',

    // Search
    'search.placeholder': '搜索...',
    'search.title': '搜索',

    // Tags
    'tags.title': '标签',
    'tags.no_tags': '暂无标签',
    'tags.count': '{count} 篇文章',
    'tags.back': '← 所有标签',
    'tags.no_posts': '此标签下暂无文章',

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

    // Homepage
    'home.recent_writing': '近期文章',
    'home.all_posts': '所有文章 →',
    'home.note_vaults': '笔记库',
    'home.all_notes': '所有笔记 →',
    'home.no_posts': '暂无文章。',

    // Post
    'post.toc': '目录',
    'post.updated': '更新于',
    'post.tags_no': '暂无标签',

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
    'nav.tags': 'Tags',
    'nav.search': 'Search',

    'header.theme_toggle': 'Toggle dark mode',

    'footer.built_with': 'Built with',
    'footer.rss': 'RSS',

    'search.placeholder': 'Search...',
    'search.title': 'Search',

    'tags.title': 'Tags',
    'tags.no_tags': 'No tags yet',
    'tags.count': '{count} post{count, plural, one {} other {s}}',
    'tags.back': '← All tags',
    'tags.no_posts': 'No posts with this tag',

    'blog.title': 'Blog',
    'blog.no_posts': 'No posts yet',

    'notes.title': 'Notes',
    'notes.no_notes': 'No notes published yet',
    'notes.count': '{count} note{count, plural, one {} other {s}}',
    'notes.graph': 'Graph →',
    'notes.no_index': 'No index.md in this folder.',
    'notes.breadcrumb': 'Notes',

    'home.recent_writing': 'Recent Writing',
    'home.all_posts': 'All posts →',
    'home.note_vaults': 'Note Vaults',
    'home.all_notes': 'All notes →',
    'home.no_posts': 'No posts yet.',

    'post.toc': 'On this page',
    'post.updated': 'Updated',
    'post.tags_no': 'No tags',

    'graph.title': 'Knowledge Graph',
    'graph.description':
      'Each folder is a self-contained knowledge domain. Nodes = notes, lines = wiki-links within the folder. Drag to rearrange, scroll to zoom, click to navigate.',
    'graph.no_connections':
      'No connections in this folder yet. Add [[wiki-links]] between notes.',
    'graph.folder_stats': '{folder}/ · {nodes} notes · {links} connections',
  },
} as const;
