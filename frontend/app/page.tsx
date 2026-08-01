export default function Home() {
  const recommendations = [
    {
      market: "Gold (XAU/USD)",
      action: "BUY",
      score: 94,
      confidence: "Very High",
      summary:
        "Weekly breakout confirmed with strong trend alignment across H4 and Daily.",
      reasons: [
        "Higher highs on Daily timeframe",
        "Momentum increasing",
        "USD weakening",
      ],
    },
    {
      market: "EUR/USD",
      action: "BUY",
      score: 88,
      confidence: "High",
      summary:
        "Bullish continuation following pullback into key support.",
      reasons: [
        "Bullish structure intact",
        "Support respected",
        "Positive momentum",
      ],
    },
    {
      market: "Crude Oil",
      action: "WATCH",
      score: 63,
      confidence: "Medium",
      summary:
        "Range-bound conditions. Wait for breakout confirmation.",
      reasons: [
        "No clear trend",
        "Mixed momentum",
        "Resistance overhead",
      ],
    },
  ];

  return (
    <main className="min-h-screen bg-zinc-950 text-white">
      <div className="max-w-7xl mx-auto p-8">

        {/* Header */}

        <div className="mb-10">
          <h1 className="text-5xl font-bold tracking-tight">
            Cerebro
          </h1>

          <p className="text-zinc-400 mt-2 text-lg">
            Market Intelligence for Forex & Commodities
          </p>
        </div>

        {/* AI Verdict */}

        <section className="rounded-2xl border border-amber-500/20 bg-gradient-to-r from-amber-500/10 to-zinc-900 p-8 mb-8">

          <div className="flex justify-between items-start">

            <div>
              <p className="uppercase tracking-widest text-xs text-amber-400">
                Today's Verdict
              </p>

              <h2 className="text-4xl font-bold mt-3">
                Buy Gold.
              </h2>

              <p className="text-zinc-300 mt-4 max-w-3xl">
                Gold shows the strongest combination of trend,
                momentum and macro alignment across all monitored
                markets. No other instrument currently exceeds its
                conviction score.
              </p>
            </div>

            <div className="text-right">
              <p className="text-sm text-zinc-400">
                Confidence
              </p>

              <div className="text-5xl font-bold text-amber-400">
                94
              </div>

              <p className="text-sm text-zinc-500">
                /100
              </p>
            </div>

          </div>

        </section>

        {/* Recommendations */}

        <div className="grid gap-6">

          {recommendations.map((market) => (

            <div
              key={market.market}
              className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6"
            >

              <div className="flex justify-between items-start">

                <div>

                  <h2 className="text-2xl font-semibold">
                    {market.market}
                  </h2>

                  <div className="flex gap-3 mt-3">

                    <span className="rounded-full bg-emerald-500/20 px-3 py-1 text-sm text-emerald-400">
                      {market.action}
                    </span>

                    <span className="rounded-full bg-zinc-800 px-3 py-1 text-sm text-zinc-300">
                      Score {market.score}
                    </span>

                    <span className="rounded-full bg-zinc-800 px-3 py-1 text-sm text-zinc-300">
                      {market.confidence}
                    </span>

                  </div>

                  <p className="text-zinc-300 mt-5 max-w-2xl">
                    {market.summary}
                  </p>

                  <div className="mt-5">

                    <p className="text-sm text-zinc-500 mb-2">
                      Key Reasons
                    </p>

                    <ul className="space-y-2">

                      {market.reasons.map((reason) => (

                        <li
                          key={reason}
                          className="text-sm text-zinc-300 flex items-center gap-2"
                        >
                          <span className="text-emerald-400">●</span>
                          {reason}
                        </li>

                      ))}

                    </ul>

                  </div>

                </div>

                <button className="rounded-xl bg-amber-500 px-5 py-3 font-semibold text-black hover:bg-amber-400 transition">
                  View Full Analysis →
                </button>

              </div>

            </div>

          ))}

        </div>

      </div>
    </main>
  );
}