# HH→bbττ preselection baked into the ScoutingNano recipe

Two new configs that take Jan-Frederik Schulte's ScoutingNano recipe
(`scoutingnano_{mc,data}_standalone2.py`) and bake in the HH→bbττ CRAB-time
preselection, plus one CMSSW plugin. Everything else is Jan's recipe unchanged.

## 1. What this adds

| New file | Role |
|---|---|
| `scoutingnano_mc_hhbbtt.py` | MC config = Jan's MC standalone + HH→bbττ preselection + gen tables + MC-L1 fix |
| `scoutingnano_data_hhbbtt.py` | Data config = Jan's data standalone − VVV selection + HH→bbττ preselection |
| `PhysicsTools/PatFromScouting/plugins/HHbbttPreselFilter.cc` | The preselection EDFilter (lives in the CMSSW topic area, not this fork) |

**Provenance of the card.** The kinematic leg is the analysis repo's **loosev2**
`preselection` card (`config/cuts.yaml`, verbatim: `nJets≥3`;
`pt[0]>20 && pt[1]>20 && pt[2]>10`; `|η[0,1,2]|<2.5`; fourth-object OR of a 4th
central jet `pt>10 |η|<2.5` OR a soft raw muon `pt>4 |η|<2.5` OR a soft raw
electron `pt>4 |η|<2.5`). The b-leg is the **group-baked** cut (decision
2026-07-10): `max_jet BvsAll > 0.65` on the leading score-ranked b candidate, no
b1 cut, no ΔR cut (ΔR deferred). The `0.65` threshold is **literal** — remapping
it is a group re-vote item, never a silent code change.

The filter runs on `patScoutingPFJetReclusterCHS` — the **same** `pat::Jet`
collection, same order, that the `ScoutingPFJetReclusterCHS` NanoAOD table reads
(table `cut=""`), so index-based cuts in the filter equal index-based cuts on the
written table. `pat::Jet::pt()` is JEC-corrected = exactly what the table stores.

## 2. The plugin patch

`HHbbttPreselFilter.cc` is a `edm::global::EDFilter<>` with all thresholds in a
PSet (`fillDescriptions` defaults match the card). Build it into the CMSSW topic
area (it is NOT part of this fork):

```
cd $CMSSW_BASE/src && cmsenv && scram b -j8
```

One-line `BuildFile.xml` addition (already applied in the topic area) — the
explicit `edm::View` dependency, after the PatCandidates line:

```xml
<use name="DataFormats/PatCandidates"/>
<use name="DataFormats/Common"/>
<use name="DataFormats/Scouting"/>
```

The `.cc` (verbatim) is in
`$CMSSW_BASE/src/PhysicsTools/PatFromScouting/plugins/HHbbttPreselFilter.cc`.
Key semantics:

- **Kinematic leg** — index-based, collection order, no re-sort, no jet ID.
  eta window strict (`std::abs(η) < 2.5`), pt cuts strict (`>`).
- **Fourth-object OR** — raw index-0 muon/electron, NO ID; absent-or-empty
  collection ⇒ that OR branch is false (mirrors the `mu1_pt=-1`/`mu1_eta=-99`
  sentinels in the offline card).
- **b-leg** — per-jet table-parity `BvsAll = tableVal(probb) / Σ₆ tableVal(p)`
  over the 6 CHS probs (`probb, probc, probuds, probg, probtaup, probtaum`),
  with `tableVal(p) = (pt>=15 && |η|<=2.5) ? bDiscriminator(prefix:p) : -1.0`
  (the guard is **inclusive** `>=15`/`<=2.5`, exactly the table Var string). The
  `-1` propagation is reproduced deliberately (a guarded jet gives `-1/-6 =
  +1/6`, NOT clamped) so an offline replay on the written table reproduces the
  filter bit-for-bit. Event passes iff `max_jet BvsAll > 0.65`. A `-1000`
  sentinel from `bDiscriminator` (discriminator not attached) throws loudly on
  event 1 — catches any `jets`/`taggerPrefix` misconfiguration.

## 3. Delta table vs Jan's configs

