import axios from 'axios'
import { Card, Badge, InputGroup, Button, Table, Form, ListGroup, Row, Col } from 'react-bootstrap'
import { ArrowBigDown } from 'lucide-react'

import { useDispatch, useSelector } from 'react-redux'

import { SendHorizontal, Check } from 'lucide-react'

import React, { useEffect, useRef, useState } from 'react';
import PropTypes from 'prop-types';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';

export const MarkdownView = ({content, className, style}) => {


    const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Configure marked with a simple renderer for links/images and highlighting
    const renderer = new marked.Renderer();

    renderer.link = (href, title, text) => {
      const titleAttr = title ? ` title="${title}"` : '';
      // target and rel for safety
      return `<a href="${href}"${titleAttr} target="_blank" rel="noopener noreferrer">${text}</a>`;
    };

    renderer.image = (href, title, text) => {
      const titleAttr = title ? ` title="${title}"` : '';
      // make images responsive
      return `<img src="${href}" alt="${text || ''}"${titleAttr} style="max-width:100%;height:auto;display:block;" />`;
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
        } catch (e) {
          return code;
        }
      }
    });

    const rawHtml = marked.parse(content || '');
    const clean = DOMPurify.sanitize(rawHtml);
    containerRef.current.innerHTML = clean;
  }, [content]);

  return (
    <div ref={containerRef} className={className} style={style} />
  );
}

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



export default MarkdownView
