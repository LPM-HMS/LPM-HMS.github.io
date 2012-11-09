import cosmos.session
from cosmos.Workflow.models import Workflow
from cosmos.contrib import step
import steps
import os
import make_data_dict
import json

##make samples dictionary
samples=[]

if os.environ['COSMOS_SETTINGS_MODULE'] == 'config.gpp':
    WF = Workflow.start(name='GATK Test',restart=True)
    data_dict = json.loads(make_data_dict.main(input_dir='/nas/erik/ngs_data/test_data3',depth=1))
#    WF = Workflow.start(name='GP 48Exomes with Simulated',default_queue='high_priority',restart=False)
#    data_dict = json.loads(make_data_dict.main(input_dir='/nas/erik/ngs_data/48exomes',depth=2))
#    simulated = [s for s in make_data_dict.yield_simulated_files(input_dir='/nas/erik/ngs_data/simulated')]
#    data_dict += simulated
elif os.environ['COSMOS_SETTINGS_MODULE'] == 'config.orchestra':
#    WF = Workflow.start(name='GPP 48Exomes GATK i2b2',default_queue='i2b2_2h',restart=True)
#    data_dict = json.loads(make_data_dict.main(input_dir='/scratch/esg21/ngs_data/test_data2',depth=1))
    WF = Workflow.start(name='GPP 48Exomes GATK Shared Queue',default_queue='shared_2h',restart=True)
    data_dict = json.loads(make_data_dict.main(input_dir='/scratch/esg21/ngs_data/48exomes',depth=2))
    simulated = [s for s in make_data_dict.yield_simulated_files(input_dir='/scratch/esg21/ngs_data/simulated')]
    data_dict += simulated

#Enable steps
step.workflow = WF

### Alignment
bwa_aln = steps.BWA_Align("BWA Align").none2many(data_dict=data_dict)
bwa_sampe = steps.BWA_Sampe("BWA Sampe").many2one(input_step=bwa_aln,group_by=['sample','lane','fq_chunk'])
clean_bams = steps.CleanSam("Clean Bams").one2one(input_step=bwa_sampe,input_type='sam')
"""
Following the "Best" GATK practices for deduping, realignment, and bqsr
for each sample
    lanes.bam <- merged lane.bams for sample
    dedup.bam <- MarkDuplicates(lanes.bam)
    realigned.bam <- realign(dedup.bam) [with known sites included if available]
    recal.bam <- recal(realigned.bam)
    sample.bam <- recal.bam
"""
contigs = [str(x) for x in range(1,23)+['X','Y']] #list of chroms: [1,2,3,..X,Y]

sample_bams = steps.MergeSamFiles("Merge Bams by Sample").many2one(clean_bams,group_by=['sample'],assume_sorted=False)
deduped_samples = steps.MarkDuplicates("Mark Duplicates in Samples").one2one(sample_bams)
index_samples = steps.BuildBamIndex("Index Deduped Samples").one2one(deduped_samples)
rtc_by_sample_chr = steps.RealignerTargetCreator("RealignerTargetCreator by Sample Chr").multi_one2many([deduped_samples,index_samples],intervals=contigs)
realigned_by_sample_chr = steps.IndelRealigner("IndelRealigner by Sample Chr").multi_one2one([rtc_by_sample_chr,deduped_samples],model='USE_READS')
bqsr_by_sample = steps.BaseQualityScoreRecalibration("Base Quality Score Recalibration by Sample").many2one(realigned_by_sample_chr,group_by=['sample'])
recalibrated_samples = steps.PrintReads("Apply BQSR").multi_many2one([realigned_by_sample_chr,bqsr_by_sample],group_by=['sample'])

# Variant Calling
ug = steps.UnifiedGenotyper("Unified Genotyper").many2many(recalibrated_samples,group_by=[],intervals=contigs)
cv1 = steps.CombineVariants("Combine Variants").many2one(ug,group_by=['glm'])
inbreeding_coeff = len(samples)> 19 #20 samples are required to use this annotation for vqr
vqr = steps.VariantQualityRecalibration("Variant Quality Recalibration").one2one(cv1,exome_or_wgs='exome',inbreeding_coeff=inbreeding_coeff)
ar = steps.ApplyRecalibration("Apply Recalibration").multi_one2one([cv1,vqr])
cv2 = steps.CombineVariants("Combine Variants2").many2one(ar,group_by=[])
    
WF.run()
