# Career and recruiting

LinkedIn.

## LinkedIn

```bash
# getprofile
mcporter call 'linkedin-scraper.get_person_profile(linkedin_url: "https://linkedin.com/in/username")'

# searchtalent
mcporter call 'linkedin-scraper.search_people(keyword: "AI engineer", limit: 10)'

# getcompany
mcporter call 'linkedin-scraper.get_company_profile(linkedin_url: "https://linkedin.com/company/xxx")'

# searchjobs
mcporter call 'linkedin-scraper.search_jobs(keyword: "software engineer", limit: 10)'
```

> **requireslog in**: LinkedIn scraper requireslogin session.

### Fallback Option

If MCP available, Jina Reader:

```bash
curl -s "https://r.jina.ai/https://linkedin.com/in/username"
```
