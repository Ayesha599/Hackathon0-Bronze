# Skill: Basic File Handler

## Purpose
Handle markdown files from Needs_Action folder, create plans, and manage file workflow.

## Capabilities

### 1. Read and Summarize
- Read any `.md` file from `/Needs_Action`
- Summarize its contents clearly
- Identify key action items

### 2. Create Plan
- Write `Plan.md` in `/Plans` folder
- Include simple checkboxes for next steps
- Format: `- [ ] Step description`

### 3. Move Completed Files
- Move processed files from `/Needs_Action` to `/Done`
- Preserve original filename
- Log the move action in `/Logs`

## Rules (Always Reference Company_Handbook.md)
1. **Always be polite in replies**
2. **Flag Payments >$500 for approval** - Check for payment amounts before processing

## Workflow
1. Check `/Needs_Action` for `.md` files
2. Read `Company_Handbook.md` for rules
3. Read and summarize target file
4. Check for payment amounts >$500 → flag if found
5. Create `Plan.md` with checkboxes
6. On completion confirmation, move file to `/Done`
7. Output success message with full file path

## Output Format
```
✅ Success: [action]
File: [full path]
Summary: [brief summary]
Plan created: /Plans/Plan.md
```
