# AI Coding Rules

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[中文](README.cn.md) | **English**

- Layered AI Rules configuration examples to meet different levels of AI coding assistant needs
- Includes meta-rules (rules for writing rules) to help AI generate new rule types reliably

## Directory Structure

```text
ai-coding-rules/
├── full-rules/                         # Full rules (MDC, docs and templates)
│   ├── ide-layer/
│   │   └── rulesets/                   # IDE layer rules (most general)
│   └── project-templates/              # Project templates (React/Vue/Python/Fullstack, etc.)
├── .concise-rules/                     # Concise rules (MDC, recommended for daily use)
│   ├── ide-layer/                      # IDE layer concise rules
│   └── project-templates/              # Project layer concise rules
├── .cursor/
│   └── rules/                          # Project-level rules used by this repo (MDC)
├── scripts/                            # Automation scripts (format, lint, migrate, reports)
├── tests/                              # Tests for scripts (pytest)
├── docs/                               # Guidance and design documents
│   ├── rule-writing-guide.md           # Rule writing guide
│   ├── ai-coding-tools.md              # AI coding tools recommendation (legacy)
│   ├── vibe-coding-tools.md            # AI coding tools recommendation (updated, for this repo)
│   ├── tech-stack-recommendation.md    # Tech stack recommendations
│   ├── mdc-frontmatter-spec.md         # MDC frontmatter specification
│   └── mdc-conditional-mode-analysis.md# MDC conditional mode analysis
├── .github/
│   └── workflows/                      # CI workflows (Markdown / rules / PR quality gate)
├── .pre-commit-config.yaml             # pre-commit hooks configuration
├── PRE_COMMIT_RULES.md                 # pre-commit configuration documentation
├── .markdownlint.json                  # Markdown lint rules
├── .prettierrc.yaml                    # Prettier config for JSON/YAML
├── pyproject.toml                      # Python project and Ruff configuration
├── uv.lock                             # uv dependency lockfile
├── IMPROVEMENT_PLAN.md                 # Improvement plan and progress
├── README.md                           # English README
├── README.cn.md                        # Chinese README
├── CONTRIBUTING.md                     # Contribution guide
├── CHANGELOG.md                        # Changelog
└── LICENSE                             # MIT License
```

## Dual-Track Rules System

This project provides **two rule systems** to balance readability and execution efficiency:

### ⚡ Concise Version (.concise-rules/) 【Recommended for Daily Use】

- **Purpose**: AI execution, improve efficiency, reduce costs
- **Features**: Concise, actionable, 73% token reduction
- **Use Cases**: Daily development, AI-assisted programming
- **Token Consumption**: ~700-1,000 tokens
- **File Count**: 13 rule files
- **Quick Start**:

  ```bash
  # 1. Copy IDE layer rules to global configuration (applies to all projects)
  mkdir -p ~/.cursor/rules
  cp .concise-rules/ide-layer/* ~/.cursor/rules/
  
  # 2. Copy project template rules to project directory (applies to current project only)
  # After entering your project directory, execute:
  mkdir -p .cursor/rules
  cp /path/to/ai-coding-rules/.concise-rules/project-templates/react-app/* .cursor/rules/
  ```

### 📦 Full Version (full-rules/)

- **Purpose**: Human reading, learning, team training
- **Features**: Detailed, comprehensive, rich examples
- **Use Cases**: Learning rule design concepts, team standards, deep understanding
- **Token Consumption**: ~2,600-3,900 tokens
- **File Count**: 21 rule files, totaling 2,998 lines
- **Usage Guide**:
  - [IDE Layer Usage Guide](./full-rules/ide-layer/README.md)
  - [Rule Writing Guide](./docs/rule-writing-guide.md)
  - [AI Coding Tools Recommendation](./docs/ai-coding-tools.md)

**Selection Recommendation**:

- **New Users**: Browse the full version first to understand rule design concepts, then switch to the concise version for daily use
- **Experienced Users**: Use the concise version directly, refer to specific parts of the full version when needed

## Usage Principles

1. **Layered Management**: IDE layer (general) → Language layer → Framework layer → Project layer (specific)
2. **Priority**: Lower layer rules override upper layer rules
3. **Progressive**: Start with preset templates, gradually refine

## Quick Start

### About Cursor Rules Directory

**Important**: Cursor IDE's official rules directory is `~/.cursor/rules/` (global rules) and `.cursor/rules/` (project rules).

- **Global Rules**: `~/.cursor/rules/` - Applies to all projects
- **Project Rules**: `.cursor/rules/` - Applies only to the current project (version controlled)

