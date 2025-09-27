#!/usr/bin/env python3
"""
Standalone Web Embedder - Modern PySide6 Web Browser Application
A clean, standalone web browser using Qt WebEngine
"""

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QProgressBar, QLabel, QStatusBar,
    QToolBar, QMenuBar, QMenu, QMessageBox
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PySide6.QtCore import QUrl, Qt, Signal, QThread
from PySide6.QtGui import QAction, QIcon, QFont


class WebEmbedder(QMainWindow):
    """Modern web browser application using PySide6"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LaTeX to SVG Converter")
        self.setMinimumSize(400, 300)

        # Initialize web engine profile
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.setHttpUserAgent(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )

        # Suppress JavaScript console messages for cleaner output
        self.profile.settings().setAttribute(
            QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, False
        )
        # Note: Qt WebEngine doesn't have a direct way to suppress console messages,
        # but we can minimize them by disabling unnecessary features

        self.setup_ui()
        self.setup_menu()
        self.load_default_page()

    def setup_ui(self):
        """Set up the user interface"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create web view
        self.web_view = QWebEngineView()
        self.web_view.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)  # Disable right-click menu

        # Connect signals
        self.web_view.loadStarted.connect(self.on_load_started)
        self.web_view.loadProgress.connect(self.on_load_progress)
        self.web_view.loadFinished.connect(self.on_load_finished)
        self.web_view.titleChanged.connect(self.on_title_changed)

        # Suppress JavaScript console messages for cleaner output
        self.web_view.page().javaScriptConsoleMessage = self.suppress_console_messages

        layout.addWidget(self.web_view)

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Progress bar for loading
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setFixedHeight(15)
        self.status_bar.addPermanentWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)


    def setup_menu(self):
        """Set up the menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        new_window_action = QAction("New Window", self)
        new_window_action.triggered.connect(self.new_window)
        file_menu.addAction(new_window_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("View")

        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.triggered.connect(lambda: self.web_view.setZoomFactor(self.web_view.zoomFactor() + 0.1))
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.triggered.connect(lambda: self.web_view.setZoomFactor(self.web_view.zoomFactor() - 0.1))
        view_menu.addAction(zoom_out_action)

        reset_zoom_action = QAction("Reset Zoom", self)
        reset_zoom_action.triggered.connect(lambda: self.web_view.setZoomFactor(1.0))
        view_menu.addAction(reset_zoom_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def navigate_to_url(self):
        """Navigate to the URL in the address bar"""
        url_text = self.url_bar.text().strip()

        if not url_text:
            return

        # Add http:// if no protocol specified
        if not url_text.startswith(('http://', 'https://')):
            # Check if it looks like a URL or search terms
            if '.' in url_text and ' ' not in url_text:
                url_text = 'https://' + url_text
            else:
                # It's search terms, use DuckDuckGo
                url_text = f'https://duckduckgo.com/?q={url_text.replace(" ", "+")}'

        self.web_view.load(QUrl(url_text))

    def go_home(self):
        """Go to the home page"""
        self.web_view.load(QUrl("https://latex.cabhinav.com"))

    def new_window(self):
        """Open a new window"""
        new_app = QApplication.instance()
        if new_app:
            new_window = WebEmbedder()
            new_window.show()

    def load_default_page(self):
        """Load the default home page"""
        self.go_home()

    def on_load_started(self):
        """Called when page loading starts"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Loading...")

    def on_load_progress(self, progress):
        """Called during page loading progress"""
        self.progress_bar.setValue(progress)

    def on_load_finished(self, success):
        """Called when page loading finishes"""
        self.progress_bar.setVisible(False)

        if success:
            self.status_label.setText("Ready")
        else:
            self.status_label.setText("Failed to load page")

    def on_title_changed(self, title):
        """Called when page title changes"""
        if title:
            self.setWindowTitle(f"{title} - LaTeX to SVG Converter")
        else:
            self.setWindowTitle("LaTeX to SVG Converter")


    def suppress_console_messages(self, level, message, line_number, source_id):
        """Suppress JavaScript console messages for cleaner output"""
        # Suppress all console messages to reduce noise
        pass

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About LaTeX to SVG Converter",
            "LaTeX to SVG Conversion Tool\n"
            "Built with PySide6 and Qt WebEngine\n\n"
            "Convert LaTeX equations to SVG format."
        )

    def closeEvent(self, event):
        """Handle application close"""
        # Clean up web engine resources
        self.web_view.stop()
        self.profile.clearAllVisitedLinks()
        self.profile.clearHttpCache()
        event.accept()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("LaTeX to SVG Converter")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("LaTeX Tools")

    # Set application style
    app.setStyle("Fusion")

    # Create and show main window
    window = WebEmbedder()
    window.show()

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
