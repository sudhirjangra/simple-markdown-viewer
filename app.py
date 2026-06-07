import sys
import os
import markdown
import webbrowser
from PyQt6.QtCore import QDir, Qt, QUrl
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QTreeView, QVBoxLayout, 
    QWidget, QToolBar, QFileDialog, QTabWidget, QTextBrowser
)
from PyQt6.QtGui import QAction, QFileSystemModel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings

# --- Custom Web Router ---
class MarkdownWebPage(QWebEnginePage):
    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.main_window = parent_window

    def acceptNavigationRequest(self, url, nav_type, isMainFrame):
        if nav_type == QWebEnginePage.NavigationType.NavigationTypeLinkClicked:
            if url.scheme() == 'file':
                file_path = url.toLocalFile()
                if file_path == self.main_window.current_file and url.hasFragment():
                    return True 
                if file_path.endswith('.md') or file_path.endswith('.markdown'):
                    self.main_window.open_specific_file(file_path)
                    return False
            if url.scheme() in ['http', 'https']:
                webbrowser.open(url.toString()) 
                return False
        return super().acceptNavigationRequest(url, nav_type, isMainFrame)

# --- Main Application ---
class MarkdownViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.is_dark_theme = True
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Markdown Reader - Sudhir Jangra")
        self.resize(1300, 800)

        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(main_splitter)

        # --- Sidebar ---
        self.sidebar_tabs = QTabWidget()
        
        self.file_model = QFileSystemModel()
        self.file_model.setFilter(QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)
        self.file_model.setNameFilters(["*.md", "*.markdown"])
        self.file_model.setNameFilterDisables(False)

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setHeaderHidden(True)
        for i in range(1, 4):
            self.tree_view.setColumnHidden(i, True)
        self.tree_view.clicked.connect(self.on_tree_clicked)
        
        self.sidebar_tabs.addTab(self.tree_view, "📁 Files")

        self.toc_viewer = QTextBrowser()
        self.toc_viewer.setOpenLinks(False)
        self.toc_viewer.anchorClicked.connect(self.on_toc_clicked)
        self.sidebar_tabs.addTab(self.toc_viewer, "📑 Outline")

        main_splitter.addWidget(self.sidebar_tabs)

        # --- Right Container ---
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)

        toolbar = QToolBar()
        right_layout.addWidget(toolbar)

        open_action = QAction("📁 Open Folder", self)
        open_action.triggered.connect(self.open_folder)
        toolbar.addAction(open_action)

        self.theme_action = QAction("🌓 Toggle Theme", self)
        self.theme_action.triggered.connect(self.toggle_theme)
        toolbar.addAction(self.theme_action)

        self.preview = QWebEngineView()
        self.preview.setPage(MarkdownWebPage(self))
        self.preview.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        self.preview.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        
        right_layout.addWidget(self.preview)
        main_splitter.addWidget(right_container)

        main_splitter.setSizes([300, 1000])
        self.set_directory(QDir.homePath())
        self.apply_theme()

    def open_folder(self):
        folder_selected = QFileDialog.getExistingDirectory(self, "Select Repository Directory")
        if folder_selected:
            self.set_directory(folder_selected)

    def set_directory(self, path):
        self.file_model.setRootPath(path)
        self.tree_view.setRootIndex(self.file_model.index(path))

    def on_tree_clicked(self, index):
        file_path = self.file_model.filePath(index)
        self.open_specific_file(file_path)

    def open_specific_file(self, file_path):
        if os.path.isfile(file_path) and file_path.endswith(('.md', '.markdown')):
            self.current_file = file_path
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.update_preview(content)

    def on_toc_clicked(self, url):
        fragment = url.fragment()
        if fragment:
            js = f"document.getElementById('{fragment}').scrollIntoView({{behavior: 'smooth'}});"
            self.preview.page().runJavaScript(js)

    def update_preview(self, raw_md):
        md = markdown.Markdown(extensions=['extra', 'toc', 'sane_lists'])
        html_content = md.convert(raw_md)
        
        # --- STYLIZED TABLE OF CONTENTS ---
        if md.toc:
            toc_color = "#58a6ff" if self.is_dark_theme else "#0969da"
            text_color = "#c9d1d9" if self.is_dark_theme else "#24292f"
            toc_html = f"""
            <html><head><style>
                body {{ font-family: -apple-system, sans-serif; color: {text_color}; }}
                .toc {{ font-size: 14px; line-height: 1.8; }}
                ul {{ list-style-type: none; padding-left: 15px; margin: 0; }}
                li {{ margin-top: 4px; }}
                a {{ text-decoration: none; color: {toc_color}; font-weight: 500; }}
            </style></head><body>
            <h3 style="margin-top: 0; border-bottom: 1px solid gray; padding-bottom: 5px;">Document Outline</h3>
            {md.toc}
            </body></html>
            """
            self.toc_viewer.setHtml(toc_html)
        else:
            self.toc_viewer.setHtml("<i>No headers found in this file.</i>")

        # --- GITHUB CSS ---
        if self.is_dark_theme:
            css = """
            body { font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; padding: 25px; line-height: 1.6; background-color: #0d1117; color: #c9d1d9; }
            h1, h2, h3 { border-bottom: 1px solid #21262d; padding-bottom: .3em; color: #c9d1d9; }
            code { background: #161b22; padding: 0.2em 0.4em; border-radius: 6px; font-family: monospace; }
            pre { background: #161b22; padding: 16px; border-radius: 6px; overflow: auto; border: 1px solid #30363d; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 16px; }
            th, td { border: 1px solid #30363d; padding: 6px 13px; }
            blockquote { border-left: .25em solid #30363d; padding: 0 1em; color: #8b949e; }
            img { max-width: 100%; box-sizing: content-box; }
            a { color: #58a6ff; text-decoration: none; }
            """
        else:
            css = """
            body { font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; padding: 25px; line-height: 1.6; background-color: #ffffff; color: #24292f; }
            h1, h2, h3 { border-bottom: 1px solid #d0d7de; padding-bottom: .3em; color: #24292f; }
            code { background: #f6f8fa; padding: 0.2em 0.4em; border-radius: 6px; font-family: monospace; }
            pre { background: #f6f8fa; padding: 16px; border-radius: 6px; overflow: auto; border: 1px solid #d0d7de; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 16px; }
            th, td { border: 1px solid #d0d7de; padding: 6px 13px; }
            blockquote { border-left: .25em solid #d0d7de; padding: 0 1em; color: #57606a; }
            img { max-width: 100%; box-sizing: content-box; }
            a { color: #0969da; text-decoration: none; }
            """

        full_html = f"<html><head><style>{css}</style></head><body>{html_content}</body></html>"
        base_url = QUrl.fromLocalFile(self.current_file) if self.current_file else QUrl("")
        self.preview.setHtml(full_html, baseUrl=base_url)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()
        if self.current_file:
            with open(self.current_file, 'r', encoding='utf-8') as f:
                self.update_preview(f.read())

    def apply_theme(self):
        if self.is_dark_theme:
            self.setStyleSheet("""
                QMainWindow { background-color: #1e1e1e; }
                QTabWidget::pane { border: none; border-right: 1px solid #3c3c3c; }
                QTabBar::tab { background: #252526; color: #cccccc; padding: 8px 15px; border: none; }
                QTabBar::tab:selected { background: #37373d; color: #ffffff; font-weight: bold; }
                QTreeView { background-color: #1e1e1e; color: #cccccc; border: none; font-size: 13px; padding-top: 5px; }
                QTreeView::item:hover { background-color: #2a2d2e; }
                QTreeView::item:selected { background-color: #37373d; color: #ffffff; }
                QTextBrowser { background-color: #1e1e1e; color: #cccccc; border: none; padding: 10px; }
                QToolBar { background-color: #3c3c3c; border: none; padding: 5px; }
                QToolBar QWidget { color: #ffffff; font-weight: bold; }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow { background-color: #ffffff; }
                QTabWidget::pane { border: none; border-right: 1px solid #dddddd; }
                QTabBar::tab { background: #f3f3f3; color: #333333; padding: 8px 15px; border: none; }
                QTabBar::tab:selected { background: #e4e4e4; color: #000000; font-weight: bold; }
                QTreeView { background-color: #ffffff; color: #333333; border: none; font-size: 13px; padding-top: 5px; }
                QTreeView::item:hover { background-color: #e4e4e4; }
                QTreeView::item:selected { background-color: #007acc; color: #ffffff; }
                QTextBrowser { background-color: #ffffff; color: #333333; border: none; padding: 10px; }
                QToolBar { background-color: #f3f3f3; border-bottom: 1px solid #dddddd; padding: 5px; }
                QToolBar QWidget { color: #333333; font-weight: bold; }
            """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MarkdownViewer()
    viewer.show()
    sys.exit(app.exec())