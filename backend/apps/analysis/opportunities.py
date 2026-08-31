class OpportunityScanner:

    def scan(self, results):

        opportunities = []

        for result in results:

            analysis = result.get("analysis", {})
            decision = analysis.get("decision")

            if not decision:
                continue

            if decision.get("signal") not in ("BUY", "SELL"):
                continue

            if decision.get("entry") is None:
                continue

            if decision.get("stop_loss") is None:
                continue

            if decision.get("take_profit") is None:
                continue

            opportunities.append({
                "date": result.get("date"),
                "experiment": result.get("experiment"),

                "signal": decision["signal"],
                "action": decision.get("action"),

                "confidence": decision.get("confidence"),

                "entry": decision["entry"],
                "stop_loss": decision["stop_loss"],
                "take_profit": decision["take_profit"],

                "reasons": decision.get(
                    "reasons",
                    [],
                ),
            })

        return opportunities