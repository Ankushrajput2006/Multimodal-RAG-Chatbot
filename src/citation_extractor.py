"""Citation extraction and formatting module."""
import logging
import re
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class CitationExtractor:
    """Extract and format citations from documents."""

    CITATION_PATTERNS = {
        "doi": r"\b(?:doi:|DOI:)?\s*(?:https?://doi\.org/)?([0-9.]+/[^\s]+)",
        "arxiv": r"\barxiv:(\d{4}\.\d{4,5}(?:v\d+)?)",
        "url": r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)",
        "author_year": r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*\(\s*(\d{4})\s*\)",
    }

    def __init__(self):
        """Initialize citation extractor."""
        self.citations = []
        self.citation_style = "APA"

    def extract_citations(self, text: str) -> List[Dict]:
        """Extract citations from text.
        
        Args:
            text: Text to extract citations from
            
        Returns:
            List of citation dictionaries
        """
        citations = []
        
        # Extract DOIs
        doi_matches = re.finditer(self.CITATION_PATTERNS["doi"], text)
        for match in doi_matches:
            citations.append({
                "type": "doi",
                "value": match.group(1),
                "full_match": match.group(0),
                "url": f"https://doi.org/{match.group(1)}"
            })
        
        # Extract arXiv
        arxiv_matches = re.finditer(self.CITATION_PATTERNS["arxiv"], text)
        for match in arxiv_matches:
            citations.append({
                "type": "arxiv",
                "value": match.group(1),
                "full_match": match.group(0),
                "url": f"https://arxiv.org/abs/{match.group(1)}"
            })
        
        # Extract URLs
        url_matches = re.finditer(self.CITATION_PATTERNS["url"], text)
        for match in url_matches:
            url = match.group(0)
            # Avoid duplicates
            if not any(c["url"] == url for c in citations):
                citations.append({
                    "type": "url",
                    "value": url,
                    "full_match": url,
                    "url": url
                })
        
        # Extract author-year citations
        author_year_matches = re.finditer(self.CITATION_PATTERNS["author_year"], text)
        for match in author_year_matches:
            citations.append({
                "type": "author_year",
                "author": match.group(1),
                "year": match.group(2),
                "full_match": match.group(0)
            })
        
        self.citations = citations
        return citations

    def format_citation(self, citation: Dict, style: str = "APA") -> str:
        """Format citation in specified style.
        
        Args:
            citation: Citation dictionary
            style: Citation style (APA, MLA, Chicago)
            
        Returns:
            Formatted citation string
        """
        if style == "APA":
            return self._format_apa(citation)
        elif style == "MLA":
            return self._format_mla(citation)
        elif style == "Chicago":
            return self._format_chicago(citation)
        else:
            return str(citation)

    def _format_apa(self, citation: Dict) -> str:
        """Format citation in APA style."""
        if citation["type"] == "doi":
            return f"https://doi.org/{citation['value']}"
        elif citation["type"] == "arxiv":
            return f"Retrieved from https://arxiv.org/abs/{citation['value']}"
        elif citation["type"] == "url":
            return f"Retrieved from {citation['url']}"
        elif citation["type"] == "author_year":
            return f"{citation['author']} ({citation['year']})"
        return str(citation)

    def _format_mla(self, citation: Dict) -> str:
        """Format citation in MLA style."""
        if citation["type"] == "doi":
            return f"doi: {citation['value']}"
        elif citation["type"] == "arxiv":
            return f"arXiv preprint: {citation['value']}"
        elif citation["type"] == "url":
            return f"{citation['url']}. Accessed {datetime.now().strftime('%d %b. %Y')}"
        elif citation["type"] == "author_year":
            return f"{citation['author']}. {citation['year']}."
        return str(citation)

    def _format_chicago(self, citation: Dict) -> str:
        """Format citation in Chicago style."""
        if citation["type"] == "doi":
            return f"https://doi.org/{citation['value']}"
        elif citation["type"] == "arxiv":
            return f"https://arxiv.org/abs/{citation['value']}"
        elif citation["type"] == "url":
            return f"{citation['url']} (accessed {datetime.now().strftime('%B %d, %Y')})"
        elif citation["type"] == "author_year":
            return f"{citation['author']}, {citation['year']}"
        return str(citation)

    def generate_bibliography(self, style: str = "APA") -> str:
        """Generate bibliography from extracted citations.
        
        Args:
            style: Citation style
            
        Returns:
            Formatted bibliography string
        """
        if not self.citations:
            return "No citations found."
        
        bibliography = f"Bibliography ({style}):\n\n"
        
        for i, citation in enumerate(self.citations, 1):
            formatted = self.format_citation(citation, style)
            bibliography += f"{i}. {formatted}\n"
        
        return bibliography

    def link_citations_in_text(self, text: str, style: str = "APA") -> str:
        """Add links to citations in text.
        
        Args:
            text: Original text
            style: Citation style
            
        Returns:
            Text with linked citations
        """
        citations = self.extract_citations(text)
        modified_text = text
        
        for citation in citations:
            if "url" in citation:
                # Replace citation with linked version
                modified_text = modified_text.replace(
                    citation["full_match"],
                    f"[{citation['full_match']}]({citation['url']})"
                )
        
        return modified_text
