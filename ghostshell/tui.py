# ghostshell/tui.py

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Checkbox
from textual.containers import Container
from textual.reactive import reactive
from ghostshell.logs_viewer import query_logs

class GhostShellTUI(App):
    CSS_PATH = "tui.css"
    suspicious_only = reactive(False)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Checkbox("Show suspicious only", id="suspicious_toggle")
        yield Container(DataTable(id="log_table"))
        yield Footer()

    def on_mount(self) -> None:
        self.table = self.query_one("#log_table", DataTable)
        self.table.add_columns("Time", "Proto", "Local", "Remote", "Status", "PID", "Country", "ISP", "⚠️ Suspicious", "Reason")
        self.load_logs()

    def load_logs(self) -> None:
        logs = query_logs(limit=100, suspicious=self.suspicious_only)
        self.table.clear()

        for row in logs:
            cells = [str(cell) for cell in row]
            if row[8]:  # suspicious = 1
                styled_cells = [f"[bold red]{cell}[/bold red]" for cell in cells]
                self.table.add_row(*styled_cells)
            else:
                self.table.add_row(*cells)

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        if event.checkbox.id == "suspicious_toggle":
            self.suspicious_only = event.value
            self.load_logs()

if __name__ == "__main__":
    app = GhostShellTUI()
    app.run()
