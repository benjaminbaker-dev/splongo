from splunklib.searchcommands import dispatch, GeneratingCommand, Configuration, Option, validators


@Configuration()
class Splongo(GeneratingCommand):
    hostname = Option(
        doc='''
        **Syntax:** **hostname=***<hostname>*
        **Description:** MongoDB host to connect to
        ''',
        require=True,
        validate=validators.Fieldname()
    )
    query = Option(
        doc='''
        **Syntax:** **query=***<query>*
        **Description:** query to perform, json.loads() will be called on field
        ''',
        require=True
    )

    def generate(self):
        pass


dispatch(Splongo)
