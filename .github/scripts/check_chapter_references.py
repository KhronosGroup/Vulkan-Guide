#!/usr/bin/env python3
# Copyright 2025 Holochip, Inc.
# SPDX-License-Identifier: Apache-2.0

"""
Script to ensure that all chapter files are properly referenced in the Guide
This script scans the chapters directory to identify all chapter files and checks if they are properly
referenced in the three files. If a chapter is missing from any of the files, the script can add it
to the appropriate section.
"""

import os
import re
import sys
from pathlib import Path

# Paths to the files that need to be checked
README_PATH = "README.adoc"
GUIDE_PATH = "guide.adoc"
NAV_PATH = "antora/modules/ROOT/nav.adoc"

# Directories to scan for chapter files
CHAPTERS_DIR = "chapters"
EXTENSIONS_DIR = os.path.join(CHAPTERS_DIR, "extensions")

def get_all_chapter_files():
    """
    Scan the chapters directory and its subdirectories to find all .adoc files.
    Returns a dictionary with relative paths as keys and file info as values.
    """
    chapter_files = {}

    # Scan main chapters directory
    for file in os.listdir(CHAPTERS_DIR):
        if file.endswith(".adoc") and os.path.isfile(os.path.join(CHAPTERS_DIR, file)):
            rel_path = os.path.join(CHAPTERS_DIR, file)
            chapter_files[rel_path] = {
                "name": file,
                "path": rel_path,
                "is_extension": False
            }

    # Scan extensions directory
    if os.path.exists(EXTENSIONS_DIR):
        for file in os.listdir(EXTENSIONS_DIR):
            if file.endswith(".adoc") and os.path.isfile(os.path.join(EXTENSIONS_DIR, file)):
                rel_path = os.path.join(EXTENSIONS_DIR, file)
                chapter_files[rel_path] = {
                    "name": file,
                    "path": rel_path,
                    "is_extension": True
                }

    return chapter_files

