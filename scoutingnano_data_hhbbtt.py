# HHBBTT: DATA ScoutingNano production with the HH->bbtautau CRAB-time preselection
# baked in. Derived from Jan-Frederik Schulte's scoutingnano_data_standalone2.py.
# Everything not marked with a '# HHBBTT:' comment is byte-identical to Jan's file.
# Deltas: Jan's VVV selection (dstJetHTFilter '/3', >=1 fat-jet, fatJetFilter_step,
# triggerFilter_step) DELETED wholesale; replaced by the SAME 5-path DST-OR trigger
# filter + loosev2 kinematic + b0-leg EDFilter MC runs (own presel_step, nano
# sequence UNGATED, SelectEvents gates writing only = FM13); data KEEPS the FED-based
# L1 path (customiseScoutingNano, NOT ...FromMini); NO nanogen on data; Recluster2
# tau-less base table dropped; KEEP_PF switch; 4 threads/streams, maxEvents param.
#
# Auto generated configuration file
# using:
# Revision: 1.19
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v
# with command line options: step2 -s NANO:@Scout --process NANO --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --era Run3_2024 --conditions 150X_mcRun3_2024_realistic_v2 --python_file scoutingnano_mc_standalone2.py -n 100 --fileout scouting_nano_MC.root --filein file:0034afa6-0d8d-4409-8154-afda2a1d7d4b.root
import FWCore.ParameterSet.Config as cms

# HHBBTT: ───────────────────────── HHbbtt knobs ─────────────────────────
KEEP_PF    = True    # HHBBTT: group vote pending; False drops the ScoutingPFCandidate table (one-line change)
MAX_EVENTS = -1      # HHBBTT: PRODUCTION (was 20000 smoke default)
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
    input = cms.untracked.int32(MAX_EVENTS),   # HHBBTT: param (was 10000)
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

#process.MessageLogger.cerr.threshold = 'ERROR'

# Input source
process.source = cms.Source("PoolSource",
    # HHBBTT: Run2024C HLTSCOUT golden-era file, Purdue door pinned explicitly
    # (Jan's bare /store path relies on a site-local xrootd fallback).
    fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/data/Run2024C/ScoutingPFRun3/HLTSCOUT/v1/000/379/530/00000/6fd781d3-46c2-4b5e-be36-2e15ca2c7c01.root'),
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
    wantSummary = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
# Output definition

process.NANOAODoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAOD'),
        filterName = cms.untracked.string('hhbbttPresel')   # HHBBTT
    ),
    fileName = cms.untracked.string('scouting_nano_data_hhbbtt.root'),   # HHBBTT
    outputCommands = process.NANOAODEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '150X_dataRun3_v8', '')

# HHBBTT: Jan's VVV selection DELETED wholesale — scoutingFatJetFilterCands,
# fatJetFilter_step, dstJetHTFilter ('DST_PFScouting_JetHT_v* / 3'; the /3 would
# divide the data yield by the prescale a SECOND time), triggerFilter_step, and
# his SelectEvents=['fatJetFilter_step']. Replaced by the HHbbtt filters below.

# HHBBTT: ─── Filters + paths + schedule (same card as MC — MC and data run one card) ───
# 5-path DST OR — plain '_v*' (fired). NO '/ 3' (offline L1-prescale weight owns it).
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

process.nanoAOD_step = cms.Path(process.scoutingNanoSequence)                            # HHBBTT: UNGATED
process.presel_step  = cms.Path(process.hhbbttDstOrFilter + process.hhbbttPreselFilter)  # HHBBTT: filters ONLY
process.endjob_step  = cms.EndPath(process.endOfProcess)
process.NANOAODoutput_step = cms.EndPath(process.NANOAODoutput)
process.schedule = cms.Schedule(process.nanoAOD_step, process.presel_step,
                                process.endjob_step, process.NANOAODoutput_step)
process.NANOAODoutput.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('presel_step'))  # HHBBTT
# HHBBTT: ──────────────────────────────────────────────────────────────────────

from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.custom_run3scouting_cff
# HHBBTT: data KEEPS the FED-based L1 path (HLTSCOUT has hltFEDSelectorL1) — do NOT
# call customiseScoutingNanoFromMini here (that is the MC-only Mini-L1 rewiring).
from PhysicsTools.NanoAOD.custom_run3scouting_cff import (
    customiseScoutingNano, addScoutingPFCandidate)

#call to customisation function customiseScoutingNano imported from PhysicsTools.NanoAOD.custom_run3scouting_cff
process = customiseScoutingNano(process)

from PhysicsTools.PatFromScouting.scoutingToMiniAODDerivedCollections_cff import customiseScoutingNanoDerived
process = customiseScoutingNanoDerived(process, "NANO")
# End of customisation functions

