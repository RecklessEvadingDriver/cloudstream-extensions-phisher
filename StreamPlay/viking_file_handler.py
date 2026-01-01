#!/usr/bin/env python3
"""
Viking File Handler - Python script to extract download links from viking file URLs

This script fetches viking file pages and extracts all available download links,
mirroring the Kotlin extractor pattern used in StreamPlay.

Usage:
    python3 viking_file_handler.py https://vik1ngfile.site/f/oDAbw3OOmy
    python3 viking_file_handler.py https://vik1ngfile.site/f/oDAbw3OOmy --json
    python3 viking_file_handler.py https://vik1ngfile.site/f/oDAbw3OOmy --output links.json
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import json
import re
import sys
import argparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Required packages not found. Install with:")
    print("  pip install requests beautifulsoup4")
    sys.exit(1)


@dataclass
class DownloadLink:
    """Represents a download link with metadata."""
    url: str
    quality: Optional[str] = None
    source: str = "viking"
    file_size: Optional[str] = None
    file_type: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'url': self.url,
            'quality': self.quality,
            'source': self.source,
            'file_size': self.file_size,
            'file_type': self.file_type
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'DownloadLink':
        """Create DownloadLink from dictionary."""
        return cls(
            url=data.get('url', ''),
            quality=data.get('quality'),
            source=data.get('source', 'viking'),
            file_size=data.get('file_size'),
            file_type=data.get('file_type')
        )


@dataclass
class VikingFileInfo:
    """Information about a viking file."""
    file_id: str
    file_name: Optional[str] = None
    file_size: Optional[str] = None
    upload_date: Optional[str] = None
    download_links: List[DownloadLink] = field(default_factory=list)
    page_url: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'file_id': self.file_id,
            'file_name': self.file_name,
            'file_size': self.file_size,
            'upload_date': self.upload_date,
            'download_links': [link.to_dict() for link in self.download_links],
            'page_url': self.page_url
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: dict) -> 'VikingFileInfo':
        """Create VikingFileInfo from dictionary."""
        download_links = [DownloadLink.from_dict(link) for link in data.get('download_links', [])]
        return cls(
            file_id=data.get('file_id', ''),
            file_name=data.get('file_name'),
            file_size=data.get('file_size'),
            upload_date=data.get('upload_date'),
            download_links=download_links,
            page_url=data.get('page_url', '')
        )


class VikingFileExtractor:
    """Extractor for viking file URLs to get all available download links."""
    
    BASE_URL = "https://vik1ngfile.site"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    def __init__(self, timeout: int = 30):
        """Initialize the extractor with optional timeout."""
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def extract_file_id(self, url: str) -> Optional[str]:
        """Extract file ID from viking URL."""
        patterns = [
            r'vik1ngfile\.site/f/([a-zA-Z0-9]+)',
            r'vik1ngfile\.site/file/([a-zA-Z0-9]+)',
            r'/f/([a-zA-Z0-9]+)',
            r'/file/([a-zA-Z0-9]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_download_links(self, url: str) -> VikingFileInfo:
        """
        Extract all download links from a viking file URL.
        
        Args:
            url: Viking file URL (e.g., https://vik1ngfile.site/f/oDAbw3OOmy)
            
        Returns:
            VikingFileInfo object containing all extracted information
        """
        file_id = self.extract_file_id(url)
        if not file_id:
            raise ValueError(f"Could not extract file ID from URL: {url}")
        
        # Normalize URL
        if not url.startswith('http'):
            url = f"{self.BASE_URL}/f/{file_id}"
        
        viking_info = VikingFileInfo(
            file_id=file_id,
            page_url=url
        )
        
        try:
            # Fetch the page
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract file information
            viking_info.file_name = self._extract_file_name(soup)
            viking_info.file_size = self._extract_file_size(soup)
            viking_info.upload_date = self._extract_upload_date(soup)
            
            # Extract all download links
            viking_info.download_links = self._extract_download_links(soup, url)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching viking file page: {e}", file=sys.stderr)
            # Return info with what we have
        
        return viking_info
    
    def _extract_file_name(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract file name from the page."""
        # Try various selectors
        selectors = [
            ('h1', {'class': 'file-name'}),
            ('h2', {'class': 'file-name'}),
            ('div', {'class': 'file-name'}),
            ('span', {'class': 'file-name'}),
            ('h1', {}),
            ('title', {})
        ]
        
        for tag, attrs in selectors:
            element = soup.find(tag, attrs)
            if element:
                text = element.get_text(strip=True)
                if text and len(text) > 0:
                    return text
        
        return None
    
    def _extract_file_size(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract file size from the page."""
        # Try to find file size
        size_patterns = [
            (r'Size[:\s]+([0-9.]+\s*[KMGT]B)', re.IGNORECASE),
            (r'File\s+Size[:\s]+([0-9.]+\s*[KMGT]B)', re.IGNORECASE),
            (r'([0-9.]+\s*[KMGT]B)', 0)
        ]
        
        text = soup.get_text()
        for pattern, flags in size_patterns:
            match = re.search(pattern, text, flags if flags else 0)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_upload_date(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract upload date from the page."""
        # Try to find upload date
        date_selectors = [
            ('span', {'class': 'upload-date'}),
            ('div', {'class': 'upload-date'}),
            ('time', {})
        ]
        
        for tag, attrs in date_selectors:
            element = soup.find(tag, attrs)
            if element:
                # Try datetime attribute first
                if element.has_attr('datetime'):
                    return element['datetime']
                text = element.get_text(strip=True)
                if text:
                    return text
        
        return None
    
    def _extract_download_links(self, soup: BeautifulSoup, page_url: str) -> List[DownloadLink]:
        """Extract all download links from the page."""
        download_links = []
        
        # Find all links that look like download links
        # Common patterns: buttons with "download", links with "download", direct file links
        
        # Strategy 1: Find download buttons/links
        download_elements = soup.find_all(['a', 'button'], 
                                          string=re.compile(r'download|Download|DOWNLOAD', re.IGNORECASE))
        
        for element in download_elements:
            href = element.get('href')
            if href:
                # Make absolute URL
                if href.startswith('http'):
                    url = href
                elif href.startswith('/'):
                    url = f"{self.BASE_URL}{href}"
                else:
                    url = f"{self.BASE_URL}/{href}"
                
                # Try to extract quality info
                quality = self._extract_quality(element.get_text())
                
                download_links.append(DownloadLink(
                    url=url,
                    quality=quality,
                    source="viking"
                ))
        
        # Strategy 2: Find all external file hosting links
        all_links = soup.find_all('a', href=True)
        
        # Common file hosting domains
        file_hosts = [
            'drive.google.com', 'gdtot', 'hubcloud', 'filepress',
            'pixeldrain', 'mediafire', 'mega.nz', 'dropbox',
            'streamtape', 'doodstream', 'mixdrop', 'upstream'
        ]
        
        for link in all_links:
            href = link.get('href', '')
            
            # Check if it's a file hosting link
            if any(host in href.lower() for host in file_hosts):
                # Avoid duplicates
                if not any(dl.url == href for dl in download_links):
                    # Determine the source
                    source = "viking"
                    for host in file_hosts:
                        if host in href.lower():
                            source = host.replace('.com', '').replace('.nz', '')
                            break
                    
                    download_links.append(DownloadLink(
                        url=href,
                        source=source
                    ))
        
        # Strategy 3: Look for direct file links in the page
        direct_file_patterns = [
            r'https?://[^\s<>"]+\.(?:mp4|mkv|avi|mov|wmv|flv|webm|m3u8)',
            r'https?://[^\s<>"]+/download/[^\s<>"]+',
            r'https?://[^\s<>"]+/dl/[^\s<>"]+',
        ]
        
        page_text = str(soup)
        for pattern in direct_file_patterns:
            matches = re.finditer(pattern, page_text, re.IGNORECASE)
            for match in matches:
                url = match.group(0).rstrip('"\'>')
                if not any(dl.url == url for dl in download_links):
                    # Try to extract quality from URL
                    quality = None
                    quality_match = re.search(r'(1080p|720p|480p|360p|4K|2K)', url, re.IGNORECASE)
                    if quality_match:
                        quality = quality_match.group(1)
                    
                    # Determine file type
                    file_type = None
                    ext_match = re.search(r'\.([a-z0-9]+)(?:\?|$)', url, re.IGNORECASE)
                    if ext_match:
                        file_type = ext_match.group(1)
                    
                    download_links.append(DownloadLink(
                        url=url,
                        quality=quality,
                        source="direct",
                        file_type=file_type
                    ))
        
        return download_links
    
    def _extract_quality(self, text: str) -> Optional[str]:
        """Extract quality information from text."""
        quality_patterns = [
            r'(1080p|720p|480p|360p|4K|2K|HD|SD|FHD|UHD)',
        ]
        
        for pattern in quality_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None


def main():
    """Main function for CLI usage."""
    parser = argparse.ArgumentParser(
        description='Extract download links from viking file URLs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://vik1ngfile.site/f/oDAbw3OOmy
  %(prog)s https://vik1ngfile.site/f/oDAbw3OOmy --json
  %(prog)s https://vik1ngfile.site/f/oDAbw3OOmy --output links.json
        """
    )
    
    parser.add_argument('url', help='Viking file URL to extract')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    parser.add_argument('--output', '-o', help='Output file path (default: stdout)')
    parser.add_argument('--timeout', type=int, default=30, help='Request timeout in seconds')
    
    args = parser.parse_args()
    
    try:
        extractor = VikingFileExtractor(timeout=args.timeout)
        viking_info = extractor.get_download_links(args.url)
        
        if args.json:
            output = viking_info.to_json()
        else:
            # Human-readable format
            output = []
            output.append(f"Viking File: {viking_info.file_id}")
            output.append(f"URL: {viking_info.page_url}")
            
            if viking_info.file_name:
                output.append(f"File Name: {viking_info.file_name}")
            if viking_info.file_size:
                output.append(f"File Size: {viking_info.file_size}")
            if viking_info.upload_date:
                output.append(f"Upload Date: {viking_info.upload_date}")
            
            output.append(f"\nFound {len(viking_info.download_links)} download link(s):")
            output.append("-" * 80)
            
            for i, link in enumerate(viking_info.download_links, 1):
                output.append(f"\n{i}. Source: {link.source}")
                if link.quality:
                    output.append(f"   Quality: {link.quality}")
                if link.file_size:
                    output.append(f"   Size: {link.file_size}")
                if link.file_type:
                    output.append(f"   Type: {link.file_type}")
                output.append(f"   URL: {link.url}")
            
            output = '\n'.join(output)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Output saved to: {args.output}")
        else:
            print(output)
        
        # Exit with success
        sys.exit(0)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
