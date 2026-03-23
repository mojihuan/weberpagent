# Feature Landscape

**Domain:** AI-driven UI automation testing platform
**Researched:** 2026-03-23

## Table Stakes

Features users expect. Missing = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **Natural language test authoring** | Core value proposition - QA shouldn't code | Medium | Already implemented via Browser-Use + Qwen |
| **Real-time execution monitoring** | Long-running tests need visibility | Medium | SSE streaming implemented; shows AI reasoning |
| **Screenshot capture** | Visual proof of test execution | Low | Playwright native support; implemented |
| **Test reports** | Documentation of results | Medium | Implemented with step details, assertions, timing |
| **Task management** | CRUD for test cases | Low | Standard CRUD operations implemented |
| **Assertion validation** | Verify expected outcomes | Medium | URL, text, no-errors assertions implemented |
| **Browser automation** | Execute UI interactions | High | Playwright integration; browser-use handles complexity |
| **Error handling & retry** | Tests fail; need resilience | Medium | Tenacity retry implemented; LLM retry logic |

## Differentiators

Features that set product apart. Not expected, but valued.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Precondition system** | Prepare test environment with Python code | High | UNIQUE - Allows API calls, data setup, variable passing |
| **External operation integration** | Connect to webseleniumerp operations | High | UNIQUE - FA1/HC1 operation codes; business logic reuse |
| **Three-layer assertions** | Data + API params + field params | High | UNIQUE - FieldParamsEditor with "now" button; AST-based discovery |
| **Variable substitution** | {{variable}} syntax across steps | Medium | Jinja2 templates; context passing between steps |
| **Multi-LLM support** | Qwen, OpenAI, DeepSeek, Azure | Medium | Factory pattern; provider switching |
| **Chinese NLP optimization** | Native Chinese test descriptions | Medium | Qwen 3.5 Plus excels at Chinese understanding |
| **API assertion layer** | Separate from UI assertions | Medium | Time-based and data-based API validation |
| **Context storage** | Persist data across execution | Low | Enables data flow between steps and assertions |

## Anti-Features

Features to explicitly NOT build.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| **Code-based test authoring** | Defeats natural language value proposition | Improve NLP understanding; add more natural patterns |
| **Video recording** | Storage cost; screenshots sufficient | Screenshot on every step; GIF compilation for reports |
| **Cross-browser testing** | Maintenance overhead; Chrome dominates | Focus on Chromium; add Firefox/WebKit only if demanded |
| **Mobile testing** | Different interaction model; scope creep | Keep desktop-first; consider mobile as separate product |
| **Visual regression testing** | High false positive rate; maintenance burden | Use AI-powered visual assertions (future enhancement) |
| **Low-code test builder** | Reinvents Selenium IDE; limited expressiveness | Invest in better natural language understanding |
| **Test case import from other tools** | One-time migration; not core value | Provide API for programmatic import; manual migration acceptable |
| **Real-time collaboration** | Complex; most teams don't need it | Single-user focus; future team features via locking |

## Feature Dependencies

```
Natural Language Input
    |
    v
Browser-Use Agent (LLM Decision)
    |
    v
Playwright Execution
    |
    +---> Screenshot Capture
    |
    +---> Assertion Validation
            |
            +---> URL Check
            +---> Text Exists
            +---> No Errors
            +---> API Assertions (external)
            +---> Business Assertions (PcAssert/MgAssert/McAssert)

Precondition System
    |
    v
Python Code Execution
    |
    +---> API Calls (requests/httpx)
    +---> External Operations (FA1/HC1)
    +---> Data Methods (inventory_list_data)
    |
    v
Context Storage
    |
    v
Variable Substitution ({{variable}})
    |
    v
Test Description Enhancement
```

## MVP Recommendation

Prioritize:
1. **Natural language execution** (table stakes, core value)
2. **Real-time monitoring with SSE** (table stakes, user confidence)
3. **Precondition system** (differentiator, enables complex scenarios)

Defer:
- **External operation integration**: Requires webseleniumerp setup; implement after core stable
- **Three-layer assertions**: Advanced feature; start with simple assertions
- **Multi-LLM support**: Qwen sufficient for MVP; add alternatives based on demand

## Competitive Analysis

| Feature | aiDriveUITest | QA Wolf | Testim | Applitools |
|---------|---------------|---------|--------|------------|
| Natural language input | YES | Limited | NO | NO |
| Chinese NLP | YES | NO | NO | NO |
| Precondition code | YES | NO | NO | NO |
| External integration | YES | NO | Limited | NO |
| Self-healing selectors | Via browser-use | YES | YES | NO |
| Visual AI | NO | NO | YES | YES |
| Cloud execution | Planned | YES | YES | YES |
| Pricing | Self-hosted | SaaS | SaaS | SaaS |

## Sources

- [Best AI Testing Tools 2026](https://www.qawolf.com/blog/the-13-best-ai-testing-tools-in-2026) - Market landscape
- [Test Automation Trends 2026](https://www.testdevlab.com/blog/test-automation-trends-2026) - Industry direction
- [AI Browser Agents Comparison](https://o-mega.ai/articles/top-10-browser-use-agents-full-review-2026) - Browser-use benchmarks
- [Natural Language Test Automation](https://mechasm.ai/blog/how-to-use-nlp-for-test-case-generation) - NLP patterns
