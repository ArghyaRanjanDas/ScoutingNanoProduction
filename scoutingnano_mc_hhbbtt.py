# HHBBTT: MC ScoutingNano production with the HH->bbtautau CRAB-time preselection
# baked in. Derived from Jan-Frederik Schulte's scoutingnano_mc_standalone2.py.
# Everything not marked with a '# HHBBTT:' comment is byte-identical to Jan's file.
# Deltas: 5-path DST-OR trigger filter + loosev2 kinematic + b0-leg EDFilter
# (own presel_step, nano sequence UNGATED, SelectEvents gates writing only so
# genEventSumw accumulates over ALL events = FM13 normalization); nanogen gen
# tables (customizeNanoGENFromMini) + the edmTriggerResults-drop revert; MC L1
# rewiring (customiseScoutingNanoFromMini); Recluster2 tau-less tables dropped
# (Tags + TagsTT4Q ONNX auto-pruned); KEEP_PF switch; 4 threads/streams,
# wantSummary, maxEvents param.
#
# Auto generated configuration file
# using:
# Revision: 1.19
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v
# with command line options: step2 -s NANO:@Scout --process NANO --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --era Run3_2024 --conditions 150X_mcRun3_2024_realistic_v2 --python_file scoutingnano_mc_standalone2.py -n 100 --fileout scouting_nano_MC.root --filein file:0034afa6-0d8d-4409-8154-afda2a1d7d4b.root
import FWCore.ParameterSet.Config as cms

# HHBBTT: ───────────────────────── HHbbtt knobs ─────────────────────────
KEEP_PF    = True    # HHBBTT: group vote pending; False drops the ScoutingPFCandidate table (one-line change)
MAX_EVENTS = 20000   # HHBBTT: smoke default; -1 for full file
# HHBBTT: ─────────────────────────────────────────────────────────────────

from Configuration.Eras.Era_Run3_2024_cff import Run3_2024

process = cms.Process('NANO',Run3_2024)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.custom_run3scouting_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(MAX_EVENTS),   # HHBBTT: param (was -1)
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    # HHBBTT: kl-1p00 GluGluHHto2B2Tau Summer24 MINIAODSIM (hosted RAL/FNAL/Colorado, NOT Purdue -> US redirector; login node has WAN)
    fileNames = cms.untracked.vstring('root://cmsxrootd.fnal.gov//store/mc/RunIII2024Summer24MiniAODv6/GluGluHHto2B2Tau_Par-c2-0p00-kl-1p00-kt-1p00_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/PowhegBugFix_150X_mcRun3_2024_realistic_v2-v2/2520000/d681d911-3503-43a5-af4d-e8242942872c.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    TryToContinue = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    holdsReferencesToDeleteEarly = cms.untracked.VPSet(),
    makeTriggerResults = cms.obsolete.untracked.bool,
    modulesToCallForTryToContinue = cms.untracked.vstring(),
    modulesToIgnoreForDeleteEarly = cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(4),        # HHBBTT: 4 (was 0)
    numberOfThreads = cms.untracked.uint32(4),        # HHBBTT: 4 (was 1)
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(True)            # HHBBTT: TrigReport => filter efficiency for free (S1)
)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000   # HHBBTT: quieter log

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('hhbbttPresel')   # HHBBTT
    ),
    fileName = cms.untracked.string('scouting_nano_MC_hhbbtt.root'),   # HHBBTT
    outputCommands = process.NANOAODSIMEventContent.outputCommands,
    # HHBBTT: gate event WRITING on the filter path only (nano sequence stays
    # ungated so the Runs-tree genEventSumw denominator sees ALL events = FM13)
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('presel_step'))
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '150X_mcRun3_2024_realistic_v2', '')

# HHBBTT: ─── Filters + paths + schedule (replaces Jan's Path/EndPath block) ───
# 5-path DST OR — plain '_v*' (fired). NO '/ 3': the offline L1-prescale weight
# owns prescale accounting; '/3' would double-count it and silently drop events.
process.hhbbttDstOrFilter = cms.EDFilter("TriggerResultsFilter",
    triggerConditions = cms.vstring(
        'DST_PFScouting_JetHT_v*',
        'DST_PFScouting_DatasetMuon_v*',
        'DST_PFScouting_DoubleMuon_v*',
        'DST_PFScouting_SingleMuon_v*',
        'DST_PFScouting_DoubleEG_v*',
    ),
    hltResults = cms.InputTag('TriggerResults', '', 'HLT'),
    l1tResults = cms.InputTag(''),
    throw = cms.bool(False),
    l1tIgnoreMaskAndPrescale = cms.bool(False),
    usePathStatus = cms.bool(False),
    daqPartitions = cms.uint32(1),
)

process.hhbbttPreselFilter = cms.EDFilter("HHbbttPreselFilter",
    jets = cms.InputTag("patScoutingPFJetReclusterCHS"),
    muons = cms.InputTag("hltScoutingMuonPackerVtx"),
    electrons = cms.InputTag("hltScoutingEgammaPacker"),
    taggerPrefix = cms.string("scoutingPFJetReclusterPFUnifiedParticleTransformerAK4TagsCHS"),
    jetPt0 = cms.double(20.), jetPt1 = cms.double(20.), jetPt2 = cms.double(10.),
    jetPt3 = cms.double(10.), jetEtaMax = cms.double(2.5),
    lepPtMin = cms.double(4.), lepEtaMax = cms.double(2.5),
    bScoreMin = cms.double(0.65),                     # LITERAL (group decision 2026-07-10)
    tagPtMin = cms.double(15.), tagEtaMax = cms.double(2.5),
)

