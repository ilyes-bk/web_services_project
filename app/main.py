import uvicorn
from app.server.app import app  # Import the 'app' instance from the correct module

if __name__ == "__main__":
    # Run the FastAPI application using uvicorn

    # - **app**: FastAPI app instance.
    # - **host**: The host on which the application will run. "0.0.0.0" makes it accessible from outside the local machine.
    # - **port**: The port on which the application will run.
    # - **reload**: If set to True, the server will automatically reload on code changes for development purposes.
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)