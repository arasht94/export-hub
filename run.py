#!/usr/bin/env python
"""
Flask application entry point
"""

import os

from app import create_app


app = create_app()


if __name__ == "__main__":
    port = os.environ.get("PORT", 10000)
    app.run(debug=True, host="0.0.0.0", port=port)
