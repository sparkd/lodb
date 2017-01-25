var generated_Module_Factory = function () {
  var generated = {
    name: 'generated',
    typeInfos: [{
        localName: 'Shiporder.Item',
        typeName: null,
        propertyInfos: [{
            name: 'title',
            required: true,
            elementName: {
              localPart: 'title'
            }
          }, {
            name: 'note',
            elementName: {
              localPart: 'note'
            }
          }, {
            name: 'quantity',
            required: true,
            elementName: {
              localPart: 'quantity'
            },
            typeInfo: 'PositiveInteger'
          }, {
            name: 'price',
            required: true,
            elementName: {
              localPart: 'price'
            },
            typeInfo: 'Decimal'
          }]
      }, {
        localName: 'Shiporder.Shipto',
        typeName: null,
        propertyInfos: [{
            name: 'name',
            required: true,
            elementName: {
              localPart: 'name'
            }
          }, {
            name: 'address',
            required: true,
            elementName: {
              localPart: 'address'
            }
          }, {
            name: 'city',
            required: true,
            elementName: {
              localPart: 'city'
            }
          }, {
            name: 'country',
            required: true,
            elementName: {
              localPart: 'country'
            }
          }]
      }, {
        localName: 'Shiporder',
        typeName: null,
        propertyInfos: [{
            name: 'orderperson',
            required: true,
            elementName: {
              localPart: 'orderperson'
            }
          }, {
            name: 'shipto',
            required: true,
            elementName: {
              localPart: 'shipto'
            },
            typeInfo: '.Shiporder.Shipto'
          }, {
            name: 'item',
            required: true,
            collection: true,
            elementName: {
              localPart: 'item'
            },
            typeInfo: '.Shiporder.Item'
          }, {
            name: 'orderid',
            required: true,
            attributeName: {
              localPart: 'orderid'
            },
            type: 'attribute'
          }]
      }],
    elementInfos: [{
        typeInfo: '.Shiporder',
        elementName: {
          localPart: 'shiporder'
        }
      }]
  };
  return {
    generated: generated
  };
};
if (typeof define === 'function' && define.amd) {
  define([], generated_Module_Factory);
}
else {
  var generated_Module = generated_Module_Factory();
  if (typeof module !== 'undefined' && module.exports) {
    module.exports.generated = generated_Module.generated;
  }
  else {
    var generated = generated_Module.generated;
  }
}