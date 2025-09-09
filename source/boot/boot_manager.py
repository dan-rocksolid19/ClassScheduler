"""
BootManager - Synchronous application initialization manager.

Handles the complete startup sequence without threading or polling loops.
"""

import traceback
from librepy.pybrex.values import pybrex_logger
from librepy.pybrex.msgbox import msgbox
from librepy.boot.bootstrap import ensure_database_ready
#from librepy.auth.bootstrap import ensure_auth_ready

logger = pybrex_logger(__name__)

class BootError(Exception):
    """Raised when boot process fails at any stage"""
    def __init__(self, stage, message, original_exception=None):
        self.stage = stage
        self.message = message
        self.original_exception = original_exception
        super().__init__(f"Boot failed at {stage}: {message}")

class BootManager:
    """
    Manages the complete application boot sequence synchronously.
    
    This replaces the threaded approach with a simple, deterministic flow:
    1. Database bootstrap
    2. Auth bootstrap   (Skipped unless needed)
    3. App creation
    4. Return initialized application
    """
    
    def __init__(self, ctx, smgr):
        self.ctx = ctx
        self.smgr = smgr
        self.logger = logger
        self.current_stage = "STARTING"
        
    def boot_application(self):
        """
        Run the complete boot sequence and return the initialized App.
        
        Returns:
            App instance if successful, None if failed
            
        Raises:
            BootError: If any stage fails critically
        """
        try:
            self.logger.info("BootManager: Starting application boot sequence")
            
            # Stage 1: Database bootstrap
            self.current_stage = "DATABASE_BOOTSTRAP"
            self.logger.info("BootManager: Running database bootstrap")
            if not ensure_database_ready(self.logger):
                raise BootError("DATABASE_BOOTSTRAP", "Database configuration or connection failed")
            
            # Stage 2: Auth bootstrap (Skipped unless needed)
            #self.current_stage = "AUTH_BOOTSTRAP"
            #self.logger.info("BootManager: Running auth bootstrap")
            #if not ensure_auth_ready(self.ctx, self.smgr, self.logger):
            #    raise BootError("AUTH_BOOTSTRAP", "Auth bootstrap failed")
            
            # Stage 3: App creation
            self.current_stage = "APP_INIT"
            self.logger.info("BootManager: Creating App")
            from librepy.app.core.main import App
            app = App(self.ctx, self.smgr)
            
            # Stage 4: Verify initialization completed
            self.current_stage = "VERIFICATION"
            if not hasattr(app, '_initialization_complete') or not app._initialization_complete:
                raise BootError("VERIFICATION", "App initialization did not complete properly")
            
            self.current_stage = "COMPLETED"
            self.logger.info("BootManager: Application boot completed successfully")
            return app
            
        except BootError:
            # Re-raise BootError as-is
            raise
        except Exception as e:
            # Wrap any other exception in BootError
            self.logger.error(f"BootManager: Unexpected error in {self.current_stage}: {str(e)}")
            self.logger.error(traceback.format_exc())
            raise BootError(self.current_stage, f"Unexpected error: {str(e)}", e)
    
    def handle_boot_failure(self, boot_error):
        """
        Handle boot failure by logging and showing user-friendly message.
        
        Args:
            boot_error: BootError instance
        """
        error_msg = f"Application failed to start during {boot_error.stage}: {boot_error.message}"
        self.logger.error(f"BootManager: {error_msg}")
        
        # Show user-friendly message
        try:
            msgbox(f"Application startup failed.\n\nStage: {boot_error.stage}\nError: {boot_error.message}", 
                   "Startup Error")
        except:
            # If msgbox fails, at least we logged the error
            pass