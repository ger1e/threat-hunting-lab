### Evidence-first threat hunting methodology

This document defines the public operating model behind the examples in this repository. It is intentionally vendor-practical and telemetry-first: a hunt is not considered useful because a query runs; it is useful when the hypothesis is falsifiable, the required telemetry is understood, the output is investigation-ready, and the result can drive a defensible decision.

#### 1. Intake and prioritization

A hunt candidate should begin with a concrete trigger rather than a query idea. Typical triggers include external threat intelligence, observed adversary behavior, incident lessons, ATT&CK technique coverage gaps, vulnerability exploitation, identity abuse patterns, control regressions, new enterprise technology, or repeated analyst pain.

A candidate is stronger when it can answer four questions:

- **Why now?** What changed, appeared, or remains insufficiently covered?
- **Why here?** Which enterprise surface or telemetry domain makes the behavior relevant?
- **What behavior?** What would an adversary actually do that produces observable evidence?
- **What decision?** What should an analyst be able to conclude or investigate from the output?

Indicators can seed a hunt, but indicator matching alone is not the hunt objective. The objective is the behavior, access path, capability, or relationship the indicator helps expose.

#### 2. Hypothesis contract

Every hunt should be reducible to a falsifiable statement:

> If the suspected behavior is occurring, then the required telemetry should contain observable pattern **X**, under conditions **Y**, with legitimate explanations **Z** considered.

A useful hypothesis names:

- the adversary behavior or abuse pattern;
- the expected observable evidence;
- the telemetry required to test it;
- the time horizon and population in scope;
- the expected benign collisions;
- what would weaken or falsify the hypothesis.

Avoid hypotheses that are simply product searches, IOC lists, or ATT&CK technique names without an observable behavior model.

#### 3. Telemetry readiness gate

Do not interpret an empty result set until telemetry readiness has been checked.

- **Availability** — does the required table/data source exist in the environment?
- **Coverage** — which users, devices, networks, tenants, platforms, or regions are represented?
- **Semantics** — do the fields mean what the query assumes they mean?
- **Retention** — does available history cover the behavior's expected dwell time or campaign window?
- **Latency** — how quickly does the source arrive, and can late ingestion change conclusions?
- **Fidelity** — is the event sufficiently detailed to distinguish the behavior from benign activity?
- **Joinability** — are stable identifiers available if cross-source correlation is required?
- **Control effects** — could filtering, proxying, EDR policy, privacy settings, or logging configuration hide the signal?

The minimum defensible statement for a negative hunt is not “nothing happened.” It is “no matching evidence was observed in the telemetry available for the defined scope and period.”

#### 4. Query engineering

The query should optimize for analyst value rather than clever syntax.

- constrain time and population early;
- filter on high-value behavioral primitives before expensive operations;
- aggregate early when raw event volume is unnecessary;
- avoid broad joins when a staged correlation or stable key is sufficient;
- project fields that support the next investigative action;
- retain timestamps, device/user identity, process/network context, source evidence, and correlation pivots where relevant;
- keep tunable assumptions visible rather than burying them in opaque logic;
- preserve enough context to distinguish “interesting” from “malicious.”

Performance limits are part of correctness. A theoretically precise hunt that routinely times out or exhausts platform limits is not production-useful.

#### 5. Evidence model

Evidence and inference should remain separate throughout the hunt.

1. **Lead** — an IOC, anomaly, external report, or weak signal that justifies investigation.
2. **Observed behavior** — telemetry directly shows a relevant action or sequence.
3. **Correlated behavior** — multiple events or telemetry sources support the same activity path.
4. **Contextual corroboration** — identity, infrastructure, malware, vulnerability, email, or CTI context independently strengthens the interpretation.
5. **Defensible finding** — the evidence supports a scoped conclusion with confidence, limitations, and plausible alternatives stated.

Do not promote confidence merely because multiple tools repeat the same upstream source. Preserve provenance so duplicated intelligence is not mistaken for independent corroboration.

#### 6. False positives and tuning

False-positive analysis is part of the first version of a hunt, not cleanup after deployment.

Document:

- known administrative and automation behavior;
- software deployment, monitoring, backup, RMM, and security tooling collisions;
- service accounts and shared infrastructure;
- expected regional, business-unit, or platform differences;
- thresholds that are behavioral assumptions rather than hard facts;
- exclusions and why each exclusion is safe.

Tune by removing known benign mechanisms while preserving the adversary behavior. Do not tune by excluding entire populations simply because they generate volume.

#### 7. CTI translation

External intelligence should pass through a translation step before becoming a hunt:

```text
SOURCE → PROVENANCE → CLAIM → CLIENT/TECH RELEVANCE → OBSERVABLE BEHAVIOR
      → TELEMETRY → HYPOTHESIS → QUERY → EVIDENCE → CONFIDENCE
```

Capture the original source URL, publication or observation time, actor/campaign claims, infrastructure or malware context, confidence, and any uncertainty. Separate confirmed technology overlap from assumed relevance.

#### 8. Hunt outcomes

A hunt can end in several useful states:

- **No evidence observed** — with scope and telemetry limitations recorded.
- **Benign pattern characterized** — producing tuning or allowlisting knowledge.
- **Finding / incident lead** — requiring deeper scoping or response.
- **Detection candidate** — behavior is repeatable and stable enough for continuous analytics.
- **Telemetry gap** — the hypothesis is valid but cannot be tested adequately.
- **Control gap** — evidence reveals a prevention, identity, logging, or hardening weakness.
- **Knowledge gain** — the hunt materially improves understanding even without a detection.

Not every hunt should become a scheduled analytic rule.

#### 9. Lifecycle states

`CANDIDATE → READY → ACTIVE → TUNED → PROMOTED / PARKED / RETIRED`

- **Candidate:** idea exists; relevance and telemetry not yet validated.
- **Ready:** hypothesis, scope, telemetry, and investigation path are defined.
- **Active:** hunt is being executed and evidence reviewed.
- **Tuned:** benign collisions and performance have been assessed.
- **Promoted:** converted into a detection, recurring hunt, playbook, or control improvement.
- **Parked:** useful idea blocked by telemetry, priority, or environmental constraints.
- **Retired:** behavior, technology, or intelligence basis is no longer relevant.

#### 10. Public-safety boundary

Public examples must never contain customer telemetry, internal hostnames, tenant identifiers, credentials, unpublished incident evidence, private architecture, proprietary rules, or sensitive infrastructure. Real operational work should be abstracted to the behavior, telemetry contract, and methodology required to understand the technique.

The goal of this repository is to demonstrate how hunts are reasoned about—not to publish production investigations.
