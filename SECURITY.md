# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in PulseCraft, please report it responsibly:

1. **DO NOT** open a public GitHub issue
1. Email the security team at: [security@yourcompany.com] (replace with actual email)
1. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

We will acknowledge your report within 48 hours and work with you to understand and resolve the issue.

## Security Best Practices

### Environment Variables

1. **NEVER** commit `.env` files to version control
1. Use `.env.example` templates for documentation only
1. Store sensitive credentials in Azure Key Vault for production
1. Rotate credentials regularly

### Azure Security

1. Enable Azure Key Vault for all production secrets
1. Use Managed Identities for Azure service authentication
1. Enable Application Insights for security monitoring
1. Configure network security groups to restrict access
1. Enable Azure AD authentication where applicable

### Code Security

1. Run `npm audit` regularly to check for vulnerable dependencies
1. Keep all dependencies up to date
1. Validate and sanitize all user inputs
1. Use parameterized queries to prevent SQL injection
1. Implement rate limiting on API endpoints
1. Enable CORS only for trusted origins

### Data Privacy

1. Follow GDPR and privacy regulations
1. Encrypt sensitive data at rest and in transit
1. Implement proper access controls
1. Log access to customer data
1. Support data deletion requests

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Known Security Considerations

1. **Demo Mode**: The current implementation uses local file storage for demo purposes. This should be replaced with Azure Cosmos DB for production.
1. **Authentication**: No authentication is implemented in the MVP. Production deployment must include Azure AD B2C or similar.
1. **Rate Limiting**: Not implemented in MVP. Add rate limiting middleware before production deployment.

## Security Checklist for Production

- [ ] Replace file-based storage with Azure Cosmos DB
- [ ] Implement authentication and authorization
- [ ] Enable Azure Key Vault for secrets management
- [ ] Configure HTTPS/TLS for all endpoints
- [ ] Enable Application Insights security monitoring
- [ ] Implement rate limiting and DDoS protection
- [ ] Add input validation and sanitization
- [ ] Enable CORS for specific origins only
- [ ] Set up automated security scanning in CI/CD
- [ ] Conduct security audit/penetration testing
