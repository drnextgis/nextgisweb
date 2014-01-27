# -*- coding: utf-8 -*-

from ..object_widget import ObjectWidget


class WMSClientLayerObjectWidget(ObjectWidget):

    def is_applicable(self):
        return self.operation in ('create', 'edit')

    def populate_obj(self):
        ObjectWidget.populate_obj(self)
        self.obj.url = self.data['url']
        self.obj.version = self.data['version']
        self.obj.srs_id = self.data['srs_id']

    def widget_params(self):
        result = ObjectWidget.widget_params(self)

        if self.obj:
            result['value'] = dict(
                url=self.obj.url,
                version=self.obj.version,
                srs_id=self.obj.srs_id,
            )

        return result

    def widget_module(self):
        return 'wmsclient/LayerWidget'


class WMSClientStyleObjectWidget(ObjectWidget):

    def is_applicable(self):
        return self.operation in ('create', 'edit')

    def populate_obj(self):
        ObjectWidget.populate_obj(self)
        self.obj.wmslayers = self.data['wmslayers']
        self.obj.imgformat = self.data['imgformat']

    def widget_params(self):
        result = ObjectWidget.widget_params(self)

        if self.obj:
            result['value'] = dict(
                wmslayers=self.obj.wmslayers,
                imgformat=self.obj.imgformat,
            )

        client = self.options['layer'].client
        result['imgformat'] = client.getOperationByName('GetMap').formatOptions

        wmslayers = []
        for l in client.contents:
            wmslayers.append(dict(
                id=l, title=client[l].title))

        result['wmslayers'] = wmslayers

        return result

    def widget_module(self):
        return 'wmsclient/StyleWidget'


def setup_pyramid(comp, config):
    WMSClientLayer = comp.WMSClientLayer

    WMSClientLayer.object_widget = (
        (WMSClientLayer.identity, WMSClientLayerObjectWidget),
    )

    WMSClientStyle = comp.WMSClientStyle

    WMSClientStyle.object_widget = (
        (WMSClientStyle.identity, WMSClientStyleObjectWidget),
    )
