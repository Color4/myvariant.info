# -*- coding: utf-8 -*-
__METADATA__ = {
    "src_name": 'clinvar',
    "src_url": 'ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/',
    "release": '2015-11',
    "field": 'clinvar'
}

# -*- coding: utf-8 -*-


def get_mapping():
    mapping = {
        "clinvar": {
            "properties": {
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
                "hg38": {
                    "properties": {
                        "start": {
                            "type": "long"
                        },
                        "end": {
                            "type": "long"
                        }
                    }
                },
                "omim": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "uniprot": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "cosmic": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "dbvar": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "chrom": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "gene": {
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                        },
                        "id": {
                            "type": "long"
                        }
                    }
                },
                "type": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "rsid": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "rcv": {
                    "type": "nested",
                    "properties": {
                        "accession": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                        },
                        "clinical_significance": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                        },
                        "number_submitters": {
                            "type": "byte"
                        },
                        "review_status": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                        },
                        "last_evaluated": {
                            "type": "date"
                        },
                        "preferred_name": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                        },
                        "origin": {
                            "type": "string",
                            "analyzer": "string_lowercase"
                        },
                        "conditions": {
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "analyzer": "string_lowercase"
                                },
                                "synonyms": {
                                    "type": "string",
                                    "analyzer": "string_lowercase"
                                },
                                "identifiers": {
                                    "properties": {
                                        "efo": {
                                            "type": "string",
                                            "analyzer": "string_lowercase"
                                        },
                                        "gene": {
                                            "type": "string",
                                            "analyzer": "string_lowercase"
                                        },
                                        "medgen": {
                                            "type": "string",
                                            "analyzer": "string_lowercase"
                                        },
                                        "omim": {
                                            "type": "string",
                                            "analyzer": "string_lowercase"
                                        },
                                        "orphanet": {
                                            "type": "string",
                                            "analyzer": "string_lowercase"
                                        },
                                        "human_phenotype_ontology": {
                                            "type": "string",
                                            "analyzer": "string_lowercase"
                                        }
                                    }
                                },
                                "age_of_onset": {
                                    "type": "string",
                                    "analyzer": "string_lowercase"
                                }
                            }
                        }
                    }
                },
                "cytogenic": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "allele_id": {
                    "type": "integer"
                },
                "variant_id": {
                    "type": "integer"
                },

                "coding_hgvs_only": {
                    "type": "boolean"
                },
                "ref": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                },
                "alt": {
                    "type": "string",
                    "analyzer": "string_lowercase"
                }
            }
        }
    }
    return mapping
