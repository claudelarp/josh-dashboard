#!/bin/zsh
# Headless morning-brief run for launchd. Conservative tool allowlist; brief degrades
# honestly (stale-data sections) if a source is unreachable rather than stalling.
VAULT="/Users/joshuanieman/Desktop/Josh Brain"
CLAUDE="/Users/joshuanieman/.local/bin/claude"
LOG="$VAULT/scripts/.launchd-brief.log"
cd "$VAULT" || exit 1
{
  echo "=== $(date '+%Y-%m-%d %H:%M:%S') morning-brief run ==="
  "$CLAUDE" -p "Run the morning-brief skill: generate today's brief now." \
    --permission-mode acceptEdits \
    --allowedTools "Read,Write,Edit,Glob,Grep,Bash(mv:*),Skill,ToolSearch,mcp__claude_ai_Google_Calendar__list_events,mcp__claude_ai_Google_Calendar__list_calendars" \
    2>&1 | tail -20
  echo "=== exit: $? ==="
} >> "$LOG" 2>&1
