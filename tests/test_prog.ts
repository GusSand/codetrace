/*
 * Copyright by LunaSec (owned by Refinery Labs, Inc)
 *
 * Licensed under the Business Source License v1.1
 * (the "License"); you may not use this file except in compliance with the
 * License. You may obtain a copy of the License at
 *
 * https://github.com/lunasec-io/lunasec/blob/master/licenses/BSL-LunaTrace.txt
 *
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */
/* eslint-disable */

// To parse this data:
//
//   import { Convert } from "./file";
//
//   const grypeCvss = Convert.toGrypeCvss(json);
//
// These functions will throw an error if the JSON doesn't
// match the expected interface, even if the JSON is valid.

export interface GrypeCvss {
    VendorMetadata: any;
    Metrics: Metrics;
    Vector: string;
    Version: string;
  }
  
  export interface Metrics {
    BaseScore: number;
    ExploitabilityScore: number;
    ImpactScore: number;
  }
  
  // Converts JSON strings to/from your types
  // and asserts the results of JSON.parse at runtime
  export class Convert {
    public static toGrypeCvss(json) {
      return cast(JSON.parse(json), a(r('GrypeCvss')));
    }
  
    public static grypeCvssToJson(value) {
      return JSON.stringify(uncast(value, a(r('GrypeCvss'))), null, 2);
    }
  }
  
  function invalidValue(typ, val, key = '') {
    if (key) {
      throw Error(`Invalid value for key "${key}". Expected type ${JSON.stringify(typ)} but got ${JSON.stringify(val)}`);
    }
    throw Error(`Invalid value ${JSON.stringify(val)} for type ${JSON.stringify(typ)}`);
  }
  
  function jsonToJSProps(typ) {
    if (typ.jsonToJS === undefined) {
      const map: any = {};
      typ.props.forEach((p) => (map[p.json] = { key: p.js, typ: p.typ }));
      typ.jsonToJS = map;
    }
    return typ.jsonToJS;
  }
  
  function jsToJSONProps(typ): <FILL> {
    if (typ.jsToJSON === undefined) {
      const map: any = {};
      typ.props.forEach((p) => (map[p.js] = { key: p.json, typ: p.typ }));
      typ.jsToJSON = map;
    }
    return typ.jsToJSON;
  }
  
  function transform(val, typ, getProps, key = '') {
    function transformPrimitive(typ, val) {
      if (typeof typ === typeof val) return val;
      return invalidValue(typ, val, key);
    }
  
    function transformUnion(typs, val) {
      // val must validate against one typ in typs
      const l = typs.length;
      for (let i = 0; i < l; i++) {
        const typ = typs[i];
        try {
          return transform(val, typ, getProps);
        } catch (_) {}
      }
      return invalidValue(typs, val);
    }
  
    function transformEnum(cases, val) {
      if (cases.indexOf(val) !== -1) return val;
      return invalidValue(cases, val);
    }
  
    function transformArray(typ, val) {
      // val must be an array with no invalid elements
      if (!Array.isArray(val)) return invalidValue('array', val);
      return val.map((el) => transform(el, typ, getProps));
    }
  
    function transformDate(val) {
      if (val === null) {
        return null;
      }
      const d = new Date(val);
      if (isNaN(d.valueOf())) {
        return invalidValue('Date', val);
      }
      return d;
    }
  
    function transformObject(props, additional, val) {
      if (val === null || typeof val !== 'object' || Array.isArray(val)) {
        return invalidValue('object', val);
      }
      const result: any = {};
      Object.getOwnPropertyNames(props).forEach((key) => {
        const prop = props[key];
        const v = Object.prototype.hasOwnProperty.call(val, key) ? val[key] : undefined;
        result[prop.key] = transform(v, prop.typ, getProps, prop.key);
      });
      Object.getOwnPropertyNames(val).forEach((key) => {
        if (!Object.prototype.hasOwnProperty.call(props, key)) {
          result[key] = transform(val[key], additional, getProps, key);
        }
      });
      return result;
    }
  
    if (typ === 'any') return val;
    if (typ === null) {
      if (val === null) return val;
      return invalidValue(typ, val);
    }
    if (typ === false) return invalidValue(typ, val);
    while (typeof typ === 'object' && typ.ref !== undefined) {
      typ = typeMap[typ.ref];
    }
    if (Array.isArray(typ)) return transformEnum(typ, val);
    if (typeof typ === 'object') {
      return typ.hasOwnProperty('unionMembers')
        ? transformUnion(typ.unionMembers, val)
        : typ.hasOwnProperty('arrayItems')
        ? transformArray(typ.arrayItems, val)
        : typ.hasOwnProperty('props')
        ? transformObject(getProps(typ), typ.additional, val)
        : invalidValue(typ, val);
    }
    // Numbers can be parsed by Date but shouldn't be.
    if (typ === Date && typeof val !== 'number') return transformDate(val);
    return transformPrimitive(typ, val);
  }
  
  function cast<T>(val, typ) {
    return transform(val, typ, jsonToJSProps);
  }
  
  function uncast<T>(val, typ) {
    return transform(val, typ, jsToJSONProps);
  }
  
  function a(typ) {
    return { arrayItems: typ };
  }
  
  function u(...typs) {
    return { unionMembers: typs };
  }
  
  function o(props, additional) {
    return { props, additional };
  }
  
  function m(additional) {
    return { props: [], additional };
  }
  
  function r(name) {
    return { ref: name };
  }
  
  const typeMap: any = {
    GrypeCvss: o(
      [
        { json: 'VendorMetadata', js: 'VendorMetadata', typ: 'any' },
        { json: 'Metrics', js: 'Metrics', typ: r('Metrics') },
        { json: 'Vector', js: 'Vector', typ: '' },
        { json: 'Version', js: 'Version', typ: '' },
      ],
      false
    ),
    Metrics: o(
      [
        { json: 'BaseScore', js: 'BaseScore', typ: 3.14 },
        { json: 'ExploitabilityScore', js: 'ExploitabilityScore', typ: 3.14 },
        { json: 'ImpactScore', js: 'ImpactScore', typ: 3.14 },
      ],
      false
    ),
  };
  
  