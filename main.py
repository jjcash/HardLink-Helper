import fnmatch
import os
import sys
import threading
from datetime import datetime
from tkinter import filedialog, messagebox
import customtkinter as ctk


class HardLinkHelperApp(ctk.CTk):
    """
    HardLink Helper - Main Application Window
    Phase 1: UI Framework (MVP)
    Phase 2: Core Logic & Safeguards
    Phase 3: Advanced Features (Dry Run, Extension Filter, Recursive Mirroring, Symlink Fallback)
    """

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("HardLink Helper")
        self.geometry("780x680")
        self.minsize(700, 580)

        # Appearance configuration
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Configure root grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)  # Console expands vertically

        # Variables
        self.dry_run_var = ctk.BooleanVar(value=False)
        self.recursive_var = ctk.BooleanVar(value=False)

        self._build_header()
        self._build_path_selection()
        self._build_options_area()
        self._build_action_area()
        self._build_console()

        # Initial greeting log
        self.log("HardLink Helper initialized.", level="INFO")
        self.log("Select a Source (Folder A) and Destination (Folder B) to begin.", level="INFO")

    def _build_header(self):
        """Header banner with title and brief description."""
        header_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(15, 8), sticky="ew")
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
        paths_frame.grid(row=1, column=0, padx=20, pady=(5, 8), sticky="ew")
        paths_frame.grid_columnconfigure(1, weight=1)

        # --- Source Directory (Folder A) ---
        src_label = ctk.CTkLabel(
            paths_frame,
            text="Source (Folder A):",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        src_label.grid(row=0, column=0, padx=(15, 10), pady=(12, 6), sticky="w")

        self.src_entry = ctk.CTkEntry(
            paths_frame,
            placeholder_text="Path to source directory...",
            font=ctk.CTkFont(size=12)
        )
        self.src_entry.grid(row=0, column=1, padx=(0, 10), pady=(12, 6), sticky="ew")

        self.src_browse_btn = ctk.CTkButton(
            paths_frame,
            text="Browse...",
            width=90,
            command=self._browse_source
        )
        self.src_browse_btn.grid(row=0, column=2, padx=(0, 15), pady=(12, 6))

        # --- Destination Directory (Folder B) ---
        dst_label = ctk.CTkLabel(
            paths_frame,
            text="Destination (Folder B):",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        dst_label.grid(row=1, column=0, padx=(15, 10), pady=(6, 12), sticky="w")

        self.dst_entry = ctk.CTkEntry(
            paths_frame,
            placeholder_text="Path to destination directory...",
            font=ctk.CTkFont(size=12)
        )
        self.dst_entry.grid(row=1, column=1, padx=(0, 10), pady=(6, 12), sticky="ew")

        self.dst_browse_btn = ctk.CTkButton(
            paths_frame,
            text="Browse...",
            width=90,
            command=self._browse_destination
        )
        self.dst_browse_btn.grid(row=1, column=2, padx=(0, 15), pady=(6, 12))

    def _build_options_area(self):
        """Phase 3: Advanced Options (Filter, Dry Run, Recursive Mirroring)."""
        options_frame = ctk.CTkFrame(self, corner_radius=10)
        options_frame.grid(row=2, column=0, padx=20, pady=(0, 8), sticky="ew")
        options_frame.grid_columnconfigure(1, weight=1)

        # Extension Filter
        filter_label = ctk.CTkLabel(
            options_frame,
            text="Extension Filter:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        filter_label.grid(row=0, column=0, padx=(15, 10), pady=(12, 8), sticky="w")

        self.filter_entry = ctk.CTkEntry(
            options_frame,
            placeholder_text="Optional, e.g. *.mp4, *.jpg or .txt (leave blank for all files)",
            font=ctk.CTkFont(size=12)
        )
        self.filter_entry.grid(row=0, column=1, columnspan=2, padx=(0, 15), pady=(12, 8), sticky="ew")

        # Checkboxes row
        checkbox_container = ctk.CTkFrame(options_frame, fg_color="transparent")
        checkbox_container.grid(row=1, column=0, columnspan=3, padx=15, pady=(0, 12), sticky="w")

        self.dry_run_cb = ctk.CTkCheckBox(
            checkbox_container,
            text="Dry Run (Simulate without linking)",
            variable=self.dry_run_var,
            font=ctk.CTkFont(size=12),
            command=self._on_dry_run_toggle
        )
        self.dry_run_cb.pack(side="left", padx=(0, 25))

        self.recursive_cb = ctk.CTkCheckBox(
            checkbox_container,
            text="Include Subfolders (Recursive Mirroring)",
            variable=self.recursive_var,
            font=ctk.CTkFont(size=12)
        )
        self.recursive_cb.pack(side="left")

    def _build_action_area(self):
        """Action area with execution button."""
        action_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        action_frame.grid(row=3, column=0, padx=20, pady=(2, 8), sticky="ew")
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
        console_container.grid(row=4, column=0, padx=20, pady=(5, 18), sticky="nsew")
        console_container.grid_columnconfigure(0, weight=1)
        console_container.grid_rowconfigure(1, weight=1)

        # Header bar above console
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

    # --- UI Callbacks & Toggles ---

    def _on_dry_run_toggle(self):
        """Update execute button label to give clear visual feedback when Dry Run is active."""
        if self.dry_run_var.get():
            self.execute_btn.configure(text="Simulate Process (Dry Run)")
        else:
            self.execute_btn.configure(text="Create Hard Links")

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
        Levels: INFO, WARN, ERROR, SKIPPED, SUCCESS, DRYRUN
        """
        def _append():
            timestamp = datetime.now().strftime("%H:%M:%S")
            prefix = f"[{timestamp}] [{level}] "
            self.console_textbox.configure(state="normal")
            self.console_textbox.insert("end", f"{prefix}{message}\n")
            self.console_textbox.see("end")
            self.console_textbox.configure(state="disabled")

        self.after(0, _append)

    # --- Helpers: Safeguards, Patterns & Checks ---

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

    @staticmethod
    def _parse_extension_filters(filter_str: str) -> list[str]:
        """
        Parse user-entered filter string into fnmatch patterns.
        Handles comma/space/semicolon delimited items:
          e.g. '*.mp4, *.jpg', '.mp4 .jpg', 'mp4, jpg', 'video_*.mkv'
        """
        if not filter_str or not filter_str.strip():
            return []

        tokens = filter_str.replace(";", ",").replace(" ", ",").split(",")
        patterns = []
        for token in tokens:
            cleaned = token.strip()
            if not cleaned:
                continue
            if "*" in cleaned or "?" in cleaned:
                patterns.append(cleaned.lower())
            elif cleaned.startswith("."):
                patterns.append(f"*{cleaned.lower()}")
            else:
                patterns.append(f"*.{cleaned.lower()}")

        # Deduplicate while preserving order
        return list(dict.fromkeys(patterns))

    @staticmethod
    def _matches_filters(filename: str, patterns: list[str]) -> bool:
        """Check if a filename matches any of the filter patterns."""
        if not patterns:
            return True
        filename_lower = filename.lower()
        return any(fnmatch.fnmatch(filename_lower, pattern) for pattern in patterns)

    # --- Execution Logic & Workflow ---

    def _on_execute_click(self):
        """Pre-flight validation and startup on the UI thread."""
        src = self.src_entry.get().strip()
        dst = self.dst_entry.get().strip()
        dry_run = self.dry_run_var.get()
        include_subfolders = self.recursive_var.get()
        filter_text = self.filter_entry.get().strip()

        # Validation 1: Inputs provided
        if not src or not dst:
            self.log("Please specify both Source (Folder A) and Destination (Folder B).", level="WARN")
            return

        src_abs = os.path.abspath(src)
        dst_abs = os.path.abspath(dst)

        # Validation 2: Directories exist
        if not os.path.isdir(src_abs):
            self.log(f"Source folder does not exist or is not a directory: {src_abs}", level="ERROR")
            return

        if not os.path.isdir(dst_abs):
            self.log(f"Destination folder does not exist or is not a directory: {dst_abs}", level="ERROR")
            return

        # Validation 3: Not identical
        if os.path.normcase(src_abs) == os.path.normcase(dst_abs):
            self.log("Source and Destination directories are identical. Operation aborted.", level="ERROR")
            return

        # Safeguard / Fallback Check: Cross-Drive Prevention & Symlink Fallback
        use_symlinks = False
        if not self._is_same_drive(src_abs, dst_abs):
            # Prompt user for Symlink Fallback via modal popup dialog
            confirm = messagebox.askyesno(
                title="Cross-Drive Detected",
                message=(
                    "Source and Destination are on different drives or mount points.\n\n"
                    "Hard links cannot cross drives, but Soft Links (Symlinks) can.\n\n"
                    "Would you like to create Soft Links (Symlinks) instead?"
                ),
                parent=self
            )
            if confirm:
                use_symlinks = True
                self.log("Cross-drive detected: Proceeding with Soft Link (Symlink) fallback as approved.", level="INFO")
            else:
                self.log(
                    f"Cross-Drive Error: Source ('{src_abs}') and Destination ('{dst_abs}') are on different drives. "
                    "Operation aborted by user (symlink fallback declined).",
                    level="ERROR"
                )
                return

        # Disable button during execution
        original_btn_text = self.execute_btn.cget("text")
        self.execute_btn.configure(state="disabled", text="Processing...")

        # Parse filter patterns
        filter_patterns = self._parse_extension_filters(filter_text)

        # Run in worker thread
        threading.Thread(
            target=self._run_batch_process,
            args=(src_abs, dst_abs, dry_run, include_subfolders, filter_patterns, use_symlinks, original_btn_text),
            daemon=True
        ).start()

    def _run_batch_process(
        self,
        src_abs: str,
        dst_abs: str,
        dry_run: bool,
        include_subfolders: bool,
        filter_patterns: list[str],
        use_symlinks: bool,
        original_btn_text: str
    ):
        """Worker thread executing the linking/simulation logic."""
        try:
            link_type_name = "Symlinks" if use_symlinks else "Hard Links"
            mode_desc = "[SIMULATION - DRY RUN]" if dry_run else "[LIVE EXECUTION]"

            self.log("=" * 66, level="INFO")
            self.log(f"Starting {link_type_name} batch operation {mode_desc}", level="INFO")
            self.log(f"  Source:             {src_abs}", level="INFO")
            self.log(f"  Destination:        {dst_abs}", level="INFO")
            self.log(f"  Mode:               {'Dry Run (No files modified)' if dry_run else 'Live Link'}", level="INFO")
            self.log(f"  Recursive:          {'Yes (Include Subfolders)' if include_subfolders else 'No (Root files only)'}", level="INFO")
            if filter_patterns:
                self.log(f"  Extension Filter:   {', '.join(filter_patterns)}", level="INFO")
            else:
                self.log("  Extension Filter:   None (All files)", level="INFO")

            # Collect files to process: list of tuples (src_file_path, rel_file_path)
            candidate_files = []
            skipped_subdirs = 0

            if include_subfolders:
                # Recursive scan
                for root, dirs, files in os.walk(src_abs):
                    # Prevent endless loop if destination is inside source folder
                    if os.path.commonpath([src_abs]) == os.path.commonpath([src_abs, dst_abs]):
                        dirs[:] = [d for d in dirs if os.path.normcase(os.path.abspath(os.path.join(root, d))) != os.path.normcase(dst_abs)]

                    for f in files:
                        abs_file = os.path.join(root, f)
                        rel_file = os.path.relpath(abs_file, src_abs)
                        candidate_files.append((abs_file, rel_file))
            else:
                # Scan root of Folder A only
                try:
                    entries = os.listdir(src_abs)
                except OSError as err:
                    self.log(f"Failed to read Source directory: {err}", level="ERROR")
                    return

                for entry in entries:
                    entry_path = os.path.join(src_abs, entry)
                    if os.path.isfile(entry_path):
                        candidate_files.append((entry_path, entry))
                    elif os.path.isdir(entry_path):
                        skipped_subdirs += 1

                if skipped_subdirs > 0:
                    self.log(
                        f"Excluded {skipped_subdirs} sub-directory(ies) (enable 'Include Subfolders' to mirror sub-directories).",
                        level="INFO"
                    )

            if not candidate_files:
                self.log("No files found in the Source directory.", level="WARN")
                return

            # Apply extension filtering
            files_to_process = []
            filtered_out_count = 0

            for abs_src, rel_path in candidate_files:
                filename = os.path.basename(abs_src)
                if self._matches_filters(filename, filter_patterns):
                    files_to_process.append((abs_src, rel_path))
                else:
                    filtered_out_count += 1

            if filtered_out_count > 0:
                self.log(f"Filtered out {filtered_out_count} file(s) not matching extension filter.", level="INFO")

            if not files_to_process:
                self.log("No files matched the specified filter criteria.", level="WARN")
                return

            self.log(f"Found {len(files_to_process)} file(s) matching criteria to process.", level="INFO")

            # Execution loop
            success_count = 0
            skipped_count = 0
            error_count = 0

            for src_file, rel_path in files_to_process:
                dst_file = os.path.join(dst_abs, rel_path)
                dst_parent_dir = os.path.dirname(dst_file)

                # Conflict Handling: If file already exists in destination, skip and do not overwrite
                if os.path.lexists(dst_file):
                    self.log(f"[SKIPPED] {rel_path} already exists. Do not overwrite.", level="SKIPPED")
                    skipped_count += 1
                    continue

                if dry_run:
                    # Dry Run Simulation
                    if not os.path.exists(dst_parent_dir):
                        self.log(f"[DRY RUN] Would create folder: {dst_parent_dir}", level="INFO")
                    link_label = "Symlink" if use_symlinks else "Hard link"
                    self.log(f"[DRY RUN] Would create {link_label}: {rel_path}", level="INFO")
                    success_count += 1
                    continue

                # Live Execution
                # Ensure destination nested directory exists
                try:
                    if not os.path.exists(dst_parent_dir):
                        os.makedirs(dst_parent_dir, exist_ok=True)
                except OSError as dir_err:
                    self.log(f"[ERROR] Failed to create destination folder '{dst_parent_dir}': {dir_err}", level="ERROR")
                    error_count += 1
                    continue

                # Create link
                try:
                    if use_symlinks:
                        os.symlink(src_file, dst_file)
                        self.log(f"[SUCCESS] Symlinked: {rel_path}", level="SUCCESS")
                    else:
                        os.link(src_file, dst_file)
                        self.log(f"[SUCCESS] Linked: {rel_path}", level="SUCCESS")
                    success_count += 1
                except OSError as err:
                    if use_symlinks and sys.platform == "win32" and getattr(err, "winerror", None) == 1314:
                        self.log(
                            f"[ERROR] Failed to symlink '{rel_path}': Windows requires Developer Mode or Administrator privileges to create symlinks.",
                            level="ERROR"
                        )
                    else:
                        self.log(f"[ERROR] Failed to link '{rel_path}': {err}", level="ERROR")
                    error_count += 1

            # Summary
            verb = "simulated" if dry_run else "linked"
            self.log(
                f"Batch completed: {success_count} {verb}, {skipped_count} skipped, {error_count} failed.",
                level="INFO"
            )
            self.log("=" * 66, level="INFO")

        finally:
            # Restore execution button on main thread
            self.after(0, lambda: self.execute_btn.configure(state="normal", text=original_btn_text))


def main():
    app = HardLinkHelperApp()
    app.mainloop()


if __name__ == "__main__":
    main()
