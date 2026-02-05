# Security Policy

## Supported Versions

Only the latest major version of this library receives security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Do not open an issue for security flaws.**

If you discover a security vulnerability, please send an email to **srivarenya.mudumba@gmail.com**. We will review it and respond within 48 hours.

## Dependency Management

This library locks versions of critical dependencies (`s3fs`, `zarr`) to prevent "dependency confusion" or breaking changes in the cloud stack. We regularly review and update dependencies to address known vulnerabilities.
