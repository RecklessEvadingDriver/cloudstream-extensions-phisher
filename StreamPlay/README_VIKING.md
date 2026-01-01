# Viking File Handler - Python Script

A Python script to extract all available download links from viking file URLs (e.g., `https://vik1ngfile.site/f/oDAbw3OOmy`).

## Overview

This script acts as a web scraper/extractor for viking file hosting service, automatically fetching the page and extracting all available download links including:
- Direct download links from viking
- External file hosting links (Google Drive, Pixeldrain, Gdtot, Hubcloud, Filepress, etc.)
- Streaming service links (Streamtape, Doodstream, Mixdrop, etc.)
- Direct file URLs (MP4, MKV, M3U8, etc.)

The script mirrors the Kotlin extractor pattern used in StreamPlay's codebase.

## Installation

### Requirements

- Python 3.7 or higher
- `requests` library
- `beautifulsoup4` library

### Install Dependencies

```bash
pip install requests beautifulsoup4
```

Or using pip3:

```bash
pip3 install requests beautifulsoup4
```

## Usage

### Command Line Interface

#### Basic Usage

Extract and display all links from a viking file URL:

```bash
python3 viking_file_handler.py https://vik1ngfile.site/f/oDAbw3OOmy
```

#### JSON Output

Output results in JSON format:

```bash
python3 viking_file_handler.py https://vik1ngfile.site/f/oDAbw3OOmy --json
```

#### Save to File

Save output to a file:

```bash
python3 viking_file_handler.py https://vik1ngfile.site/f/oDAbw3OOmy --output links.json
```

#### Custom Timeout

Set a custom timeout (in seconds):

```bash
python3 viking_file_handler.py https://vik1ngfile.site/f/oDAbw3OOmy --timeout 60
```

### Python API

You can also use the script as a Python module:

```python
from viking_file_handler import VikingFileExtractor

# Create extractor instance
extractor = VikingFileExtractor(timeout=30)

# Extract links from URL
viking_info = extractor.get_download_links("https://vik1ngfile.site/f/oDAbw3OOmy")

# Access file information
print(f"File ID: {viking_info.file_id}")
print(f"File Name: {viking_info.file_name}")
print(f"File Size: {viking_info.file_size}")

# Access download links
for link in viking_info.download_links:
    print(f"Source: {link.source}")
    print(f"URL: {link.url}")
    if link.quality:
        print(f"Quality: {link.quality}")
```

## Features

### Automatic Link Extraction

The script employs multiple strategies to find all available download links:

1. **Download Buttons/Links**: Searches for elements with "download" text
2. **External File Hosts**: Identifies links to known file hosting services
3. **Direct File Links**: Finds direct links to video files (MP4, MKV, etc.)

### Supported File Hosting Services

- Google Drive
- Pixeldrain
- Gdtot
- Hubcloud
- Filepress
- Mediafire
- Mega.nz
- Dropbox
- Streamtape
- Doodstream
- Mixdrop
- Upstream

### Metadata Extraction

The script attempts to extract:
- File name
- File size
- Upload date
- Quality information (1080p, 720p, 4K, etc.)
- File type (MP4, MKV, etc.)

## Output Formats

### Human-Readable Output

```
Viking File: oDAbw3OOmy
URL: https://vik1ngfile.site/f/oDAbw3OOmy
File Name: Example Movie.mkv
File Size: 2.5 GB
Upload Date: 2024-01-01

Found 5 download link(s):
--------------------------------------------------------------------------------

1. Source: viking
   Quality: 1080p
   URL: https://vik1ngfile.site/download/abc123

2. Source: drive.google
   URL: https://drive.google.com/file/d/xyz789/view

3. Source: pixeldrain
   URL: https://pixeldrain.com/u/def456

4. Source: direct
   Quality: 720p
   Type: mp4
   URL: https://cdn.example.com/video.mp4

5. Source: streamtape
   URL: https://streamtape.com/v/ghi012
```

### JSON Output

```json
{
  "file_id": "oDAbw3OOmy",
  "file_name": "Example Movie.mkv",
  "file_size": "2.5 GB",
  "upload_date": "2024-01-01",
  "download_links": [
    {
      "url": "https://vik1ngfile.site/download/abc123",
      "quality": "1080p",
      "source": "viking",
      "file_size": null,
      "file_type": null
    },
    {
      "url": "https://drive.google.com/file/d/xyz789/view",
      "quality": null,
      "source": "drive.google",
      "file_size": null,
      "file_type": null
    }
  ],
  "page_url": "https://vik1ngfile.site/f/oDAbw3OOmy"
}
```

## Data Classes

### VikingFileInfo

Represents information about a viking file.

**Attributes:**
- `file_id` (str): The unique file identifier
- `file_name` (Optional[str]): The name of the file
- `file_size` (Optional[str]): The size of the file
- `upload_date` (Optional[str]): When the file was uploaded
- `download_links` (List[DownloadLink]): List of all download links
- `page_url` (str): The original page URL

**Methods:**
- `to_dict()`: Convert to dictionary
- `to_json(indent=2)`: Convert to JSON string
- `from_dict(data)`: Create from dictionary

### DownloadLink

Represents a single download link.

**Attributes:**
- `url` (str): The download URL
- `quality` (Optional[str]): Quality indicator (1080p, 720p, etc.)
- `source` (str): Source service name
- `file_size` (Optional[str]): Size of the file at this link
- `file_type` (Optional[str]): File type/extension

**Methods:**
- `to_dict()`: Convert to dictionary
- `from_dict(data)`: Create from dictionary

### VikingFileExtractor

Main extractor class for processing viking file URLs.

**Methods:**
- `__init__(timeout=30)`: Initialize with optional timeout
- `extract_file_id(url)`: Extract file ID from URL
- `get_download_links(url)`: Extract all links from URL

## Error Handling

The script gracefully handles errors:
- Network errors (timeouts, connection failures)
- Invalid URLs
- Missing or inaccessible pages
- Parsing errors

When an error occurs, the script will:
1. Print an error message to stderr
2. Return available data (if any)
3. Exit with appropriate exit code

## Relation to Kotlin Code

This Python implementation mirrors the extractor pattern used in `StreamPlay/src/main/kotlin/com/Phisher98/Extractors.kt`, following the same principles:

- Extract file metadata from the page
- Find all available download sources
- Return structured data for further processing
- Handle errors gracefully

The data model is based on the OXXFile structure from `StreamPlayParser.kt` which includes viking link fields.

## Troubleshooting

### Connection Errors

If you get connection errors:
- Check if the viking file site is accessible
- Try increasing the timeout: `--timeout 60`
- Check your internet connection
- The site may be temporarily unavailable

### Missing Dependencies

If you get import errors:
```bash
pip install --upgrade requests beautifulsoup4
```

### No Links Found

If no links are found:
- The page structure may have changed
- The file may have been removed
- Try accessing the URL in a browser to verify it exists

## License

This script is part of the cloudstream-extensions-phisher project and follows the same license.
