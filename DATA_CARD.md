# Synthetic data and limitations

Reference and current batches are generated with NumPy seed 42. All identifiers,
dates, providers, and amounts are synthetic. There is no employer code or data.
This new portfolio demo illustrates selected skills discussed during an internship;
it is not a copy of Novacis Digital's framework and does not claim its check counts.

Current batch deliberately includes duplicate identifiers, missing identifiers,
a malformed date, a negative amount, a non-numeric amount, and a high amount.
Amount distributions also differ. A high value may be legitimate. Negative amounts
may represent refunds; the demo flags them for verification instead of deleting them.

Robust score = abs(x - median)/(1.4826*MAD), review threshold 3.5.
When MAD is zero, this check is marked unavailable rather than dividing by zero.
Amount PSI uses reference quantile boundaries and additive 0.5 smoothing; it is
sample-size dependent and not a hypothesis test. No universal PSI cutoff is asserted.
Missing columns stop analysis; schema additions/removals are reported by the CLI.
Data is not repaired automatically. Next steps: configurable domain rules, peer
groups, reviewed remediation actions, lineage, and streaming batch monitoring.