| Aspect | Jan's standalone | HHbbtt config |
|---|---|---|
| Trigger filter | data: `DST_PFScouting_JetHT_v* / 3` | 5-path plain `_v*` OR (JetHT, DatasetMuon, DoubleMuon, SingleMuon, DoubleEG); NO `/3` — offline L1-prescale weight owns prescales |
| Event filter | data: ≥1 fat jet (`CandViewCountFilter`); MC: none | `HHbbttPreselFilter`: loosev2 kinematics + b0-leg on `patScoutingPFJetReclusterCHS` |
| Path layout | data: filters gate output directly | filters in own `presel_step`; `nanoAOD_step` (nano sequence) UNGATED; `SelectEvents=['presel_step']` gates writing only ⇒ **FM13**: Runs-tree `genEventSumw` accumulates over ALL events |
| MC gen tables | `-s NANO:@Scout` ⇒ no GenPart/GenJet/LHE | `nanogen_cff` + `customizeNanoGENFromMini` + revert of its `drop edmTriggerResults_*_*_*` (that drop would kill all DST_* and L1_* branches — `l1bits` is also an `edm::TriggerResults`) |
| MC L1 wiring | `customiseScoutingNano` (reads `hltFEDSelectorL1`, absent in MiniAODSIM ⇒ dead L1_*) | `customiseScoutingNanoFromMini` — rewires L1 tables/bits to `gmtStage2Digis`/`caloStage2Digis` |
| Recluster2 tables | Jack's tau-less base + `_TT4Q` sets kept | 3 Recluster2 TABLE producers deleted (base + MCTable + FlavourCategory); Tags + TagsTT4Q ONNX auto-pruned by `deleteNonConsumedUnscheduledModules` |
| Data pat-jet gen flags | `addGenPartonMatch`/`addGenJetMatch`/`getJetMCFlavour`/`addJetFlavourInfo` left ON on `patScoutingPFJetReclusterCHS` (derived cff sets them unconditionally) | data config strips all four (+ clears the gen InputTags) — HLTSCOUT has no `prunedGenParticles`/`slimmedGenJets`, so without this `PATJetProducer` throws `ProductNotFound` on every event; the b-discriminator chain is gen-free so b-leg/table parity is untouched |
| PF candidates | not written (stock) | `KEEP_PF` switch (default True ⇒ `addScoutingPFCandidate`; one-line group vote) |
| Threads / IO | 1 thread/stream; MC `wantSummary=False` | 4 threads/streams; `wantSummary=True` (TrigReport ⇒ filter ε); `reportEvery=1000`; `MAX_EVENTS` param |
| Inputs | TT MINIAODSIM / Run2024D HLTSCOUT | kl-1p00 GluGluHHto2B2Tau MINIAODSIM / Run2024C HLTSCOUT (Purdue door pinned) |

Data keeps `customiseScoutingNano` (HLTSCOUT has the FED); NO nanogen on data.

## 4. Upstream report-back (for Jan / JFS)

- **Data config SelectEvents bug**: in `scoutingnano_data_standalone2.py`,
  `triggerFilter_step` (his `dstJetHTFilter`) is scheduled but NOT referenced by
  `SelectEvents` (only `fatJetFilter_step` gates the output) — his DST trigger
  filter never actually gated writing.
- **MC gen tables**: `-s NANO:@Scout` ships MC NanoAOD with no GenPart/GenJet/LHE
  tables (Marc requires the full gen block).
- **MC L1**: `customiseScoutingNano` on MINIAODSIM reads `hltFEDSelectorL1`, which
  is absent in MiniAODSIM ⇒ `L1_*` branches come out dead; the `...FromMini`
  variant is required for MC.
- **Data pat-jet gen throw**: the derived cff sets the MC-only gen-match/flavour
  flags unconditionally on `patScoutingPFJetReclusterCHS`, so any **data** config
  whose output consumes the CHS jet table (Jan's does) drives `PATJetProducer` into
  the absent `prunedGenParticles`/`slimmedGenJets` handles ⇒ `ProductNotFound` on
  every event (silent under `TryToContinue`). Strongly suggests the derivedScouting
  **data** leg was never run end-to-end. Fix = disable those flags on data (done in
  our data config).

## 5. Known caveats

- Table Var `precision=10` vs the full-precision filter ⇒ sub-permille boundary
  migration at `BvsAll≈0.65` in offline replays (validation tolerance <0.1%).
- `rivetProducerHTXS` runs on HH (two Higgs) — stock nano does this too; watch the
  first 2k-event smoke stderr.
- Bulk non-Higgs MC (QCD/DY) with the nanogen block: verify HTXS/rivet does not
  throw before CRAB (flagged for the submission plan).
- The whitelist narrowing happens at CRAB time (a later plan). For smokes these
  configs keep full stock content so validation can inventory everything.

## 6. Smoke commands

```
cd $CMSSW_BASE/src && cmsenv
cmsRun ScoutingNanoProduction/scoutingnano_mc_hhbbtt.py     # 20k MC  (MAX_EVENTS knob)
cmsRun ScoutingNanoProduction/scoutingnano_data_hhbbtt.py   # 20k data
```