# HHBBTT: DATA has no gen — strip the MC-only pat flags the derived cff leaves ON.
# scoutingToMiniAODDerivedCollections_cff sets addGenPartonMatch/addGenJetMatch/
# getJetMCFlavour/addJetFlavourInfo = True UNCONDITIONALLY on patScoutingPFJetReclusterCHS
# (cff L728-738, no data toModify), pointing at scoutingPFJetReclusterCHSGen{Parton,Jet}Match
# / FlavourAssociation, which read prunedGenParticles / slimmedGenJets — ABSENT in HLTSCOUT.
# Our presel_step CONSUMES this pat collection, so without this fix PATJetProducer
# dereferences the missing gen handles and throws ProductNotFound on EVERY data event;
# with TryToContinue=['ProductNotFound'] (installed by customiseScoutingForStandalone)
# that is SILENT: presel_step fails every event, SelectEvents writes ~zero events, exit 0.
# PATJetProducer's gen consumes are flag-conditional, so False is sufficient; the InputTag
# clears are belt-and-suspenders. The bDiscriminator tagger chain is gen-free -> filter/
# table b-leg parity is untouched. (Jan's own data config has this same latent throw.)
process.patScoutingPFJetReclusterCHS.addGenPartonMatch    = False
process.patScoutingPFJetReclusterCHS.embedGenPartonMatch  = False
process.patScoutingPFJetReclusterCHS.genPartonMatch       = cms.InputTag("")
process.patScoutingPFJetReclusterCHS.addGenJetMatch       = False
process.patScoutingPFJetReclusterCHS.embedGenJetMatch     = False
process.patScoutingPFJetReclusterCHS.genJetMatch          = cms.InputTag("")
process.patScoutingPFJetReclusterCHS.getJetMCFlavour      = False
process.patScoutingPFJetReclusterCHS.addJetFlavourInfo    = False
process.patScoutingPFJetReclusterCHS.JetFlavourInfoSource = cms.InputTag("")

# HHBBTT: NO nanogen block on data (no gen tables, no genEventSumw denominator).

# HHBBTT: ─── drop Jack's tau-less AK4 set: delete the Recluster2 base TABLE producer. ───
# The upstream chain then loses ALL consumers and is auto-pruned by
# deleteNonConsumedUnscheduledModules=True. The MC-only MCTable/FlavourCategory
# hasattr guard is a no-op here (data has no MC table task).
process.scoutingPFJetRecluster2TableTask.remove(process.scoutingPFJetRecluster2Table)
del process.scoutingPFJetRecluster2Table
if hasattr(process, 'scoutingPFJetRecluster2MCTableTask'):          # data: no-op
    process.scoutingPFJetRecluster2MCTableTask.remove(process.scoutingPFJetRecluster2MCTable)
    process.scoutingPFJetRecluster2MCTableTask.remove(process.scoutingPFJetRecluster2FlavourCategory)
    del process.scoutingPFJetRecluster2MCTable
    del process.scoutingPFJetRecluster2FlavourCategory

# HHBBTT: whitelist v3 — drop the 20 muon track-parametrization vars (JFS 2026-07-11).
# outputCommands cannot drop FlatTable columns -> delete the Var entries at table level.
_MUON_TRK_DROP = [
    "trk_lambda", "trk_lambdaError", "trk_lambda_dsz_cov", "trk_lambda_dxy_cov",
    "trk_lambda_phi_cov", "trk_ndof", "trk_phi", "trk_phiError",
    "trk_phi_dsz_cov", "trk_phi_dxy_cov", "trk_pt", "trk_qoverp",
    "trk_qoverpError", "trk_qoverp_dsz_cov", "trk_qoverp_dxy_cov",
    "trk_qoverp_lambda_cov", "trk_qoverp_phi_cov", "trk_vx", "trk_vy", "trk_vz",
]
for _v in _MUON_TRK_DROP:
    if hasattr(process.scoutingMuonVtxTable.variables, _v):
        delattr(process.scoutingMuonVtxTable.variables, _v)
    # HHBBTT: NoVtx mirror PENDING Marc/JFS confirm — uncomment to enable:
    # if hasattr(process.scoutingMuonNoVtxTable.variables, _v):
    #     delattr(process.scoutingMuonNoVtxTable.variables, _v)

# HHBBTT: PF-candidate table — stock scouting nano does NOT write it. KEEP_PF=True keeps it.
if KEEP_PF:
    process = addScoutingPFCandidate(process)


# Customisation from command line

#process.source.delayReadingEventProducts = cms.untracked.bool(False)
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
