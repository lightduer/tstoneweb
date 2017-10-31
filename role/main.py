from role.model import EndpointResource


class EndpointResourceManager(object):
    @staticmethod
    def script_init_endpoint_resource_table(app):
        if not app.first_time:
            return
        for k, v in app.view_functions.items():
            methods = getattr(v, 'methods', ['GET', 'POST', 'PUT', 'DELETE'])
            for method in methods:
                er = EndpointResource(k, method, 'no desc')
                app.db.session.add(er)
        app.db.session.commit()
