
JSON-LD Document:

{
  "@context": {
    "name": "http://xmlns.com/foaf/0.1/name",
    "homepage": {
      "@id": "http://xmlns.com/foaf/0.1/workplaceHomepage",
      "@type": "@id"
    },
    "Person": "http://xmlns.com/foaf/0.1/Person"
  },
  "@id": "http://me.example.com",
  "@type": "Person",
  "name": "John Smith",
  "homepage": "http://www.example.com/"
}

How to validate this?


https://lists.w3.org/Archives/Public/public-linked-json/2013Aug/0070.html

For processing data
json.loads(src, object_hook=func)


Is a better way of doing validation, to convert JSON to RDF, and then use XSD?

We need a schema, to build the forms and validate the data.


So create a JSON doc that has both the schema to validate, and then URIs to use in the 

https://github.com/common-workflow-language/schema_salad

When schemas change, store with date in mongo.  Docs can therefore be processes with the appropriate schema.


HOW TO MERGE SCHEMA AND JSON_LD????

https://www.npmjs.com/package/schema-jsonld-context

https://www.youtube.com/watch?v=vioCbTo3C-4


http://stackoverflow.com/questions/36152972/validate-json-against-xml-schema-xsd

https://openbadgespec.org/v2/context.json



One approach
Adding prefix and context info to json-schema - https://github.com/valueflows/valueflows/issues/13#issuecomment-79457550

When publishing, json-ld, tools like https://github.com/holodex/schema-jsonld-context


Another approach - open badges https://lists.w3.org/Archives/Public/public-linked-json/2015Mar/0030.html
https://lists.w3.org/Archives/Public/public-linked-json/2015Mar/0030.html
https://openbadgespec.org/v2/context.json



Check this out - tools for building forms and validation

https://github.com/ahdinosaur?utf8=%E2%9C%93&tab=repositories&q=json&type=&language=
https://github.com/ahdinosaur/jsonform
https://github.com/garycourt/JSV


https://msdn.microsoft.com/en-us/library/dd489271.aspx


https://brandur.org/elegant-apis

https://github.com/interagent/prmd

https://www.haykranen.nl/2015/07/08/perfect-cms/





http://python-eve.org/
http://stackoverflow.com/questions/37587620/python-json-rest-framework-with-deserialiser-and-schema-validation-jsonschema
https://github.com/nicolaiarocci/cerberus/issues/254
https://github.com/inveniosoftware-attic/jsonalchemy/tree/master/jsonalchemy
http://tech.degica.com/en/2015/05/02/automating-api-documentation-with-json-schema/
https://jeffersonheard.github.io/2016/11/creating-new-fields-and-widgets-for-mozillas-react-jsonschema-form/

https://www.youtube.com/watch?v=upGiAG7-Sa4
https://gitscout.com/?utm_content=buffer441a8&utm_medium=social&utm_source=twitter.com&utm_campaign=buffer
https://github.com/flask-restful/flask-restful/issues/204
http://flask-restful.readthedocs.io/en/0.3.5/


https://github.com/mattupstate/flask-jsonschema
http://stackoverflow.com/questions/24238743/flask-decorator-to-verify-json-and-json-schema

http://jsonpatch.com/

Build in such a way, models can be extended???


## Plan

JSON-LD - Can be used to store.

1. Can I create data based on JSON-LD.  
	How does this work with json-schema?  
	Validation process?  	
	Try using some from schema.org?

2. Build process to drop in json-ld schema.  Automatically build API & forms?

3. Can json-ld/json-schema work with any rdf/xsd schema? Try converting DwC-A to JSON-LD?


https://www.haykranen.nl/2015/07/08/perfect-cms/

https://github.com/jdorn/json-editor

http://madebymany.github.io/sir-trevor-js/example.html

http://stackoverflow.com/questions/403420/convert-xsd-into-sql-relational-tables








