# Install: pip install watchdog
# Run: python watchers/filesystem_watcher.py
# Test: Drop any file in /Inbox folder

import os
import time
import shutil
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
INBOX_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Inbox")
NEEDS_ACTION_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Needs_Action")
CHECK_INTERVAL = 5  # seconds

class InboxEventHandler(FileSystemEventHandler):
    """Handle file creation events in Inbox folder."""
    
    def __init__(self):
        self.processed_files = set()
    
    def on_created(self, event):
        """Handle new file creation."""
        if event.is_directory:
            return
        
        file_path = event.src_path
        filename = os.path.basename(file_path)
        
        # Skip if already processed
        if filename in self.processed_files:
            return
        
        # Skip temporary files (e.g., ~$filename, .tmp)
        if filename.startswith('~$') or filename.endswith('.tmp'):
            return
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] New file detected: {filename}")
        
        try:
            self.process_file(file_path, filename)
        except Exception as e:
            print(f"[ERROR] Failed to process {filename}: {str(e)}")
            # Skip bad files gracefully
            return
    
    def process_file(self, file_path, filename):
        """Process and move file to Needs_Action with metadata."""
        
        # Wait a moment to ensure file is fully written
        time.sleep(0.5)
        
        # Generate new filename with prefix
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_filename = f"FILE_{timestamp}_{filename}"
        new_file_path = os.path.join(NEEDS_ACTION_FOLDER, new_filename)
        
        # Get file size
        try:
            file_size = os.path.getsize(file_path)
        except OSError:
            file_size = 0
        
        # Copy file to Needs_Action
        shutil.copy2(file_path, new_file_path)
        print(f"[INFO] Copied: {filename} -> {new_filename}")
        
        # Create metadata file
        metadata_filename = f"FILE_{timestamp}_{os.path.splitext(filename)[0]}.md"
        metadata_path = os.path.join(NEEDS_ACTION_FOLDER, metadata_filename)
        
        metadata_content = f"""---
type: file_drop
original_name: {filename}
size: {file_size}
status: pending
timestamp: {datetime.now().isoformat()}
---

# File Drop: {filename}

## Details
- **Original Name:** {filename}
- **Size:** {file_size} bytes
- **Received:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Status:** Pending review

## Actions Required
- [ ] Review file contents
- [ ] Determine next steps
- [ ] Move to appropriate folder

"""
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write(metadata_content)
        
        print(f"[INFO] Metadata created: {metadata_filename}")
        
        # Mark as processed
        self.processed_files.add(filename)
        
        # Remove from processed set after some time to allow re-processing if needed
        def cleanup():
            time.sleep(60)
            self.processed_files.discard(filename)
        
        import threading
        threading.Thread(target=cleanup, daemon=True).start()
        
        print(f"[SUCCESS] File processing complete: {new_filename}")


def ensure_folders_exist():
    """Ensure required folders exist."""
    for folder in [INBOX_FOLDER, NEEDS_ACTION_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"[INFO] Created folder: {folder}")


def main():
    """Main function to start the file system watcher."""
    print("=" * 60)
    print("File System Watcher - Bronze Tier")
    print("=" * 60)
    print(f"Monitoring: {INBOX_FOLDER}")
    print(f"Output: {NEEDS_ACTION_FOLDER}")
    print(f"Check Interval: {CHECK_INTERVAL} seconds")
    print("=" * 60)
    print("Press Ctrl+C to stop...\n")
    
    # Ensure folders exist
    ensure_folders_exist()
    
    # Set up the observer
    event_handler = InboxEventHandler()
    observer = Observer()
    observer.schedule(event_handler, INBOX_FOLDER, recursive=False)
    
    # Start observing
    observer.start()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Watcher started successfully")
    
    try:
        while True:
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\n[INFO] Stopping watcher...")
        observer.stop()
    
    observer.join()
    print("[INFO] Watcher stopped")


if __name__ == "__main__":
    main()
