import os
import sys
import threading
from datetime import datetime
from tkinter import filedialog
import customtkinter as ctk


class HardLinkHelperApp(ctk.CTk):
    """
    HardLink Helper - Main Application Window
    Phase 1: UI Framework (MVP)
    Phase 2: Core Logic & Safeguards
    """

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("HardLink Helper")
        self.geometry("760x600")
        self.minsize(680, 520)

        # Appearance configuration
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Configure root grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)  # Console expands vertically

        self._build_header()
        self._build_path_selection()
        self._build_action_area()
        self._build_console()

        # Initial greeting log
        self.log("HardLink Helper initialized.", level="INFO")
        self.log("Select a Source (Folder A) and Destination (Folder B) to begin.", level="INFO")

    def _build_header(self):
        """Header banner with title and brief description."""
        header_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            header_frame,
            text="HardLink Helper",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title_label.grid(row=0, column=0, sticky="w")

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Batch-create hard links from a source directory to a destination directory",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70")
        )
        subtitle_label.grid(row=1, column=0, sticky="w", pady=(2, 0))

    def _build_path_selection(self):
        """Source and Destination directory selectors."""
        paths_frame = ctk.CTkFrame(self, corner_radius=10)
        paths_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        paths_frame.grid_columnconfigure(1, weight=1)

        # --- Source Directory (Folder A) ---
        src_label = ctk.CTkLabel(
            paths_frame,
            text="Source (Folder A):",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        src_label.grid(row=0, column=0, padx=(15, 10), pady=(15, 10), sticky="w")

        self.src_entry = ctk.CTkEntry(
            paths_frame,
            placeholder_text="Path to source directory...",
            font=ctk.CTkFont(size=12)
        )
        self.src_entry.grid(row=0, column=1, padx=(0, 10), pady=(15, 10), sticky="ew")

        self.src_browse_btn = ctk.CTkButton(
            paths_frame,
            text="Browse...",
            width=90,
            command=self._browse_source
        )
        self.src_browse_btn.grid(row=0, column=2, padx=(0, 15), pady=(15, 10))

        # --- Destination Directory (Folder B) ---
        dst_label = ctk.CTkLabel(
            paths_frame,
            text="Destination (Folder B):",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        dst_label.grid(row=1, column=0, padx=(15, 10), pady=(0, 15), sticky="w")

        self.dst_entry = ctk.CTkEntry(
            paths_frame,
            placeholder_text="Path to destination directory...",
            font=ctk.CTkFont(size=12)
        )
        self.dst_entry.grid(row=1, column=1, padx=(0, 10), pady=(0, 15), sticky="ew")

        self.dst_browse_btn = ctk.CTkButton(
            paths_frame,
            text="Browse...",
            width=90,
            command=self._browse_destination
        )
        self.dst_browse_btn.grid(row=1, column=2, padx=(0, 15), pady=(0, 15))

    def _build_action_area(self):
        """Action area with prominent execution button."""
        action_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        action_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        action_frame.grid_columnconfigure(0, weight=1)

        self.execute_btn = ctk.CTkButton(
            action_frame,
            text="Create Hard Links",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=44,
            command=self._on_execute_click
        )
        self.execute_btn.grid(row=0, column=0, sticky="ew")

    def _build_console(self):
        """Scrollable text box console for logging and output."""
        console_container = ctk.CTkFrame(self, corner_radius=10)
        console_container.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="nsew")
        console_container.grid_columnconfigure(0, weight=1)
        console_container.grid_rowconfigure(1, weight=1)

        # Header bar above the console
        header_bar = ctk.CTkFrame(console_container, fg_color="transparent")
        header_bar.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="ew")
        header_bar.grid_columnconfigure(0, weight=1)

        console_title = ctk.CTkLabel(
            header_bar,
            text="Activity Log / Console",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        console_title.grid(row=0, column=0, sticky="w")

        clear_btn = ctk.CTkButton(
            header_bar,
            text="Clear Log",
            width=80,
            height=26,
            fg_color="transparent",
            border_width=1,
            text_color=("gray20", "gray85"),
            command=self._clear_console
        )
        clear_btn.grid(row=0, column=1, sticky="e")

        # Scrollable textbox
        self.console_textbox = ctk.CTkTextbox(
            console_container,
            wrap="word",
            font=ctk.CTkFont(family="Consolas" if sys.platform == "win32" else "Courier", size=12),
            state="disabled"
        )
        self.console_textbox.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="nsew")

    # --- UI Callbacks ---

    def _browse_source(self):
        current_dir = self.src_entry.get().strip() or os.getcwd()
        selected = filedialog.askdirectory(
            title="Select Source Directory (Folder A)",
            initialdir=current_dir if os.path.isdir(current_dir) else os.getcwd()
        )
        if selected:
            normalized_path = os.path.normpath(selected)
            self.src_entry.delete(0, "end")
            self.src_entry.insert(0, normalized_path)
            self.log(f"Source selected: {normalized_path}", level="INFO")

    def _browse_destination(self):
        current_dir = self.dst_entry.get().strip() or os.getcwd()
        selected = filedialog.askdirectory(
            title="Select Destination Directory (Folder B)",
            initialdir=current_dir if os.path.isdir(current_dir) else os.getcwd()
        )
        if selected:
            normalized_path = os.path.normpath(selected)
            self.dst_entry.delete(0, "end")
            self.dst_entry.insert(0, normalized_path)
            self.log(f"Destination selected: {normalized_path}", level="INFO")

    def _clear_console(self):
        self.console_textbox.configure(state="normal")
        self.console_textbox.delete("1.0", "end")
        self.console_textbox.configure(state="disabled")

    def log(self, message: str, level: str = "INFO"):
        """
        Thread-safe append of a formatted message to the UI console.
        Levels: INFO, WARN, ERROR, SKIPPED, SUCCESS
        """
        def _append():
            timestamp = datetime.now().strftime("%H:%M:%S")
            prefix = f"[{timestamp}] [{level}] "
            self.console_textbox.configure(state="normal")
            self.console_textbox.insert("end", f"{prefix}{message}\n")
            self.console_textbox.see("end")
            self.console_textbox.configure(state="disabled")

        # Safely schedule GUI update on main Tkinter thread
        self.after(0, _append)

    # --- Safeguards & Verification ---

    @staticmethod
    def _is_same_drive(path_a: str, path_b: str) -> bool:
        """
        Check if two paths reside on the same drive / filesystem mount.
        Hard links cannot cross filesystem or drive boundaries.
        """
        abs_a = os.path.abspath(path_a)
        abs_b = os.path.abspath(path_b)

        # On Windows, compare drive letters (e.g. 'C:', 'F:')
        drive_a, _ = os.path.splitdrive(abs_a)
        drive_b, _ = os.path.splitdrive(abs_b)
        if drive_a and drive_b:
            return drive_a.upper() == drive_b.upper()

        # Fallback / POSIX: Compare filesystem device IDs
        try:
            stat_a = os.stat(abs_a)
            stat_b = os.stat(abs_b)
            return stat_a.st_dev == stat_b.st_dev
        except OSError:
            return False

    # --- Core Execution Logic (Phase 2) ---

    def _on_execute_click(self):
        """Trigger hard link creation in a background thread."""
        src = self.src_entry.get().strip()
        dst = self.dst_entry.get().strip()

        # Validation: Check non-empty
        if not src or not dst:
            self.log("Please specify both Source (Folder A) and Destination (Folder B).", level="WARN")
            return

        # Disable button during processing
        self.execute_btn.configure(state="disabled", text="Processing...")

        # Run linking process in background thread to keep UI completely responsive
        threading.Thread(
            target=self._run_hardlink_process,
            args=(src, dst),
            daemon=True
        ).start()

    def _run_hardlink_process(self, src: str, dst: str):
        """Core process: scans, validates safeguards, and executes hard links."""
        try:
            src_abs = os.path.abspath(src)
            dst_abs = os.path.abspath(dst)

            self.log("=" * 64, level="INFO")
            self.log("Starting Hard Link batch operation...", level="INFO")
            self.log(f"  Source:      {src_abs}", level="INFO")
            self.log(f"  Destination: {dst_abs}", level="INFO")

            # Safeguard 1: Verify directories exist
            if not os.path.isdir(src_abs):
                self.log(f"Source folder does not exist or is not a directory: {src_abs}", level="ERROR")
                return

            if not os.path.isdir(dst_abs):
                self.log(f"Destination folder does not exist or is not a directory: {dst_abs}", level="ERROR")
                return

            # Safeguard 2: Verify source and destination are not identical
            if os.path.normcase(src_abs) == os.path.normcase(dst_abs):
                self.log("Source and Destination directories are identical. Operation aborted.", level="ERROR")
                return

            # Safeguard 3: Cross-Drive Prevention
            if not self._is_same_drive(src_abs, dst_abs):
                self.log(
                    f"Cross-Drive Error: Source ('{src_abs}') and Destination ('{dst_abs}') "
                    "are on different drives or mount points. Hard links cannot cross filesystem boundaries.",
                    level="ERROR"
                )
                self.log("Operation aborted due to cross-drive restriction.", level="ERROR")
                return

            # Scan root of Folder A
            try:
                raw_entries = os.listdir(src_abs)
            except OSError as err:
                self.log(f"Failed to read Source directory: {err}", level="ERROR")
                return

            # Safeguard 4: Directory Exclusion - only process files, exclude sub-directories
            files_to_process = []
            skipped_subdirs = 0

            for entry in raw_entries:
                entry_path = os.path.join(src_abs, entry)
                if os.path.isfile(entry_path):
                    files_to_process.append(entry)
                elif os.path.isdir(entry_path):
                    skipped_subdirs += 1

            if skipped_subdirs > 0:
                self.log(f"Excluded {skipped_subdirs} sub-directory(ies) (only files are linked).", level="INFO")

            if not files_to_process:
                self.log("No files found to link in the root of the Source directory.", level="WARN")
                return

            self.log(f"Found {len(files_to_process)} file(s) to process.", level="INFO")

            # Execution & Conflict Handling
            success_count = 0
            skipped_count = 0
            error_count = 0

            for filename in files_to_process:
                src_file = os.path.join(src_abs, filename)
                dst_file = os.path.join(dst_abs, filename)

                # Safeguard 5: Conflict Handling (do not overwrite existing files)
                if os.path.lexists(dst_file):
                    self.log(f"[SKIPPED] {filename} already exists. Do not overwrite.", level="SKIPPED")
                    skipped_count += 1
                    continue

                # Execution: Create hard link
                try:
                    os.link(src_file, dst_file)
                    self.log(f"[SUCCESS] Linked: {filename}", level="SUCCESS")
                    success_count += 1
                except OSError as err:
                    self.log(f"[ERROR] Failed to link {filename}: {err}", level="ERROR")
                    error_count += 1

            # Summary
            self.log(
                f"Batch completed: {success_count} linked, {skipped_count} skipped, {error_count} failed.",
                level="INFO"
            )
            self.log("=" * 64, level="INFO")

        finally:
            # Re-enable execution button on main thread
            self.after(0, lambda: self.execute_btn.configure(state="normal", text="Create Hard Links"))


def main():
    app = HardLinkHelperApp()
    app.mainloop()


if __name__ == "__main__":
    main()
