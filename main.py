"""Entry point — starts the interactive Transcriber console session."""

import sys
from console.session import Session

if __name__ == "__main__":
    session: Session = Session()
    session.run()