process.nanoAOD_step  = cms.Path(process.scoutingNanoSequence)                              # HHBBTT: UNGATED (FM13)
process.presel_step   = cms.Path(process.hhbbttDstOrFilter + process.hhbbttPreselFilter)    # HHBBTT: filters ONLY
process.endjob_step   = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

process.schedule = cms.Schedule(process.nanoAOD_step, process.presel_step,
                                process.endjob_step, process.NANOAODSIMoutput_step)
# HHBBTT: ──────────────────────────────────────────────────────────────────────

from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# HHBBTT: ORDER MATTERS. customiseScoutingNano first, then the MC L1 fix, then derived.
from PhysicsTools.NanoAOD.custom_run3scouting_cff import (
    customiseScoutingNano, customiseScoutingNanoFromMini, addScoutingPFCandidate)

process = customiseScoutingNano(process)          # adds trigger_step to schedule + MC gen-weight/PU/genJet task
# HHBBTT: MC L1 fix — MiniAODSIM has NO hltFEDSelectorL1 FED; rewire L1 tables/bits
# to the gmtStage2Digis/caloStage2Digis/gtStage2Digis products stored in Mini.
process = customiseScoutingNanoFromMini(process)  # VERIFIED present, custom_run3scouting_cff.py:214
# HHBBTT: FromMini mis-sniffs MC as data (hasattr NANOAODSIMoutput) and creates a
# DANGLING 'scoutingNanoSkim_step' Path — it is NOT in our schedule and NOT in any
# SelectEvents (ours stays ['presel_step']), so it never runs. Harmless; noted so a
# config-dump reader does not panic. L1_* fill (gmt/calo/gtStage2Digis products from
# Mini) is a SMOKE gate: assert nonzero fire fractions for the 13 analysis L1 seeds
# in MC validation (plan S7 applied to MC) — not something the config can self-check.

from PhysicsTools.PatFromScouting.scoutingToMiniAODDerivedCollections_cff import customiseScoutingNanoDerived
process = customiseScoutingNanoDerived(process, "NANO")
# End of customisation functions

# HHBBTT: ─── gen tables: '-s NANO:@Scout' carries NO GenPart/GenJet/LHE — add full NanoGEN ───
process.load('PhysicsTools.NanoAOD.nanogen_cff')
from PhysicsTools.NanoAOD.nanogen_cff import customizeNanoGENFromMini
process = customizeNanoGENFromMini(process)       # VERIFIED present, nanogen_cff.py:64

# HHBBTT: CRITICAL un-do — nanoGenCommonCustomize appended 'drop edmTriggerResults_*_*_*'
# to NANOAODSIMoutput (nanogen_cff.py:62). That drop would kill every DST_* AND L1_*
# branch (l1bits also emits an edm::TriggerResults). Remove it; nano content's
# 'keep edmTriggerResults_*_*_*' then applies.
while 'drop edmTriggerResults_*_*_*' in process.NANOAODSIMoutput.outputCommands:
    process.NANOAODSIMoutput.outputCommands.remove('drop edmTriggerResults_*_*_*')

# HHBBTT: FIX (smoke crash, exit 73): nanogen's metMCTable makes the GenMET
# branches by calling genMET() on 'slimmedMETs' — but the scouting-standalone
# customization PRODUCES its own slimmedMETs in THIS process (scouting MET,
# no genMET embedded), which shadows the MiniAOD one and returns a null ptr
# ("method genMET returned void"). Pin the src past the current process so it
# reads the INPUT MiniAOD slimmedMETs (genMET embedded).
if hasattr(process, "metMCTable"):
    process.metMCTable.src = cms.InputTag("slimmedMETs", "", cms.InputTag.skipCurrentProcess())

process.nanogen_step = cms.Path(process.nanogenSequence)   # HHBBTT: UNGATED (gen tables + genWeights for ALL events)
process.schedule.extend([process.nanogen_step])

# HHBBTT: ─── drop Jack's tau-less AK4 set: delete the 3 Recluster2 TABLE producers. ───
# NanoAODOutputModule consumes every kept FlatTable, so the tables must go
# explicitly; the upstream chain (recluster + UParT TagInfos, Tags + TagsTT4Q
# ONNX, patScoutingPFJetRecluster, slimmedJets, gen matches) then loses ALL
# consumers and is auto-pruned by deleteNonConsumedUnscheduledModules=True (both
# ONNX sessions never load). Do NOT delete non-table modules by hand — unscheduled
# pruning resolves them. ScoutingPFJetReclusterCHS* tables stay untouched.
process.scoutingPFJetRecluster2TableTask.remove(process.scoutingPFJetRecluster2Table)
del process.scoutingPFJetRecluster2Table
if hasattr(process, 'scoutingPFJetRecluster2MCTableTask'):          # MC only
    process.scoutingPFJetRecluster2MCTableTask.remove(process.scoutingPFJetRecluster2MCTable)
    process.scoutingPFJetRecluster2MCTableTask.remove(process.scoutingPFJetRecluster2FlavourCategory)
    del process.scoutingPFJetRecluster2MCTable
    del process.scoutingPFJetRecluster2FlavourCategory

# HHBBTT: PF-candidate table — stock scouting nano does NOT write it
# (custom_run3scouting_cff.py:100). KEEP_PF=True calls addScoutingPFCandidate.
if KEEP_PF:
    process = addScoutingPFCandidate(process)


# Customisation from command line

process.source.delayReadingEventProducts = cms.untracked.bool(False)
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
