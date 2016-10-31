import FWCore.ParameterSet.Config as cms

from DQMServices.Components.DQMMessageLogger_cfi import *
from DQMServices.Components.DQMDcsInfo_cfi import *
from DQMServices.Components.DQMFastTimerService_cff import *

from DQMOffline.Ecal.ecal_dqm_source_offline_HI_cff import *
from DQM.HcalTasks.OfflineSourceSequence_hi import *
from DQM.SiStripMonitorClient.SiStripSourceConfigTier0_HeavyIons_cff import *
from DQM.SiPixelCommon.SiPixelOfflineDQM_source_cff import *
from DQM.DTMonitorModule.dtDQMOfflineSources_HI_cff import *
from DQM.RPCMonitorClient.RPCTier0Source_cff import *
from DQM.CSCMonitorModule.csc_dqm_sourceclient_offline_cff import *
from DQM.EcalPreshowerMonitorModule.es_dqm_source_offline_cff import *
from DQM.BeamMonitor.AlcaBeamMonitorHeavyIons_cff import *
from DQMOffline.L1Trigger.L1TriggerDqmOffline_cff import *

DQMOfflineHeavyIonsPreDPG = cms.Sequence( dqmDcsInfo *
                                          l1TriggerDqmOffline * # L1 emulator is run within this sequence for real data
                                          ecal_dqm_source_offline *
                                          hcalOfflineSourceSequence *
                                          SiStripDQMTier0_hi *
                                          siPixelOfflineDQM_heavyions_source *
                                          dtSources *
                                          rpcTier0Source *
                                          cscSources *
                                          es_dqm_source_offline )

DQMOfflineHeavyIonsDPG = cms.Sequence( DQMOfflineHeavyIonsPreDPG *
                                       DQMMessageLogger )

from DQMOffline.Muon.muonMonitors_cff import *
diMuonHistos.etaBin = cms.int32(175) #dimuonhistograms mass, bin
diMuonHistos.etaBBin = cms.int32(175)
diMuonHistos.etaEBin = cms.int32(175)
diMuonHistos.etaBinLM = cms.int32(30)
diMuonHistos.etaBBinLM = cms.int32(30)
diMuonHistos.etaEBinLM = cms.int32(30)
diMuonHistos.LowMassMin = cms.double(2.0)
diMuonHistos.LowMassMax = cms.double(14.0)
diMuonHistos.HighMassMin = cms.double(55.0)
diMuonHistos.HighMassMax = cms.double(125.0)
from DQMOffline.JetMET.jetMETDQMOfflineSourceHI_cff import *
from DQMOffline.EGamma.egammaDQMOffline_cff import *
from DQMOffline.Trigger.DQMOffline_Trigger_cff import *
from DQMOffline.RecoB.PrimaryVertexMonitor_cff import *
from DQM.Physics.DQMPhysics_cff import *
from DQM.TrackingMonitorSource.TrackingSourceConfig_Tier0_HeavyIons_cff import *


triggerOfflineDQMSource.remove(jetMETHLTOfflineAnalyzer)

#egammaDQMOffline.remove(electronAnalyzerSequence)
egammaDQMOffline.remove(zmumugammaAnalysis)
egammaDQMOffline.remove(zmumugammaOldAnalysis)
#egammaDQMOffline.remove(photonAnalysis)
photonAnalysis.phoProducer = cms.InputTag("gedPhotonsTmp")
photonAnalysis.isHeavyIon = True
photonAnalysis.barrelRecHitProducer = cms.InputTag("ecalRecHit", "EcalRecHitsEB")
photonAnalysis.endcapRecHitProducer = cms.InputTag("ecalRecHit", "EcalRecHitsEE")

triggerOfflineDQMSource.remove(ak4PFL1FastL2L3CorrectorChain)
from DQMOffline.Trigger.FSQHLTOfflineSource_cfi import getFSQHI
fsqHLTOfflineSource.todo = getFSQHI()


dqmElectronGeneralAnalysis.ElectronCollection = cms.InputTag("gedGsfElectronsTmp")
dqmElectronGeneralAnalysis.TrackCollection = cms.InputTag("hiGeneralTracks")
dqmElectronGeneralAnalysis.VertexCollection = cms.InputTag("hiSelectedVertex")
dqmElectronAnalysisAllElectrons.ElectronCollection = cms.InputTag("gedGsfElectronsTmp")
dqmElectronAnalysisSelectionEt.ElectronCollection = cms.InputTag("gedGsfElectronsTmp")
dqmElectronAnalysisSelectionEtIso.ElectronCollection = cms.InputTag("gedGsfElectronsTmp")
dqmElectronTagProbeAnalysis.ElectronCollection = cms.InputTag("gedGsfElectronsTmp")


