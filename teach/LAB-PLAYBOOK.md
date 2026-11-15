# Practical Engineering Lab Playbook

These are illustrative patterns, not a mandatory curriculum. Adapt to the learner's actual source, tools and experience. Never pretend example results were measured.

## Example A: Inverting op-amp (beginner)

**Goal:** explain signal inversion and distinguish predicted gain from simulated behavior.

**Principle:** For an ideal inverting amplifier with negative feedback and an appropriate operating region, closed-loop gain is `Vout/Vin = -Rf/Rin`; the minus sign indicates inversion. Real devices may saturate, have finite gain-bandwidth and depend on supply rails.

**Worked demonstration:** With `Rin = 10 kΩ`, `Rf = 20 kΩ` and `Vin = +0.1 V` DC, ideal `Vout ≈ -0.2 V`, *if powered appropriately and within the output swing*. Note input/output sign and resistor ratio.

**Learner decision:** “Without running the simulator, predict the effect of replacing `Rf` with `30 kΩ` on output magnitude and sign. Why?” Do not reveal the answer in the same turn.

**Test:** Build or edit the smallest schematic compatible with the chosen tool. Verify supply pins, source polarity and resistor connections; run operating point or transient. Show exactly one action and expected plot after the learner has responded.

**Diagnose:** If the waveform clips, check supply rails, input amplitude, common-mode range and model limitations before blaming resistor arithmetic. Change one variable at a time.

**Transfer:** Given a target magnitude of three and available resistors, the learner chooses values and verifies their own prediction.

## Example B: RF low-noise amplifier (LNA)

**Goal:** interpret operating point, input match, gain and noise around a named center frequency without confusing metrics.

**Principle:** Start from topology, DC bias and port impedances. S11 represents input reflection under the defined test conditions; S21 is forward transmission between reference ports. Noise figure depends on device bias, matching, frequency and models.

**Worked demonstration:** Explain a Smith-chart or impedance-match intuition and calculate a simple reflection coefficient from `Γ = (Zin-Z0)/(Zin+Z0)` using explicitly illustrative values, clearly distinguishing numerical examples from device simulation data.

**Learner decision:** Before running an AC/S-parameter sweep, ask which measured quantity should change when input matching is adjusted and why. Choose a single controlled edit to the actual project.

**Test:** Verify frequency units, port setup, reference impedance, model include, temperature/corner and analysis method. Present the expected plot axes and one step at a time.

**Diagnose:** Compare theoretical reflection with simulator S11 at the exact frequency, then check whether the analysis/port definition is consistent. Don't claim that an attractive schematic or layout image proves DRC/LVS, parasitic extraction or fabrication readiness.

**Transfer:** Have the learner propose one trade-off among matching, noise figure, power, stability and gain and test it.

## Example C: HDL / microcontroller debugging

**Goal:** identify why a state machine or peripheral output differs from a specification.

**Worked demonstration:** Draw a tiny state transition on a clock edge and narrate how reset and input samples influence output.

**Learner prediction:** Ask for the state/output after a short input sequence before viewing the waveform.

**Test:** Run one reproducible testbench command (platform-specific), inspect a concrete assertion or timestamp, and ask for the exact log/waveform section.

**Diagnose:** Distinguish compiler/elaboration failures, wrong reset polarity, edge timing, stale build artifacts and actual logic errors. Change only the most discriminating variable and rerun the previously failing test.

**Transfer:** The learner adds an edge case and explains the resulting behavior.

## Debugging conversation template (adapt, don't recite)

- “What you expected: …; what your output shows: …”
- “The first discrepancy is …; one plausible cause is … because …”
- “Do this ONE check at [exact place]: … . Expected evidence: … . Share …”
- After results: “That supports/rejects our hypothesis because … . Next we …”

## Essential guardrails

Use actual tools only when available and authorized. Make explicit when no simulation has been executed. Use original work as reference; avoid destructive overwrites. Do not submit fabricated waveforms, measurement tables or screenshots. Keep real hardware experiments within appropriate safety bounds.
