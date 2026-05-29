"""Citation Viewer component."""
import React, { useState } from "react";
import * as Types from "../types/api";
import "../styles/CitationViewer.css";

interface Props {
  citations: Types.Citation[];
}

const CitationViewer: React.FC<Props> = ({ citations }) => {
  const [showCitations, setShowCitations] = useState(false);

  return (
    <div className="citations-section">
      <button
        onClick={() => setShowCitations(!showCitations)}
        className="citations-toggle"
      >
        📚 Citations ({citations.length}) {showCitations ? "▼" : "▶"}
      </button>

      {showCitations && (
        <div className="citations-list">
          {citations.map((citation, index) => (
            <div key={index} className="citation-item">
              <span className="citation-number">[{index + 1}]</span>
              <div className="citation-content">
                <span className="citation-type">{citation.type}</span>
                {citation.url ? (
                  <a
                    href={citation.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="citation-link"
                  >
                    {citation.full_match}
                  </a>
                ) : (
                  <span>{citation.full_match}</span>
                )}
                {citation.author && (
                  <span className="citation-author"> - {citation.author} ({citation.year})</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CitationViewer;
