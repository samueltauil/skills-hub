"""Reader-facing wording for the cost reduction actions.

Kept apart from `actions.py` so the merge logic reads as logic and the copy can
be reviewed (or translated) on its own. Nothing here makes a decision.
"""

# --- Verdict labels, keyed on `assurance.level` ------------------------------
LEVEL_LABELS = {
    "unmeasured": "Not quantified",
    "estimated": "Estimated — your call",
    "judgement": "Your call",
    "confirm": "Confirm before applying",
    "ready": "Ready to apply",
}

# --- How the saving was arrived at -------------------------------------------
HOW_MEASURED_LEVER = "The saving is measured against your billing metrics."
HOW_MEASURED_RULE = (
    "The saving is projected from this stream's share of a log sample, not"
    " read from a billing metric, so treat it as an estimate. The filter"
    " itself is exact."
)

# --- What the reader still has to decide (a lever's `flag`) ------------------
FLAG_INTENT_INFERRED = (
    "An exclusion rule on this project says this volume was meant to be"
    " dropped, but that rule no longer matches the stream carrying it."
    " Confirm dropping the stream is still what you want."
)
FLAG_NOT_QUANTIFIED = (
    "The change is real, but the metrics used here do not expose the"
    " volume behind it, so no saving is claimed."
)

CONFIDENCE_MEANINGS = {
    "high": "Removing this is routine and rarely costs a signal anyone wanted.",
    "medium": "There is a trade-off here; read the evidence before applying.",
    "low": (
        "The case for removing this is weak; read the evidence before acting."
    ),
}

SCOPE_JUDGEMENT = {
    "stream": (
        "Applying this stops every log of this severity in the stream being"
        " ingested."
    ),
    "signature": (
        "Applying this drops only the matching lines; the rest of the stream is"
        " still ingested."
    ),
}
READ_SAMPLE = " Read the example log below before deciding."

ALTERNATIVE_TO = (
    'An alternative to "{title}" on the same stream: applying both does not'
    " save the sum of the two figures."
)

# --- Security telemetry ------------------------------------------------------
SECURITY_CAVEAT_DROPS = (
    "This is security telemetry: dropping it removes {what}. Teams do drop it"
    " for cost, but check first whether an audit obligation or an"
    " incident-response process depends on it."
)
SECURITY_CAVEAT_REDUCES = (
    "This is security telemetry: {what}. It is still captured after this"
    " change, at lower fidelity, so check whoever relies on it can work with"
    " the coarser data."
)

# --- Why something is not offered --------------------------------------------
WITHHELD_NO_VOLUME = "no volume measured, so no saving can be quoted"
WITHHELD_NO_REMEDY = (
    "no exclusion filter could be built for the streams it measured, so there"
    " is nothing to apply"
)
WITHHELD_DATA_ACCESS = (
    "{gib:.1f} GiB/mo of Data Access audit logs, left out of the savings"
    " figure because it is a compliance decision: disabling or excluding them"
    " is frequently prohibited by audit, regulatory or security policy, so the"
    " owner must confirm with their compliance team before acting."
)

REFUSED_NO_LOG_ID = (
    "the stream has no log ID, so a filter for it would match every stream in"
    " the project"
)
REFUSED_FILTER_TOO_LONG = (
    "does not fit within Cloud Logging's {limit:,}-character exclusion filter"
    " limit; add a second exclusion for the remaining streams"
)
