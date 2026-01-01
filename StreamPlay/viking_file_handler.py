#!/usr/bin/env python3
"""
Viking File Handler - Python implementation based on Kotlin OXXFile data classes

This script provides Python data models and utilities for handling viking file links
and their metadata, mirroring the Kotlin implementation in StreamPlayParser.kt.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import json


@dataclass
class DriveLink:
    """Represents a Google Drive link with associated metadata."""
    file_id: str
    web_view_link: str
    drive_label: str
    credential_index: int
    is_login_drive: bool
    is_drive2: bool

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'fileId': self.file_id,
            'webViewLink': self.web_view_link,
            'driveLabel': self.drive_label,
            'credentialIndex': self.credential_index,
            'isLoginDrive': self.is_login_drive,
            'isDrive2': self.is_drive2
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'DriveLink':
        """Create DriveLink from dictionary."""
        return cls(
            file_id=data.get('fileId', ''),
            web_view_link=data.get('webViewLink', ''),
            drive_label=data.get('driveLabel', ''),
            credential_index=data.get('credentialIndex', 0),
            is_login_drive=data.get('isLoginDrive', False),
            is_drive2=data.get('isDrive2', False)
        )


@dataclass
class Metadata:
    """File metadata including conversion status for various services."""
    mime_type: str
    file_extension: str
    modified_time: str
    created_time: str
    pixeldrain_conversion_failed: bool
    pixeldrain_conversion_failed_at: str
    pixeldrain_conversion_error: str
    viking_conversion_failed: bool
    viking_conversion_failed_at: str

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'mimeType': self.mime_type,
            'fileExtension': self.file_extension,
            'modifiedTime': self.modified_time,
            'createdTime': self.created_time,
            'pixeldrainConversionFailed': self.pixeldrain_conversion_failed,
            'pixeldrainConversionFailedAt': self.pixeldrain_conversion_failed_at,
            'pixeldrainConversionError': self.pixeldrain_conversion_error,
            'vikingConversionFailed': self.viking_conversion_failed,
            'vikingConversionFailedAt': self.viking_conversion_failed_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Metadata':
        """Create Metadata from dictionary."""
        return cls(
            mime_type=data.get('mimeType', ''),
            file_extension=data.get('fileExtension', ''),
            modified_time=data.get('modifiedTime', ''),
            created_time=data.get('createdTime', ''),
            pixeldrain_conversion_failed=data.get('pixeldrainConversionFailed', False),
            pixeldrain_conversion_failed_at=data.get('pixeldrainConversionFailedAt', ''),
            pixeldrain_conversion_error=data.get('pixeldrainConversionError', ''),
            viking_conversion_failed=data.get('vikingConversionFailed', False),
            viking_conversion_failed_at=data.get('vikingConversionFailedAt', '')
        )


@dataclass
class OxxFile:
    """
    OXXFile data model representing a file with multiple hosting service links.
    
    Includes links to various file hosting services such as:
    - Viking
    - Pixeldrain
    - Gdtot
    - Hubcloud
    - Filepress
    - Google Drive (multiple)
    """
    id: str
    code: str
    file_name: str
    size: int
    drive_links: List[DriveLink]
    metadata: Metadata
    created_at: str
    views: int
    status: str
    gdtot_link: Optional[str] = None
    gdtot_name: Optional[str] = None
    hubcloud_link: str = ""
    filepress_link: str = ""
    viking_link: Optional[str] = None
    pixeldrain_link: Optional[str] = None
    credential_index: int = 0
    duration: Optional[str] = None
    user_name: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'code': self.code,
            'fileName': self.file_name,
            'size': self.size,
            'driveLinks': [link.to_dict() for link in self.drive_links],
            'metadata': self.metadata.to_dict(),
            'createdAt': self.created_at,
            'views': self.views,
            'status': self.status,
            'gdtotLink': self.gdtot_link,
            'gdtotName': self.gdtot_name,
            'hubcloudLink': self.hubcloud_link,
            'filepressLink': self.filepress_link,
            'vikingLink': self.viking_link,
            'pixeldrainLink': self.pixeldrain_link,
            'credential_index': self.credential_index,
            'duration': self.duration,
            'userName': self.user_name
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'OxxFile':
        """Create OxxFile from dictionary."""
        drive_links = [DriveLink.from_dict(link) for link in data.get('driveLinks', [])]
        metadata = Metadata.from_dict(data.get('metadata', {}))
        
        return cls(
            id=data.get('id', ''),
            code=data.get('code', ''),
            file_name=data.get('fileName', ''),
            size=data.get('size', 0),
            drive_links=drive_links,
            metadata=metadata,
            created_at=data.get('createdAt', ''),
            views=data.get('views', 0),
            status=data.get('status', ''),
            gdtot_link=data.get('gdtotLink'),
            gdtot_name=data.get('gdtotName'),
            hubcloud_link=data.get('hubcloudLink', ''),
            filepress_link=data.get('filepressLink', ''),
            viking_link=data.get('vikingLink'),
            pixeldrain_link=data.get('pixeldrainLink'),
            credential_index=data.get('credential_index', 0),
            duration=data.get('duration'),
            user_name=data.get('userName', '')
        )

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> 'OxxFile':
        """Create OxxFile from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def has_viking_link(self) -> bool:
        """Check if the file has a viking link."""
        return self.viking_link is not None and len(self.viking_link) > 0

    def is_viking_conversion_failed(self) -> bool:
        """Check if viking conversion has failed."""
        return self.metadata.viking_conversion_failed

    def get_all_links(self) -> dict:
        """Get all available file hosting links."""
        links = {}
        
        if self.viking_link:
            links['viking'] = self.viking_link
        if self.pixeldrain_link:
            links['pixeldrain'] = self.pixeldrain_link
        if self.gdtot_link:
            links['gdtot'] = self.gdtot_link
        if self.hubcloud_link:
            links['hubcloud'] = self.hubcloud_link
        if self.filepress_link:
            links['filepress'] = self.filepress_link
        
        # Add drive links
        for i, drive_link in enumerate(self.drive_links):
            links[f'drive_{i+1}'] = drive_link.web_view_link
        
        return links

    def get_viking_info(self) -> dict:
        """Get viking-specific information."""
        return {
            'viking_link': self.viking_link,
            'viking_conversion_failed': self.metadata.viking_conversion_failed,
            'viking_conversion_failed_at': self.metadata.viking_conversion_failed_at,
            'has_viking_link': self.has_viking_link()
        }


