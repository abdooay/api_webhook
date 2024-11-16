import PyInstaller.__main__  # type: ignore

PyInstaller.__main__.run([
    'app.py',
    '--onefile',
    # '--add-data', 'templates:templates',  # If you have templates
    # '--add-data', 'static:static',        # If you have static files
    '--name', 'webhook_echo',
    # '--icon', 'icon.ico',                 # Optional: add if you have an icon
]) 
