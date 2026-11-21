# HSMART Ownership and Marketplace Governance

## 1. Hybrid operating model

### HSMART Foundation
Responsible for mission, architecture constitution, interoperability standards, trust and certification policy, trademark policy, contribution governance, and community rules.

### Commercial Operator
Responsible for managed infrastructure, operations, billing, support, marketplace operations, service commitments, and enterprise delivery, subject to Foundation standards.

### Publisher
An independent individual or organization that owns or is authorized to distribute a capability. Publisher retains declared IP and grants HSMART and consumers only rights explicitly stated by the selected license and service terms.

This is an architecture and governance proposal, not legal advice or proof of corporate formation. Obtain legal review for entity structure, IP ownership, copyright assignments, trademarks, data roles, consumer terms, payments, taxes, liability, and licensing.

## 2. Separation of authority

| Action | Foundation | Operator | Publisher |
|---|---|---|---|
| Core standard change | Approves | Implements | Consulted |
| Managed infrastructure | Sets baseline | Operates | No default admin |
| Capability source | No automatic ownership | No automatic ownership | Owns/controls |
| Release publication | Sets policy | Operates pipeline | Submits and attests |
| Marketplace listing | Sets admission standard | Operates review | Owns listing claims |
| Access to capability | Defines policy framework | Enforces service | Declares requested permissions |
| Quarantine | Defines criteria/appeal | Executes response | Can remediate/appeal |
| Pricing | Policy oversight | Operates service pricing | Sets publisher price within terms |

## 3. Publisher lifecycle

applicant → identity_pending → verified → approved → active → restricted/suspended → revoked.

Verification level must be risk-proportionate. Higher-risk capabilities require stronger identity, ownership, and security evidence.

## 4. Listing requirements

Every listing discloses capability identity and publisher; current version and release channel; functional description and limitations; requested permissions and purpose; runtime mode and network egress; data classification and retention behavior; dependencies and external providers; license and usage terms; compatibility declarations; evaluation status and evidence; and support/deprecation policy.

A listing is not an execution grant. Invocation is separately authorized by identity, tenant policy, entitlement, permission scope, runtime constraints, and current release status.

## 5. Marketplace trust controls

Verified publisher identity; artifact signature and digest verification; provenance and SBOM where required; risk-based review; permission transparency and consent; abuse reporting, takedown, quarantine, and appeal; version history and security advisories; consumer notification for security-relevant changes.

## 6. Licensing and revenue

Licensing distinguishes source license, artifact distribution rights, hosted execution rights, data processing terms, trademark permission, support obligations, commercial use, and redistribution rights.

Marketplace payment, payout, tax, refunds, chargebacks, and revenue share require a selected payment provider and legal/financial review. Commercial rights must not be inferred solely from a repository's open-source license.

## 7. Content and security enforcement

The operator may restrict or quarantine a listing under published policy when credible evidence indicates malware, unauthorized data handling, rights infringement, credential theft, dangerous behavior, or policy evasion. Preserve evidence, record the decision, notify affected parties where appropriate, and provide an appeal path.

## 8. Governance records

Maintain versioned policies, publisher verification evidence, release approvals, listing reviews, exceptions, incident records, and appeals. Privileged decisions require actor, reason, timestamp, and evidence reference.
