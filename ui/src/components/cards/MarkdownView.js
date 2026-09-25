import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';

export const MarkdownView = ({ content, className, style }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const renderer = new marked.Renderer();

    renderer.link = (href, title, text) => {
      const titleAttr = title ? ` title="${title}"` : '';
      return `<a href="${href}"${titleAttr} target="_blank" rel="noopener noreferrer">${text}</a>`;
    };

    renderer.image = (href, title, text) => {
      const titleAttr = title ? ` title="${title}"` : '';
      return `<img src="${href}" alt="${text || ''}"${titleAttr} style="max-width:100%;height:auto;display:block;text-align:left;margin-left:0;margin-right:auto;" />`;
    };

    marked.setOptions({
      renderer,
      breaks: true,
      gfm: true,
      highlight: (code, lang) => {
        try {
          if (lang && hljs.getLanguage(lang)) {
            return hljs.highlight(code, { language: lang }).value;
          }
          return hljs.highlightAuto(code).value;
        } catch {
          return code;
        }
      }
    });

    const rawHtml = marked.parse(content || '');
    const cleanHtml = DOMPurify.sanitize(rawHtml);

    containerRef.current.innerHTML = cleanHtml;
    containerRef.current.style.textAlign = 'left';

    containerRef.current
      .querySelectorAll('h1,h2,h3,h4,h5,h6,p,ul,ol,li,blockquote,pre,code,table,thead,tbody,tr,th,td')
      .forEach((element) => {
        element.style.textAlign = 'left';
      });
  }, [content]);

  return (
    <div
      ref={containerRef}
      className={className}
      style={{ ...style, textAlign: 'left' }}
    />
  );
};

MarkdownView.propTypes = {
  content: PropTypes.string,
  className: PropTypes.string,
  style: PropTypes.object
};

MarkdownView.defaultProps = {
  content: '',
  className: '',
  style: {}
};

export default MarkdownView;
