import { useState, useCallback, useRef } from "react";

const URN1 = { id: 0, label: "Urn I", ones: 4, tens: 6 };
const URN2 = { id: 1, label: "Urn II", ones: 3, tens: 7 };

function buildChips(urn) {
  return [
    ...Array(urn.ones).fill(1).map((v, i) => ({ id: `1-${i}`, val: 1 })),
    ...Array(urn.tens).fill(10).map((v, i) => ({ id: `10-${i}`, val: 10 })),
  ];
}

function pickRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function getExpectedValues(sourceUrnId, removedChipId) {
  const urns = [URN1, URN2];
  const src = urns[sourceUrnId];
  const other = urns[1 - sourceUrnId];

  const srcChips = buildChips(src).filter((c) => c.id !== removedChipId);
  const stayEV =
    srcChips.reduce((s, c) => s + c.val, 0) / srcChips.length;

  const otherChips = buildChips(other);
  const switchEV =
    otherChips.reduce((s, c) => s + c.val, 0) / otherChips.length;

  // Since urns are indistinguishable, player commits to one strategy.
  // Optimal overall is always "stay" (EV=52/7 vs switch EV=242/35)
  return { stayEV, switchEV, optimal: "stay" };
}

function computeTheory() {
  // Urns are indistinguishable — player cannot observe which urn they drew from.
  // Given drew $1: P(Urn1) = 4/7, P(Urn2) = 3/7 (Bayesian posterior)
  // Stay EV = 4/7 * (6/9*10 + 3/9*1) + 3/7 * (7/9*10 + 2/9*1)
  //         = 4/7 * 7 + 3/7 * 8 = 52/7
  // Switch EV = 4/7 * (7/10*10 + 3/10*1) + 3/7 * (6/10*10 + 4/10*1) = 242/35
  // Stay wins → optimal EV = 52/7
  return (52 / 7).toFixed(4); // ≈ 7.4286
}

const THEORY = computeTheory();

function Chip({ val, state }) {
  const base =
    "w-10 h-10 rounded-full flex items-center justify-center text-xs font-bold border-2 transition-all duration-300 select-none";
  const style =
    val === 1
      ? "bg-zinc-800 border-zinc-600 text-zinc-300"
      : "bg-amber-500 border-amber-300 text-amber-900";
  const mod =
    state === "picked"
      ? "opacity-30 scale-90"
      : state === "highlight"
      ? "ring-4 ring-cyan-400 scale-110"
      : "";
  return (
    <div className={`${base} ${style} ${mod}`}>
      {val === 1 ? "$1" : "$10"}
    </div>
  );
}

function UrnDisplay({ urn, chips, pickedId, highlightId, isSource, isOther }) {
  const border = isSource
    ? "border-cyan-500"
    : isOther
    ? "border-violet-500"
    : "border-zinc-700";
  const label = isSource
    ? "border-cyan-500 text-cyan-400"
    : isOther
    ? "border-violet-500 text-violet-400"
    : "border-zinc-700 text-zinc-500";

  return (
    <div
      className={`relative rounded-2xl border ${border} bg-zinc-900 p-5 transition-all duration-300`}
    >
      <div
        className={`absolute -top-3 left-4 px-3 py-0.5 rounded-full border text-xs font-bold tracking-widest uppercase bg-zinc-950 ${label}`}
      >
        {urn.label}
      </div>
      <div className="mt-2 text-xs text-zinc-600 mb-3">
        {urn.ones} × $1 &nbsp;·&nbsp; {urn.tens} × $10
      </div>
      <div className="flex flex-wrap gap-2">
        {chips.map((c) => (
          <Chip
            key={c.id}
            val={c.val}
            state={
              c.id === pickedId
                ? "picked"
                : c.id === highlightId
                ? "highlight"
                : "normal"
            }
          />
        ))}
      </div>
    </div>
  );
}

function StatCard({ label, value, accent }) {
  return (
    <div className="flex flex-col gap-1 bg-zinc-900 rounded-xl p-4 border border-zinc-800">
      <span className="text-xs text-zinc-500 uppercase tracking-widest">{label}</span>
      <span className={`text-2xl font-bold ${accent || "text-zinc-100"}`}>
        {value}
      </span>
    </div>
  );
}

