#include "stdafx.h"

#include <iostream>
#include <iomanip>
#include <string>
#include "ESObservation.h"
#include "ESBluetooth.h"
//#include "ESObsType.h"
//#include "ESEMF.h"
//#include "DTime.h"

using namespace std;

int compteur = 0;

ESSetResultReal res_(int n) {
	ESSetResultReal res;
	for (int i=0; i < n; i++) int j = res.addValue(RealValue(i));
	return res;
}
int testEgal(string a, string b) {
	int erreur = 0;
	compteur += 1;
	if (a != b) { cout << "erreur n° " << compteur << " : " << b << endl; erreur = 1; }
	return erreur;
}
int test1(bool a) {
	int erreur = 0;
	compteur += 1;
	if (!a) { cout << "erreur n° " << compteur << endl; erreur = 1;	}
	return erreur;
}
void testNonRegression() {
	bool detail = 1;
	const int capa(1000);
	StaticJsonDocument<capa> doc;

	string stparis = "[2.35, 48.87]";
	LocationValue paris = LocationValue(2.35, 48.87); string _paris = "[2.35, 48.87]";
	ESSetResultReal res6 = res_(6); string _res6 = "\"realValue\":[0,1,2,3,4,5]";
	LocationValue lyon = LocationValue(4.83, 45.76);
	LocationValue marseille = LocationValue(5.38, 43.3);
	LocationValue mini_PL = LocationValue(2.35, 45.76);
	LocationValue maxi_PLM = LocationValue(5.38, 48.87);
	string obs_1 = "\"type\":\"observation\"";
	string truc_mach = "\"$truc\":\"machin\"";
	DTime	pt1 = DTime(2020, 2, 4, 12, 5, 0);
	DTime	pt2 = DTime(2020, 5, 4, 12, 5, 0);
	DTime	pt3 = DTime(2020, 7, 4, 12, 5, 0);
	DTime	t1 = DTime(2021, 2, 4, 12, 5, 0);
	DTime	t2 = DTime(2021, 5, 4, 12, 5, 0);
	DTime	t3 = DTime(2021, 7, 4, 12, 5, 0);
	ESSetDatation dat1 = ESSetDatation(); dat1.addValue(TimeValue(t1)); string _dat1 = "\"dateTime\":\"4-2-2021T12:5:0\"";
	ESSetDatation dat2 = ESSetDatation(); dat2.addValue(TimeValue(t1)); dat2.addValue(TimeValue(t2)); string _dat2 = "\"dateTime\":[\"4-2-2021T12:5:0\",\"4-5-2021T12:5:0\"]";
	ESSetDatation dat3 = ESSetDatation(); dat3.addValue(TimeValue(t1)); dat3.addValue(TimeValue(t2)); dat3.addValue(TimeValue(t3)); string _dat3 = "\"dateTime\":[\"4-2-2021T12:5:0\",\"4-5-2021T12:5:0\",\"4-7-2021T12:5:0\"]";
	ESSetDatation pdat3 = ESSetDatation(); pdat3.addValue(TimeValue(pt1)); pdat3.addValue(TimeValue(pt2)); pdat3.addValue(TimeValue(pt3));
	ESSetProperty prop1 = ESSetProperty(); prop1.addValue(PropertyValue("PM10", "ppm")); string _prop1 = "\"propertyList\":{\"property\":\"PM10\",\"unit\":\"ppm\"}";
	ESSetProperty prop2 = ESSetProperty(); prop2.addValue(PropertyValue("PM25", "ppm")); prop2.addValue(PropertyValue("PM10", "ppm"));
	ESSetProperty pprop2 = ESSetProperty(); pprop2.addValue(PropertyValue("PM25", "ppm", "smp")); pprop2.addValue(PropertyValue("PM10", "ppm", "smp")); string _pprop2 = "\"propertyList\":[{\"property\":\"PM25\",\"unit\":\"ppm\",\"EMFId\":\"smp\"},{\"property\":\"PM10\",\"unit\":\"ppm\",\"EMFId\":\"smp\"}]";
	ESSetLocation loc1 = ESSetLocation(); loc1.addValue(paris); string _loc1 = "\"coordinates\":[2.35, 48.87]";
	ESSetLocation loc3 = ESSetLocation(); loc3.addValue(paris); loc3.addValue(lyon); loc3.addValue(marseille); string _loc3 = "\"coordinates\":[[2.35, 48.87],[4.83, 45.76],[5.38, 43.3]]";

	cout << endl << "------------------------------------------------------------------------------------" << endl;
	string objs;
	int err = 0;

	// test_value
	err += testEgal(paris.json(1, 1), _paris);
	err += testEgal(res6.json(0, 1, 0), _res6);
	err += testEgal(dat1.json(0, 1, 0), _dat1);
	err += testEgal(dat2.json(0, 1, 0), _dat2);
	err += testEgal(dat3.json(0, 1, 0), _dat3);
	err += testEgal(prop1.json(0, 1, 0), _prop1);
	err += testEgal(prop1.json(0, 1, 0), _prop1);
	err += testEgal(pprop2.json(0, 1, 0), _pprop2);
	err += testEgal(loc1.json(0, 1, 0), _loc1);
	err += testEgal(loc3.json(0, 1, 0), _loc3);

	// test_obs_simple
	objs = "{" + obs_1 + "," + dat3.json(0, 1, 0) + "}";
	err += testEgal(Observation(objs).json(0, 1, 0), objs);
	objs = "{" + obs_1 + "," + loc3.json(0, 1, 0) + "}";
	err += testEgal(Observation(objs).json(0, 1, 0), objs);
	objs = "{" + obs_1 + "," + prop2.json(0, 1, 0) + "}";
	err += testEgal(Observation(objs).json(0, 1, 0), objs);
	objs = "{" + obs_1 + "," + res_(9).json(0, 1, 0) + "}";
	err += testEgal(Observation(objs).json(0, 1, 0), objs);
	objs = "{" + obs_1 + "," + dat3.json(0, 1, 0) + "," + loc3.json(0, 1, 0) + "," + prop2.json(0, 1, 0) + "," + res_(9).json(0, 1, 0) + "}";
	err += testEgal(Observation(objs).json(0, 1, 0), objs);
	
	// test_obs_maj_type
	err += test1(Observation().score == 0);
	objs = "{" + obs_1 + "," + dat1.json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 1);
	objs = "{" + obs_1 + "," + dat3.json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 2);
	objs = "{" + obs_1 + "," + loc1.json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 10);
	objs = "{" + obs_1 + "," + dat1.json(0, 1, 0) + "," + loc1.json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 11);
	objs = "{" + obs_1 + "," + dat3.json(0, 1, 0) + "," + loc1.json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 12);
	objs = "{" + obs_1 + "," + loc3.json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 20);
	objs = "{" + obs_1 + "," + dat1.json(0, 1, 0) + "," + loc3.json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 21);
	objs = "{" + obs_1 + "," + dat3.json(0, 1, 0) + "," + loc3.json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 22);
	objs = "{" + obs_1 + "," + res_(1).json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 100);
	objs = "{" + obs_1 + "," + dat1.json(0, 1, 0) + "," + res_(1).json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 101);
	objs = "{" + obs_1 + "," + dat3.json(0, 1, 0) + "," + res_(1).json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 102);
	objs = "{" + obs_1 + "," + res_(1).json(0, 1, 0) + "," + loc1.json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 110);
	objs = "{" + obs_1 + "," + dat1.json(0, 1, 0) + "," + loc1.json(0, 1, 0) + "," + res_(1).json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 111);
	objs = "{" + obs_1 + "," + dat3.json(0, 1, 0) + "," + loc1.json(0, 1, 0) + "," + res_(1).json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 112);
	objs = "{" + obs_1 + "," + res_(1).json(0, 1, 0) + "," + loc3.json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 120);
	objs = "{" + obs_1 + "," + dat1.json(0, 1, 0) + "," + loc3.json(0, 1, 0) + "," + res_(1).json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 121);
	objs = "{" + obs_1 + "," + dat3.json(0, 1, 0) + "," + loc3.json(0, 1, 0) + "," + res_(1).json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 122);
	objs = "{" + obs_1 + "," + res_(9).json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 200);
	objs = "{" + obs_1 + "," + dat1.json(0, 1, 0) + "," + res_(9).json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 201);
	objs = "{" + obs_1 + "," + dat3.json(0, 1, 0) + "," + res_(9).json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 202);
	objs = "{" + obs_1 + "," + res_(3).json(0, 1, 0) + "," + loc1.json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 210);
	objs = "{" + obs_1 + "," + dat1.json(0, 1, 0) + "," + loc1.json(0, 1, 0) + "," + res_(6).json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 211);
	objs = "{" + obs_1 + "," + dat3.json(0, 1, 0) + "," + loc1.json(0, 1, 0) + "," + res_(3).json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 212);
	objs = "{" + obs_1 + "," + res_(9).json(0, 1, 0) + "," + loc3.json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 220);
	objs = "{" + obs_1 + "," + dat1.json(0, 1, 0) + "," + loc3.json(0, 1, 0) + "," + res_(9).json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 221);
	objs = "{" + obs_1 + "," + dat3.json(0, 1, 0) + "," + loc3.json(0, 1, 0) + "," + res_(18).json(0, 1, 0) + "}";
	err += test1(Observation(objs).score == 222);

	// test_obs_creation
	err += testEgal(Observation().getClassES(), Observation::ESclass);
	err += testEgal(ESSetDatation(&Observation()).getClassES(), Datation::ESclass);
	err += testEgal(ESSetLocation(&Observation()).getClassES(), Location::ESclass);
	err += testEgal(ESSetProperty(&Observation()).getClassES(), Property::ESclass);
	err += testEgal(ESSetResultReal(&Observation()).getClassES(), Result::ESclass);
	err += testEgal(ESSetResultString(&Observation()).getClassES(), Result::ESclass);
	err += testEgal(ESSetResultInt(&Observation()).getClassES(), Result::ESclass);

	// test_sensor
	Observation obs = Observation();
	obs.setAtt("name", "essai 7");
	int nprop1 = obs.addValue(PropertyValue("PM25", "ppm"));
	// simule une boucle de mesure
	for (int i = 0; i < 6; i++) {
		std::string value = "test";
		//std::string value = pRemoteCharacteristic->readValue();
		int nres = obs.addValueSensor(StringValue(value + std::to_string(i)), TimeValue(2021, 6, 4 + i, 12, 5, 0), LocationValue(14.0 + i, 40.0), nprop1);
	}
	/*obs.Result_()->dim = 1;
	obs.majType();
	err += testEgal(obs.getmAtt()["type"], "obsPath");
	cout << obs.json(1, 1, 1);*/
	cout << endl << "   " << compteur << " tests de regression : " << err << " erreurs " << endl << endl;
	cout << "------------------------------------------------------------------------------------" << endl;
}

