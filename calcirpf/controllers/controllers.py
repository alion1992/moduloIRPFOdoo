# -*- coding: utf-8 -*-
# from odoo import http


# class Calcirpf(http.Controller):
#     @http.route('/calcirpf/calcirpf', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/calcirpf/calcirpf/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('calcirpf.listing', {
#             'root': '/calcirpf/calcirpf',
#             'objects': http.request.env['calcirpf.calcirpf'].search([]),
#         })

#     @http.route('/calcirpf/calcirpf/objects/<model("calcirpf.calcirpf"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('calcirpf.object', {
#             'object': obj
#         })

