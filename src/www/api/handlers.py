import re
import json

from tornado.web import HTTPError
from www.helper import BaseHandler
from .es import ESQuery
from utils.common import split_ids
import config


class VariantHandler(BaseHandler):
    esq = ESQuery()

    def get(self, vid=None):
        '''
        /variant/<variantid>
            varintid can be HGVS name.
        /variant/chr1:g.160145907G>T
        /variant/chr1:g.160145907G>T?fields=dbsnp
        /variant/chr1:g.160145907G>T?fields=dbnsfp.genename,dbnsfp.cadd

        parameters:
            fields
            callback
            email
        '''
        if vid:
            kwargs = self.get_query_params()
            if kwargs.pop('hg38', False):
                self.esq._use_hg38()
            variant = self.esq.get_variant(vid, **kwargs)
            if variant:
                self.return_json(variant)
                self.ga_track(event={'category': 'v1_api',
                                     'action': 'variant_get'})
            else:
                raise HTTPError(404)
        else:
            raise HTTPError(404)

    def post(self, ids=None):
        '''
           This is essentially the same as post request in QueryHandler, with different defaults.

           parameters:
            ids
            fields
            email
        '''
        kwargs = self.get_query_params()
        if kwargs.pop('hg38', False):
            self.esq._use_hg38()
        ids = kwargs.pop('ids', None)
        if ids:
            ids = re.split('[\s\r\n+|,]+', ids)
            res = self.esq.mget_variants2(ids, **kwargs)
        else:
            res = {'success': False, 'error': "Missing required parameters."}
        encode = not isinstance(res, str)    # when res is a string, e.g. when rawquery is true, do not encode it as json
        self.return_json(res, encode=encode)
        self.ga_track(event={'category': 'v1_api',
                             'action': 'variant_post',
                             'label': 'qsize',
                             'value': len(ids) if ids else 0})


class QueryHandler(BaseHandler):
    esq = ESQuery()

    def get(self):
        '''
        parameters:
            q
            fields
            from
            size
            sort
            facets
            callback
            email
            fetch_all

            explain
            raw
        '''
        kwargs = self.get_query_params()
        if kwargs.pop('hg38', False):
            self.esq._use_hg38()
        q = kwargs.pop('q', None)
        scroll_id = kwargs.pop('scroll_id', None)
        _has_error = False
        if scroll_id:
            res = self.esq.scroll(scroll_id, **kwargs)
        elif q:
            for arg in ['from', 'size']:
                value = kwargs.get(arg, None)
                if value:
                    try:
                        kwargs[arg] = int(value)
                    except ValueError:
                        res = {'success': False, 'error': 'Parameter "{}" must be an integer.'.format(arg)}
                        _has_error = True
            if not _has_error:
                res = self.esq.query(q, **kwargs)
                if kwargs.get('fetch_all', False):
                    self.ga_track(event={'category': 'v1_api',
                                         'action': 'fetch_all',
                                         'label': 'total',
                                         'value': res.get('total', None)})

        else:
            res = {'success': False, 'error': "Missing required parameters."}

        self.return_json(res)
        self.ga_track(event={'category': 'v1_api',
                             'action': 'query_get',
                             'label': 'qsize',
                             'value': len(q) if q else 0})

    def post(self):
        '''
        parameters:
            q
            scopes
            fields
            email

            jsoninput   if true, input "q" is a json string, must be decoded as a list.
        '''
        kwargs = self.get_query_params()
        if kwargs.pop('hg38', False):
            self.esq._use_hg38()
        q = kwargs.pop('q', None)
        jsoninput = kwargs.pop('jsoninput', None) in ('1', 'true')
        if q:
            # ids = re.split('[\s\r\n+|,]+', q)
            try:
                ids = json.loads(q) if jsoninput else split_ids(q)
                if not isinstance(ids, list):
                    raise ValueError
            except ValueError:
                ids = None
                res = {'success': False, 'error': 'Invalid input for "q" parameter.'}
            if ids:
                scopes = kwargs.pop('scopes', None)
                fields = kwargs.pop('fields', None)
                res = self.esq.mget_variants2(ids, fields=fields, scopes=scopes, **kwargs)
        else:
            res = {'success': False, 'error': "Missing required parameters."}

        encode = not isinstance(res, str)    # when res is a string, e.g. when rawquery is true, do not encode it as json
        self.return_json(res, encode=encode)
        self.ga_track(event={'category': 'v1_api',
                             'action': 'query_post',
                             'label': 'qsize',
                             'value': len(q) if q else 0})


class MetaDataHandler(BaseHandler):
    disable_caching = True

    def get(self):
        # For now, just return a hardcoded object, later we'll actually query the ES db for this information
        self.return_json({
            "stats": {
                "total": 334293173,
                "cadd": 226932858,
                "clinvar": 127745,
                "cosmic": 1024498,
                "dbnsfp": 82030830,
                "dbsnp": 145132257,
                "docm": 1119,
                "emv": 12066,
                "evs": 1977300,
                "exac": 10195872,
                "grasp": 2212148,
                "gwassnps": 15243,
                "mutdb": 420221,
                "snpedia": 5907,
                "snpeff": 316823328,
                "wellderly": 21240519
            },
            "src_version": {
                "cadd": "1.3",
                "clinvar": "201511",
                "cosmic": "68",
                "dbnsfp": "3.0c",
                "dbsnp": "144",
                "evs": "2",
                "exac": "0.3",
                "grasp": "2.0.0.0"
            },
            "timestamp": "2015-10-21T07:02:18.178506"
        })


class FieldsHandler(BaseHandler):
    esq = ESQuery()

    def get(self):
        notes = json.load(open(config.FIELD_NOTES_PATH, 'r'))
        es_mapping = self.esq.query_fields()

        def get_indexed_properties_in_dict(d, prefix):
            r = {}
            for (k, v) in d.items():
                r[prefix + '.' + k] = {}
                r[prefix + '.' + k]['indexed'] = False
                if 'type' in v:
                    r[prefix + '.' + k]['type'] = v['type']
                    if ('index' not in v) or ('index' in v and v['index'] != 'no'):
                        # indexed field
                        r[prefix + '.' + k]['indexed'] = True
                else:
                    r[prefix + '.' + k]['type'] = 'object'
                    r.update(get_indexed_properties_in_dict(v['properties'], prefix + '.' + k))
                if ('include_in_all' in v) and v['include_in_all']:
                    r[prefix + '.' + k]['include_in_all'] = True
                else:
                    r[prefix + '.' + k]['include_in_all'] = False
            return r

        r = {}
        for (k, v) in get_indexed_properties_in_dict(es_mapping, '').items():
            k1 = k.lstrip('.')
            r[k1] = v
            if k1 in notes:
                r[k1]['notes'] = notes[k1]
        self.return_json(r)


APP_LIST = [
    (r"/variant/(.+)/?", VariantHandler),   # for variant get request
    (r"/variant/?$", VariantHandler),       # for variant post request
    (r"/query/?", QueryHandler),            # for query get/post request
    (r"/metadata", MetaDataHandler),        # for metadata requests
    (r"/metadata/fields", FieldsHandler),   # for available field information
]
