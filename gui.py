# -*- coding: UTF-8 -*-

from SpatialiteAlgorithmProvider import SpatialiteAlgorithmProvider
from EpanetAlgorithmProvider import EpanetAlgorithmProvider
from processing.core.Processing import Processing

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *

from pylab import *

import os

class Gui:

    def __init__(self, iface):
        self.iface = iface
        self.actions = []
    
    def initGui(self):

        self.actions.append( QAction(
            QIcon(os.path.dirname(__file__) + "/timeplot.svg"),
            u"timeplot", self.iface.mainWindow()) )
        self.actions[-1].setWhatsThis("timeplot")
        self.actions[-1].triggered.connect(self.timeplot)

        for a in self.actions:
            self.iface.addToolBarIcon(a)

        print "here"
        self.epanetAlgoProvider = EpanetAlgorithmProvider()
        print self.epanetAlgoProvider 
        Processing.addProvider(self.epanetAlgoProvider, True)
        self.spatialiteAlgorithmProvider = SpatialiteAlgorithmProvider()
        Processing.addProvider(self.spatialiteAlgorithmProvider, True)

        QgsMapLayerRegistry.instance().layersAdded.connect( self.layerAdded )
    
    def unload(self):
        Processing.removeProvider(self.spatialiteAlgorithmProvider)
        Processing.removeProvider(self.epanetAlgoProvider)
        # Remove the plugin menu item and icon
        for a in self.actions:
            self.iface.removeToolBarIcon(a)

    def timeplot(self):
        layer = self.iface.activeLayer()
        print layer.name()
        if layer.name().lower() == 'reservoirs' or layer.name().lower() == 'tanks':
            res = QgsMapLayerRegistry.instance().mapLayersByName('Node output table')
            if res: 
                print res
                assert(len(res) == 1)
                nbfeat = len(layer.selectedFeatures())
                fig, p = None,[]
                if nbfeat >= 1 : fig,p = subplots(1,nbfeat)
                if nbfeat == 1 : p = [p]
                print nbfeat, p
                for i,s in enumerate(layer.selectedFeatures()):
                    x,y = [],[]
                    for f in res[0].getFeatures(QgsFeatureRequest(QgsExpression("Node = '"+s['ID Noeud']+"'"))):
                        #print s['ID Noeud'],' ',f['Time'],' ',f['Head']
                        t = f['Time'].split(' ')[1].split(':')
                        x.append(int(t[0])*60+int(t[1]))
                        y.append(f['Pressure'])
                    p[i].axhspan(float(s['Niv Min']), float(s['Niv Max']), color='lightgreen')
                    p[i].text(0, float(s['Niv Max']), ' overflow')
                    p[i].text(0, float(s['Niv Min']), ' empty')
                    p[i].set_axis_bgcolor('r')
                    p[i].plot(x,y)
                    p[i].set_title(layer.name()+' '+s['ID Noeud'])
                    p[i].set_xlabel('Time [min]')
                    p[i].set_ylabel('Level [m]')
                if fig : show()

        if layer.name().lower() == 'pumps':
            res = QgsMapLayerRegistry.instance().mapLayersByName('Link output table')
            if res: 
                assert(len(res) == 1)
                nbfeat = len(layer.selectedFeatures())
                fig, p = None,[]
                if nbfeat >= 1 : fig,p = subplots(1,nbfeat)
                if nbfeat == 1 : p = [p]
                for i,s in enumerate(layer.selectedFeatures()):
                    x,y = [],[]
                    for f in res[0].getFeatures(QgsFeatureRequest(QgsExpression("Link = '"+s['ID Arc']+"'"))):
                        #print s['ID Noeud'],' ',f['Time'],' ',f['Head']
                        t = f['Time'].split(' ')[1].split(':')
                        x.append(int(t[0])*60+int(t[1]))
                        y.append(f['Flow'])
                    p[i].plot(x,y)
                    p[i].set_title(layer.name()+' '+s['ID Arc'])
                    p[i].set_xlabel('Time [min]')
                    p[i].set_ylabel('Flow [m3/h]')
                if fig : show()

        if layer.name().lower() == 'pipes':
            res = QgsMapLayerRegistry.instance().mapLayersByName('Link output table')
            if res: 
                assert(len(res) == 1)
                nbfeat = len(layer.selectedFeatures())
                fig, p = None,[]
                if nbfeat >= 1 : fig,p = subplots(1,nbfeat)
                if nbfeat == 1 : p = [p]
                for i,s in enumerate(layer.selectedFeatures()):
                    x,y = [],[]
                    for f in res[0].getFeatures(QgsFeatureRequest(QgsExpression("Link = '"+s['ID Arc']+"'"))):
                        #print s['ID Noeud'],' ',f['Time'],' ',f['Head']
                        t = f['Time'].split(' ')[1].split(':')
                        x.append(int(t[0])*60+int(t[1]))
                        y.append(f['Velocity'])
                    p[i].plot(x,y)
                    p[i].set_title(layer.name()+' '+s['ID Arc'])
                    p[i].set_xlabel('Time [min]')
                    p[i].set_ylabel('Velocity [m/s]')
                if fig : show()

        if layer.name().lower() == 'junctions':
            res = QgsMapLayerRegistry.instance().mapLayersByName('Node output table')
            if res: 
                assert(len(res) == 1)
                nbfeat = len(layer.selectedFeatures())
                fig, p = None,[]
                if nbfeat >= 1 : fig,p = subplots(1,nbfeat)
                if nbfeat == 1 : p = [p]
                for i,s in enumerate(layer.selectedFeatures()):
                    x,y = [],[]
                    for f in res[0].getFeatures(QgsFeatureRequest(QgsExpression("Node = '"+s['ID Noeud']+"'"))):
                        #print s['ID Noeud'],' ',f['Time'],' ',f['Head']
                        t = f['Time'].split(' ')[1].split(':')
                        x.append(int(t[0])*60+int(t[1]))
                        y.append(f['Pressure'])
                    p[i].plot(x,y)
                    p[i].set_title(layer.name()+' '+s['ID Noeud'])
                    p[i].set_xlabel('Time [min]')
                    p[i].set_ylabel('Pressure [m]')
                if fig : show()

    def layerAdded(self, layers):
        print 'layers added ', layers

        # get a map from layer names
        epanet_layers = {}
        for name,l in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            short_name = l.name().lower()
            if short_name in ['tanks','sources','reservoirs','pumps','pipes','junctions','valves','emitters']:
                epanet_layers[short_name] = l

        for l in layers :
            if l.type() != QgsMapLayer.VectorLayer : continue 
            result_type = None
            fields = [f.name() for f in l.pendingFields()]
            if 'Link' in fields and 'AvgVelocity' in fields:
                result_type = 'Link time agregates'
            if 'Node' in fields and 'MaxPressure' in fields:
                result_type = 'Node time agregates'
            print result_type
            if result_type == 'Node time agregates':
                # create join on first field
                print 'create join on junctions'
                join_info = QgsVectorJoinInfo()
                join_info.targetFieldName = 'ID Noeud'
                join_info.targetFieldIndex = 0
                join_info.joinLayerId = l.id() 
                join_info.joinFieldName = 'Node'
                join_info.joinFieldIndex = 0
                join_info.memoryCache = False
                #join_info.cachedAttributes = 
                for name in ['junctions','emitters','tanks','sources','reservoirs']:
                    if name in epanet_layers: epanet_layers[name].addJoin( join_info )
            if result_type == 'Link time agregates':
                # create join on first field
                print 'create join on junctions'
                join_info = QgsVectorJoinInfo()
                join_info.targetFieldName = 'ID Arc'
                join_info.targetFieldIndex = 0
                join_info.joinLayerId = l.id() 
                join_info.joinFieldName = 'Link'
                join_info.joinFieldIndex = 0
                join_info.memoryCache = False
                #join_info.cachedAttributes = 
                for name in ['pipes','valves','pumps']:
                    if name in epanet_layers: epanet_layers[name].addJoin( join_info )

