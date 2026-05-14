"""Export service for generating downloadable files."""
import csv
import json
import io
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path

from core.logging import get_logger
from models.schemas import Creator

logger = get_logger(__name__)


class ExportService:
    """Service for exporting creator data in various formats."""

    @staticmethod
    def export_to_csv(creators: List[Creator]) -> bytes:
        """Export creators to CSV format.

        Args:
            creators: List of Creator objects

        Returns:
            CSV file bytes
        """
        try:
            output = io.StringIO()
            fieldnames = [
                "ID",
                "Name",
                "Handle",
                "Platform",
                "Followers",
                "Engagement",
                "Consistency",
                "Campaign Ready",
                "Niche",
                "Recent Posts",
                "Avg Views",
            ]

            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()

            for creator in creators:
                writer.writerow({
                    "ID": creator.id,
                    "Name": creator.name,
                    "Handle": creator.handle,
                    "Platform": creator.platform,
                    "Followers": creator.followers,
                    "Engagement": creator.engagement,
                    "Consistency": creator.uploadConsistency,
                    "Campaign Ready": creator.campaignReady,
                    "Niche": creator.niche,
                    "Recent Posts": creator.recentPosts,
                    "Avg Views": creator.avgViews,
                })

            return output.getvalue().encode("utf-8")

        except Exception as e:
            logger.error(f"CSV export error: {str(e)}")
            raise

    @staticmethod
    def export_to_json(creators: List[Creator]) -> bytes:
        """Export creators to JSON format.

        Args:
            creators: List of Creator objects

        Returns:
            JSON file bytes
        """
        try:
            data = {
                "export_date": datetime.utcnow().isoformat(),
                "total_creators": len(creators),
                "creators": [creator.model_dump() for creator in creators],
            }

            return json.dumps(data, indent=2).encode("utf-8")

        except Exception as e:
            logger.error(f"JSON export error: {str(e)}")
            raise

    @staticmethod
    def export_to_pdf(creators: List[Creator]) -> bytes:
        """Export creators to PDF format (simplified).

        Args:
            creators: List of Creator objects

        Returns:
            PDF file bytes
        """
        try:
            # Simplified PDF generation - would use reportlab in production
            html_content = ExportService._generate_html_report(creators)
            # In production, convert HTML to PDF using a library like WeasyPrint
            return html_content.encode("utf-8")

        except Exception as e:
            logger.error(f"PDF export error: {str(e)}")
            raise

    @staticmethod
    def _generate_html_report(creators: List[Creator]) -> str:
        """Generate HTML report for creators.

        Args:
            creators: List of Creator objects

        Returns:
            HTML string
        """
        rows = "".join([
            f"""
            <tr>
                <td>{creator.name}</td>
                <td>{creator.handle}</td>
                <td>{creator.platform}</td>
                <td>{creator.followers}</td>
                <td>{creator.engagement}%</td>
                <td>{creator.uploadConsistency}</td>
                <td>{creator.campaignReady}</td>
            </tr>
            """
            for creator in creators
        ])

        html = f"""
        <html>
            <head>
                <title>CreatorScope AI - Creator Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                    th {{ background-color: #1a1a2e; color: white; }}
                    tr:nth-child(even) {{ background-color: #f2f2f2; }}
                    h1 {{ color: #1a1a2e; }}
                </style>
            </head>
            <body>
                <h1>CreatorScope AI - Creator Report</h1>
                <p>Generated: {datetime.utcnow().isoformat()}</p>
                <p>Total Creators: {len(creators)}</p>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Handle</th>
                            <th>Platform</th>
                            <th>Followers</th>
                            <th>Engagement</th>
                            <th>Consistency</th>
                            <th>Campaign Ready</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </body>
        </html>
        """

        return html
