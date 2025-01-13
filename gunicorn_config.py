import os

workers = 2  # Number of worker processes
threads = 4  # Number of threads per worker
bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"  # Bind to the port set in the environment variable or default to 8000