### Step 1: Install IDE Layer Rules

Copy IDE layer rules to Cursor configuration directory:

```bash
# Use concise version (recommended)
# Note: Cursor IDE official rules directory is ~/.cursor/rules/
mkdir -p ~/.cursor/rules
cp .concise-rules/ide-layer/* ~/.cursor/rules/

# Or use full version
cp full-rules/ide-layer/rulesets/* ~/.cursor/rules/
```

### Step 2: Add Project Template Rules

Based on project type, copy corresponding template rules to project root:

```bash
# Enter your project directory
cd /path/to/your/project

# Create .cursor/rules directory (Cursor official rules directory)
mkdir -p .cursor/rules

# Copy project template rules (using React as example)
cp /path/to/ai-coding-rules/.concise-rules/project-templates/react-app/* .cursor/rules/
```

### Step 3: Customize Project Rules

Add project-specific rule files in the project's `.cursor/rules/` directory.

**Tip**: Use symbolic links to keep rules synchronized:

```bash
# Use symbolic links (recommended)
# Note: Cursor IDE official rules directory is ~/.cursor/rules/
mkdir -p ~/.cursor/rules
ln -s /path/to/ai-coding-rules/.concise-rules/ide-layer/* ~/.cursor/rules/
```

## Detailed Documentation

- [IDE Layer Usage Guide](./full-rules/ide-layer/README.md)
- [React Application](./full-rules/project-templates/react-app/docs/coding-standards.md)
- [Vue Application](./full-rules/project-templates/vue-app/docs/coding-standards.md)
- [Python Backend](./full-rules/project-templates/python-backend/docs/coding-standards.md)
- [Golang Backend](./full-rules/project-templates/golang-app/docs/coding-standards.md)
- [Shell Scripts](./full-rules/project-templates/shell-scripts/docs/coding-standards.md)
- [Full-Stack Project](./full-rules/project-templates/fullstack-monorepo/docs/coding-standards.md)
- [Rule Writing Guide (including Agile and Design Patterns)](./docs/rule-writing-guide.md)

## Prompt Examples for Generating New Rule Types with AI

When you want to generate a new rule set (for a specific framework, tool, or workflow), you only need to describe the **goal** and tell the AI which rule files to follow. The implementation details (MDC structure, frontmatter, full vs concise, etc.) are already defined in the meta-rules.

```text
Strictly follow the meta-rules in `.cursor/rules/meta-rules.mdc` to generate a new rule set for "{tech stack / scenario}".
```

## 🔧 Recommended Tools

For a better AI coding experience, we recommend the following tools:

- **[Context7 MCP Server](https://github.com/upstash/context7)** ⭐⭐⭐⭐⭐
  - Get latest API documentation and code examples in real-time
  - Eliminate AI hallucinations, ensure code accuracy
  - Reduce code error rate by 55%
  - **System Requirements**: Node.js ≥ v18.0.0
  - **Quick Install**: `npx -y @upstash/context7-mcp --api-key YOUR_API_KEY`
  - **Configuration**: [Detailed Configuration Guide](./docs/ai-coding-tools.md#context7-mcp-server-)

- **[ast-grep](https://ast-grep.github.io/)** ⭐⭐⭐⭐☆
  - AST-based code search and refactoring tool
  - Verify quality of AI-generated code
  - Support for 40+ programming languages
  - **Install**: `npm i -g @ast-grep/cli`
  - **Configuration**: [Detailed Configuration Guide](./docs/ai-coding-tools.md#ast-grep-)

- **[Knowledge Graph Memory Server](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)** ⭐⭐⭐⭐☆
  - Maintain project context across sessions
  - Accumulate project knowledge and experience
  - Suitable for long-term project development
  - **Install**: `npm install @modelcontextprotocol/server-memory`
  - **Configuration**: [Detailed Configuration Guide](./docs/ai-coding-tools.md#knowledge-graph-memory-server-)

For detailed usage guide, please refer to [AI Coding Tools Recommendation Guide](./docs/ai-coding-tools.md).

## How to Contribute

If you want to add new project templates or improve existing rules, please refer to:

- [Contribution Guide](./CONTRIBUTING.md) - Learn about contribution process and standards
- [Rule Writing Guide](./docs/rule-writing-guide.md) - Detailed rule writing instructions

The rule writing guide includes:

- Rule layered architecture and priority
- File naming and organization standards
- Expression of Agile development principles
- Hierarchy distinction of software design patterns
- Complete process for creating new templates
- Common mistakes and how to avoid them

## License

This project is licensed under the [MIT License](./LICENSE).
