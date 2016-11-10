import biothings.dataload.uploader as uploader
from dataload.uploader import SnepffPostUpdateUploader

class MutDBUploader(uploader.DummySourceUploader,SnepffPostUpdateUploader):
    """Originally downloaded from: http://www.mutdb.org/"""

    name = "mutdb"
    id_type = 'observed'

    @classmethod
    def get_mapping(klass):
        mapping = {
            "mutdb": {
                "properties": {
                    "rsid": {
                        "type": "string",
                        "include_in_all": True,
                        "analyzer": "string_lowercase",
                    },
                    "ref": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "alt": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "uniprot_id": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "mutpred_score": {
                        "type": "double"
                    },
                    "cosmic_id": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "chrom": {
                        "type": "string",
                        "analyzer": "string_lowercase"
                    },
                    "hg19": {
                        "properties": {
                            "start": {
                                "type": "long"
                            },
                            "end": {
                                "type": "long"
                            }
                        }
                    },
                    "strand": {
                        "type": "string",
                        "index": "not_analyzed"
                    }
                }
            }
        }
        return mapping

