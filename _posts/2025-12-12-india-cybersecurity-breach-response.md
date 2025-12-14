---
title: "India’s CERT issues rapid advisory after fintech breach"
description: "Incident response teams race to contain API credential leak impacting thousands of merchants."
author: ananya-singh
lang: en
categories: [cybersecurity]
tags: [cybersecurity, fintech, breach, india]
news_keywords: ["cybersecurity India", "fintech breach", "CERT advisory", "API security"]
image: "/assets/images/posts/cert-advisory.svg"
image_alt: "Security operations dashboard"
key_takeaways:
  - Compromised API keys rotated within six hours
  - CERT-In urges HMAC signing and IP allowlists
  - Merchants advised to audit third-party SDKs
last_modified_at: 2025-12-12 18:30:00 +05:30
---
India’s Computer Emergency Response Team (CERT-In) issued an urgent advisory after a leading fintech aggregator reported exposed API credentials affecting payment routing. The breach was detected during routine log analysis late Thursday.

Initial forensics indicate credentials were leaked from an outdated SDK used by multiple merchants. CERT-In recommended immediate key rotation, HMAC-based request signing, and IP allowlisting for all admin endpoints.

Affected payment flows were switched to backup gateways, limiting downtime to 14 minutes. Merchants have been asked to check tamper-proof logs and regenerate secrets stored in CI/CD pipelines.

> “Third-party SDK hygiene is now a board-level issue. We’re pushing mandatory key expiry and least-privilege policies,” a CERT-In official told KB Tech News.

The fintech sector has faced rising credential stuffing attacks in 2025, prompting regulators to tighten incident reporting timelines.
