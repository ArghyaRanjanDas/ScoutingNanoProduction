// HH->bbtautau CRAB-time preselection (loosev2 kinematic card + group-baked
// b0-leg, group decision 2026-07-10). Runs on the SAME pat::Jet collection the
// ScoutingPFJetReclusterCHS NanoAOD table reads (patScoutingPFJetReclusterCHS,
// table cut="") so index-based cuts here == index-based cuts on the table.
// Collection order, no re-sort, no jet ID. pat::Jet::pt() is JEC-corrected,
// which is exactly what the table stores.

#include <cmath>
#include <cstddef>
#include <string>
#include <vector>

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/Scouting/interface/Run3ScoutingMuon.h"
#include "DataFormats/Scouting/interface/Run3ScoutingElectron.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/global/EDFilter.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/Exception.h"

class HHbbttPreselFilter : public edm::global::EDFilter<> {
public:
  explicit HHbbttPreselFilter(const edm::ParameterSet& cfg);
  bool filter(edm::StreamID, edm::Event& ev, const edm::EventSetup&) const override;
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  const edm::EDGetTokenT<edm::View<pat::Jet>> jetsToken_;
  const edm::EDGetTokenT<std::vector<Run3ScoutingMuon>> muonsToken_;
  const edm::EDGetTokenT<std::vector<Run3ScoutingElectron>> electronsToken_;
  // kinematic card (loosev2; config/cuts.yaml 'preselection')
  const double jetPt0_, jetPt1_, jetPt2_, jetPt3_, jetEtaMax_;
  const double lepPtMin_, lepEtaMax_;
  // b-leg (group-baked): max_j BvsAll[j] > bScoreMin_. 0.65 is LITERAL.
  const double bScoreMin_;
  // NanoAOD-table guard reproduced EXACTLY (Var string: pt>=15 && abs(eta)<=2.5,
  // both INCLUSIVE — distinct from the strict kinematic |eta|<2.5 above).
  const double tagPtMin_, tagEtaMax_;
  std::vector<std::string> discNames_;  // prefix:probb first, then c,uds,g,taup,taum
};

HHbbttPreselFilter::HHbbttPreselFilter(const edm::ParameterSet& cfg)
    : jetsToken_(consumes<edm::View<pat::Jet>>(cfg.getParameter<edm::InputTag>("jets"))),
      muonsToken_(consumes<std::vector<Run3ScoutingMuon>>(cfg.getParameter<edm::InputTag>("muons"))),
      electronsToken_(consumes<std::vector<Run3ScoutingElectron>>(cfg.getParameter<edm::InputTag>("electrons"))),
      jetPt0_(cfg.getParameter<double>("jetPt0")),
      jetPt1_(cfg.getParameter<double>("jetPt1")),
      jetPt2_(cfg.getParameter<double>("jetPt2")),
      jetPt3_(cfg.getParameter<double>("jetPt3")),
      jetEtaMax_(cfg.getParameter<double>("jetEtaMax")),
      lepPtMin_(cfg.getParameter<double>("lepPtMin")),
      lepEtaMax_(cfg.getParameter<double>("lepEtaMax")),
      bScoreMin_(cfg.getParameter<double>("bScoreMin")),
      tagPtMin_(cfg.getParameter<double>("tagPtMin")),
      tagEtaMax_(cfg.getParameter<double>("tagEtaMax")) {
  const std::string prefix = cfg.getParameter<std::string>("taggerPrefix");
  for (const char* p : {"probb", "probc", "probuds", "probg", "probtaup", "probtaum"})
    discNames_.push_back(prefix + ":" + p);
}