function LogEntry({ entry, idx }) {
  const isNew = idx === 0;
  return (
    <div
      className={`flex items-center justify-between py-2 px-3 rounded-lg text-sm border ${
        isNew
          ? "border-zinc-600 bg-zinc-800"
          : "border-transparent bg-transparent"
      } transition-all duration-300`}
    >
      <span className="text-zinc-600 w-10">#{entry.trial}</span>
      <span className="text-zinc-400 w-14">{entry.urn}</span>
      <span
        className={`w-20 text-center rounded-full px-2 py-0.5 text-xs font-semibold ${
          entry.action === "switch"
            ? "bg-violet-900 text-violet-300"
            : entry.action === "stay"
            ? "bg-zinc-700 text-zinc-300"
            : "bg-zinc-800 text-zinc-500"
        }`}
      >
        {entry.action}
      </span>
      <span
        className={`w-12 text-right font-bold ${
          entry.payout === 10 ? "text-amber-400" : "text-zinc-400"
        }`}
      >
        ${entry.payout}
      </span>
    </div>
  );
}

export default function UrnSimulation() {
  const [phase, setPhase] = useState("idle"); // idle | drawn | choice | result
  const [sourceUrnId, setSourceUrnId] = useState(null);
  const [pickedChip, setPickedChip] = useState(null);
  const [resultChip, setResultChip] = useState(null);
  const [actionTaken, setActionTaken] = useState(null);
  const [evInfo, setEvInfo] = useState(null);

  const [trials, setTrials] = useState(0);
  const [totalPayout, setTotalPayout] = useState(0);
  const [switchCount, setSwitchCount] = useState(0);
  const [stayCount, setStayCount] = useState(0);
  const [switchPayout, setSwitchPayout] = useState(0);
  const [stayPayout, setStayPayout] = useState(0);
  const [log, setLog] = useState([]);

  const urn1Chips = buildChips(URN1);
  const urn2Chips = buildChips(URN2);

  const addLog = useCallback((entry) => {
    setLog((prev) => [entry, ...prev].slice(0, 80));
  }, []);

  function drawFirst() {
    // First chip is always $1 — urn weighted by P(Urn|drew $1): 4/7 vs 3/7
    const uid = Math.random() < 4 / 7 ? 0 : 1;
    const oneChips = (uid === 0 ? urn1Chips : urn2Chips).filter((c) => c.val === 1);
    const chip = pickRandom(oneChips);
    setSourceUrnId(uid);
    setPickedChip(chip);
    setResultChip(null);
    setActionTaken(null);
    const ev = getExpectedValues(uid, chip.id);
    setEvInfo(ev);
    setPhase("choice");
  }

  function choose(action) {
    const srcChips =
      sourceUrnId === 0 ? urn1Chips : urn2Chips;
    const otherChips =
      sourceUrnId === 0 ? urn2Chips : urn1Chips;

    let pool;
    if (action === "stay") {
      pool = srcChips.filter((c) => c.id !== pickedChip.id);
    } else {
      pool = otherChips;
    }
    const drawn = pickRandom(pool);
    setResultChip(drawn);
    setActionTaken(action);
    setPhase("result");

    const isSwitch = action === "switch";
    setTrials((t) => t + 1);
    setTotalPayout((t) => t + drawn.val);
    if (isSwitch) { setSwitchCount((c) => c + 1); setSwitchPayout((p) => p + drawn.val); }
    else { setStayCount((c) => c + 1); setStayPayout((p) => p + drawn.val); }
    addLog({
      trial: trials + 1,
      urn: `Urn ${sourceUrnId + 1}`,
      action,
      payout: drawn.val,
    });
  }

  function runBulk(n, strategy = "stay") {
    let tNew = trials,
      payNew = totalPayout,
      swNew = switchCount,
      stNew = stayCount,
      swPayNew = switchPayout,
      stPayNew = stayPayout;
    const newLogs = [];

    for (let i = 0; i < n; i++) {
      // First chip is always $1 — weighted urn selection
      const uid = Math.random() < 4 / 7 ? 0 : 1;
      const chips = uid === 0 ? urn1Chips : urn2Chips;
      const oneChips = chips.filter((c) => c.val === 1);
      const chip = pickRandom(oneChips);
      tNew++;

      const isSwitch = strategy === "switch";
      const otherChips = uid === 0 ? urn2Chips : urn1Chips;
      let pool = isSwitch
        ? otherChips
        : chips.filter((c) => c.id !== chip.id);
      const drawn = pickRandom(pool);

      payNew += drawn.val;
      if (isSwitch) { swNew++; swPayNew += drawn.val; }
      else { stNew++; stPayNew += drawn.val; }
      newLogs.push({ trial: tNew, urn: `Urn ${uid + 1}`, action: isSwitch ? "switch" : "stay", payout: drawn.val });
    }

    setTrials(tNew);
    setTotalPayout(payNew);
    setSwitchCount(swNew);
    setStayCount(stNew);
    setSwitchPayout(swPayNew);
    setStayPayout(stPayNew);
    setLog((prev) => [...newLogs.reverse(), ...prev].slice(0, 80));
    setPhase("idle");
    setPickedChip(null);
    setResultChip(null);
    setSourceUrnId(null);
    setEvInfo(null);
    setActionTaken(null);
  }

  function reset() {
    setPhase("idle");
    setSourceUrnId(null);
    setPickedChip(null);
    setResultChip(null);
    setActionTaken(null);
    setEvInfo(null);
    setTrials(0);
    setTotalPayout(0);
    setSwitchCount(0);
    setStayCount(0);
    setSwitchPayout(0);
    setStayPayout(0);
    setLog([]);
  }

  const avgPayout = trials > 0 ? (totalPayout / trials).toFixed(3) : "—";
  const switchRate =
    switchCount + stayCount > 0
      ? ((switchCount / (switchCount + stayCount)) * 100).toFixed(1) + "%"
      : "—";

  const pickedId = pickedChip?.id ?? null;

  return (
    <div
      style={{ fontFamily: "'DM Mono', 'Courier New', monospace" }}
      className="min-h-screen bg-zinc-950 text-zinc-100 p-6"
    >
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@700;800&display=swap');
        .title-font { font-family: 'Syne', sans-serif; }
        .mono { font-family: 'DM Mono', monospace; }
        .glow-cyan { box-shadow: 0 0 20px rgba(34,211,238,0.15); }
        .glow-violet { box-shadow: 0 0 20px rgba(167,139,250,0.15); }
        .btn-action {
          padding: 10px 22px; border-radius: 10px; font-size: 13px;
          font-weight: 500; cursor: pointer; transition: all 0.18s;
          letter-spacing: 0.03em; border: 1px solid;
        }
        .btn-draw {
          background: rgba(34,211,238,0.12); border-color: rgba(34,211,238,0.4);
          color: #67e8f9;
        }
        .btn-draw:hover { background: rgba(34,211,238,0.22); }
        .btn-switch {
          background: rgba(167,139,250,0.12); border-color: rgba(167,139,250,0.5);
          color: #c4b5fd;
        }
        .btn-switch:hover { background: rgba(167,139,250,0.25); glow-violet; }
        .btn-stay {
          background: rgba(255,255,255,0.04); border-color: rgba(255,255,255,0.15);
          color: #a1a1aa;
        }
        .btn-stay:hover { background: rgba(255,255,255,0.08); }
        .btn-ghost {
          background: transparent; border-color: rgba(255,255,255,0.1);
          color: #71717a; font-size: 12px; padding: 7px 16px;
        }
        .btn-ghost:hover { border-color: rgba(255,255,255,0.2); color: #a1a1aa; }
        .chip-result {
          animation: pop 0.35s cubic-bezier(0.34,1.56,0.64,1) forwards;
        }
        @keyframes pop {
          from { transform: scale(0.5); opacity: 0; }
          to { transform: scale(1); opacity: 1; }
        }
        .fade-in { animation: fadeIn 0.3s ease forwards; }
        @keyframes fadeIn { from { opacity:0; transform:translateY(6px); } to { opacity:1; transform:none; } }
      `}</style>

      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="title-font text-4xl font-extrabold text-zinc-100 mb-1 tracking-tight">
            Urn Probability
          </h1>
          <p className="text-zinc-500 text-sm mono">
            Optimal strategy: <strong>stay</strong> · expected payout ={" "}
            <span className="text-amber-400 font-semibold">52/7 ≈ ${THEORY}</span>
          </p>
        </div>

        {/* Urns */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <UrnDisplay
            urn={URN1}
            chips={urn1Chips}
            pickedId={sourceUrnId === 0 ? pickedId : null}
            highlightId={
              phase === "result" && actionTaken === "stay" && sourceUrnId === 0
                ? resultChip?.id
                : null
            }
            isSource={sourceUrnId === 0 && phase !== "idle"}
            isOther={
              (phase === "choice" || phase === "result") && sourceUrnId === 1
            }
          />
          <UrnDisplay
            urn={URN2}
            chips={urn2Chips}
            pickedId={sourceUrnId === 1 ? pickedId : null}
            highlightId={
              phase === "result" && actionTaken === "stay" && sourceUrnId === 1
                ? resultChip?.id
                : null
            }
            isSource={sourceUrnId === 1 && phase !== "idle"}
            isOther={
              (phase === "choice" || phase === "result") && sourceUrnId === 0
            }
          />
        </div>

        {/* Phase Panel */}
        <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-5 mb-5 min-h-[120px] flex flex-col justify-center fade-in">
          {phase === "idle" && (
            <div className="flex items-center gap-4">
              <span className="text-zinc-500 text-sm mono flex-1">
                Ready — draw a chip from a random urn to begin.
              </span>
              <button className="btn-action btn-draw" onClick={drawFirst}>
                Draw first chip ↓
              </button>
            </div>
          )}

          {phase === "choice" && pickedChip && evInfo && (
            <div className="fade-in">
              <div className="flex items-center gap-3 mb-4">
                <div className="text-sm text-zinc-400 mono">
                  Drew{" "}
                  <span className="text-zinc-100 font-bold">
                    ${pickedChip.val}
                  </span>{" "}
                  from{" "}
                  <span className="text-cyan-400">
                    Urn {sourceUrnId + 1}
                  </span>
                </div>
                <div className="ml-auto text-xs text-zinc-600 mono">
                  EV stay {evInfo.stayEV.toFixed(2)} · EV switch{" "}
                  {evInfo.switchEV.toFixed(2)}
                </div>
              </div>
              <div className="flex gap-3">
                <div className="flex-1">
                  <button
                    className="btn-action btn-switch w-full"
                    onClick={() => choose("switch")}
                  >
                    Switch to Urn {sourceUrnId === 0 ? "II" : "I"}
                    {evInfo.optimal === "switch" && (
                      <span className="ml-2 text-xs opacity-70">★ optimal</span>
                    )}
                  </button>
                  <div className="text-xs text-zinc-600 mono mt-1 text-center">
                    EV = ${evInfo.switchEV.toFixed(2)}
                  </div>
                </div>
                <div className="flex-1">
                  <button
                    className="btn-action btn-stay w-full"
                    onClick={() => choose("stay")}
                  >
                    Stay in Urn {sourceUrnId + 1}
                    {evInfo.optimal === "stay" && (
                      <span className="ml-2 text-xs opacity-70">★ optimal</span>
                    )}
                  </button>
                  <div className="text-xs text-zinc-600 mono mt-1 text-center">
                    EV = ${evInfo.stayEV.toFixed(2)}
                  </div>
                </div>
              </div>
            </div>
          )}

          {phase === "result" && resultChip && (
            <div className="fade-in flex items-center gap-5">
              <div className="chip-result">
                <Chip val={resultChip.val} state="highlight" />
              </div>
              <div className="flex-1">
                <div className="text-sm text-zinc-400 mono mb-1">
                  You {actionTaken} →{" "}
                  <span
                    className={`font-bold text-xl ${
                      resultChip.val === 10
                        ? "text-amber-400"
                        : "text-zinc-300"
                    }`}
                  >
                    ${resultChip.val}
                  </span>
                </div>
                <div className="text-xs text-zinc-600 mono">
                  Running avg: ${avgPayout}
                </div>
              </div>
              <button className="btn-action btn-draw" onClick={drawFirst}>
                Next →
              </button>
            </div>
          )}
        </div>

        {/* Stats */}
        <div className="grid grid-cols-4 gap-3 mb-5">
          <StatCard label="Trials" value={trials} />
          <StatCard
            label="Avg payout"
            value={avgPayout === "—" ? "—" : `$${avgPayout}`}
            accent="text-amber-400"
          />
          <StatCard
            label="Switched"
            value={switchCount}
            accent="text-violet-400"
          />
          <StatCard
            label="Stayed"
            value={stayCount}
            accent="text-zinc-400"
          />
        </div>

        {/* Bulk controls */}
        <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4 mb-5">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <div className="text-xs text-zinc-500 uppercase tracking-widest mb-2">
                Stay strategy <span className="text-amber-400 ml-1">★ optimal</span>
              </div>
              <div className="flex gap-2 flex-wrap">
                <button className="btn-action btn-ghost" onClick={() => runBulk(100, "stay")}>100</button>
                <button className="btn-action btn-ghost" onClick={() => runBulk(1000, "stay")}>1,000</button>
                <button className="btn-action btn-ghost" onClick={() => runBulk(10000, "stay")}>10,000</button>
              </div>
            </div>
            <div>
              <div className="text-xs text-zinc-500 uppercase tracking-widest mb-2">
                Switch strategy
              </div>
              <div className="flex gap-2 flex-wrap">
                <button className="btn-action btn-ghost" style={{borderColor:"rgba(167,139,250,0.3)",color:"#c4b5fd"}} onClick={() => runBulk(100, "switch")}>100</button>
                <button className="btn-action btn-ghost" style={{borderColor:"rgba(167,139,250,0.3)",color:"#c4b5fd"}} onClick={() => runBulk(1000, "switch")}>1,000</button>
                <button className="btn-action btn-ghost" style={{borderColor:"rgba(167,139,250,0.3)",color:"#c4b5fd"}} onClick={() => runBulk(10000, "switch")}>10,000</button>
              </div>
            </div>
          </div>
          <div className="mt-3 flex justify-end">
            <button
              className="btn-action btn-ghost"
              onClick={reset}
              style={{ borderColor: "rgba(239,68,68,0.3)", color: "#f87171" }}
            >
              Reset
            </button>
          </div>
        </div>

        {/* Theory vs sim */}
        {trials > 0 && (
          <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4 mb-5 mono fade-in">
            <div className="text-xs text-zinc-500 uppercase tracking-widest mb-3">Convergence</div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <div className="text-xs text-zinc-600 mb-1">Stay theory <span className="text-amber-400">52/7</span></div>
                <div className="text-xs text-zinc-600 mb-1">Stay simulated</div>
                <div className="flex items-baseline gap-2">
                  <span className="text-lg text-amber-400 font-bold">${THEORY}</span>
                  <span className="text-zinc-700">→</span>
                  <span className="text-lg text-cyan-400 font-bold">
                    {stayCount > 0 ? "$" + (stayPayout / stayCount).toFixed(3) : "—"}
                  </span>
                  {stayCount >= 100 && (
                    <span className={`text-xs ml-1 ${Math.abs(stayPayout/stayCount - 52/7) < 0.05 ? "text-green-400" : "text-zinc-500"}`}>
                      Δ{(Math.abs(stayPayout/stayCount - 52/7)).toFixed(3)}
                    </span>
                  )}
                </div>
              </div>
              <div>
                <div className="text-xs text-zinc-600 mb-1">Switch theory <span className="text-violet-400">242/35</span></div>
                <div className="text-xs text-zinc-600 mb-1">Switch simulated</div>
                <div className="flex items-baseline gap-2">
                  <span className="text-lg text-violet-400 font-bold">{(242/35).toFixed(4)}</span>
                  <span className="text-zinc-700">→</span>
                  <span className="text-lg text-cyan-400 font-bold">
                    {switchCount > 0 ? "$" + (switchPayout / switchCount).toFixed(3) : "—"}
                  </span>
                  {switchCount >= 100 && (
                    <span className={`text-xs ml-1 ${Math.abs(switchPayout/switchCount - 242/35) < 0.05 ? "text-green-400" : "text-zinc-500"}`}>
                      Δ{(Math.abs(switchPayout/switchCount - 242/35)).toFixed(3)}
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Log */}
        {log.length > 0 && (
          <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
            <div className="text-xs text-zinc-600 uppercase tracking-widest mono mb-3">
              Trial log
            </div>
            <div className="flex text-xs text-zinc-600 mono px-3 mb-1">
              <span className="w-10">#</span>
              <span className="w-14">Urn</span>
              <span className="w-20 text-center">Action</span>
              <span className="ml-auto">Payout</span>
            </div>
            <div className="overflow-y-auto" style={{ maxHeight: 260 }}>
              {log.map((entry, i) => (
                <LogEntry key={entry.trial} entry={entry} idx={i} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