def extract_title_from_chapter(file_path):
    """
    Extract the title from a chapter file.
    Returns the title or the filename if no title is found.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

            # Look for a title pattern like "= Title" or "== Title"
            title_match = re.search(r'^=+\s+(.+?)$', content, re.MULTILINE)
            if title_match:
                return title_match.group(1).strip()

            # If no title found, use the filename without extension
            return os.path.splitext(os.path.basename(file_path))[0]
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return os.path.splitext(os.path.basename(file_path))[0]

def check_readme_references(chapter_files):
    """
    Check if all chapter files are referenced in README.adoc.
    Returns a list of files that are not referenced.
    """
    try:
        with open(README_PATH, 'r', encoding='utf-8') as f:
            readme_content = f.read()

        missing_files = []
        for file_path, info in chapter_files.items():
            # Convert path to the format used in README.adoc
            rel_path = file_path.replace(CHAPTERS_DIR + "/", "")

            # Check if the file is referenced in README.adoc
            if not re.search(rf'xref:\{{chapters\}}{re.escape(rel_path)}', readme_content):
                missing_files.append(info)

        return missing_files
    except Exception as e:
        print(f"Error checking README.adoc: {e}")
        return list(chapter_files.values())

def check_guide_references(chapter_files):
    """
    Check if all chapter files are referenced in guide.adoc.
    Returns a list of files that are not referenced.
    """
    try:
        with open(GUIDE_PATH, 'r', encoding='utf-8') as f:
            guide_content = f.read()

        missing_files = []
        for file_path, info in chapter_files.items():
            # Convert path to the format used in guide.adoc
            rel_path = file_path.replace(CHAPTERS_DIR + "/", "")

            # Check if the file is referenced in guide.adoc
            # The pattern needs to match both include:{chapters}file.adoc[] and include::{chapters}file.adoc[]
            if not (re.search(rf'include:\{{chapters\}}{re.escape(rel_path)}', guide_content) or
                   re.search(rf'include::\{{chapters\}}{re.escape(rel_path)}', guide_content)):
                missing_files.append(info)

        return missing_files
    except Exception as e:
        print(f"Error checking guide.adoc: {e}")
        return list(chapter_files.values())

def check_nav_references(chapter_files):
    """
    Check if all chapter files are referenced in nav.adoc.
    Returns a list of files that are not referenced.
    """
    try:
        with open(NAV_PATH, 'r', encoding='utf-8') as f:
            nav_content = f.read()

        missing_files = []
        for file_path, info in chapter_files.items():
            # Convert path to the format used in nav.adoc
            rel_path = file_path.replace(CHAPTERS_DIR + "/", "")

            # Check if the file is referenced in nav.adoc
            if not re.search(rf'xref:\{{chapters\}}{re.escape(rel_path)}', nav_content):
                missing_files.append(info)

        return missing_files
    except Exception as e:
        print(f"Error checking nav.adoc: {e}")
        return list(chapter_files.values())

def update_readme(missing_files):
    """
    Update README.adoc to include missing chapter references.
    Returns True if the file was updated, False otherwise.
    """
    if not missing_files:
        return False

    try:
        with open(README_PATH, 'r', encoding='utf-8') as f:
            content = f.readlines()

        # Find appropriate sections to add the missing files
        extensions_section_idx = None
        main_section_idx = None

        for i, line in enumerate(content):
            if "= When and Why to use Extensions" in line:
                extensions_section_idx = i
            elif "= Using Vulkan" in line:
                main_section_idx = i

        if extensions_section_idx is None or main_section_idx is None:
            print("Could not find appropriate sections in README.adoc")
            return False

        # Add missing files to appropriate sections
        for file_info in missing_files:
            title = extract_title_from_chapter(file_info["path"])
            rel_path = file_info["path"].replace(CHAPTERS_DIR + "/", "")

            if file_info["is_extension"]:
                # Add to extensions section
                content.insert(extensions_section_idx + 2, f"== xref:{{chapters}}{rel_path}[{title}]\n\n")
                extensions_section_idx += 2  # Adjust index for next insertion
            else:
                # Add to main section
                content.insert(main_section_idx + 2, f"== xref:{{chapters}}{rel_path}[{title}]\n\n")
                main_section_idx += 2  # Adjust index for next insertion

        # Write updated content back to file
        with open(README_PATH, 'w', encoding='utf-8') as f:
            f.writelines(content)

        return True
    except Exception as e:
        print(f"Error updating README.adoc: {e}")
        return False

def update_guide(missing_files):
    """
    Update guide.adoc to include missing chapter references.
    Returns True if the file was updated, False otherwise.
    """
    if not missing_files:
        return False

    try:
        with open(GUIDE_PATH, 'r', encoding='utf-8') as f:
            content = f.readlines()

        # Find appropriate sections to add the missing files
        extensions_section_idx = None
        main_section_idx = None

        for i, line in enumerate(content):
            if "= When and Why to use Extensions" in line:
                extensions_section_idx = i
            elif "= Using Vulkan" in line:
                main_section_idx = i

        if extensions_section_idx is None or main_section_idx is None:
            print("Could not find appropriate sections in guide.adoc")
            return False

        # Add missing files to appropriate sections
        for file_info in missing_files:
            rel_path = file_info["path"].replace(CHAPTERS_DIR + "/", "")

            if file_info["is_extension"]:
                # Add to extensions section
                content.insert(extensions_section_idx + 2, f"include::{{chapters}}{rel_path}[]\n\n")
                extensions_section_idx += 2  # Adjust index for next insertion
            else:
                # Add to main section
                content.insert(main_section_idx + 2, f"include::{{chapters}}{rel_path}[]\n\n")
                main_section_idx += 2  # Adjust index for next insertion

        # Write updated content back to file
        with open(GUIDE_PATH, 'w', encoding='utf-8') as f:
            f.writelines(content)

        return True
    except Exception as e:
        print(f"Error updating guide.adoc: {e}")
        return False

def update_nav(missing_files):
    """
    Update nav.adoc to include missing chapter references.
    Returns True if the file was updated, False otherwise.
    """
    if not missing_files:
        return False

    try:
        with open(NAV_PATH, 'r', encoding='utf-8') as f:
            content = f.readlines()

        # Find appropriate sections to add the missing files
        extensions_section_idx = None
        main_section_idx = None

        for i, line in enumerate(content):
            if "* When and Why to use Extensions" in line:
                extensions_section_idx = i
            elif "* Using Vulkan" in line:
                main_section_idx = i

        if extensions_section_idx is None or main_section_idx is None:
            print("Could not find appropriate sections in nav.adoc")
            return False

        # Add missing files to appropriate sections
        for file_info in missing_files:
            rel_path = file_info["path"].replace(CHAPTERS_DIR + "/", "")

            if file_info["is_extension"]:
                # Add to extensions section
                content.insert(extensions_section_idx + 1, f"** xref:{{chapters}}{rel_path}[]\n")
                extensions_section_idx += 1  # Adjust index for next insertion
            else:
                # Add to main section
                content.insert(main_section_idx + 1, f"** xref:{{chapters}}{rel_path}[]\n")
                main_section_idx += 1  # Adjust index for next insertion

        # Write updated content back to file
        with open(NAV_PATH, 'w', encoding='utf-8') as f:
            f.writelines(content)

        return True
    except Exception as e:
        print(f"Error updating nav.adoc: {e}")
        return False

def main():
    """
    Main function to check and update chapter references.
    """
    print("Checking chapter references...")

    # Get all chapter files
    chapter_files = get_all_chapter_files()
    print(f"Found {len(chapter_files)} chapter files")

    # Check if all chapter files are referenced in the three files
    readme_missing = check_readme_references(chapter_files)
    guide_missing = check_guide_references(chapter_files)
    nav_missing = check_nav_references(chapter_files)

    print(f"Missing from README.adoc: {len(readme_missing)}")
    print(f"Missing from guide.adoc: {len(guide_missing)}")
    print(f"Missing from nav.adoc: {len(nav_missing)}")

    # Update files if needed
    readme_updated = update_readme(readme_missing)
    guide_updated = update_guide(guide_missing)
    nav_updated = update_nav(nav_missing)

    if readme_updated:
        print("Updated README.adoc")
    if guide_updated:
        print("Updated guide.adoc")
    if nav_updated:
        print("Updated nav.adoc")

    # Return non-zero exit code if any files were missing references
    if readme_missing or guide_missing or nav_missing:
        print("Some chapter files were missing references and have been added.")
        return 1
    else:
        print("All chapter files are properly referenced.")
        return 0

if __name__ == "__main__":
    sys.exit(main())
