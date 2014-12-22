from rdflib import URIRef, RDF


def enrich(graph):
    for uri in graph.subjects(predicate=RDF.type, object=URIRef('http://schema.org/WebPage')):
        if str(uri).startswith('http://www.bbc.co.uk/programmes/'):
            graph.parse(str(uri) + '.rdf')
            graph.add((uri, URIRef('http://xmlns.com/foaf/0.1/primaryTopic'), uri + '#programme'))


