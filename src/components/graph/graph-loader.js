/**
 * Browser-only graph loader. Loads force-graph from CDN to avoid SSR issues
 * (the library references `window` at import time which breaks Astro/Vite SSR).
 */

const CDN_URL = 'https://cdn.jsdelivr.net/npm/force-graph@1.49.0/dist/force-graph.min.js';

let ForceGraphModule = null;

async function loadForceGraph() {
  if (ForceGraphModule) return ForceGraphModule;
  return new Promise((resolve, reject) => {
    // Check if already loaded via script tag
    if (typeof window !== 'undefined' && window.ForceGraph) {
      ForceGraphModule = window.ForceGraph;
      resolve(ForceGraphModule);
      return;
    }
    const script = document.createElement('script');
    script.src = CDN_URL;
    script.onload = () => {
      ForceGraphModule = window.ForceGraph;
      resolve(ForceGraphModule);
    };
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

export async function mountGraph(container) {
  try {
    const ForceGraph = await loadForceGraph();
    const data = JSON.parse(container.dataset.graph || '{}');

    if (!data.nodes || data.nodes.length === 0) return;

    const width = container.clientWidth;
    const height = Math.min(600, Math.max(300, data.nodes.length * 15 + 200));

    container.innerHTML = '';
    const elem = document.createElement('div');
    container.appendChild(elem);

    const isDark = document.documentElement.dataset.theme === 'dark';

    const graph = ForceGraph()(elem)
      .graphData(data)
      .width(width)
      .height(height)
      .backgroundColor(isDark ? '#1d1e20' : '#ffffff')
      .nodeLabel((node) => `${node.name}\n${node.backlinks} backlink${node.backlinks !== 1 ? 's' : ''}`)
      .nodeVal((node) => node.val)
      .nodeColor((node) => node.color || '#999')
      .nodeCanvasObjectMode(() => 'after')
      .nodeCanvasObject((node, ctx, globalScale) => {
        const label = node.name;
        const fontSize = Math.max(6, 12 / globalScale);
        ctx.font = `${fontSize}px -apple-system, BlinkMacSystemFont, sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = isDark ? '#dadadb' : '#1e1e1e';
        const displayLabel = label.length > 24 ? label.slice(0, 22) + '...' : label;
        ctx.fillText(displayLabel, node.x, node.y + 10 / globalScale);
      })
      .linkColor(() => 'rgba(150, 150, 150, 0.2)')
      .linkWidth(0.5)
      .linkDirectionalParticles(1)
      .linkDirectionalParticleWidth(1)
      .linkDirectionalParticleSpeed(0.004)
      .onNodeClick((node) => {
        if (node.url) window.location.href = node.url;
      })
      .onNodeHover((node) => {
        if (node) {
          const neighbors = new Set();
          data.links.forEach((link) => {
            const s = typeof link.source === 'object' ? link.source.id : link.source;
            const t = typeof link.target === 'object' ? link.target.id : link.target;
            if (s === node.id) neighbors.add(t);
            if (t === node.id) neighbors.add(s);
          });
          graph
            .linkColor((link) => {
              const s = typeof link.source === 'object' ? link.source.id : link.source;
              const t = typeof link.target === 'object' ? link.target.id : link.target;
              return s === node.id || t === node.id
                ? 'rgba(255, 160, 0, 0.8)'
                : 'rgba(150, 150, 150, 0.2)';
            })
            .linkWidth((link) => {
              const s = typeof link.source === 'object' ? link.source.id : link.source;
              const t = typeof link.target === 'object' ? link.target.id : link.target;
              return s === node.id || t === node.id ? 2 : 0.5;
            });
        } else {
          graph.linkColor(() => 'rgba(150, 150, 150, 0.2)').linkWidth(0.5);
        }
      })
      .onNodeDragEnd((node) => {
        node.fx = node.x;
        node.fy = node.y;
      })
      .enableNodeDrag(true)
      .enableZoomInteraction(true)
      .enablePanInteraction(true);

    // Configure forces
    graph.d3Force('charge').strength(-120);
    graph.d3Force('link').distance(60);

    // Reheat simulation after a short delay for proper layout
    setTimeout(() => {
      try { graph.d3ReheatSimulation(); } catch (e) { /* ok */ }
    }, 200);

    // Handle theme changes
    const observer = new MutationObserver(() => {
      const dark = document.documentElement.dataset.theme === 'dark';
      graph.backgroundColor(dark ? '#1d1e20' : '#ffffff');
    });
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  } catch (err) {
    console.error('Failed to load graph:', err);
    container.innerHTML =
      '<p style="padding: 2rem; text-align: center; color: var(--secondary);">Failed to load graph visualization. Is your network connected?</p>';
  }
}
