# Lessons from Building Claude Code: How We Use Skills

> **Author:** Thariq ([@trq212](https://x.com/trq212))  
> **Published:** March 17, 2026

---

Skills have become one of the most used extension points in Claude Code. They're flexible, easy to make, and simple to distribute.

But this flexibility also makes it hard to know what works best. What type of skills are worth making? What's the secret to writing a good skill? When do you share them with others?

We've been using skills in Claude Code extensively at Anthropic with hundreds of them in active use. These are the lessons we've learned about using skills to accelerate our development.

---

## What are Skills?

A common misconception is that skills are "just markdown files", but the most interesting part of skills is that they're **not just text files**. They're folders that can include scripts, assets, data, etc. that the agent can discover, explore and manipulate.

In Claude Code, skills also have a wide variety of configuration options including registering dynamic hooks. The most interesting skills use these configuration options and folder structure creatively.

---

## Types of Skills

After cataloging all of our skills, we noticed they cluster into a few recurring categories. The best skills fit cleanly into one; the more confusing ones straddle several.

### 1. Library & API Reference

Skills that explain how to correctly use a library, CLI, or SDKs — both internal libraries and common libraries that Claude Code sometimes has trouble with. These often include a folder of reference code snippets and a list of gotchas.

**Examples:**
- `billing-lib` — your internal billing library: edge cases, footguns, etc.
- `internal-platform-cli` — every subcommand of your internal CLI wrapper with examples
- `frontend-design` — make Claude better at your design system

---

### 2. Product Verification

Skills that describe how to test or verify that your code is working. Often paired with external tools like Playwright, tmux, etc.

Verification skills are extremely useful for ensuring Claude's output is correct. It can be worth having an engineer spend a week just making your verification skills excellent.

Consider techniques like:
- Having Claude record a video of its output
- Enforcing programmatic assertions on state at each step

**Examples:**
- `signup-flow-driver` — runs through signup → email verify → onboarding in a headless browser
- `checkout-verifier` — drives the checkout UI with Stripe test cards, verifies invoice state
- `tmux-cli-driver` — for interactive CLI testing that needs a TTY

---

### 3. Data Fetching & Analysis

Skills that connect to your data and monitoring stacks, including libraries to fetch data with credentials, dashboard IDs, and instructions on common workflows.

**Examples:**
- `funnel-query` — "which events do I join to see signup → activation → paid" plus canonical table info
- `cohort-compare` — compare two cohorts' retention or conversion, flag statistically significant deltas
- `grafana` — datasource UIDs, cluster names, problem → dashboard lookup table

---

### 4. Business Process & Team Automation

Skills that automate repetitive workflows into one command. Usually fairly simple instructions but may have more complicated dependencies on other skills or MCPs. Saving previous results in log files helps the model stay consistent.

**Examples:**
- `standup-post` — aggregates ticket tracker, GitHub activity, and prior Slack → formatted standup
- `create-<ticket-system>-ticket` — enforces schema (valid enum values, required fields) plus post-creation workflow
- `weekly-recap` — merged PRs + closed tickets + deploys → formatted recap post

---

### 5. Code Scaffolding & Templates

Skills that generate framework boilerplate for a specific function in the codebase. Especially useful when your scaffolding has natural language requirements that can't be purely covered by code.

**Examples:**
- `new-<framework>-workflow` — scaffolds a new service/workflow/handler with your annotations
- `new-migration` — your migration file template plus common gotchas
- `create-app` — new internal app with your auth, logging, and deploy config pre-wired

---

### 6. Code Quality & Review

Skills that enforce code quality and help review code. Can include deterministic scripts or tools for maximum robustness. May run automatically as part of hooks or inside a GitHub Action.

**Examples:**
- `adversarial-review` — spawns a fresh-eyes subagent to critique, implements fixes, iterates until findings degrade to nitpicks
- `code-style` — enforces code style, especially styles Claude does not do well by default
- `testing-practices` — instructions on how to write tests and what to test

---

### 7. CI/CD & Deployment

Skills that help you fetch, push, and deploy code inside your codebase. May reference other skills to collect data.

**Examples:**
- `babysit-pr` — monitors a PR → retries flaky CI → resolves merge conflicts → enables auto-merge
- `deploy-<service>` — build → smoke test → gradual traffic rollout with error-rate comparison → auto-rollback
- `cherry-pick-prod` — isolated worktree → cherry-pick → conflict resolution → PR with template

---

### 8. Runbooks

Skills that take a symptom (Slack thread, alert, or error signature), walk through a multi-tool investigation, and produce a structured report.

**Examples:**
- `<service>-debugging` — maps symptoms → tools → query patterns for your highest-traffic services
- `oncall-runner` — fetches the alert → checks the usual suspects → formats a finding
- `log-correlator` — given a request ID, pulls matching logs from every system that might have touched it

---

### 9. Infrastructure Operations

Skills that perform routine maintenance and operational procedures — some of which involve destructive actions that benefit from guardrails.

**Examples:**
- `<resource>-orphans` — finds orphaned pods/volumes → posts to Slack → soak period → user confirms → cascading cleanup
- `dependency-management` — your org's dependency approval workflow
- `cost-investigation` — "why did our storage/egress bill spike" with specific buckets and query patterns

---

## Tips for Making Skills

### Don't State the Obvious

Claude Code knows a lot about your codebase, and Claude knows a lot about coding. If you're publishing a knowledge-focused skill, focus on information that **pushes Claude out of its normal way of thinking**.

The `frontend-design` skill is a great example — built by iterating with customers on improving Claude's design taste, avoiding classic patterns like the Inter font and purple gradients.

### Build a Gotchas Section

The highest-signal content in any skill is the **Gotchas section**. These should be built up from common failure points that Claude runs into. Update your skill over time to capture new gotchas.

### Use the File System & Progressive Disclosure

A skill is a folder, not just a markdown file. Think of the entire file system as a form of **context engineering and progressive disclosure**.

- Split detailed function signatures into `references/api.md`
- Include template files in `assets/` for output formats
- Add folders of references, scripts, and examples

### Avoid Railroading Claude

Give Claude the information it needs, but give it **flexibility to adapt to the situation**. Being too specific in reusable skills can be counterproductive.

### Think through the Setup

Some skills need context from the user (e.g., which Slack channel to post to). A good pattern:
- Store setup information in a `config.json` file in the skill directory
- If the config is not set up, have the agent ask the user for information
- Use the `AskUserQuestion` tool to present structured, multiple choice questions

### The Description Field Is For the Model

When Claude Code starts a session, it builds a listing of every available skill with its description. This listing is what Claude scans to decide "is there a skill for this request?" The description field is not a summary — **it's a trigger condition for invocation**.

### Memory & Storing Data

Skills can include a form of memory by storing data within them:
- Simple: append-only text log file or JSON files
- Complex: a SQLite database

> ⚠️ Data stored in the skill directory may be deleted when you upgrade the skill. Use `${CLAUDE_PLUGIN_DATA}` as a stable folder per plugin.

### Store Scripts & Generate Code

Giving Claude scripts and libraries lets Claude spend its turns on **composition** — deciding what to do next rather than reconstructing boilerplate. Provide helper functions so Claude can compose them for complex analysis on the fly.

### On Demand Hooks

Skills can include hooks that are only activated when the skill is called, lasting for the duration of the session.

**Examples:**
- `/careful` — blocks `rm -rf`, `DROP TABLE`, force-push, `kubectl delete` via `PreToolUse` matcher on Bash
- `/freeze` — blocks any Edit/Write outside a specific directory (useful when debugging)

---

## Distributing Skills

Two ways to share skills with your team:

1. **Check skills into your repo** (under `./.claude/skills`)
2. **Create a plugin** and use a Claude Code Plugin marketplace

For smaller teams, checking skills into repos works well. But every checked-in skill adds a bit to the model's context. As you scale, an **internal plugin marketplace** lets your team selectively install what they need.

### Managing a Marketplace

- No need for a centralized team to decide — find the most useful skills organically
- Post candidate skills to a sandbox folder in GitHub and share via Slack
- Once a skill gains traction, the owner can PR it into the marketplace
- ⚠️ It can be easy to create bad or redundant skills — ensure some method of curation before release

### Composing Skills

Skills can depend on each other. Reference other skills by name, and the model will invoke them if they are installed. (Dependency management is not yet natively built into marketplaces.)

### Measuring Skills

Use a `PreToolUse` hook to log skill usage. This allows you to:
- Find popular skills
- Identify skills that are undertriggering compared to expectations

---

## Conclusion

Skills are incredibly powerful, flexible tools for agents, but it's still early and we're all figuring out how to use them best.

Think of this as a grab bag of useful tips rather than a definitive guide. The best way to understand skills is to **get started, experiment, and see what works for you**. Most skills began as a few lines and a single gotcha, and got better because people kept adding to them as Claude hit new edge cases.