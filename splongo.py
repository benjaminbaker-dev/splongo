import json

from pymongo import MongoClient
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
    db = Option(
        doc='''
        **Syntax:** **db=***<db>*
        **Description:** MongoDB database to connect to
        ''',
        require=True
    )
    collection = Option(
        doc='''
        **Syntax:** **collection=***<collection>*
        **Description:** MongoDB collection to connect to
        '''
    )

    def generate(self):
        client = MongoClient(self.hostname)
        coll = client[self.db][self.collection]

        try:
            query = self.fieldnames[0]
            formatted_query = query.replace("'", '"')  # replace single qoutes with double qoutes
            json_query = json.loads(formatted_query)
        except Exception as e:
            raise SyntaxError("could not parse raw query ")

        data = coll.find(json_query)
        for doc in data:
            doc = self._format_result(doc)
            yield {'_raw': json.dumps(doc)}

    def _format_result(self, doc):
        """
        need to stringify object id
        """
        for key, value in doc.items():
            if type(value).__name__ == 'ObjectId':
                doc[key] = str(value)
        return doc


dispatch(Splongo)
