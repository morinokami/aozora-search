from elasticsearch import Elasticsearch


class SearchEngine:

    index = 'aozora-search'

    def __init__(self):
        self.es = Elasticsearch()

    def search(self, q, page):
        query = {
            'match': {
                'main_text': {
                    'query': q,
                    'operator': 'and'
                }
            }
        }
        highlight = {
            'fields': {
                'main_text': {}
            }
        }
        from_ = (page - 1) * 10

        res = self.es.search(
            index=SearchEngine.index,
            body={
                'query': query,
                'highlight': highlight,
                'from': from_
            }
        )
        total = res['hits']['total']

        return res, total

    def advanced_search(self, q, title, author, publisher, page):
        must = []
        if q:
            query = {
                'match': {
                    'main_text': {
                        'query': q,
                        'operator': 'and'
                    }
                }
            }
        if title:
            must.append({'term': {'title': title}})
        if author:
            must.append({'term': {'author': author}})
        if publisher:
            must.append({'term': {'orig_pub': publisher}})

        highlight = {
            'fields': {
                'main_text': {}
            }
        }
        from_ = (page - 1) * 10

        if q and must:
            res = self.es.search(
                index=SearchEngine.index,
                body={
                    'query': {
                        'filtered': {
                            'query': query,
                            'filter': {
                                'bool': {
                                    'must': must
                                }
                            }
                        }
                    },
                    'highlight': highlight,
                    'from': from_
                }
            )
        elif not must:
            res = self.es.search(
                index=SearchEngine.index,
                body={
                    'query': query,
                    'highlight': highlight,
                    'from': from_
                }
            )
        elif not q:
            res = self.es.search(
                index=SearchEngine.index,
                body={
                    'query': {
                        'filtered': {
                            'filter': {
                                'bool': {
                                    'must': must
                                }
                            }
                        }
                    },
                    'from': from_
                }
            )
            for r in res['hits']['hits']:
                r['highlight'] = None
        else:
            pass  # err
        total = res['hits']['total']

        return res, total

    def search_book(self, book_id):
        query = {
            'filtered': {
                'query': {
                    'match_all': {}
                },
                'filter': {
                    'term': {
                        'book_id': book_id
                    }
                }
            }
        }

        return self.es.search(
            index=SearchEngine.index,
            body={
                'query': query
            }
        )

    def search_inside_book(self, q, book_id):
        query = {
            "filtered": {
                "query": {
                    "match": {
                        "main_text": q
                    }
                },
                "filter": {
                    "term": {
                        "book_id": book_id
                    }
                }
            }
        }
        highlight = {
            'fields': {
                'main_text': {}
            }
        }

        return self.es.search(
            index=SearchEngine.index,
            body={
                'query': query,
                'highlight': highlight
            }
        )
