# -*- coding: utf-8 -*-

import logging

from app.flask_app import create_app

logger = logging.getLogger(__name__)

flask_app = create_app()
