# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 22:05:08 2021

@author: Philippe@loco-labs.io

The `ES.test_esvalue` module contains the unit tests (class unittest) for the
`ESValue` functions.
"""
import unittest, json
from ilist import Ilist

from ESValue import ResultValue, LocationValue, DatationValue, \
    PropertyValue, ESValue #, _gshape
from ESconstante import ES
#from pprint import pprint
import datetime
from test_observation import dat3, loc3, prop2, _res, lyon, paris, pol1, \
    pol75, t1, pprop_pm25, t2, s1, t1n, matin, travail, pt1, tnull, pprop_pm10, \
    prop_pm25, pol2, pol13, aprem

# couverture tests (True if non passed)----------------------------------------
simple  = False  # False

# datas-----------------------------------------------------------------------
'''def _val(n): return list(i for i in range(n))
def _res(n): return (ES.res_classES, _val(n))
with open('C:\\Users\\a179227\\OneDrive - Alliance\\perso Wx\\ES standard\\python ESstandard\\departements-version-simplifiee.geojson') as f:
    dp = f.read()
dpt = json.loads(dp)['features']
#https://github.com/gregoiredavid/france-geojson
pol13 = {dpt[12]['properties']['code'] + ' ' + dpt[12]['properties']['nom'] :
         dpt[12]['geometry']['coordinates']}
pol69 = {dpt[69]['properties']['code'] + ' ' + dpt[69]['properties']['nom'] :
         dpt[69]['geometry']['coordinates']}
pol75 = {dpt[75]['properties']['code'] + ' ' + dpt[75]['properties']['nom'] :
         dpt[75]['geometry']['coordinates']}
pol1 = [[[0.0,1.0], [1.0,2.0], [1.0,1.0], [0.0,1.0]]]
pol1centre = [0.6666666666666666, 1.3333333333333333]
pol2 = [[[0.0,2.0], [2.0,2.0], [1.0,1.0], [0.0,2.0]]]
dpt2 = (ES.loc_classES, [pol1, pol2])
dpt3 = (ES.loc_classES, [pol75, pol69, pol13])
pparis       = [2.4, 48.9]
plyon        = [4.8, 45.8]
pmarseille   = [5.4, 43.3]
paris       = [2.35, 48.87]
parisn      = json.dumps({'loca1' : paris})
lyon        = [4.83, 45.76]
marseille   = [5.38, 43.3]
mini_PL     = [2.35, 45.76]
maxi_PLM    = [5.38, 48.87]
obs_1       = (ES.type, ES.obs_classES)
truc_mach   = ("truc", "machin")
prop_pm25   = dict([(ES.prp_type,"PM25"), (ES.prp_unit, "kg/m3")])
prop_pm10   = dict([(ES.prp_type,"PM10"), (ES.prp_unit, "kg/m3")])
prop_co2    = dict([(ES.prp_type,"CO2"), (ES.prp_unit, "kg/m3")])
pprop_pm25   = dict([(ES.prp_type,"PM25"), (ES.prp_unit, "kg/m3"), (ES.prp_appli, "air")])
pprop_pm10   = dict([(ES.prp_type,"PM10"), (ES.prp_unit, "kg/m3"), (ES.prp_appli, "air"), ("truc", "machin")])
matin = [ datetime(2020, 2, 4, 8), datetime(2020, 2, 4, 12)]
midi  = [ datetime(2020, 2, 4, 12), datetime(2020, 2, 4, 14)]
aprem  = [ datetime(2020, 2, 4, 14), datetime(2020, 2, 4, 18)]
travail = [matin, aprem]
pt1 = datetime(2020, 2, 4, 12, 5, 0)
pt2 = datetime(2020, 5, 4, 12, 5, 0)
pt3 = datetime(2020, 7, 4, 12, 5, 0)
tnull = datetime(1970, 1, 1, 0, 0, 0)
snull = (tnull.isoformat(), tnull.isoformat())
t1 = datetime(2021, 2, 4, 12, 5, 0)
t1n = json.dumps({'date1' : t1.isoformat()})
t2 = datetime(2021, 7, 4, 12, 5, 0)
t3 = datetime(2021, 5, 4, 12, 5, 0)
r1 = ResultValue('{"er":2}')
r2 = ResultValue(23)
r3 = ResultValue("coucou")
r4 = ResultValue(41.2)
r5 = ResultValue(18)
#r6 = ResultValue([41, [2, 2, 0]])
#r7 = ResultValue([18, [1, 2, 1]])
s1 = [t1, t2]
dat1 = (ES.dat_classES, {'date1' : t1.isoformat()})
dat2 = (ES.dat_classES, [t1.isoformat(), t2.isoformat()])
dat3 = (ES.dat_classES, [{'date1' : t1.isoformat()}, t2.isoformat(), t3.isoformat()])
dat3ord = (ES.dat_classES, [{'date1' : t1.isoformat()}, t3.isoformat(), t2.isoformat()])
dat3sn = (ES.dat_classES, [t1.isoformat(), t2.isoformat(), t3.isoformat()])
pdat3 = (ES.dat_classES, [pt1.isoformat(), pt2.isoformat(), pt3.isoformat()])
prop1 = (ES.prp_classES, prop_pm10)
prop2 = (ES.prp_classES, [prop_pm25, prop_pm10])
prop2ord = (ES.prp_classES, [prop_pm10, prop_pm25])
prop3 = (ES.prp_classES, [prop_pm25, prop_pm10, prop_co2])
pprop2 = (ES.prp_classES, [pprop_pm25, pprop_pm10])
loc1 = (ES.loc_classES, {'paris' : paris})
loc1sn = (ES.loc_classES, paris)
loc2 = (ES.loc_classES, [paris, lyon])
loc3 = (ES.loc_classES, [{'paris' : paris}, lyon, marseille])
loc3sn = (ES.loc_classES, [paris, lyon, marseille])
ploc3 = (ES.loc_classES, [pparis, plyon, pmarseille])
res2 = (ES.res_classES, [[41, [2, 2, 0]], [18, [1, 2, 1]]])'''

@unittest.skipIf(simple, "test unitaire")
class TestObsUnitaire(unittest.TestCase):
    '''Unit tests for `ES.ESValue`, `ES.ESObs`, `ES.ESElement` '''
    opt = ES.mOption.copy()

    def test_ResultValue(self):
        self.assertEqual(ResultValue("coucou").json(), '"coucou"')
        self.assertEqual(ResultValue('{"er":2}').json(), '{"er": 2}')
        self.assertEqual(ResultValue(21).json(), '21')
        self.assertEqual(ResultValue(2.1).json(), '2.1')
        self.assertEqual(ResultValue('{"er":2}').EStype, 132)
        self.assertEqual(ResultValue(22).EStype, 32)
        self.assertEqual(ResultValue("coucou").EStype, 32)

    def test_locationValue(self):
        self.opt = ES.mOption.copy()
        self.assertEqual(LocationValue(lyon).json(**self.opt), json.dumps(lyon))
        self.assertEqual(LocationValue(lyon), LocationValue(LocationValue(lyon)))
        self.assertTrue(LocationValue(lyon) > LocationValue(paris))
        self.assertEqual(LocationValue(pol1).json(**self.opt), json.dumps(pol1))
        self.assertTrue(LocationValue(paris).value == LocationValue({'paris':paris}).value ==
                        LocationValue(name='paris', shape=LocationValue._gshape(paris)).value)
        self.assertTrue(LocationValue('paris').name == LocationValue({'paris':paris}).name ==
                        LocationValue(name='paris', shape=LocationValue._gshape(paris)).name)
        self.assertEqual(LocationValue.Box(LocationValue(paris).bounds).bounds,
                         LocationValue({'box':paris}).bounds)
        self.assertEqual(LocationValue(lyon).EStype, 12)
        self.assertEqual(LocationValue(pol1).EStype, 13)
        self.assertEqual(LocationValue(pol75).EStype, 113)
        self.assertEqual(LocationValue('pol75').EStype, 100)
        self.assertEqual(LocationValue(LocationValue.nullValue()).EStype, 0)


    def test_DatationValue(self):
        self.opt = ES.mOption.copy()
        self.assertEqual(DatationValue(t1), DatationValue(DatationValue(t1)))
        self.assertEqual(DatationValue(t1).json(encoded=False), t1.astimezone(datetime.timezone.utc))
        self.assertTrue(DatationValue(t1) < DatationValue(t2))
        self.assertEqual(DatationValue(json.loads(t1n)).json(), t1n)
        self.opt["json_dat_name"] = True
        self.assertEqual(DatationValue(json.loads(t1n)).json(**self.opt), t1n)
        self.assertTrue(DatationValue(t1).value == DatationValue({'t1':t1}).value ==
                        DatationValue(name='t1', slot=t1).value)
        self.assertTrue(DatationValue('t1').name == DatationValue({'t1':t1}).name ==
                        DatationValue(name='t1', slot=t1).name)
        self.assertEqual(DatationValue(matin).EStype, 3)
        self.assertEqual(DatationValue(travail).EStype, 4)
        self.assertEqual(DatationValue(pt1).EStype, 2)
        self.assertEqual(DatationValue(tnull).EStype, 0)
        self.assertEqual(DatationValue(t1n).EStype, 102)
        self.assertEqual(DatationValue('t1n').EStype, 100)


    def test_propertyValue(self):
        self.opt = ES.mOption.copy()
        self.assertEqual(PropertyValue().json(**self.opt), '{}')
        self.assertEqual(PropertyValue({ES.prp_type : "PM25"}, prp_dict=True).json(**self.opt),
                         '{"'+ES.prp_type+'": "PM25", "unit": "kg/m3"}')
        self.assertEqual(PropertyValue({ES.prp_type : "PM25"}).json(**self.opt),
                         '{"'+ES.prp_type+'": "PM25"}')
        self.assertEqual(PropertyValue(pprop_pm10).json(**self.opt), json.dumps(pprop_pm10))
        self.assertEqual(PropertyValue(prop_pm25).EStype, 22)
        self.assertEqual(PropertyValue(pprop_pm25).EStype, 23)
        self.assertEqual(PropertyValue({'truc':2}).EStype, 23)
        self.assertEqual(PropertyValue({'machin':{'truc':2}}).EStype, 123)
        self.assertEqual(PropertyValue('truc').EStype, 100)
        self.assertEqual(PropertyValue(PropertyValue.nullValue()).EStype, 0)

    def test_nameValue(self):
        self.assertEqual(DatationValue('recre').json(encoded=False), 'recre')
        self.opt["json_prp_name"] = True
        self.assertEqual(PropertyValue(pprop_pm25).json(**self.opt), json.dumps(pprop_pm25))
        self.assertEqual(PropertyValue('test').json(**self.opt), '"test"')
        self.opt["json_loc_name"] = True
        self.assertEqual(LocationValue(lyon).json(**self.opt), json.dumps(lyon))
        self.assertEqual(LocationValue('test').json(**self.opt), '"test"')

    def test_setValue_setName(self):
        val = LocationValue(lyon)
        val.setValue(LocationValue([4,5]))
        self.assertEqual(val.vSimple(), [4,5])
        self.assertEqual(val.EStype, 12)
        val.setValue(LocationValue([[6,7], [7,8], [8,6]]))
        self.assertEqual(val.EStype, 14)
        self.assertEqual(val.value, LocationValue._gshape([[6,7], [7,8], [8,6]]))
        val.setValue(LocationValue([[[6,7], [7,8], [8,6]]]))
        self.assertEqual(val.EStype, 13)
        self.assertEqual(val.value, LocationValue._gshape([[[6,7], [7,8], [8,6]]]))
        val.setName('truc')
        self.assertEqual(val.name, 'truc')
        self.assertEqual(val.EStype, 113)
        val = DatationValue(t1)
        val.setValue(t2)
        self.assertEqual(val.simple, t2)
        val.setValue(DatationValue(s1))
        self.assertEqual(val.EStype, 3)
        self.assertEqual(val.vInterval(encoded=False), s1)
        val.setName('truc')
        self.assertEqual(val.name, 'truc')
        self.assertEqual(val.EStype, 103)

    def test_link(self):
        dat = DatationValue(datetime.datetime(2005,1,1))
        dat2 = DatationValue([datetime.datetime(2000,1,2), datetime.datetime(2006,1,1)])
        self.assertEqual(dat.link(dat2), 'within')
        self.assertTrue(dat.within(dat2))

        loc = LocationValue([[[0,1],[1,1], [1,0], [0,0]]])
        loc2 = LocationValue([[[0,10],[10,10], [10,0],[0,0]]])
        loc3 = LocationValue([0.5, 0.5])
        self.assertEqual(loc.link(loc2), 'within')
        self.assertTrue(loc.within(loc2))
        self.assertEqual(loc.link(loc3), 'contains')
        self.assertEqual(LocationValue([0.5, 0.5]).link(LocationValue([0.5, 0.5])), 'equals')

        prp10 = PropertyValue({"prp":'PM10', "truc":12})
        prp25 = PropertyValue({"prp":'PM25', "truc":15})
        prp25bis = PropertyValue({"prp":'PM25', "truc":12})
        prp25ter = PropertyValue({"prp":'PM25'})
        prp10_20 = PropertyValue.Simple(['PM10', 'PM20'])
        prp10_25 = PropertyValue.Simple(['PM10', 'PM25'])
        self.assertEqual(prp10_20.link(prp10), 'contains')
        self.assertTrue(prp10_20.contains(prp10))
        self.assertEqual(prp10.link(prp10_20), 'within')
        self.assertEqual(prp10_20.link(prp10_25), 'intersects')
        self.assertEqual(prp25.link(prp25bis), 'intersects')
        self.assertEqual(prp25.link(prp25ter), 'within')

    def test_bjson(self):
        v = DatationValue({"date1": "2021-02-04T12:05:00"})
        self.assertTrue(v == DatationValue.from_json(v.json(encoded=True,  encode_format='bson'))
                          == DatationValue.from_json(v.json(encoded=True,  encode_format='json'))
                          == DatationValue.from_json(v.json(encoded=False, encode_format='json'))
                          == DatationValue.from_json(v.json(encoded=False, encode_format='json')))
        v = LocationValue({"loc1": pol2})
        self.assertTrue(v == LocationValue.from_json(v.json(encoded=True,  encode_format='bson'))
                          == LocationValue.from_json(v.json(encoded=True,  encode_format='json'))
                          == LocationValue.from_json(v.json(encoded=False, encode_format='json'))
                          == LocationValue.from_json(v.json(encoded=False, encode_format='json')))
        v = DatationValue({"date1": "2021-02-04T12:05:00"})
        self.assertTrue(v == DatationValue(ESValue.__from_bytes__(v.__to_bytes__(encoded=True)))
                          == DatationValue(ESValue.__from_bytes__(v.__to_bytes__(encoded=False))))
        v = LocationValue({"loc1": pol2})
        self.assertTrue(v == LocationValue(ESValue.__from_bytes__(v.__to_bytes__(encoded=True)))
                          == LocationValue(ESValue.__from_bytes__(v.__to_bytes__(encoded=False))))

    def test_box_bounds(self):
        v = LocationValue.Box(LocationValue(pol13))
        self.assertTrue(v.isEqual(v.Box(v.bounds), name=False))
        self.assertTrue(v == v.Box(v.bounds))
        v = DatationValue.Box(DatationValue(travail))
        self.assertTrue(v.isEqual(v.Box(v.bounds), name=False))
        self.assertTrue(v == v.Box(v.bounds))
        l = LocationValue(lyon)
        p = LocationValue(paris)
        self.assertEqual(l.boxUnion(p, 'union').bounds,
                         (min(l.bounds[0], p.bounds[0]), min(l.bounds[1], p.bounds[1]),
                          max(l.bounds[2], p.bounds[2]), max(l.bounds[3], p.bounds[3])))
        l = DatationValue(matin)
        p = DatationValue(aprem)
        self.assertEqual(l.boxUnion(p, 'union').bounds,
                         (min(l.bounds[0], p.bounds[0]), max(l.bounds[1], p.bounds[1])))
        prp10_20 = PropertyValue.Simple(['PM10', 'PM20'])
        prp10_25 = PropertyValue.Simple(['PM10', 'PM25'])
        self.assertEqual(prp10_20.boxUnion(prp10_25).vSimple(), ["PM10", "PM20", "PM25"])

if __name__ == '__main__':
    unittest.main(verbosity=2)