class VikingFileHandler:
    """Handler class for working with viking files."""
    
    @staticmethod
    def parse_file(file_path: str) -> OxxFile:
        """Parse a JSON file containing OxxFile data."""
        with open(file_path, 'r', encoding='utf-8') as f:
            json_str = f.read()
        return OxxFile.from_json(json_str)

    @staticmethod
    def save_file(oxx_file: OxxFile, file_path: str) -> None:
        """Save OxxFile to a JSON file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(oxx_file.to_json())

    @staticmethod
    def filter_by_viking_link(files: List[OxxFile]) -> List[OxxFile]:
        """Filter files that have viking links."""
        return [f for f in files if f.has_viking_link()]

    @staticmethod
    def filter_by_viking_conversion_failed(files: List[OxxFile]) -> List[OxxFile]:
        """Filter files where viking conversion has failed."""
        return [f for f in files if f.is_viking_conversion_failed()]

    @staticmethod
    def get_viking_statistics(files: List[OxxFile]) -> dict:
        """Get statistics about viking links in a list of files."""
        total_files = len(files)
        files_with_viking = len([f for f in files if f.has_viking_link()])
        failed_conversions = len([f for f in files if f.is_viking_conversion_failed()])
        
        return {
            'total_files': total_files,
            'files_with_viking_link': files_with_viking,
            'viking_conversion_failures': failed_conversions,
            'success_rate': (files_with_viking - failed_conversions) / files_with_viking * 100 
                           if files_with_viking > 0 else 0
        }


# Example usage
if __name__ == "__main__":
    # Example: Create a sample OxxFile with viking link
    sample_metadata = Metadata(
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
    
    sample_drive_link = DriveLink(
        file_id="abc123",
        web_view_link="https://drive.google.com/file/d/abc123/view",
        drive_label="Primary Drive",
        credential_index=0,
        is_login_drive=False,
        is_drive2=False
    )
    
    sample_file = OxxFile(
        id="file001",
        code="XYZ123",
        file_name="sample_video.mp4",
        size=1048576000,  # 1GB in bytes
        drive_links=[sample_drive_link],
        metadata=sample_metadata,
        created_at="2024-01-01T00:00:00Z",
        views=100,
        status="active",
        gdtot_link="https://gdtot.example/file123",
        gdtot_name="sample_video.mp4",
        hubcloud_link="https://hubcloud.example/file123",
        filepress_link="https://filepress.example/file123",
        viking_link="https://viking.example/file123",
        pixeldrain_link="https://pixeldrain.example/file123",
        credential_index=0,
        duration="01:30:00",
        user_name="user123"
    )
    
    print("=== Sample OxxFile with Viking Link ===")
    print(sample_file.to_json())
    
    print("\n=== Viking Information ===")
    viking_info = sample_file.get_viking_info()
    for key, value in viking_info.items():
        print(f"{key}: {value}")
    
    print("\n=== All Available Links ===")
    all_links = sample_file.get_all_links()
    for service, link in all_links.items():
        print(f"{service}: {link}")
