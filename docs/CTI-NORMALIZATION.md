<!-- GER1E-DOC-SCHEMA: v1 -->
<a id="cti-normalization-and-provenance-model"></a>
<div align="center">

<strong>CTI normalization and provenance model</strong><br/>
<sub>GER1E // THREAT HUNTING LAB // DOCUMENTATION</sub>

</div>

The repository's CTI schema is intentionally small, but the handling model is strict: enrichment should add context without erasing provenance, and correlation should not turn repeated reporting into artificial confidence.

<a id="core-principles"></a>
<sub><strong>01 // Core principles</strong></sub>

1. **Preserve source identity.** Keep the originating provider, source URL, and ingestion time with the observation.
2. **Separate source claims from analyst conclusions.** Actor, campaign, victim, or malware attribution can be reported by a source without becoming independently confirmed fact.
3. **Normalize observables, not meaning.** IPs, domains, URLs, hashes, and emails can share a common representation while retaining source-specific context.
4. **Retain time semantics.** `first_seen`, `last_seen`, publication time, and ingestion time describe different things and should not be collapsed.
5. **Deduplicate evidence carefully.** Multiple feeds repeating the same upstream report are not independent corroboration.
6. **Confidence needs a basis.** A numeric confidence score is useful only when the reason for the score is understood.

<a id="minimal-record"></a>
<sub><strong>02 // Minimal record</strong></sub>

The public schema in [`../cti-schema.json`](../cti-schema.json) requires `source`, `ingested_at`, and `confidence`. Optional fields carry source URL, observation times, actor/campaign/victim context, sector/geography, a normalized IOC, and free-form context.

<a id="normalization-pipeline"></a>
<sub><strong>03 // Normalization pipeline</strong></sub>

```text
COLLECT
  ↓
IDENTIFY SOURCE + RECORD PROVENANCE
  ↓
PARSE OBSERVABLES + CONTEXT
  ↓
NORMALIZE TYPES / TIMESTAMPS
  ↓
DEDUPLICATE WITHOUT LOSING SOURCE EVIDENCE
  ↓
ENRICH
  ↓
CORRELATE
  ↓
ASSESS RELEVANCE + CONFIDENCE
  ↓
HUNT / DETECTION / INVESTIGATION OUTPUT
```

<a id="provenance-rules"></a>
<sub><strong>04 // Provenance rules</strong></sub>

For every observation, retain enough information to answer:

- Who reported it?
- Where can the original report or record be found?
- When did the source first/last observe it?
- When was it ingested locally?
- Was actor/campaign attribution explicit, inferred, or absent?
- Which enrichment values came from another provider?
- Are two matching records genuinely independent or derived from the same upstream evidence?

<a id="observable-handling"></a>
<sub><strong>05 // Observable handling</strong></sub>

Normalize the basic type/value pair while preserving richer context separately.

<sub>Supported public-schema IOC types: `ip` · `domain` · `url` · `sha256` · `sha1` · `md5` · `email` · `other`</sub>

Normalization should avoid destructive transformations. For example, canonicalizing a domain to lowercase is reasonable; discarding the original URL path, source record, or surrounding campaign context is not.

<a id="confidence"></a>
<sub><strong>06 // Confidence</strong></sub>

A `0–100` confidence value should reflect evidence quality and context, not provider popularity. Useful considerations include:

- direct observation versus secondary reporting;
- recency and temporal consistency;
- source reliability and transparency;
- independent corroboration;
- infrastructure or malware linkage;
- ambiguity and legitimate-use prevalence;
- relevance to the technology/environment being investigated.

Confidence should decrease when the provenance chain is unclear or when corroborating sources appear to repeat the same upstream claim.

<a id="correlation"></a>
<sub><strong>07 // Correlation</strong></sub>

Correlation can use shared infrastructure, certificates, passive DNS, ASN/BGP context, malware configuration, campaign naming, victimology, temporal overlap, or behavioral similarity. A correlation should state which relationship is observed and which relationship is inferred.

- **Observed:** two domains resolve to the same IP during overlapping time windows.
- **Observed:** two samples contain the same C2 hostname.
- **Inferred:** the domains are operated by the same actor.
- **Inferred:** infrastructure reuse implies the same campaign.

The distinction matters because operational decisions should be based on the evidence actually available.

<a id="lifecycle"></a>
<sub><strong>08 // Lifecycle</strong></sub>

Indicators and context age differently. Operational pipelines should support:

- first/last-seen tracking;
- expiration or decay for stale indicators;
- revalidation when a value is reused by legitimate infrastructure;
- source withdrawal or correction;
- superseding confidence when stronger evidence appears;
- preserving historical provenance even after an indicator is no longer actionable.

<a id="public-safety-boundary"></a>
<sub><strong>09 // Public-safety boundary</strong></sub>

The public schema and examples are abstractions. Do not place private customer names, internal identifiers, proprietary intelligence, credentials, unpublished incident details, or sensitive infrastructure into this repository.

<p align="center"><sub>GER1E // THREAT HUNTING LAB // MOBILE-SAFE DOCUMENTATION</sub></p>
