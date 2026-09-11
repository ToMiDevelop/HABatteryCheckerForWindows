from pathlib import Path
import webview

class ReportWindow:
    def __init__(self, htmlPath: str):
        self.htmlPath = htmlPath

    def showReport(self) -> None:
        """Otwiera czyste okno GUI (WebView2 / Edge) z raportem HTML."""
        absPath = Path(self.htmlPath).resolve()
        # pywebview tworzy lekkie natywne okno w Windowsie (Edge WebView2)
        webview.create_window(
            title="Raport AI - Stan Baterii Urządzeń Zigbee",
            url=absPath.as_uri(),
            width=1000,
            height=750,
            resizable=True,
        )
        webview.start()