import os
import infer

infer.app.run(debug=True, port=int(os.getenv('PORT', 5000)))

