# Plan: Refine Session Logging

## Objective
Update the session logging mechanism to organize logs into date-based folders and use a sequential, titled naming convention. Ensure the improved structure supports both development and future project usage.

## Tasks

### Phase 1: Update Logging Logic
- [ ] **task-001**: Modify `VibeState` and `VibeSprint` to support new log path structure.
    - Start a new folder for each day: `session_logs/YYYY-MM-DD/`.
    - determine the next sequence number for the day.
    - naming convention: `NN-title.md` (e.g., `01-initial-setup.md`).

- [ ] **task-002**: Retain "Template" Log
    - Ensure `session_logs/TEMPLATE.md` (or similar) is preserved and not overwritten.
    - ignore development logs for the template project itself in git? (User said "WE don't need sesssion logs for the development *of this template project*", implying we should maybe gitignore them or just delete the current ones). *Clarification: User said "keep the log template", so I will ensure a template exists.*

### Phase 2: Migration & Cleanup
- [ ] **task-003**: Cleanup existing logs.
    - Move existing `session_logs/*.md` to `session_logs/archive/` or delete if irrelevant.
    - Ensure `session_logs/.gitkeep` or `TEMPLATE.md` exists.

### Phase 3: Verification
- [ ] **task-004**: Verify new log creation.
    - Run a test sprint start to see if it creates `session_logs/2026-02-10/01-test-sprint.md`.
