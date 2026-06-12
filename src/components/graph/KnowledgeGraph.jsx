import { useCallback, useRef, useEffect, useState } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

/**
 * Knowledge graph visualization using react-force-graph-2d.
 *
 * Features:
 * - Force-directed layout with D3-force
 * - Node size proportional to backlink count
 * - Tag-based node coloring
 * - Click to navigate to note
 * - Hover to highlight neighbors
 * - Zoom and pan
 */
export default function KnowledgeGraph({
  data,
  width,
  height,
  onNodeClick,
}) {
  const fgRef = useRef();
  const [dimensions, setDimensions] = useState({
    width: width || 800,
    height: height || 600,
  });

  // Responsive sizing
  useEffect(() => {
    if (!width || !height) {
      const handleResize = () => {
        const container = document.querySelector('.graph-container');
        if (container) {
          setDimensions({
            width: container.clientWidth,
            height: height || Math.min(window.innerHeight * 0.7, 600),
          });
        }
      };
      handleResize();
      window.addEventListener('resize', handleResize);
      return () => window.removeEventListener('resize', handleResize);
    }
  }, [width, height]);

  const handleNodeClick = useCallback(
    (node) => {
      if (onNodeClick) {
        onNodeClick(node);
      } else if (node.url) {
        window.location.href = node.url;
      }
    },
    [onNodeClick],
  );

  const handleNodeHover = useCallback(
    (node) => {
      if (!fgRef.current) return;
      // Highlight connected links on hover
      const graph = fgRef.current;
      if (node) {
        const neighbors = new Set();
        graph.graphData().links.forEach((link) => {
          const sourceId =
            typeof link.source === 'object' ? link.source.id : link.source;
          const targetId =
            typeof link.target === 'object' ? link.target.id : link.target;
          if (sourceId === node.id) neighbors.add(targetId);
          if (targetId === node.id) neighbors.add(sourceId);
        });

        graph
          .linkColor((link) => {
            const sourceId =
              typeof link.source === 'object' ? link.source.id : link.source;
            const targetId =
              typeof link.target === 'object' ? link.target.id : link.target;
            return sourceId === node.id || targetId === node.id
              ? 'rgba(255, 160, 0, 0.8)'
              : 'rgba(150, 150, 150, 0.2)';
          })
          .linkWidth((link) => {
            const sourceId =
              typeof link.source === 'object' ? link.source.id : link.source;
            const targetId =
              typeof link.target === 'object' ? link.target.id : link.target;
            return sourceId === node.id || targetId === node.id ? 2 : 0.5;
          });
      } else {
        graph
          .linkColor(() => 'rgba(150, 150, 150, 0.2)')
          .linkWidth(() => 0.5);
      }
    },
    [],
  );

  if (!data || !data.nodes || data.nodes.length === 0) {
    return (
      <div
        style={{
          padding: '2rem',
          textAlign: 'center',
          color: 'var(--secondary)',
        }}
      >
        No graph data available. Add some notes with wiki-links to see the graph.
      </div>
    );
  }

  return (
    <ForceGraph2D
      ref={fgRef}
      graphData={data}
      width={dimensions.width}
      height={dimensions.height}
      nodeLabel={(node) =>
        `${node.name}\n${node.backlinks} backlink${node.backlinks !== 1 ? 's' : ''}`
      }
      nodeVal={(node) => node.val}
      nodeColor={(node) => node.color || '#999'}
      nodeCanvasObjectMode={() => 'after'}
      nodeCanvasObject={(node, ctx, globalScale) => {
        // Draw label after the default node circle
        const label = node.name;
        const fontSize = 12 / globalScale;
        ctx.font = `${fontSize}px -apple-system, BlinkMacSystemFont, sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle =
          document.documentElement.dataset.theme === 'dark'
            ? '#dadadb'
            : '#1e1e1e';
        ctx.fillText(
          label.length > 20 ? label.slice(0, 18) + '...' : label,
          node.x,
          node.y + 10 / globalScale,
        );
      }}
      linkColor={() => 'rgba(150, 150, 150, 0.2)'}
      linkWidth={0.5}
      linkDirectionalParticles={1}
      linkDirectionalParticleWidth={1}
      linkDirectionalParticleSpeed={0.005}
      warmupTicks={100}
      cooldownTicks={0}
      onNodeClick={handleNodeClick}
      onNodeHover={handleNodeHover}
      enableNodeDrag={true}
      enableZoomInteraction={true}
      enablePanInteraction={true}
      minZoom={0.1}
      maxZoom={5}
      backgroundColor={
        typeof document !== 'undefined' &&
        document.documentElement?.dataset?.theme === 'dark'
          ? '#1d1e20'
          : '#ffffff'
      }
    />
  );
}
