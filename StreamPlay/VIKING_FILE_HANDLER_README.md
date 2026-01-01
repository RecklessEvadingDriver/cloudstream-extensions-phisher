# Viking File Handler - Python Script

A Python implementation of the OXXFile data models from the Kotlin `StreamPlayParser.kt`, specifically designed for handling viking file links and their associated metadata.

## Overview

This script provides Python data classes and utilities that mirror the Kotlin implementation for handling files with multiple hosting service links, including:
- **Viking** (primary focus)
- Pixeldrain
- Gdtot
- Hubcloud
- Filepress
- Google Drive (multiple links)

## Features

### Data Models

1. **OxxFile**: Main data class representing a file with multiple hosting service links
   - Contains fields for all hosting service links (viking, pixeldrain, gdtot, etc.)
   - Includes metadata about the file
   - Supports JSON serialization/deserialization

2. **Metadata**: File metadata including conversion status
   - Tracks conversion status for viking and pixeldrain services
   - Contains file type, creation time, and modification time information

3. **DriveLink**: Represents Google Drive links
   - Contains drive file ID, view link, and credential information

### Utility Methods

The `OxxFile` class provides several utility methods:

- `has_viking_link()`: Check if the file has a viking link
- `is_viking_conversion_failed()`: Check if viking conversion has failed
- `get_all_links()`: Get dictionary of all available hosting links
- `get_viking_info()`: Get viking-specific information
- `to_json()`: Export to JSON format
- `from_json()`: Import from JSON format

### Handler Class

The `VikingFileHandler` class provides static methods for:

- `parse_file(file_path)`: Load OxxFile from JSON file
- `save_file(oxx_file, file_path)`: Save OxxFile to JSON file
- `filter_by_viking_link(files)`: Filter files that have viking links
- `filter_by_viking_conversion_failed(files)`: Filter files with failed conversions
- `get_viking_statistics(files)`: Get statistics about viking links

## Usage Examples

### Basic Usage

```python
from viking_file_handler import OxxFile, Metadata, DriveLink

# Create a file object
metadata = Metadata(
    mime_type="video/mp4",
    file_extension="mp4",
    modified_time="2024-01-01T00:00:00Z",
    created_time="2024-01-01T00:00:00Z",
    pixeldrain_conversion_failed=False,
    pixeldrain_conversion_failed_at="",
    pixeldrain_conversion_error="",
    viking_conversion_failed=False,
    viking_conversion_failed_at=""
)

file_obj = OxxFile(
    id="file001",
    code="ABC123",
    file_name="movie.mp4",
    size=1048576000,
    drive_links=[],
    metadata=metadata,
    created_at="2024-01-01T00:00:00Z",
    views=100,
    status="active",
    viking_link="https://viking.example/file123"
)

# Check viking link
if file_obj.has_viking_link():
    print(f"Viking link: {file_obj.viking_link}")

# Get viking info
viking_info = file_obj.get_viking_info()
print(viking_info)
```

### Working with JSON

```python
from viking_file_handler import OxxFile, VikingFileHandler

# Parse from JSON file
file_obj = VikingFileHandler.parse_file("data.json")

# Save to JSON file
VikingFileHandler.save_file(file_obj, "output.json")

# Convert to JSON string
json_str = file_obj.to_json()
print(json_str)

# Parse from JSON string
file_obj = OxxFile.from_json(json_str)
```

### Filtering and Statistics

```python
from viking_file_handler import VikingFileHandler

# Assuming you have a list of OxxFile objects
files = [...]  # Your list of files

# Filter files with viking links
viking_files = VikingFileHandler.filter_by_viking_link(files)
print(f"Found {len(viking_files)} files with viking links")

# Filter files with failed conversions
failed_files = VikingFileHandler.filter_by_viking_conversion_failed(files)
print(f"Found {len(failed_files)} files with failed conversions")

# Get statistics
stats = VikingFileHandler.get_viking_statistics(files)
print(f"Total files: {stats['total_files']}")
print(f"Files with viking link: {stats['files_with_viking_link']}")
print(f"Failed conversions: {stats['viking_conversion_failures']}")
print(f"Success rate: {stats['success_rate']:.2f}%")
```

### Getting All Links

```python
# Get all available hosting links for a file
all_links = file_obj.get_all_links()
for service, link in all_links.items():
    print(f"{service}: {link}")
```

## Running the Example

To run the built-in example:

```bash
cd StreamPlay
python3 viking_file_handler.py
```

This will demonstrate:
- Creating a sample OxxFile with viking link
- Displaying the JSON representation
- Showing viking-specific information
- Listing all available links

## Data Structure Reference

### OxxFile Fields

| Field | Type | Description |
|-------|------|-------------|
| `viking_link` | `Optional[str]` | Link to viking hosting service |
| `pixeldrain_link` | `Optional[str]` | Link to pixeldrain hosting service |
| `gdtot_link` | `Optional[str]` | Link to gdtot hosting service |
| `hubcloud_link` | `str` | Link to hubcloud hosting service |
| `filepress_link` | `str` | Link to filepress hosting service |
| `drive_links` | `List[DriveLink]` | List of Google Drive links |

### Metadata Fields (Viking-related)

| Field | Type | Description |
|-------|------|-------------|
| `viking_conversion_failed` | `bool` | Whether viking conversion failed |
| `viking_conversion_failed_at` | `str` | Timestamp of conversion failure |

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Relation to Kotlin Code

This Python implementation mirrors the following Kotlin data classes from `StreamPlayParser.kt`:

- `oxxfile` (lines 1987-2007) → `OxxFile`
- `Metadata` (lines 2018-2028) → `Metadata`
- `DriveLink` (lines 2009-2016) → `DriveLink`

The Python version adds utility methods and a handler class for easier manipulation and filtering of viking files.
