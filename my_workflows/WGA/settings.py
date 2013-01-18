import os
from cosmos import session

if session.settings.server_name == 'gpp':
    resource_bundle_path = '/nas/erik/bundle/1.5/b37'
    tools_dir = '/home/ch158749/tools'
    settings = {
        'GATK_path' : os.path.join(tools_dir,'GenomeAnalysisTKLite-2.1-8-gbb7f038/GenomeAnalysisTKLite.jar'),
        'Picard_dir' : os.path.join(tools_dir,'picard-tools-1.77'),
        'bwa_path' : os.path.join(tools_dir,'bwa-0.6.2/bwa'),
        'bwa_reference_fasta_path' : '/nas/erik/bwa_reference/human_g1k_v37.fasta',
        }
elif session.settings.server_name  == 'orchestra':
    resource_bundle_path = '/groups/lpm/erik/WGA/bundle/2.2/b37'
    tools_dir = '/groups/lpm/erik/WGA/tools'
    settings = {
        'GATK_path' :os.path.join(tools_dir,'GenomeAnalysisTKLite-2.2-16-g2cc9ef8/GenomeAnalysisTKLite.jar'),
        'Picard_dir' : os.path.join(tools_dir,'picard-tools-1.78'),
        'bwa_path' : os.path.join(tools_dir,'bwa-0.6.2/bwa'),
        'bwa_reference_fasta_path' : '/groups/lpm/erik/WGA/bwa_reference/human_g1k_v37.fasta',
        }
elif session.settings.server_name  == 'bioseq':
    resource_bundle_path = '/cosmos/WGA/bundle/2.2/b37/'
    tools_dir = '/cosmos/WGA/tools'
    settings = {
        'GATK_path' :os.path.join(tools_dir,'GenomeAnalysisTKLite-2.2-16-g2cc9ef8/GenomeAnalysisTKLite.jar'),
        'Picard_dir' : os.path.join(tools_dir,'picard-tools-1.81'),
        'bwa_path' : os.path.join(tools_dir,'bwa-0.6.2/bwa'),
        'bwa_reference_fasta_path' : '/cosmos/WGA/bwa_reference/human_g1k_v37.fasta',
        }
elif session.settings.server_name  == 'default':
    resource_bundle_path = '/cosmos/WGA/bundle/2.2/b37/'
    tools_dir = '/cosmos/WGA/tools'
    settings = {
        'GATK_path' :os.path.join(tools_dir,'GenomeAnalysisTKLite-2.2-16-g2cc9ef8/GenomeAnalysisTKLite.jar'),
        'Picard_dir' : os.path.join(tools_dir,'picard-tools-1.81'),
        'bwa_path' : os.path.join(tools_dir,'bwa-0.6.2/bwa'),
        'bwa_reference_fasta_path' : '/cosmos/WGA/bwa_reference/human_g1k_v37.fasta',
        }
settings.update({
    'resource_bundle_path' : resource_bundle_path,
    'tmp_dir' : session.settings.tmp_dir,
    'reference_fasta_path' : os.path.join(resource_bundle_path,'human_g1k_v37.fasta'),
    'dbsnp_path' : os.path.join(resource_bundle_path,'dbsnp_137.b37.vcf'),
    'hapmap_path' : os.path.join(resource_bundle_path,'hapmap_3.3.b37.vcf'),
    'omni_path' : os.path.join(resource_bundle_path,'1000G_omni2.5.b37.vcf'),
    'mills_path' : os.path.join(resource_bundle_path,'Mills_and_1000G_gold_standard.indels.b37.vcf'),
    'indels_1000g_phase1_path' : os.path.join(resource_bundle_path,'1000G_phase1.indels.b37.vcf')
})