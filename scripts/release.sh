#!/bin/bash
# Create a new release
# Usage: ./scripts/release.sh [major|minor|patch]
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION_FILE="$PROJECT_DIR/VERSION"

# Read current version
CURRENT=$(cat "$VERSION_FILE" | tr -d '\n')
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

# Bump version based on argument
case "${1:-patch}" in
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    patch)
        PATCH=$((PATCH + 1))
        ;;
    *)
        echo "Usage: $0 [major|minor|patch]"
        exit 1
        ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"

echo "Bumping version: $CURRENT -> $NEW_VERSION"

# Update VERSION file
echo "$NEW_VERSION" > "$VERSION_FILE"

# Commit and tag
cd "$PROJECT_DIR"
git add VERSION
git commit -m "Release v$NEW_VERSION"
git tag "v$NEW_VERSION"

echo ""
echo "Created tag v$NEW_VERSION"
echo ""
echo "To publish:"
echo "  git push && git push --tags"
echo ""
echo "This will trigger GitHub Actions to build and release the firmware."
