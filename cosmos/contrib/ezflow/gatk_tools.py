from tool import Tool,return_inputs
from decorators import fromtags, opoi

def list2input(l):
    return " -I ".join(map(lambda x: str(x),l))

class FASTQ(Tool):
    NOOP = True
    
    __verbose__ = "Fastq Input"
    outputs = ['fastq']

class ALN(Tool):
    __verbose__ = "Reference Alignment"
    inputs = ['fastq']
    outputs = ['sai']
    
    @opoi
    def cmd(self,fastq):
        return 'bwa aln {fastq} > $OUT.sai'
    
class SAMPE(Tool):
    __verbose__ = "Paired End Mapping"
    
    inputs = ['fastq','sai']
    outputs = ['sam']
    
    def map_inputs(self):
        "Expecting 2 parents"
        ps = self.parents
        return return_inputs(fastq1=ps[0].parent.get_output('fastq'),
                      fastq2=ps[1].parent.get_output('fastq'),
                      sai1=ps[0].get_output('sai'),
                      sai2=ps[1].get_output('sai'))
    
    def cmd(self,i,t,p):
        return 'bwa sampe {i[fastq1]} {i[fastq2]} {i[sai1]} {i[sai2]} > $OUT.sam'
    
class CLEAN_SAM(Tool):
    __verbose__ = "Sam Cleaning"
    
    inputs = ['sam']
    outputs = ['bam']
    
    def cmd(self,i,t,p):
        return 'cleansam {0} -o $OUT.bam'.format(list2input(i['sam']))
    
class IRTC(Tool):
    __verbose__ = "Indel Realigner Target Creator"
    
    inputs = ['bam']
    outputs = ['targets']
    
    @fromtags('interval')
    def cmd(self,i,t,p):
        return 'IRTC -I {0} -L {{t[interval]}} > $OUT.targets'.format(list2input(i['bam']))
    
class IR(Tool):
    __verbose__ = "Indel Realigner"
    inputs = ['bam','targets']
    outputs = ['bam']
    
    def map_inputs(self):
        input_bam = self.parent.parent.get_output('bam')
        return return_inputs(input_bam = input_bam,
                      targets = self.parent.get_output('targets'),
                      interval = self.tags['interval'])
    
    def cmd(self,input_bam,targets,interval):
        return 'IR -I {input_bam} -L {interval} -t {targets}'
    
class BQSR(Tool):
    __verbose__ = "Base Quality Score Recalibration"
    inputs = ['bam']
    outputs = ['recal']
    
    def cmd(self,input_bams):
        return 'BQSR -I {0} > $OUT.recal'.format(list2input(input_bams))
    
class PR(Tool):
    __verbose__ = "Apply BQSR"
    inputs = ['bam','recal']
    outputs = ['bam']
    
    def map_inputs(self):
        input_bams = [p.get_output('bam') for p in self.parent.parents ] 
        return return_inputs(input_bams = input_bams,
                      recal = self.parent.get_output('recal'))
    
    def cmd(self,input_bams,recal):
        return 'PrintReads -I {0} -r {{recal}}'.format(list2input(input_bams))
    
    
class UG(Tool):
    __verbose__ = "Unified Genotyper"
    inputs = ['bam']
    outputs = ['vcf']
    
    @fromtags('interval','glm')
    def cmd(self,input_bams,glm,interval):
        return 'UnifiedGenotyper -I {0} -glm {{glm}} -L {{interval}}'.format(list2input(input_bams))
    
class CV(Tool):
    __verbose__ = "Combine Variants"
    
    inputs = ['vcf']
    outputs = ['vcf']
    
    def cmd(self,input_vcfs):
        return 'CombineVariants {ins}'.format(ins=list2input(input_vcfs))
    
class VQSR(Tool):
    __verbose__ = "Variant Quality Score Recalibration"
    inputs = ['vcf']
    outputs = ['recal']
    
    @opoi
    def cmd(self,input_vcf):
        return 'vqsr {input_vcf} > $OUT.recal'
    
class Apply_VQSR(Tool):
    __verbose__ = "Apply VQSR"
    
    inputs = ['vcf','recal']
    outputs = ['vcf']
    
    def map_inputs(self):
        input_vcf = self.parent.get_output('recal') 
        return return_inputs(input_vcf,self.parent.parent.get_output('vcf'))
    
    def cmd(self,input_vcf,recal):
        return 'apply vqsr {input_vcf} {recal} > $OUT.vcf'
    
class ANNOVAR(Tool):
    __verbose__ = "Annovar"
    inputs = ['vcf']
    outputs = ['tsv']
    
    @fromtags('database')
    @opoi
    def cmd(self,input_vcf,database):
        return 'annovar {input_vcf} {database}'
    
class PROCESS_ANNOVAR(Tool):
    __verbose__ = "Process Annovar"
    inputs = ['tsv']
    outputs = ['tsv']
    
    @opoi
    def cmd(self,input_tsv):
        return 'genomekey {input_tsv}'
    
class MERGE_ANNOTATIONS(Tool):
    __verbose__ = "Merge Annotations"
    inputs = ['tsv']
    outputs = ['tsv']
    
    def cmd(self,input_tsvs):
        return 'genomekey merge {0}'.format(','.join(map(lambda x:str(x),input_tsvs)))
    
class SQL_DUMP(Tool):
    __verbose__ = "SQL Dump"
    inputs = ['tsv']
    outputs = ['sql']
    
    @opoi
    def cmd(self,input_tsv):
        return 'sql dump {input_tsv}'
    
class ANALYSIS(Tool):
    __verbose__ = "Filtration And Analysis"
    inputs = ['sql']
    outputs = ['analysis']
    
    @opoi
    def cmd(self,input_sql):
        return 'analyze {input_sql}'
    