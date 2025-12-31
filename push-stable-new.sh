#!/bin/bash

# Script to push the stable-new branch to origin
# This script should be run by a user with push access to the repository

echo "Pushing stable-new branch to origin..."
git push origin stable-new

if [ $? -eq 0 ]; then
    echo "✓ Successfully pushed stable-new branch to origin"
    echo "✓ The branch is now available at: https://github.com/rsxdalv/GPT-SoVITS/tree/stable-new"
else
    echo "✗ Failed to push stable-new branch"
    echo "Please ensure you have push access to the repository"
    exit 1
fi
