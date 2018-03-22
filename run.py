from app import app
import os
port = int(os.environ.get('PORT', 5000))
if os.envrion.get('HEROKU') is None:
	app.run(debug=True, host='0.0.0.0', port=port)
else:
	app.run(host='0.0.0.0', port=port)