int main() {
	
	std::string test = "testtest";
	std::string t1 = test.substr(0, 2);
	std::string t2 = test.substr(2, 4);
	uint16_t v1 = *(uint16_t*)test.substr(0, 2).data();
	uint32_t v2 = *(uint32_t*)test.substr(2, 4).data();
	
	testNonRegression();

	float res = 102;
	BLEServer *			pESserv = new BLEServer;
	BLEService*			pServic = pESserv->createService("181A");
	ESserverCharac*		pcharPm25;
	pcharPm25 = new ESserverCharac(pServic, "2BD6");

	ESBluetooth pm25;
	pm25 = ESBluetooth("2BD6");
	cout << "property : " << pm25.propertyType << "   " << pm25.unit << endl;

	pm25.setPropValue(pcharPm25);
	pm25.value = res;
	cout << pm25.value << endl;
	pm25.setResultValue(pcharPm25);
//------------------------------------------------------------------------------------------------
	BLEclient*			pESclient = new BLEclient;
	BLERemoteService*	pRemoteService = pESclient->getService("181A");
	/*if (pRemoteService == nullptr) {
		cout << "Failed to find service 2BD6" << endl;
		pESclient->disconnect();
		return 0;
	}*/
	ESclientCharac		*premoteCharPm25;
	premoteCharPm25 = new ESclientCharac(pRemoteService, "2BD6");

	ESBluetooth remotePm25 = ESBluetooth("2BD6");

	remotePm25.getPropValue(premoteCharPm25);
	remotePm25.getResultValue(premoteCharPm25);
	cout << remotePm25.value << endl;


	Observation obs1 = Observation();
	//cout << obs1.ESclass << " " << Observation::ESclass << endl;
	/*
	//ESElement* plast, *plast2;
	//string json = "{\"observation\":{\"truc\":\"machin\",\"PropertyValue\":[{\"propertyType\":\"PM10\"}],\"RealValue\":[45.000000, 0.500000,40.000000, 2.000000], \
	//					   \"LocationValue\":[[14.000000,42.299999], [24.000000,22.9]], \"phenomenonTime\" :[\"7-04-2021T12:05\",\"5-04-2021T13:05\"]}}"; 
	//string json = "{\"observation\":{\"truc\":\"machin\",\"PropertyValue\":[{\"propertyType\":\"PM10\"}],\"RealValue\":[[45.000000, 0, 0, 0 ],[0.500000, 0, 1, 0 ],[40.000000, 1, 0, 0 ],[2.000000, 1, 1, 0 ] ], \
	//					   \"LocationValue\":[[14.000000,42.299999], [24.000000,22.9]], \"phenomenonTime\" :[\"7-04-2021T12:05\",\"5-04-2021T13:05\"]}}";
	//string json = "{\"observation\":{\"truc\":\"machin\",\"PropertyValue\":[{\"PropertyType\":\"PM10\"}],\"realValue\":[[45.000000, [0, 0, 0] ],[0.500000, [0, 1, 0] ],[40.000000, [1, 0, 0] ],[2.000000, [1, 1, 0] ] ], \
	//					   \"LocationValue\":[[14.000000,42.299999], [24.000000,22.9]]}}";
	//string json = "{\"observation\":{\"truc\":\"machin\",\"PropertyValue\":[{\"PropertyType\":\"PM10\"}],\"intValue\":[[45, [0, 0, 0] ],[5, [0, 1, 0] ],[40, [1, 0, 0] ],[2, [1, 1, 0] ] ], \
	//					   \"LocationValue\":[[14.000000,42.299999], [24.000000,22.9]]}}";
	//string json = "{\"observation\":{\"truc\":\"machin\",\"PropertyValue\":[{\"PropertyType\":\"PM10\"}],\"stringValue\":[[\"merde\", [0, 0, 0] ],[\"ca marche\", [0, 1, 0] ],[\"et\", [1, 0, 0] ],[\"toc\", [1, 1, 0] ] ], \
	//					   \"LocationValue\":[[14.000000,42.299999], [24.000000,22.9]]}}";
	//string json = "{\"observation\":{\"truc\":\"machin\",\"PropertyValue\":[{\"PropertyType\":\"PM10\"}],\"stringValue\":[{\"prout\":\"caca\"}, \"ca marche\", \"27\", {\"prout\":7.1}], \
	//					   \"LocationValue\":[[14.000000,42.299999], [24.000000,22.9]],\"phenomenonTime\":[\"5-4-2021T12:5:0\",\"7-4-2021T12:5:0\"]}}";
	//string json = "{\"observation\":{\"truc\":\"machin\",\"PropertyValue\":[{\"PropertyType\":\"PM10\"}],\"intValue\":[45, 5, 40, 2], \
	//					   \"LocationValue\":[[14.000000,42.299999], [24.000000,22.9]],\"phenomenonTime\":[\"5-4-2021T12:5:0\",\"7-4-2021T12:5:0\"]}}";
	string json = "{\"type\":\"observation\", \"$truc\":\"machin\",\"propertyList\":[{\"property\":\"PM10\"}],\"intValue\":[45, 5, 40, 2], \
						   \"coordinates\":[[14.000000,42.299999], [24.000000,22.9]],\"dateTime\":[\"5-4-2021T12:5:0\",\"7-4-2021T12:5:0\"]}}";

	std::cout << endl << "essai 1 ----------------------------------------------------------------------------" << endl;
	Observation obs(json);
	obs.print();
	std::cout << endl << obs.json(1, 0, detail) << endl << "nResValue : " << static_cast<ESObs *>(obs.element("result"))->getNvalue() << endl;
	Observation obs3(obs);
	std::cout << endl << obs3.json(1, 0, detail) << endl;
	Observation obs4;
	obs4 = obs;
	std::cout << endl << obs4.json(1, 0, detail) << endl;
	obs.element("result")->print();
	std::cout << "bboxmin : " << obs.getboxMin<LocationValue, Location>() << endl;
	std::cout << "bboxmax : " << obs.getboxMax<LocationValue, Location>() << endl;
	std::cout << "datemin : " << obs.getboxMin<TimeValue, Datation>() << endl;
	std::cout << "datemax : " << obs.getboxMax<TimeValue, Datation>() << endl;

	std::cout << endl << "essai 2 ----------------------------------------------------------------------------" << endl;
	string json2 = "{" + obs.json(1, 0, detail) + "}";
	std::cout << endl << obs.json(1, 1, detail) << endl << endl;
	std::cout << endl << json2 << endl << endl;
	Observation obs2(json2);
	std::cout << endl << obs2.json(1, 0, detail) << endl << endl;
	std::cout << endl << obs2.json(0, 0, detail) << endl << endl;

	{std::cout << endl << "essai 3 ----------------------------------------------------------------------------" << endl;
	MainEMF* pMain = new MainEMF();
	ObservingEMF* pMc = new ObservingEMF(pMain);
	ObservingEMF* pMc2 = new ObservingEMF(pMain);
	Observation* pObs = new Observation();
	ESSet<PropertyValue, Property>*   pMes = new ESSet<PropertyValue, Property>(pObs);
	ESSet<ResultValue<RealValue>, Result>* pRes = new ESSet<ResultValue<RealValue>, Result>(pObs);
	ESSet<TimeValue, Datation>*   pDat = new ESSet<TimeValue, Datation>(pObs);
	ESSet<LocationValue, Location>* pGeo = new ESSet<LocationValue, Location>(pObs);
	//cout << "deb" << endl;
	indexRes i = { 0,0,0 };
	pRes->addValue(ResultValue<RealValue>(45.5, i));
	//cout << "deb1" << endl;
	i = { 1,0,0 };
	//cout << "ind : " << i.idat << " " << i.iloc << " " << i.iprop << endl;
	pRes->addValue(ResultValue<RealValue>(22, i));
	//cout << "res" << endl;
	pMes->addValue(PropertyValue("PM25", "mg/m3"));
	pDat->addValue(TimeValue("5-04-2021T12:05"));
	pDat->addValue(TimeValue("5-04-2021T22:05"));
	pGeo->addValue(LocationValue(14, 42.3));
	pGeo->addValue(LocationValue(10, 22.3));
	std::cout << endl << pRes->json(1, 0, detail) << endl << endl;
	std::cout << endl << pRes->json(0, 0, detail) << endl << endl;
	pObs->print();
	std::cout << endl << pObs->json(1, 0, detail) << endl;

	std::cout << endl << "essai 4 ----------------------------------------------------------------------------" << endl;
	pMain->setAtt("EMFType", "station");
	pMc->setAtt("id", "ds212");
	pMc2->setAtt("id", "ds212121");
	pMc->setAtt("EMFType", "sensor");
	cout << "ok" << endl;
	std::cout << endl << pMain->json(1, 0, detail) << endl << endl;
	std::cout << endl << pMain->json(0, 0, detail) << endl << endl;
	}
	{std::cout << endl << "essai 5 ----------------------------------------------------------------------------" << endl;
	MainEMF* pMain = new MainEMF();
	ObservingEMF* pMc = new ObservingEMF(pMain);
	pMain->setAtt("EMFType", "station");
	pMc->setAtt("id", "ds212");
	std::cout << endl << pMain->json(1, 0, detail) << endl << endl;
	Observation* pObs = new Observation();
	//PropertySet* pMes = new PropertySet(pObs);
	ESSet<PropertyValue, Property>*   pMes = new ESSet<PropertyValue, Property>(pObs);
	ESSet<ResultValue<RealValue>, Result>* pRes = new ESSet<ResultValue<RealValue>, Result>(pObs);
	ESSet<TimeValue, Datation>*   pDat = new ESSet<TimeValue, Datation>(pObs);
	//TimeStampSet* pDat = new TimeStampSet(pObs);
	ESSet<LocationValue, Location>* pGeo = new ESSet<LocationValue, Location>(pObs);
	//RealValue resVal, resVal1;
	//resVal.addMeasureValue(MeasureValue(45, 0.5));
	pMes->addValue(PropertyValue("PM25", "mg/m3"));
	//pMes->addPropertyValue("PM25", "mg/m3", pMc);
	pDat->addValue(TimeValue("5-04-2021T12:05"));
	pGeo->addValue(LocationValue(14, 42.3));
	pObs->print();
	std::cout << endl << pObs->json(0, 0, detail) << endl << endl;
	std::cout << endl << pObs->json(1, 0, detail) << endl;

	// mesure simple
	indexRes i = { 0,0,0 };
	Observation* pObssi = new Observation();
	ESSet<ResultValue<RealValue>, Result>* pRessi = new ESSet<ResultValue<RealValue>, Result>(pObssi);
	pRessi->addValue(ResultValue<RealValue>(40, i));
	//pObssi->addComposant(pRessi);
	std::cout << endl << pObssi->json(0, 0, detail) << endl << endl;
	std::cout << endl << pObssi->json(1, 0, detail) << endl; }
	
	{std::cout << endl << "essai 6 ----------------------------------------------------------------------------" << endl;
	//Observation obs = Observation("measure", "result", "geometry", "time");
	Observation obs = Observation();
	//obs.measure()->addPropertyValue("PM25", "mg/m3", nullptr);
	//RealValue resval;
	//resval.addMeasureValue(MeasureValue(10.3, 0.1));
	//resval.addMeasureValue(MeasureValue(10.8, 0.8));
	//cout << endl << resval.json(1) << endl;
	//obs.result()->addRealValue(43.5);
	//obs.result()->addRealValue(98.85);
	indexRes i = { 0,0,0 };
	std::cout << "1";
	obs.addValue<PropertyValue, Property>(PropertyValue("PM10", "mg/m3"));
	std::cout << "2";
	obs.addValue<PropertyValue, Property>(PropertyValue("PM25", "mg/m3"));
	std::cout << "3";
	obs.addValue<ResultValue<RealValue>, Result>(ResultValue<RealValue>(47, i));
	std::cout << "4";
	obs.addValue<TimeValue, Datation>(TimeValue("5-4-2021T12:5"));
	std::cout << "5";

	obs.print();
	std::cout << endl << obs.json(0, 0, detail) << endl << endl;
	std::cout << endl << obs.json(1, 0, detail) << endl;

	}
	{std::cout << endl << "essai 7 ----------------------------------------------------------------------------" << endl;
	ObsFixe obs(LocationValue(14, 42.3));
	int nprop1 = obs.init(PropertyValue("PM10", "mg/m3"));
	int nprop2 = obs.init(PropertyValue("PM25", "mg/m3"));
	obs.setAtt("name", "essai 7");
	int nres = obs.addValueFixe(RealValue(47), TimeValue("5-4-2021T12:5"), nprop1);
	nres = obs.addValueFixe(RealValue(247), TimeValue("7-4-2021T12:5"), nprop2);
	nres = obs.addValueFixe(RealValue(49), TimeValue("5-4-2021T12:5"), nprop2);

	obs.print();
	std::cout << endl << obs.json(0, 0, detail) << endl << endl;
	std::cout << endl << obs.json(1, 0, detail) << endl;
	}
	{std::cout << endl << "essai 8 ----------------------------------------------------------------------------" << endl;
	ObsFixe obs(LocationValue(14, 42.3));
	int nprop1 = obs.init(PropertyValue("PM10", "mg/m3"));
	int nprop2 = obs.init(PropertyValue("PM25", "mg/m3"));
	obs.setAtt("name", "essai 8");
	int nres = obs.addValueFixe(StringValue("mesure1"), TimeValue("5-4-2021T12:5"), nprop1);
	nres = obs.addValueFixe(StringValue("mesure2"), TimeValue("7-4-2021T12:5"), nprop2);
	nres = obs.addValueFixe(StringValue("mesure3"), TimeValue("5-4-2021T12:5"), nprop2);

	obs.print();
	std::cout << endl << obs.json(0, 0, detail) << endl << endl;
	}
	{std::cout << endl << "exemple capteur mobile -----------------------------------------------------------------------------" << endl;

	Observation obs = Observation(); // création d'un objet observation vide
	int nprop1 = obs.init(PropertyValue("Temp", "°C")); // ajout d'une propriété correspondante aux mesures à effectuer
	for (int i = 0; i < 6; i++) { // simule une boucle de mesure
		int nres = obs.addValueSensor(RealValue(25+i), TimeValue(2021, 5, 4+i, 12, 5, 0), LocationValue(14+i, 42), nprop1);
		// ajoute à l'objet obs une mesure constituée d'une valeur mesurée, de l'instant de mesure et des coordonnées 
		// et l'associe à la propriété prop1 
	}
	//string json_a_envoyer = obs.json()

	std::cout << endl << obs.json(0, 1, 0) << endl << endl;
	//resultat :

	//bidule
	
	std::cout << endl << obs.json(1, 0, 0) << endl << endl;
	
	std::cout << endl << "datesize : " << obs.setDatation()->size() << endl << endl;
	std::cout << endl << "locsize : " << obs.setLocation()->size() << endl << endl;
	std::cout << endl << "propsize : " << obs.setProperty()->size() << endl << endl;
	std::cout << endl << "realsize : " << obs.setResultReal()->size() << endl << endl;
	}
	*/
	return 0;
}
