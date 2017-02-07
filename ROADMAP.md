
# ROADMAP

## API

* Config directory for JSON schema files
* API for listing schemas
* API for returning a schema
* API for CRUD operations against a particular schema, including validation.

## API Documentation

https://github.com/OAI/OpenAPI-Specification/wiki/Hello-World-Sample

## Import schema

Write command to import a schema - can be JSON Schema or XSD, remote or local.
On import, file in transformed to JSON Schema / Validated as JSON Schema.  
If no title or description in JSON Schema, user is prompted to enter them.  
JSON Schema file is added to config/schema dir.

## User auth

Implement user auth
BASIC: API write endpoints protected; read endpoints exposed
Identify a JSON-LD schema to use for the user.  This is installed by default. Editable in code to change user settings.

https://jwt.io/introduction/

https://auth0.com/blog/build-an-app-with-vuejs/

## Schema versioning

JSON schema files loaded into MongoDB.  When changed, new version is created with timestamp.  Data can be rebuilt with the correct schema.

Easy to write migration scripts for the data - possibly using http://jsonpatch.com/

## Data versioning

On save, all data is versioned.  Only create revision if data has changed.
  
## API Hooks / Override

Need to provide a mechanism for sites to alter and override the default API functionality.  
Most intuitive way: allow users to add classes, which override particular methods of the API class? Possibly specify __meta__?
 
e.g. Schema file: DwC.
User creates a DwCAPI model, and overrides put method:
```
class DwCAPI(API):
    def put():
        ... Overide code here

```











