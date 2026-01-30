# Agent Instructions for atom-skills

This repository contains Agent Skills following the open standard (https://agentskills.io).

## Repository Structure

```
skills/
├── dev/        # Development
├── hr/         # Human Resources
├── finance/    # Finance
├── sales/      # Sales
└── common/     # Cross-domain
```

## Creating a Skill

### 1. Directory Structure

```
skills/<domain>/<skill-name>/
├── SKILL.md              # Required: Main skill definition
├── README.md             # Optional: Human documentation
└── templates/            # Optional: Supporting files
```

### 2. SKILL.md Format

```yaml
---
name: skill-name
description: One-line description of when to use this skill
---

# Skill Title

## When to Use
- Trigger conditions

## Process
1. Step one
2. Step two

## Examples
Concrete usage examples

## Cautions
- What NOT to do
```

**Required frontmatter:**
- `name`: Skill identifier (must match folder name)
- `description`: Used by AI to determine when to invoke

**Optional frontmatter:**
- `allowed-tools`: Tools the skill can access
- `context: fork`: Run in isolation
- `disable-model-invocation: true`: Prevent auto-invocation

### 3. Naming Rules

- Folder: `kebab-case` (e.g., `code-review`, `data-analysis`)
- Language: English preferred
- Be specific and concise

## Quality Checklist

Before submitting:
- [ ] `name` matches folder name
- [ ] `description` clearly states trigger condition
- [ ] Process steps are actionable
- [ ] Examples are concrete
- [ ] No hardcoded secrets or paths

## PR Process

1. Branch: `feat/<domain>/<skill-name>`
2. Create skill following structure above
3. Submit PR for review
4. Merge after approval

## Do NOT

- Create skills without clear use cases
- Include sensitive information
- Use non-standard frontmatter fields without documentation
- Duplicate existing skills
