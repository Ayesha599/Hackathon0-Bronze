# Skill: Task Analyzer

## Purpose
Analyze files in Needs_Action, identify task types, create action plans, and handle approvals.

## Capabilities

### 1. Analyze Files
- Scan all files in `/Needs_Action`
- Identify task type:
  - File drop
  - Payment request
  - Message/communication
  - Data processing
  - General task

### 2. Create Action Plan
- Write detailed action plan in `/Plans/Plan.md`
- Break down into sequential steps
- Include estimated priority

### 3. Approval Check
- Detect sensitive content:
  - Payments (especially >$500 per Company Handbook)
  - Personal information
  - Confidential data
- Write to `/Pending_Approval` if sensitive
- Include reason for flagging

### 4. Ralph Wiggum Loop (Multi-Step Tasks)
For complex multi-step tasks, use iterative approach:
```
Step 1: Analyze → Step 2: Plan → Step 3: Execute → Step 4: Verify → Loop back if needed
```
- Break task into smallest units
- Process one step at a time
- Verify each step before proceeding
- Loop until all steps complete

## Workflow
1. Scan `/Needs_Action` for files
2. Read each file and identify type
3. Check Company_Handbook.md for rules
4. Detect if approval needed (payments >$500, sensitive info)
5. If sensitive → copy to `/Pending_Approval` with note
6. Create action plan in `/Plans/Plan.md`
7. For multi-step: Apply Ralph Wiggum loop
8. Report findings and next actions

## Output Format
```
📊 Task Analysis Complete
File: [filename]
Type: [task type]
Approval Needed: [Yes/No + reason]
Plan: /Plans/Plan.md
Next: [recommended action]
```
