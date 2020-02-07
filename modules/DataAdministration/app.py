'''
    Bottle routings for data administration
    (i.e., image, annotation, and prediction
    down- and uploads).
    Needs to be run from instance responsible
    for serving files (i.e., FileServer module).

    2020 Benjamin Kellenberger
'''

import os
import datetime
from bottle import request, response, abort
from .backend.middleware import DataAdministrationMiddleware
from util import helpers


class DataAdministrator:

    def __init__(self, config, app):
        self.config = config
        self.app = app

        if not helpers.is_fileServer(config):
            raise Exception('DataAdministrator module must be run on file server instance.')

        self.middleware = DataAdministrationMiddleware(config)

        self.login_check = None
        self._initBottle()


    def loginCheck(self, project=None, admin=False, superuser=False, canCreateProjects=False, extend_session=False):
        return self.login_check(project, admin, superuser, canCreateProjects, extend_session)


    def addLoginCheckFun(self, loginCheckFun):
        self.login_check = loginCheckFun

    
    @staticmethod
    def _parse_range(params, paramName, minValue, maxValue):
        '''
            Parses "params" (dict) for a given keyword
            "paramName" (str), and expects a dict with
            keywords "min" and "max" there. One of the
            two may be missing, in which case the values
            of "minValue" and "maxValue" will be used.
            Returns a tuple of (min, max) values, or None
            if "paramName" is not in "params."
        '''
        if not paramName in params:
            return None
        entry = params[paramName].copy()
        if not 'min' in entry:
            entry['min'] = minValue
        if not 'max' in entry:
            entry['max'] = maxValue
        return (entry['min'], entry['max'])


    def _initBottle(self):

        ''' Image management functionalities '''
        @self.app.get('/<project>/listImages')
        def list_images(project):
            '''
                Returns a list of images and various properties
                and statistics (id, filename, viewcount, etc.),
                all filterable by date and value ranges.
            '''
            if not self.loginCheck(project=project, admin=True):
                abort(401, 'forbidden')
            
            # parse parameters
            now = helpers.current_time()
            params = request.json

            imageAddedRange = self._parse_range(params, 'imageAddedRange',
                                            datetime.time.min,
                                            now)
            lastViewedRange = self._parse_range(params, 'lastViewedRange',
                                            datetime.time.min,
                                            now)
            viewcountRange = self._parse_range(params, 'viewcountRange',
                                            0,
                                            1e9)
            numAnnoRange = self._parse_range(params, 'numAnnoRange',
                                            0,
                                            1e9)
            numPredRange = self._parse_range(params, 'numPredRange',
                                            0,
                                            1e9)
            limit = (params['limit'] if 'limit' in params else None)


            # get images
            result = self.middleware.listImages(project,
                                            imageAddedRange,
                                            lastViewedRange,
                                            viewcountRange,
                                            numAnnoRange,
                                            numPredRange,
                                            limit)
            
            return {'response': result}


        @self.app.post('/<project>/uploadImages')
        def upload_images(project):
            '''
                Upload image files through UI.
            '''
            #TODO
            raise Exception('Not yet implemented.')


        @self.app.get('/<project>/scanForImages')
        def scan_for_images(project):
            '''
                Search project file directory on disk for
                images that are not registered in database.
            '''
            #TODO
            raise Exception('Not yet implemented.')


        @self.app.get('/<project>/addImages')
        def add_images(project):
            '''
                Add images that exist in project file directory
                on disk, but are not yet registered in database.
            '''
            #TODO
            raise Exception('Not yet implemented.')


        @self.app.post('/<project>/removeImages')
        def remove_images(project):
            '''
                Remove images from database, including predictions
                and annotations (if flag is set).
                Also remove images from disk (if flag is set).
            '''
            #TODO
            raise Exception('Not yet implemented.')


        ''' Annotation and prediction up- and download functionalities '''
        #TODO