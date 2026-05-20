#!/bin/bash
# Removes CCA-copied skill directories listed in .ccaskills
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$(cd "$SCRIPT_DIR/../../skills" && pwd)"
SKILLS_DIR_REAL="$(cd "$SKILLS_DIR" && pwd -P)"
CCASKILLS="$SCRIPT_DIR/.ccaskills"

if [ ! -f "$CCASKILLS" ]; then
    echo "No .ccaskills file found, nothing to clean."
    exit 0
fi

while IFS= read -r skill; do
    skill="${skill%$'\r'}"
    [ -z "$skill" ] && continue

    case "$skill" in
        /*|*\\*|*/*|*..*)
            echo "Skipping invalid skill entry: $skill"
            continue
            ;;
    esac

    target="$SKILLS_DIR/$skill"
    if [ -d "$target" ]; then
        target_real="$(cd "$target" 2>/dev/null && pwd -P)"
        if [ -z "$target_real" ]; then
            echo "Skipping unresolved path: $skill"
            continue
        fi

        case "$target_real" in
            "$SKILLS_DIR_REAL"/*)
                rm -rf -- "$target_real"
                echo "Removed: $skill"
                ;;
            *)
                echo "Skipping out-of-scope path: $skill"
                ;;
        esac
    fi
done < "$CCASKILLS"

rm -f "$CCASKILLS"
echo "Cleanup complete."
