# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 22:44:05 2022

@author: Philippe@loco-labs.io

The `ES.test_iindex` module contains the unit tests (class unittest) for the
`Iindex` class.
"""
import unittest
from iindex import Iindex, util
from ilist import Ilist
from copy import copy
#os.chdir('C:/Users/a179227/OneDrive - Alliance/perso Wx/ES standard/python ESstandard/ES')
from test_observation import dat3, loc3, prop2, _res
from ESObservation import Observation
from ESValue import NamedValue, DatationValue, LocationValue, PropertyValue, ESValue #, ReesultValue
import datetime
from ESconstante import ES
from itertools import product
from timeslot import TimeSlot


'''f = ['er', 'rt', 'er', 'ry']
l = [30, 12, 20, 15]
il=Ilist.Iext(f,l)'''
tlis = (1,2) 
if ES.def_clsName: lis = [1,2]
else:              lis = (1,2)

class Test_iindex(unittest.TestCase):

    def test_init(self) :

        idx = Iindex(codec=['er', 2, lis], name='test', keys=[0,1,2,1])
        idx2 = Iindex.Iext(['er', 2, lis, 2], 'test')
        idx3 = Iindex.Idic({'test': ['er', 2, lis, 2]})
        idx4 = Iindex.Idic({'test': ['er', 2, lis, 2]}, fullcodec=True)
        idx5 = Iindex.Iext(['er', 2, lis, 2], 'test', fullcodec=True)
        self.assertTrue(Iindex(idx) == Iindex.Iext(idx) == Iindex.Idic(idx) == idx)
        self.assertTrue(idx.name == 'test' and idx.cod == ['er', 2, tlis] and idx.keys == [0,1,2,1])
        self.assertTrue(idx == idx2 == idx3)
        self.assertTrue(idx.val == idx4.val == idx4.cod == ['er', 2, tlis, 2] 
                        == idx5.val == idx5.cod and len(idx) == 4)
        idx = Iindex() 
        idx2 = Iindex.Iext()
        idx3 = Iindex.Idic()
        self.assertTrue(idx == idx2 == idx3 == Iindex(idx))
        self.assertTrue(idx.name == 'default index' and idx.codec == [] and idx.keys == [])
        self.assertTrue(idx.values == [])
        idx = Iindex(lendefault=3) 
        self.assertTrue(idx.name == 'default index' and idx.cod == [0,1,2] and idx.keys == [0,1,2])
        self.assertTrue(idx.val == [0,1,2])
        idx = Iindex(['er', 'rt', 'ty'], 'datation', [0,1,2,2])
        idx2 = Iindex.Iext(['er', 'rt', 'ty', 'ty'], 'datation')
        idx3 = Iindex.Idic({'datation': ['er', 'rt', 'ty', 'ty']})
        self.assertTrue(idx == idx2 == idx3)
        self.assertTrue(isinstance(idx.codec[0], DatationValue))
        self.assertTrue(idx.values[3] == DatationValue(name='ty'))
        idx = Iindex(['er', 'rt', Ilist()], 'result', [0,1,2,2])
        idx2 = Iindex.Iext(['er', 'rt', Ilist(), Ilist()], 'result')
        idx3 = Iindex.Idic({'result': ['er', 'rt', Ilist(), Ilist()]})
        self.assertTrue(idx == idx2 == idx3)
        if ES.def_clsName: self.assertTrue(isinstance(idx.codec[0], NamedValue))
        self.assertTrue(idx.values[3] == Ilist())
        self.assertTrue(Iindex.from_obj([1,2,3])[1] == Iindex([1,2,3]))
        self.assertTrue(Iindex(codec=[True], lendefault=3).val == [True, True, True])
    
    def test_infos(self) :
        idx = Iindex.Iext(['er', 2, lis])
        self.assertTrue(idx.infos == {'lencodec': 3, 'typeindex': 'complete',
         'rate': 0.0, 'disttomin': 2, 'disttomax': 0})
        #idx2 = Iindex.Iext(['er', Ilist(), Ilist()], 'result') #!!! ?? remettre
        #self.assertTrue(idx2.infos == {'lencodec': 2, 'typeindex': 'mixte',
        # 'rate': 0.5, 'disttomin': 1, 'disttomax': 1})
        idx2 = Iindex()
        self.assertTrue(idx2.infos == {'lencodec': 0, 'typeindex': 'null',
         'rate': 0.0, 'disttomin': 0, 'disttomax': 0})
        
    def test_append(self) :
        idx = Iindex.Iext(['er', 2, lis])
        self.assertTrue(idx.append(8)==3)
        self.assertTrue(idx.append(8)==3)
        self.assertTrue(idx.append(8, unique=False)==4)
        
    def test_loc_keyval(self):
        idx = Iindex.Iext(['er', 2, lis])
        self.assertTrue(idx.keytoval(idx.valtokey(lis)) == tlis)
        self.assertTrue(idx.isvalue(tlis))

    def test_setvalue_setname(self):
        idx = Iindex.Iext(['er', 2, lis])
        idx[1] = 'er'
        self.assertTrue(idx.val == ['er', 'er', tlis])
        idx.setcodecvalue('er', 'ez')
        self.assertTrue(idx.val == ['ez', 'ez', tlis])        
        idx[1] = 3
        self.assertTrue(idx.val == ['ez', 3, tlis])
        idx.setvalue(0, 'ez', dtype='datvalue')
        if ES.def_clsName: self.assertTrue(idx.val == ['ez', 3, tlis])
        self.assertTrue(idx.values[0] == DatationValue(name='ez'))
        idx.setlistvalue([3, (3,4), 'ee'])
        self.assertTrue(idx.val == [3, (3,4), 'ee'])
        idx.setname('truc')
        self.assertEqual(idx.name, 'truc')

    def test_record(self):
        ia = Iindex.Iext(['anne', 'paul', 'lea', 'andre', 'paul', 'lea'])
        self.assertEqual([ia[i] for i in ia.recordfromvalue('paul')], ['paul', 'paul'])

    def test_reset_reorder_sort(self):
        idx = Iindex.Iext(['er', 2, 'er', lis])
        cod = copy(idx.codec)
        idx.codec.append('ez')
        #idx.resetkeys()
        idx.reorder()
        self.assertEqual(cod, idx.codec)
        order=[1,3,0,2]
        idx.reorder(order)
        self.assertEqual(idx.val, [2, tlis, 'er', 'er'])
        #idx.sort()
        self.assertEqual(idx.sort().val, [tlis, 2, 'er', 'er'])      
        idxs = idx.sort(inplace=False, reverse=True)
        self.assertEqual(idxs.val, ['er', 'er', 2, tlis])      
        idx = Iindex.Iext([1,3,3,2,5,3,4]).sort(inplace=False)
        self.assertEqual(idx.val, [1, 2, 3, 3, 3, 4, 5])
        self.assertEqual(idx.cod,  [1, 2, 3, 4, 5])
        
    def test_derived_coupled(self):
        der = Iindex.Iext([1,1,1,2])
        ref = Iindex.Iext([1,1,3,4])
        self.assertTrue(der.isderived(ref) and not der.iscoupled(ref))
        der.tocoupled(ref)
        self.assertTrue(not der.isderived(ref) and der.iscoupled(ref))
        #der.resetkeys()
        der.reorder()
        self.assertTrue(der.isderived(ref) and not der.iscoupled(ref))
        ia = Iindex.Iext(['anne', 'paul', 'anne', 'lea', 'anne'])
        ib = Iindex.Iext([25,25,12,12,25])
        self.assertTrue(not ia.isderived(ib) and not ia.iscoupled(ib))
        self.assertTrue(not ib.isderived(ia) and not ib.iscoupled(ia))
        ia.coupling(ib)
        self.assertTrue(ib.isderived(ia))
        ia.coupling(ib, derived=False)
        self.assertTrue(ib.iscoupled(ia))
        
    def test_coupling_infos(self):
        ia = Iindex.Iext()
        ib = Iindex.Iext([25,25,12,12,25])
        self.assertEqual(ia.couplinginfos(ib), {'lencoupling': 0, 'rate': 0, 
                    'disttomin': 0, 'disttomax': 0, 'distmin': 0, 'distmax': 0,
                    'diff': 0, 'typecoupl': 'null'})
        ia = Iindex.Iext(['anne', 'paul', 'anne', 'lea', 'anne'])
        self.assertEqual(ia.couplinginfos(ib), {'lencoupling': 4, 'rate': 0.3333333333333333,
                    'disttomin': 1, 'disttomax': 2, 'distmin': 3, 'distmax': 6, 
                    'diff': 1, 'typecoupl': 'link'})
        self.assertTrue(ia.islinked(ib))
        ia = Iindex.Iext(['anne', 'lea', 'anne', 'lea', 'anne'])
        self.assertEqual(ia.couplinginfos(ib), {'lencoupling': 4, 'rate': 1.0,
                    'disttomin': 2, 'disttomax': 0, 'distmin': 2, 'distmax': 4,
                    'diff': 0, 'typecoupl': 'crossed'})
        self.assertTrue(ia.iscrossed(ib))

    def test_vlist(self):
        testidx = [Iindex(), Iindex.Iext(['er', 2, 'er', lis])]
        residx  = [[], ['er', '2', 'er', str(tlis)]]
        for idx, res in zip(testidx, residx):
            self.assertEqual(idx.vlist(str), res)

    def test_numpy(self):
        idx = Iindex.Iext(['er', 2, 'er', lis])
        self.assertEqual(len(idx.to_numpy(func=str)), len(idx)) 

    def test_coupled_extendvalues(self):
        ia = Iindex.Iext(['anne', 'paul', 'lea', 'andre', 'paul', 'lea'])
        ib = Iindex.Iext([25,25,12,12])   
        self.assertTrue(ib.isderived(ia))
        #ib.extendvalues(ia)
        ib.tocoupled(ia)
        self.assertEqual(ib.val, [25, 25, 12, 12, 25, 12])
        self.assertTrue(ib.keys == ia.keys and ib.iscoupled(ia))
        #ib.extendvalues(ia, coupling=False)
        ib.tocoupled(ia, coupling=False)
        self.assertEqual(ib.val, [25, 25, 12, 12, 25, 12])
        self.assertTrue(ib.cod, [25, 12] and ib.isderived(ia))
        
    '''def test_crossed(self):
        ia = Iindex.Iext(['anne', 'paul', 'anne', 'lea'])
        ib = Iindex.Iext([25,25,12,12])
        Iindex.tocrossed([ia,ib])
        self.assertTrue(ib.iscrossed(ia))
        ia = Iindex.Iext(['anne', 'paul', 'anne', 'lea'])
        ib = Iindex.Iext([25,25,12,12])
        ic = Iindex.Iext(['White', 'Grey', 'White', 'Grey'])
        Iindex.tocrossed([ia,ib, ic])
        self.assertTrue(ib.iscrossed(ia) and ib.iscrossed(ic))'''

    '''def test_tocodec(self):
        v = [10,10,10,10,30,10,20,20,20]        
        k = [1, 1, 1, 2, 3, 2, 0, 0, 0 ]
        self.assertEqual(util.tocodec(v, k), util.tocodec(v, k))
        self.assertEqual(sorted(util.tocodec(v ), 
                         sorted(util.tocodec(v)))'''

    def test_to_std(self):   
        idx = Iindex.Iext(['d1', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6'])
        self.assertEqual(len(idx.tostdcodec().codec), len(idx))
        self.assertEqual(len(idx.tostdcodec(full=False).codec), len(idx.codec))
        self.assertTrue(idx == idx.tostdcodec(full=False) == idx.tostdcodec())
        idx = Iindex.Iext(['d1', 'd1', 'd1', 'd1', 'd1', 'd1', 'd1'])
        self.assertEqual(len(idx.tostdcodec().codec), len(idx))
        self.assertEqual(len(idx.tostdcodec(full=False).codec), len(idx.codec))
        self.assertTrue(idx == idx.tostdcodec(full=False) == idx.tostdcodec())
        
    def test_extendcodec(self):
        papy = Iindex.Iext(['d1', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6'])
        parent = Iindex.Iext(['j', 'j', 'f', 'f', 'm', 's', 's'])
        idx = Iindex.Iext(['t1', 't1', 't1', 't1', 't2', 't3', 't3'])
        parent2 = parent.setkeys(papy.keys, inplace=False)
        idx2 = idx.setkeys(parent.keys, inplace=False)
        self.assertEqual(idx.values, idx2.values)
        self.assertEqual(len(parent2.codec), len(papy.codec))
        self.assertEqual(len(idx2.codec), len(parent.codec))
        self.assertTrue(idx2.isderived(parent2) and parent2.iscoupled(papy))
        idxcalc = Iindex.from_parent(idx2.codec, parent=parent)
        self.assertTrue(idxcalc.values == idx2.values == idx.values)
        idx=Iindex(codec=['s', 'n', 's', 'd', 's', 'd'], keys=[0, 4, 2, 1, 5, 3, 3])
        values = idx.values
        parent=Iindex(codec=[6, 9, 8, 11, 7, 9], keys=[0, 4, 2, 1, 5, 3, 3])
        idx.setkeys(parent.keys)
        idxcalc = Iindex.from_parent(idx.codec, parent=parent)
        self.assertTrue(idxcalc.values == idx.values == values)

    def test_duplicates(self):
        il = Iindex(['a', 'b', 'c', 'a', 'b', 'c', 'a', 'e', 'f', 'b', 'd', 'a', 'b', 'c',
         'c', 'a', 'a', 'a', 'b', 'c', 'a', 'e', 'f', 'b', 'd'])
        il.setkeys([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 1, 2, 2, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(set([il.val[item] for item in il.getduplicates()]), set(['a', 'b', 'c']))
        
    def test_derkeys(self):
        parent = Iindex.Iext(['j', 'j', 'f', 'f', 'm', 's', 's'])
        fils = Iindex.Iext(['t1', 't1', 't1', 't1', 't2', 't3', 't3'])
        idx = Iindex(fils.codec, keys=Iindex.keysfromderkeys(parent.keys, fils.derkeys(parent))) 
        self.assertEqual(idx, fils)
        grandpere=Iindex.Iext([0,     0,   2,   3,   4,   4,   6,   7,   8,   9,   9,  11,  12 ])
        pere = Iindex.Iext(['j', 'j', 'f', 'a', 'm', 'm', 's', 's', 's', 'n', 'd', 'd', 'd' ])
        fils = Iindex.Iext(['t1','t1','t1','t2','t2','t2','t3','t3','t3','t4','t4','t4','t4'])
        petitfils =Iindex.Iext(['s11','s1','s1','s1','s1','s11','s2','s2','s2','s1','s2','s2','s2'])
        fils.coupling(petitfils)
        pere.coupling(fils)
        grandpere.coupling(pere)
        self.assertTrue(petitfils.isderived(fils)==fils.isderived(pere)
                        ==pere.isderived(grandpere))
        idx = Iindex(petitfils.codec, 
                     keys=Iindex.keysfromderkeys(fils.keys, petitfils.derkeys(fils))) 
        self.assertEqual(idx, petitfils)
        idx = Iindex(fils.codec, 
                     keys=Iindex.keysfromderkeys(pere.keys, fils.derkeys(pere))) 
        self.assertEqual(idx, fils)
        idx = Iindex(pere.codec, 
                     keys=Iindex.keysfromderkeys(grandpere.keys, pere.derkeys(grandpere))) 
        self.assertEqual(idx, pere)


    def test_json(self):
        self.assertTrue(Iindex.from_obj(Iindex(['a']).to_obj())[1].to_obj()==Iindex(['a']).to_obj()==['a'])
        self.assertTrue(Iindex.from_obj(Iindex([0]).to_obj())[1].to_obj()==Iindex([0]).to_obj()==[0])
        self.assertTrue(Iindex.from_obj(Iindex().to_obj())[1].to_obj()==Iindex().to_obj()==[])
        parent = Iindex.Iext(['j', 'j', 'f', 'f', 'm', 's', 's'])
        fils = Iindex.Iext(['t1', 't1', 't1', 't1', 't2', 't3', 't3'])
        js=fils.tostdcodec().to_obj(parent=-1)
        prt, idx = Iindex.from_obj(js)
        self.assertEqual(idx, fils)
        self.assertEqual(prt, -1)      
        js=fils.to_obj(keys=fils.derkeys(parent), parent=1)
        prt, idx = Iindex.from_obj(js, extkeys=parent.keys)
        self.assertEqual(idx, fils)
        self.assertEqual(prt, 1) 
        encoded    = [True, False]
        format     = ['json', 'cbor']
        test = list(product(encoded, format))
        for ts in test:
            option = {'encoded': ts[0], 'encode_format': ts[1]}
            idx2=Iindex.from_obj(idx.to_obj(keys=True, **option))[1]
            self.assertEqual(idx.values, idx2.values)
            idx2=Iindex.from_obj(idx.tostdcodec().to_obj(**option))[1] # full format
            self.assertEqual(idx.values, idx2.values)
            idx2=Iindex.from_obj(idx.to_obj(keys=fils.derkeys(parent), parent=1, **option), 
                                 extkeys=parent.keys)[1] # default format
            self.assertEqual(idx.values, idx2.values)

    def test_castobj(self): #!!!
        lis = [['{"namvalue":{"val":21}}',   'ESValue',         NamedValue],
               [{"val":21},                  'ESValue',         NamedValue],
               [{"val":21},                  None,              dict],
               ['{"namvalue":{"val":21}}',   None,              str],
               ['{"locvalue":{"val":21}}',   'LocationValue',   LocationValue],
               ['{"observation":{"val":21}}','Observation',     Observation],
               #[Observation(),               'Observation',     Observation],
               #[Observation(),               None,              Observation],
               [datetime.datetime(2020,1,1), 'DatationValue',   DatationValue],
               [datetime.datetime(2020,1,1), 'TimeSlot',        TimeSlot],
               [datetime.datetime(2020,1,1), None,              datetime.datetime]]
        '''for t in lis:
            print(type(util.castobj([t[0]], t[1])[0]))
            self.assertTrue(isinstance(util.castobj([t[0]], t[1])[0], t[2]))'''
        idx = Iindex.Idic({'datation': ['er', 'rt', 'ty', 'ty']})
        self.assertTrue(isinstance(idx.values[0], DatationValue))
        idx = Iindex.Idic({'ESdatation': ['er', 'rt', 'ty', 'ty']})
        self.assertTrue(isinstance(idx.values[0], NamedValue))
        idx = Iindex.Idic({'dates': ['er', 'rt', 'ty', 'ty']})
        if not ES.def_clsName: self.assertTrue(isinstance(idx.values[0], str))
        else: self.assertTrue(isinstance(idx.values[0], NamedValue))

    def test_to_from_obj(self):          #!!!  
        idx = Iindex.Iext([[1,2], [2,3]], fullcodec=True)
        self.assertEqual(Iindex.from_obj(idx.to_obj(encoded=False))[1], idx)
        self.assertEqual(Iindex.from_obj(idx.to_obj(encoded=True, keys=True))[1], idx)
        idx  = Iindex.from_obj(['datation', [DatationValue.from_obj(dat3[1][0]), 
                                             DatationValue.from_obj(dat3[1][1]),
                                             DatationValue.from_obj(dat3[1][2])]])[1]
        idx2 = Iindex.from_obj(['location', [LocationValue.from_obj(loc3[1][0]), 
                                             LocationValue.from_obj(loc3[1][1]),
                                             LocationValue.from_obj(loc3[1][2])], 0])[1]
        idx3 = Iindex.from_obj(['property', [PropertyValue(prop2[1][0]), PropertyValue(prop2[1][1])]])[1]
    
    def test_iadd(self):            
        idx = Iindex.Iext(['er', 2, lis])
        idx2 = idx + idx
        self.assertEqual(idx2.val, idx.val + idx.val)
        self.assertEqual(len(idx2), 2 * len(idx))
        self.assertEqual(len(idx2), 2 * len(idx))
        idx += idx
        self.assertEqual(idx2, idx)
        
if __name__ == '__main__':  unittest.main(verbosity=2)
