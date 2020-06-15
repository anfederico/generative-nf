from . import *

class Components():

    def __init__(self):
        pass

    @pretty_format
    def config_manifest(self):
        return '''\
        manifest {
          description = 'Proof of concept for generative workflows in Nextflow'
          nextflowVersion = '>= 20.04.1'
        }
        '''

    @pretty_format
    def config_profiles(self):
        return '''\
        profiles {
          local {includeConfig 'configs/local.config'}
          sge {includeConfig 'configs/sge.config'}
          aws {includeConfig 'configs/aws.config'}
        }
        '''

    @pretty_format
    def config_params(self):
        return '''\
        params {
          output = ''
          email = ''
        }
        '''

    def workflow_shebang(self):
        return '#!/usr/bin/env nextflow\n'

    def workflow_version(self):
        return 'VERSION="1.0"\n'

    @pretty_format
    def workflow_help(self):
        return '''\
        params.help = ""
        if (params.help) {
          log.info " "
          log.info "USAGE: "
          log.info " "
          log.info "nextflow run workflow.nf -c workflow.config -profile {profile}"
          log.info " "
          exit 1
        }
        '''

    @pretty_format
    def workflow_header(self, tree):
        hierarchy = render_tree(tree, 'label')
        return '''\
        log.info """

        W O R K F L O W ~ Configuration
        ===============================
        output    : ${{params.output}}
        -------------------------------
        Hierarchy

        {hierarchy}

        """
        '''.format(hierarchy=hierarchy)

    @pretty_format
    def workflow_complete(self):
        return '''\
        workflow.onComplete {
          println (workflow.success ? "Success: Pipeline Done :)" : "Error: Pipeline Broke :/")
          def subject = 'Pipeline Status'
          def recipient = (params.email)
            ['mail', '-s', subject, recipient].execute() << """
            Pipeline Summary
            ---------------------------
            Timestamp    : ${workflow.complete}
            Duration     : ${workflow.duration}
            Success      : ${workflow.success}
            Work Dir     : ${workflow.workDir}
            Exit Status  : ${workflow.exitStatus}
            Error Report : ${workflow.errorReport ?: '-'}
            """
        }
        '''