stdPhotonAnalysis.isHeavyIon = True
stdPhotonAnalysis.barrelRecHitProducer = cms.InputTag("ecalRecHit", "EcalRecHitsEB")
stdPhotonAnalysis.endcapRecHitProducer = cms.InputTag("ecalRecHit", "EcalRecHitsEE")
hltResults.RecHitsEBTag = cms.untracked.InputTag("ecalRecHit", "EcalRecHitsEB")
hltResults.RecHitsEETag = cms.untracked.InputTag("ecalRecHit", "EcalRecHitsEE")


globalAnalyzer.inputTags.offlinePVs = cms.InputTag("hiSelectedVertex")
trackerAnalyzer.inputTags.offlinePVs = cms.InputTag("hiSelectedVertex")
tightAnalyzer.inputTags.offlinePVs = cms.InputTag("hiSelectedVertex")
looseAnalyzer.inputTags.offlinePVs = cms.InputTag("hiSelectedVertex")

pvMonitor.vertexLabel = cms.InputTag("hiSelectedVertex")


DQMOfflineHeavyIonsPrePOG = cms.Sequence( muonMonitors
                                          * TrackMonDQMTier0_hi
                                          * jetMETDQMOfflineSource
                                          * egammaDQMOffline
                                          * triggerOfflineDQMSource
                                          * pvMonitor
                                          * alcaBeamMonitor
                                          * dqmPhysicsHI
                                          )

#disabled, until an appropriate configuration is set
hltTauOfflineMonitor_PFTaus.Matching.doMatching = False

DQMOfflineHeavyIonsPOG = cms.Sequence( DQMOfflineHeavyIonsPrePOG *
                                       DQMMessageLogger )

DQMOfflineHeavyIons = cms.Sequence( DQMOfflineHeavyIonsPreDPG *
                                    DQMOfflineHeavyIonsPrePOG *
                                    DQMMessageLogger )

#this is needed to have a light sequence for T0 processing
liteDQMOfflineHeavyIons = cms.Sequence ( DQMOfflineHeavyIons )
liteDQMOfflineHeavyIons.remove( SiStripMonitorCluster )
liteDQMOfflineHeavyIons.remove( jetMETDQMOfflineSource )

#DQMOfflineHeavyIonsPhysics = cms.Sequence( dqmPhysics )

##############################################################################
# modifications of muon DQMOffline for pPb run
def customiseRun2PPB_MuonDQMOffline(process):
  if hasattr(process, 'globalAnalyzer'):
    process.globalAnalyzer.targetParams.ptCut_Jpsi = cms.untracked.double( 5.0)
    process.globalAnalyzer.binParams.ptCoarse = cms.untracked.vdouble(  0.,1.,2.,3.,4.,5.,7.,9.,12.,15.,20.,30.,40.)
  if hasattr(process, 'trackerAnalyzer'):
    process.trackerAnalyzer.targetParams.ptCut_Jpsi = cms.untracked.double(5.0)
    process.trackerAnalyzer.binParams.ptCoarse = cms.untracked.vdouble( 0.,1.,2.,3.,4.,5.,7.,9.,12.,15.,20.,30.,40.)
  if hasattr(process, 'tightAnalyzer'):
    process.tightAnalyzer.targetParams.ptCut_Jpsi = cms.untracked.double(  5.0)
    process.tightAnalyzer.binParams.ptCoarse = cms.untracked.vdouble(   0.,1.,2.,3.,4.,5.,7.,9.,12.,15.,20.,30.,40.)
  if hasattr(process, 'looseAnalyzer'):
    process.looseAnalyzer.targetParams.ptCut_Jpsi = cms.untracked.double(  5.0)
    process.looseAnalyzer.binParams.ptCoarse = cms.untracked.vdouble(   0.,1.,2.,3.,4.,5.,7.,9.,12.,15.,20.,30.,40.)
  if hasattr(process, 'diMuonHistos'):
    process.diMuonHistos.etaBin = cms.int32(175)
    process.diMuonHistos.etaBBin = cms.int32(175)
    process.diMuonHistos.etaEBin = cms.int32(175)
    process.diMuonHistos.etaBinLM = cms.int32(30)
    process.diMuonHistos.etaBBinLM = cms.int32(30)
    process.diMuonHistos.etaEBinLM = cms.int32(30)
    process.diMuonHistos.LowMassMin = cms.double(2.0)
    process.diMuonHistos.LowMassMax = cms.double(14.0)
    process.diMuonHistos.HighMassMin = cms.double(55.0)
    process.diMuonHistos.HighMassMax = cms.double(125.0)
  return process