bool HHbbttPreselFilter::filter(edm::StreamID, edm::Event& ev, const edm::EventSetup&) const {
  const auto& jets = ev.get(jetsToken_);  // throws loudly if absent (config error)
  const size_t n = jets.size();

  // ---- kinematic leg (index-based, collection order, no re-sort, no jet ID)
  if (n < 3)
    return false;
  auto etaOK = [this](double eta) { return std::abs(eta) < jetEtaMax_; };  // strict, == (>-2.5 && <2.5)
  if (!(jets[0].pt() > jetPt0_ && jets[1].pt() > jetPt1_ && jets[2].pt() > jetPt2_))
    return false;
  if (!(etaOK(jets[0].eta()) && etaOK(jets[1].eta()) && etaOK(jets[2].eta())))
    return false;

  // ---- fourth-object OR (raw index-0 leptons, NO ID; absent/empty => false)
  bool fourth = (n >= 4 && jets[3].pt() > jetPt3_ && etaOK(jets[3].eta()));
  if (!fourth) {
    auto muons = ev.getHandle(muonsToken_);
    if (muons.isValid() && !muons->empty())
      fourth = (*muons)[0].pt() > lepPtMin_ && std::abs((*muons)[0].eta()) < lepEtaMax_;
  }
  if (!fourth) {
    auto electrons = ev.getHandle(electronsToken_);
    if (electrons.isValid() && !electrons->empty())
      fourth = (*electrons)[0].pt() > lepPtMin_ && std::abs((*electrons)[0].eta()) < lepEtaMax_;
  }
  if (!fourth)
    return false;

  // ---- b-leg: max over ALL jets of table-parity BvsAll, > bScoreMin_ (b0 ONLY, NO dR cut)
  // tableVal(p) = (pt>=15 && |eta|<=2.5) ? bDiscriminator(prefix:p) : -1.0   [Var-string parity]
  // BvsAll = tableVal(probb) / sum_{6} tableVal(p). Guarded jet: -1/-6 = +1/6
  // exactly — deliberately NOT clamped, so an offline replay on the written
  // table reproduces this filter bit-for-bit (modulo table float rounding).
  double maxBvsAll = -1e30;
  for (const auto& jet : jets) {
    const bool inGuard = jet.pt() >= tagPtMin_ && std::abs(jet.eta()) <= tagEtaMax_;  // INCLUSIVE
    double num = 0., den = 0.;
    for (size_t i = 0; i < discNames_.size(); ++i) {
      double v = -1.;
      if (inGuard) {
        v = jet.bDiscriminator(discNames_[i]);
        if (v == -1000.)  // pat::Jet sentinel: discriminator not attached => misconfiguration
          throw cms::Exception("Configuration")
              << "HHbbttPreselFilter: discriminator '" << discNames_[i]
              << "' missing on pat::Jet — wrong jets/taggerPrefix wiring?";
      }
      if (i == 0)
        num = v;
      den += v;
    }
    const double bva = num / den;
    if (bva > maxBvsAll)
      maxBvsAll = bva;
  }
  return maxBvsAll > bScoreMin_;
}

void HHbbttPreselFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("jets", edm::InputTag("patScoutingPFJetReclusterCHS"));
  desc.add<edm::InputTag>("muons", edm::InputTag("hltScoutingMuonPackerVtx"));
  desc.add<edm::InputTag>("electrons", edm::InputTag("hltScoutingEgammaPacker"));
  desc.add<std::string>("taggerPrefix", "scoutingPFJetReclusterPFUnifiedParticleTransformerAK4TagsCHS");
  desc.add<double>("jetPt0", 20.);
  desc.add<double>("jetPt1", 20.);
  desc.add<double>("jetPt2", 10.);
  desc.add<double>("jetPt3", 10.);
  desc.add<double>("jetEtaMax", 2.5);
  desc.add<double>("lepPtMin", 4.);
  desc.add<double>("lepEtaMax", 2.5);
  desc.add<double>("bScoreMin", 0.65);  // LITERAL group decision — never remap silently
  desc.add<double>("tagPtMin", 15.);
  desc.add<double>("tagEtaMax", 2.5);
  descriptions.add("hhbbttPreselFilter", desc);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(HHbbttPreselFilter);
