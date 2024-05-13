from flask_restx import Api, Namespace, Resource, fields

app_ns = Namespace('App', description='Operations:')

status_model = app_ns.model('Status', {
    'status': fields.String,
})

metrics_model = app_ns.model('Metrics', {
    'requests_per_second': fields.Integer(description='The number of requests per second.'),
    'average_request_duration_seconds': fields.Float(description='Average duration of HTTP requests in seconds.')
})

@app_ns.route('/health')
class HealthCheck(Resource):
    @app_ns.marshal_with(status_model)
    def get(self):
        return {'status': 'OK'}


@app_ns.route('/readyz')
class ReadinessProbe(Resource):
    def get(self):
        try:
            is_ready = True
            if is_ready:
                return {'status': 'OK'}
            else:
                return {'status': 'SERVICE UNAVAILABLE'}, 503
        except Exception as e:
            print(f"Error occurred: {e}")
            return {"message": "An error occurred while processing your request."}, 500


@app_ns.route('/readyz/enable')
class EnableReadiness(Resource):
    def get(self):
        return {'message': 'Readiness enabled'}, 202


@app_ns.route('/readyz/disable')
class DisableReadiness(Resource):
    def get(self):
        return {'message': 'Readiness disabled'}, 202


@app_ns.route('/metrics')
class Metrics(Resource):
    @app_ns.marshal_with(metrics_model)
    def get(self):
        # Example values, replace with actual metric computations
        requests_per_second = 100  # Replace with real computation
        average_request_duration_seconds = 0.350  # Replace with real computation
        return {
            'requests_per_second': requests_per_second,
            'average_request_duration_seconds': average_request_duration_seconds
        }



def init_api(app):
    api = Api(app, version='1.0', title='The App API',
        description='A simple App API')
    api.add_namespace(app_ns, path='/app')
