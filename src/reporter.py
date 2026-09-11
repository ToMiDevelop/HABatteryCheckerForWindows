import os
import markdown
from pathlib import Path
from messages import footers
import sys

class Reporter:
    def __init__(self, geminiResponse : str):
        self.markdownReport = geminiResponse

    @staticmethod
    def _get_base_dir() -> Path:
        """Zwraca folder, w którym znajduje się plik .exe (lub main.py w trybie deweloperskim)."""
        if getattr(sys, "frozen", False):
            # Aplikacja uruchomiona jako .exe z PyInstallera
            return Path(sys.executable).resolve().parent
        else:
            # Aplikacja uruchomiona z kodu źródłowego .py
            return Path(__file__).resolve().parent

    def saveAnalysisToHml(self, outputPath: str = "reports\report.html") -> str:
        """
        Converts Markdown text received  from Gemini to a good looking HTML
        with special tailored dedicated CSS.
        """
        # Markdown to HTML (with tables)
        htmlContent = markdown.markdown(self.markdownReport, extensions=['tables', 'fenced_code'])

        # Elegant html file structure with Home Assistant (dark mode)
        fullHtml = f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raport Baterii & Zigbee - Gemini AI</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #111827;
            color: #E5E7EB;
            line-height: 1.6;
            padding: 2rem;
            max-width: 900px;
            margin: 0 auto;
        }}
        h1, h2, h3 {{ color: #38BDF8; margin-top: 1.5rem; }}
        h1 {{ border-bottom: 2px solid #1F2937; padding-bottom: 0.5rem; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            background-color: #1F2937;
            border-radius: 8px;
            overflow: hidden;
        }}
        th, td {{ padding: 10px 14px; text-align: left; border-bottom: 1px solid #374151; }}
        th {{ background-color: #0F172A; color: #38BDF8; font-weight: 600; }}
        tr:hover {{ background-color: #2D3748; }}
        ul, ol {{ padding-left: 1.5rem; }}
        li {{ margin-bottom: 0.5rem; }}
        strong {{ color: #F43F5E; }}
        .footer {{
            margin-top: 3rem;
            font-size: 0.85rem;
            color: #9CA3AF;
            text-align: center;
            border-top: 1px solid #1F2937;
            padding-top: 1rem;
        }}
    </style>
</head>
<body>
    {htmlContent}
    <div class="footer">
        {footers["plFooter"]}
    </div>
</body>
</html>"""

        # 1. Taking the path to the program folder
        BASE_DIR = self._get_base_dir()
        # 2. Creating path to 'reports' next to program file
        reportsDir = BASE_DIR / "reports"
        reportsDir.mkdir(parents=True, exist_ok=True)
        # 3. full and safe path to HTML
        targetPath = reportsDir / "report.html"
        # 4. File saving
        with open(targetPath, "w", encoding="utf-8") as f:
            f.write(fullHtml)
        return str(targetPath)