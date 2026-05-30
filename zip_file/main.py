"""
Main entry point for the Transcriber application.
Initializes and starts the interactive REPL session.
"""

from console import Session

if __name__ == "__main__":
    # Initialize the REPL session
    session: Session = Session()
    
    # Start the interactive command loop
    session.run()
