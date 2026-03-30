# Privacy Surface Mapper Instructions

## Overview

This skill maps personal data collection, storage, and processing to ensure privacy compliance (GDPR, CCPA).

## Execution Steps

### Step 1: Understand Data Requirements

1. **Read PM documents** from `docs/pm/{feature-name}/`:
   - PRD: identify what user data is collected and why
   - Extract data fields (name, email, phone, address, etc.)

### Step 2: Map Data Collection Points

**A. Find data collection code:**
- Search for form inputs, API endpoints collecting user data
- Search for user registration/profile endpoints
- Search for analytics/tracking code

**B. Classify data types:**
- **Personal Identifiable Information (PII):** name, email, phone, address
- **Sensitive data:** health info, financial data, biometric data
- **Behavioral data:** browsing history, preferences, usage patterns

### Step 3: Analyze Data Storage and Transmission

**A. Storage:**
- Where is data stored (database, files, cache)
- Is data encrypted at rest
- Data retention period

**B. Transmission:**
- Is data encrypted in transit (HTTPS)
- Third-party data sharing
- Cross-border data transfers

### Step 4: Check User Rights Implementation

**GDPR/CCPA requires:**
- Right to access (data export)
- Right to deletion (data erasure)
- Right to rectification (data correction)
- Right to portability (data download)

Search for implementation of these features.

### Step 5: Generate Privacy Map Report

Create `docs/security/{feature-name}/privacy-map.md`:

**Frontmatter:**
```yaml
---
feature: {feature-name}
version: v1
date: YYYY-MM-DD
last_updated: YYYY-MM-DD
---
```

**Report Structure:**

1. **Personal Data Inventory**
   - Table of all personal data collected
   - Data type, purpose, legal basis

2. **Data Flow Diagram**
   - Collection → Storage → Processing → Deletion

3. **Third-Party Data Sharing**
   - List of third parties receiving data
   - Purpose and legal basis

4. **User Rights Implementation Status**
   - Access: ✅/❌
   - Deletion: ✅/❌
   - Export: ✅/❌
   - Correction: ✅/❌

5. **Privacy Risks**
   - Compliance gaps
   - Missing consent mechanisms
   - Inadequate data protection

6. **Recommendations**
   - Priority fixes for compliance
   - Privacy policy updates needed

## Output Format

```markdown
## Personal Data Inventory

| Data Field | Type | Purpose | Legal Basis | Retention |
|-----------|------|---------|-------------|-----------|
| Email | PII | Account login | Contract | Account lifetime |
| Name | PII | Personalization | Consent | Account lifetime |
| IP Address | PII | Security | Legitimate interest | 90 days |

## User Rights Status

- ✅ Right to Access: Implemented via /api/user/export
- ❌ Right to Deletion: Not implemented
- ❌ Right to Export: Partial (missing transaction history)
- ✅ Right to Correction: Implemented via profile edit

## Privacy Risks

### [HIGH] Missing Data Deletion Endpoint

**Issue:** No way for users to delete their account and data

**Compliance Impact:** GDPR Article 17 violation

**Fix:** Implement account deletion endpoint with cascading data removal
```
