from . import *

class Modules(Components):

    @pretty_format
    def workflow_view(self, **kwargs):
       return '''\
       A.view { it }
       B.view { it }
       C.view { it }
       D.view { it }
       E.view { it }
       '''

    @pretty_format
    def echo(self, **kwargs):
        return('''\
        process {child} {{
            output:
            stdout into {child}

            """
            printf {word}
            """
        }}
        '''.format(**kwargs))

    @pretty_format
    def join(self, **kwargs):
        return('''\
        process {child} {{
            input:
            val x from {parent}

            output:
            stdout into {child}

            """
            printf "${{x}}_{word}"
            """
        }}
        '''.format(**kwargs))
