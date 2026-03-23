# Technology Stack

**Project:** aiDriveUITest
**Researched:** 2026-03-23

## Recommended Stack

### Core Framework
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **Browser-Use** | 0.12+ | AI browser agent framework | Industry-leading 89.1% success rate on WebVoyager; native LLM integration; active development |
| **Playwright** | 1.50+ | Browser automation execution | Microsoft-backed; fastest execution; built-in parallelism; stable selectors; cross-browser support |
| **FastAPI** | 0.135+ | Backend API framework | Async-first; OpenAPI auto-generation; high performance; Python ecosystem compatibility |
| **React** | 19+ | Frontend framework | Component ecosystem; TypeScript support; React Query for state management |
| **TypeScript** | 5.9+ | Type safety | Catches errors early; improves maintainability; industry standard |

### Database
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **SQLite** | 3.x + aiosqlite | Data persistence | Zero-config; sufficient for single-team deployments; easy backup/migration |
| **SQLAlchemy** | 2.0+ | ORM | Async support; type safety; migration tools |

**Future consideration:** PostgreSQL for multi-tenant deployments or high-concurrency scenarios.

### Infrastructure
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **Uvicorn** | 0.34+ | ASGI server | Production-ready; WebSocket/SSE support; Windows compatibility via ProactorEventLoop |
| **Vite** | 7.3+ | Frontend build tool | Fast HMR; optimized builds; native TypeScript support |
| **Tailwind CSS** | 4.2+ | Styling | Utility-first; rapid prototyping; small bundle size |

### AI/LLM
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **Qwen 3.5 Plus** | Latest | Primary LLM via DashScope | Strong Chinese/English bilingual; visual agent capabilities; cost-effective for China |
| **OpenAI GPT-4o** | Latest | Alternative LLM | Best-in-class reasoning; fallback option; Azure deployment for enterprise |
| **LangChain** | 0.3+ | LLM abstraction | Multi-provider support; structured output; retry logic |

### Supporting Libraries
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **Pydantic** | 2.4+ | Data validation | All API schemas; configuration; CVE-2024-3772 fixed in 2.4+ |
| **httpx** | 0.28+ | HTTP client | API calls in preconditions; async support |
| **tenacity** | 8.0+ | Retry logic | LLM API calls; flaky network operations |
| **Jinja2** | 3.1+ | Template engine | Variable substitution in test descriptions |
| **Pytest** | 8.0+ | Testing framework | Unit/integration tests; async support via pytest-asyncio |
| **React Query** | 5.90+ | Server state | API caching; background refetching; optimistic updates |
| **React Router** | 7.13+ | Routing | SPA navigation; nested routes |

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| Browser Automation | Playwright | Selenium | Slower; less reliable selectors; no built-in parallelism |
| Browser Automation | Playwright | Puppeteer | Chrome-only; smaller ecosystem; less community support |
| AI Agent Framework | Browser-Use | Custom implementation | Reinventing the wheel; 89.1% success rate hard to match |
| AI Agent Framework | Browser-Use | MultiOn | Proprietary; less control; vendor lock-in |
| Backend Framework | FastAPI | Django | Heavier; async support less mature; overkill for API-only |
| Backend Framework | FastAPI | Flask | No async; manual OpenAPI; smaller ecosystem |
| Frontend Framework | React | Vue | Smaller hiring pool; less TypeScript ecosystem |
| Database | SQLite | PostgreSQL | Overkill for single-team; adds operational complexity |
| LLM Provider | Qwen | DeepSeek | No JSON mode; parsing errors in structured output |
| LLM Provider | Qwen | Claude | Higher cost; no DashScope integration in China |

## Installation

```bash
# Backend (using uv - recommended)
uv sync
uv run playwright install chromium

# Backend (using pip + venv)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

# Frontend
cd frontend
npm install
```

## Key Configuration

```env
# LLM Configuration (required)
DASHSCOPE_API_KEY=sk-xxx          # Qwen via Alibaba Cloud
OPENAI_API_KEY=sk-xxx              # Fallback/OpenAI mode
LLM_PROVIDER=qwen                  # qwen | openai | deepseek

# Target System (required)
ERP_BASE_URL=https://erp.example.com
ERP_USERNAME=test_user
ERP_PASSWORD=test_password

# External Integration (optional)
WEBSERP_PATH=/path/to/webseleniumerp
ERP_API_MODULE_PATH=/path/to/api/module

# Browser Configuration
BROWSER_MODE=launch                # launch | cdp
BROWSER_HEADLESS=true
```

## Sources

### Primary (HIGH confidence)
- [Browser-Use GitHub](https://github.com/browser-use/browser-use) - Official repository with benchmarks
- [Playwright Best Practices](https://playwright.dev/docs/best-practices) - Official documentation
- [FastAPI Production Tools 2026](https://aws.plainenglish.io/best-python-fastapi-production-tools-2026-complete-developer-guide-47b97be96d8b) - pytest + httpx recommended
- [Qwen 3.5 Multimodal Agents](https://qwen.ai/blog?id=qwen3.5) - Visual agent capabilities
- [CVE-2024-3772 NVD](https://nvd.nist.gov/vuln/detail/cve-2024-3772) - Pydantic vulnerability

### Secondary (MEDIUM confidence)
- [Best AI Browser Agents 2026](https://www.firecrawl.dev/blog/best-browser-agents) - Market analysis
- [Playwright MCP Servers for AI Testing](https://bug0.com/blog/playwright-mcp-servers-ai-testing) - Integration patterns
- [LangChain Migration Docs](https://tanstack.com/query/v5/docs/react/guides/migrating-to-v5) - React Query compatibility

---
*Stack research for: aiDriveUITest*
*Researched: 2026-03-23*
