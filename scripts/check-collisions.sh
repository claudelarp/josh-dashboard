#!/bin/zsh
# Vault-wide basename collision check. Obsidian resolves [[wikilinks]] by basename
# across the whole vault — a duplicate basename breaks linking silently.
# Exit 0 = clean, exit 1 = collisions printed.
cd "/Users/joshuanieman/Desktop/Josh Brain" || exit 2
DUPES=$(find wiki raw -name "*.md" | xargs -n1 basename | sort | uniq -d)
if [ -n "$DUPES" ]; then
  echo "BASENAME COLLISIONS:"
  echo "$DUPES"
  exit 1
fi
echo "clean"
exit 0
