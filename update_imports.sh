#!/bin/bash

# Update import paths for Python files
echo "Starting import path update for Python files..."

# Find all Python files in the project
find /workspaces/GPT-SoVITS -type f -name "*.py" | while read file; do
    # Skip files in the venv directory if it exists
    if [[ "$file" == *"venv"* ]]; then
        continue
    fi
    
    # Update direct imports for the moved modules
    # 1. Update Synthesizers imports
    sed -i 's/from Synthesizers\./from gpt_sovits.Synthesizers./g' "$file"
    sed -i 's/import Synthesizers\./import gpt_sovits.Synthesizers./g' "$file"
    
    # 2. Update tools imports
    sed -i 's/from tools\./from gpt_sovits.tools./g' "$file"
    sed -i 's/import tools\./import gpt_sovits.tools./g' "$file"
    
    # 3. Update src imports
    sed -i 's/from src\./from gpt_sovits.src./g' "$file"
    sed -i 's/import src\./import gpt_sovits.src./g' "$file"
    
    # 4. Update webuis imports
    sed -i 's/from webuis\./from gpt_sovits.webuis./g' "$file"
    sed -i 's/import webuis\./import gpt_sovits.webuis./g' "$file"
    
    # 5. Update GPT_SoVITS imports
    sed -i 's/from GPT_SoVITS\./from gpt_sovits.GPT_SoVITS./g' "$file"
    sed -i 's/import GPT_SoVITS\./import gpt_sovits.GPT_SoVITS./g' "$file"
    
    # Handle dynamic imports with f-strings and import_module
    sed -i 's/import_module(f"Synthesizers/import_module(f"gpt_sovits.Synthesizers/g' "$file"
    sed -i 's/import_module("Synthesizers/import_module("gpt_sovits.Synthesizers/g' "$file"
    
    # Update i18n path references
    sed -i 's#"Synthesizers/\(.*\)/configs/i18n/locale"#"gpt_sovits/Synthesizers/\1/configs/i18n/locale"#g' "$file"
    
    echo "Updated imports in $file"
done

# Update relative imports within the gpt_sovits package
find /workspaces/GPT-SoVITS/gpt_sovits -type f -name "*.py" | while read file; do
    # For files inside the gpt_sovits package, we may need to fix relative imports between components
    # that were previously at the same level but now are in different subpackages
    
    # Get the directory structure relative to gpt_sovits
    rel_path=${file#/workspaces/GPT-SoVITS/gpt_sovits/}
    dir_path=$(dirname "$rel_path")
    
    # If it's a direct subpackage like Synthesizers, tools, etc.
    if [[ "$dir_path" == "Synthesizers"* ]]; then
        # Fix imports from other direct subpackages
        sed -i 's/from \.\./from gpt_sovits./g' "$file"
    elif [[ "$dir_path" == "tools"* ]]; then
        sed -i 's/from \.\./from gpt_sovits./g' "$file"
    elif [[ "$dir_path" == "src"* ]]; then
        sed -i 's/from \.\./from gpt_sovits./g' "$file"
    elif [[ "$dir_path" == "webuis"* ]]; then
        sed -i 's/from \.\./from gpt_sovits./g' "$file"
    elif [[ "$dir_path" == "GPT_SoVITS"* ]]; then
        sed -i 's/from \.\./from gpt_sovits./g' "$file"
    fi
    
    echo "Checked relative imports in $file"
done

echo "Import path update completed!"
