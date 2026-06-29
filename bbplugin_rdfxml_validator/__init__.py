"""
bblocks rdf/xml validator plugin.

Follows the bblocks validator plugin contract:
  - class attributes `mime_types` and/or `file_extensions` declare which files are handled
  - validate(self, meta) receives a meta namespace and returns list[dict] | None
      meta.input_path              absolute path to the file
      meta.mime_type               MIME type string or None
      meta.display_filename        original filename for use in messages
      meta.schema_ref              schema ref from snippet, or None
      meta.context                 namespace with:
        .bblock_id                   building block identifier
        .bblock_name                 building block name
        .register_base_url           base URL of the register
        .validation_resources        list of {ref, format[, conformsTo]} dicts where ref
                                     is a cwd-relative local path or a URL
  - each dict: {"message": str, "is_error": bool, "payload"?: dict}
  - return None or [] to signal "nothing to report"
"""

from rdflib import Graph
from rdflib.exceptions import Error

class RdfXmlValidator:
    """Validates RDF/XML files declared as bblock resources.

    Example bblock.json declaration:
        "resources": [{
            "role": "validation",
            "ref": "",
            "format": "application/rdf+xml",
            "conformsTo": "https://www.w3.org/2001/XMLSchema"
        }]
    """

    mime_types = ['application/rdf+xml']
    file_extensions = ['.xml', '.rdf']

    def validate(self, meta):
        """Validate the RDF/XML file at meta.input_path.

        Returns list[dict] | None
        """
        try:
            graph = Graph()
            graph.parse(meta.input_path, format='xml')

            graph.serialize(meta.input_path.replace('.xml', '.ttl'), format='turtle')
        except Error as err:
            return [{'message': f'Invalid RDF/XML file: {err}', 'is_error': True}]

        return [{'message': f'RDF/XML file is valid ({meta.display_filename})',
                 'is_error': False}]
        